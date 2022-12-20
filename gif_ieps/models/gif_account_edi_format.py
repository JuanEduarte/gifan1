# -*- coding: utf-8 -*-
from odoo import models,fields,api, _
from datetime import datetime
from math import copysign
import base64
from io import BytesIO

import logging

_logger = logging.getLogger(__name__)
from odoo.tools.xml_utils import _check_with_xsd
from lxml import etree


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _l10n_mx_edi_get_invoice_templates(self):
        if self.code == 'cfdi_3_3':
            return self.env.ref('gif_ieps.gif_cfdiv33'), self.sudo().env.ref('l10n_mx_edi.xsd_cached_cfdv33_xsd', False)
        else:
            return self.env.ref('gif_ieps.gif_cfdiv40'), self.sudo().env.ref('l10n_mx_edi.xsd_cached_cfdv40_xsd', False)
    
    def _l10n_mx_edi_post_invoice_pac(self, invoice, exported):
        pac_name = invoice.company_id.l10n_mx_edi_pac
        res = super(AccountEdiFormat,self)._l10n_mx_edi_post_invoice_pac(invoice,exported)
        for ieps in invoice.invoice_line_ids:
            if ieps.gif_AccountMoveIeps != 0:
                has_ieps = True
                break
            else:
                has_ieps = False
        if res['error']:
            if (has_ieps == True and '[Error #CFDI40108]' in res['error']) or (has_ieps == True and 'c_TasaOCuota' in res['error']):
                res['error'] = None
        return res

    def _l10n_mx_edi_get_invoice_cfdi_values(self, invoice):

        cfdi_date = datetime.combine(
            fields.Datetime.from_string(invoice.invoice_date),
            invoice.l10n_mx_edi_post_time.time(),
        ).strftime('%Y-%m-%dT%H:%M:%S')

        cfdi_values = {
            **invoice._prepare_edi_vals_to_export(),
            **self._l10n_mx_edi_get_common_cfdi_values(invoice),
            'document_type': 'I' if invoice.move_type == 'out_invoice' else 'E',
            'currency_name': invoice.currency_id.name,
            'payment_method_code': (invoice.l10n_mx_edi_payment_method_id.code or '').replace('NA', '99'),
            'payment_policy': invoice.l10n_mx_edi_payment_policy,
            'cfdi_date': cfdi_date,
            'l10n_mx_edi_external_trade_type': '01', # CFDI 4.0
            'tax_objected': '02',
        }

        # ==== Invoice Values ====
        if invoice.currency_id.name == 'MXN':
            cfdi_values['currency_conversion_rate'] = None
        else:  # assumes that invoice.company_id.country_id.code == 'MX', as checked in '_is_required_for_invoice'
            cfdi_values['currency_conversion_rate'] = abs(invoice.amount_total_signed) / abs(invoice.amount_total) if invoice.amount_total else 1.0

        if invoice.partner_bank_id:
            digits = [s for s in invoice.partner_bank_id.acc_number if s.isdigit()]
            acc_4number = ''.join(digits)[-4:]
            cfdi_values['account_4num'] = acc_4number if len(acc_4number) == 4 else None
        else:
            cfdi_values['account_4num'] = None

        if cfdi_values['customer'].country_id.l10n_mx_edi_code != 'MEX' and cfdi_values['customer_rfc'] not in ('XEXX010101000', 'XAXX010101000'):
            cfdi_values['customer_fiscal_residence'] = cfdi_values['customer'].country_id.l10n_mx_edi_code
        else:
            cfdi_values['customer_fiscal_residence'] = None


        # ==== Tax details ====

        def get_tax_cfdi_name(tax_detail_vals):
            tags = set()
            for detail in tax_detail_vals['group_tax_details']:
                for tag in detail['tax_repartition_line_id'].tag_ids:
                    tags.add(tag)
            tags = list(tags)
            if len(tags) == 1:
                return {'ISR': '001', 'IVA': '002', 'IEPS': '003'}.get(tags[0].name)
            elif tax_detail_vals['tax'].l10n_mx_tax_type == 'Exento':
                return '002'
            else:
                return None

        def gif_has_ieps(customer):
            if customer.gif_ieps_desglose == True:
                return '01'
            else:
                return '02'

        def gif_line_has_ieps(line):
            for record in line.tax_ids:
                if 'IEPS' in record.name and line.move_id.partner_id.gif_ieps_desglose == False:
                    return '02'
            return '01'

        def filter_void_tax_line(inv_line):
            return inv_line.discount != 100.0

        def filter_tax_transferred(tax_values):
            return tax_values['tax_id'].amount >= 0.0

        def filter_tax_withholding(tax_values):
            return tax_values['tax_id'].amount < 0.0

        compute_mode = 'tax_details' if invoice.company_id.tax_calculation_rounding_method == 'round_globally' else 'compute_all'

        tax_details_transferred = invoice._prepare_edi_tax_details(filter_to_apply=filter_tax_transferred, compute_mode=compute_mode, filter_invl_to_apply=filter_void_tax_line)
        for tax_detail_transferred in (list(tax_details_transferred['invoice_line_tax_details'].values())
                                       + [tax_details_transferred]):
            for tax_detail_vals in tax_detail_transferred['tax_details'].values():
                tax = tax_detail_vals['tax']
                if tax.l10n_mx_tax_type == 'Tasa':
                    tax_detail_vals['tax_rate_transferred'] =  tax.amount / 100.0  #gif_amount / 100.0 
                elif tax.l10n_mx_tax_type == 'Cuota':
                    tax_detail_vals['tax_rate_transferred'] = tax_detail_vals['tax_amount_currency'] / tax_detail_vals['base_amount_currency']
                else:
                    tax_detail_vals['tax_rate_transferred'] = None
                

        tax_details_withholding = invoice._prepare_edi_tax_details(filter_to_apply=filter_tax_withholding, compute_mode=compute_mode, filter_invl_to_apply=filter_void_tax_line)
        for tax_detail_withholding in (list(tax_details_withholding['invoice_line_tax_details'].values())
                                       + [tax_details_withholding]):
            for tax_detail_vals in tax_detail_withholding['tax_details'].values():
                tax = tax_detail_vals['tax']
                if tax.l10n_mx_tax_type == 'Tasa':
                    tax_detail_vals['tax_rate_withholding'] = - tax.amount / 100.0 # gif_amount / 100.0
                elif tax.l10n_mx_tax_type == 'Cuota':
                    tax_detail_vals['tax_rate_withholding'] = - tax_detail_vals['tax_amount_currency'] / tax_detail_vals['base_amount_currency']
                else:
                    tax_detail_vals['tax_rate_withholding'] = None
                

        cfdi_values.update({
            'gif_has_ieps': gif_has_ieps,
            'gif_line_has_ieps': gif_line_has_ieps,
            'get_tax_cfdi_name': get_tax_cfdi_name,
            'tax_details_transferred': tax_details_transferred,
            'tax_details_withholding': tax_details_withholding,
        })

        cfdi_values.update({
            'has_tax_details_transferred_no_exento': any(x['tax'].l10n_mx_tax_type != 'Exento' for x in cfdi_values['tax_details_transferred']['tax_details'].values()),
            'has_tax_details_withholding_no_exento': any(x['tax'].l10n_mx_tax_type != 'Exento' for x in cfdi_values['tax_details_withholding']['tax_details'].values()),
        })

        for line_vals in cfdi_values['invoice_line_vals_list']:
            line_vals['custom_numbers'] = line_vals['line']._l10n_mx_edi_get_custom_numbers()

        if not invoice._l10n_mx_edi_is_managing_invoice_negative_lines_allowed():
            return cfdi_values

        # ==== Distribute negative lines ====

        def is_discount_line(line):
            return line.price_subtotal < 0.0

        def is_candidate(discount_line, other_line):
            discount_taxes = discount_line.tax_ids.flatten_taxes_hierarchy()
            other_line_taxes = other_line.tax_ids.flatten_taxes_hierarchy()
            return set(discount_taxes.ids) == set(other_line_taxes.ids)

        def put_discount_on(cfdi_values, discount_vals, other_line_vals):
            discount_line = discount_vals['line']
            other_line = other_line_vals['line']

            # Update price_discount.

            remaining_discount = discount_vals['price_discount'] - discount_vals['price_subtotal_before_discount']
            remaining_price_subtotal = other_line_vals['price_subtotal_before_discount'] - other_line_vals['price_discount']
            discount_to_allow = min(remaining_discount, remaining_price_subtotal)

            other_line_vals['price_discount'] += discount_to_allow
            discount_vals['price_discount'] -= discount_to_allow

            # Update taxes.

            for tax_key in ('tax_details_transferred', 'tax_details_withholding'):
                discount_line_tax_details = cfdi_values[tax_key]['invoice_line_tax_details'][discount_line]['tax_details']
                other_line_tax_details = cfdi_values[tax_key]['invoice_line_tax_details'][other_line]['tax_details']
                for k, tax_values in discount_line_tax_details.items():
                    if discount_line.currency_id.is_zero(tax_values['tax_amount_currency']):
                        continue

                    other_tax_values = other_line_tax_details[k]
                    tax_amount_to_allow = copysign(
                        min(abs(tax_values['tax_amount_currency']), abs(other_tax_values['tax_amount_currency'])),
                        other_tax_values['tax_amount_currency'],
                    )
                    other_tax_values['tax_amount_currency'] -= tax_amount_to_allow
                    tax_values['tax_amount_currency'] += tax_amount_to_allow
                    base_amount_to_allow = copysign(
                        min(abs(tax_values['base_amount_currency']), abs(other_tax_values['base_amount_currency'])),
                        other_tax_values['base_amount_currency'],
                    )
                    other_tax_values['base_amount_currency'] -= base_amount_to_allow
                    tax_values['base_amount_currency'] += base_amount_to_allow

            return discount_line.currency_id.is_zero(remaining_discount - discount_to_allow)

        for line_vals in cfdi_values['invoice_line_vals_list']:
            line = line_vals['line']

            if not is_discount_line(line):
                continue

            # Search for lines on which distribute the global discount.
            candidate_vals_list = [x for x in cfdi_values['invoice_line_vals_list']
                                   if not is_discount_line(x['line']) and is_candidate(line, x['line'])]

            # Put the discount on the biggest lines first.
            candidate_vals_list = sorted(candidate_vals_list, key=lambda x: x['line'].price_subtotal, reverse=True)
            for candidate_vals in candidate_vals_list:
                if put_discount_on(cfdi_values, line_vals, candidate_vals):
                    break

        # ==== Remove discount lines ====

        cfdi_values['invoice_line_vals_list'] = [x for x in cfdi_values['invoice_line_vals_list']
                                                 if not is_discount_line(x['line'])]

        # ==== Remove taxes for zero lines ====

        for line_vals in cfdi_values['invoice_line_vals_list']:
            line = line_vals['line']

            if line.currency_id.is_zero(line_vals['price_subtotal_before_discount'] - line_vals['price_discount']):
                for tax_key in ('tax_details_transferred', 'tax_details_withholding'):
                    cfdi_values[tax_key]['invoice_line_tax_details'].pop(line, None)
            line_vals['custom_numbers'] = line_vals['line']._l10n_mx_edi_get_custom_numbers()

        # Recompute Totals since lines changed.
        cfdi_values.update({
            'total_price_subtotal_before_discount': sum(x['price_subtotal_before_discount'] for x in cfdi_values['invoice_line_vals_list']),
            'total_price_discount': sum(x['price_discount'] for x in cfdi_values['invoice_line_vals_list']),
        })

        return cfdi_values
