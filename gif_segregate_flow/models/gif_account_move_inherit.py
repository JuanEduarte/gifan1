from odoo import models,api,fields,_
from json import dumps
import json


class AccountMoveSegregateFlow(models.Model):
    _inherit = 'account.move'

    amount_tax_show = fields.Monetary(string='Impuestos', compute='_compute_amount_show')
    amount_untaxed_show = fields.Monetary(string='Importe sin impuestos', compute='_compute_amount_show')
    amount_total_show = fields.Monetary(string='Totals', compute='_compute_amount_show')
    amount_residual_show = fields.Monetary(string='Cantidad a Pagar', compute='_compute_amount_show')
    amount_untaxed_signed_show = fields.Monetary(string='Impuestos no incluidos', compute='_compute_amount_show',currency_field='company_currency_id')
    amount_tax_signed_show = fields.Monetary(string='Impuesto', compute='_compute_amount_show',currency_field='company_currency_id')
    amount_total_signed_show = fields.Monetary(string='Total', compute='_compute_amount_show',currency_field='company_currency_id')
    amount_total_in_currency_signed_show = fields.Monetary(string='Total en divisa', compute='_compute_amount_show',currency_field='currency_id')
    amount_residual_signed_show = fields.Monetary(string='Importe pendiente', compute='_compute_amount_show',currency_field='currency_id')


    def _compute_payments_widget_to_reconcile_info(self):
        for move in self:
            move.invoice_outstanding_credits_debits_widget = json.dumps(False)
            move.invoice_has_outstanding = False

            if move.state != 'posted' \
                    or move.payment_state not in ('not_paid', 'partial') \
                    or not move.is_invoice(include_receipts=True):
                continue

            pay_term_lines = move.line_ids\
                .filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            domain = [
                ('account_id', 'in', pay_term_lines.account_id.ids),
                ('parent_state', '=', 'posted'),
                ('partner_id', '=', move.commercial_partner_id.id),
                ('reconciled', '=', False),
                '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0),
            ]

            payments_widget_vals = {'outstanding': True, 'content': [], 'move_id': move.id}

            if move.is_inbound():
                domain.append(('balance', '<', 0.0))
                payments_widget_vals['title'] = _('Outstanding credits')
            else:
                domain.append(('balance', '>', 0.0))
                payments_widget_vals['title'] = _('Outstanding debits')

            for line in self.env['account.move.line'].search(domain):
                if move.move_type == 'in_invoice' or move.move_type == 'in_refund' or move.move_type == 'in_receipt':
                    if line.payment_id.type_of_purchase == move.type_of_purchase:
                        if line.currency_id == move.currency_id:
                            # Same foreign currency.
                            amount = abs(line.amount_residual_currency)
                        else:
                            # Different foreign currencies.
                            amount = move.company_currency_id._convert(
                                abs(line.amount_residual),
                                move.currency_id,
                                move.company_id,
                                line.date,
                            )

                        if move.currency_id.is_zero(amount):
                            continue

                        payments_widget_vals['content'].append({
                            'journal_name': line.ref or line.move_id.name,
                            'amount': amount,
                            'currency': move.currency_id.symbol,
                            'id': line.id,
                            'move_id': line.move_id.id,
                            'position': move.currency_id.position,
                            'digits': [69, move.currency_id.decimal_places],
                            'payment_date': fields.Date.to_string(line.date),
                        })
                    else:
                        pass
                elif move.move_type == 'out_invoice' or move.move_type == 'out_refund' or move.move_type == 'out_receipt':
                    if line.payment_id.type_of_sale == move.type_of_sale:
                        if line.currency_id == move.currency_id:
                            # Same foreign currency.
                            amount = abs(line.amount_residual_currency)
                        else:
                            # Different foreign currencies.
                            amount = move.company_currency_id._convert(
                                abs(line.amount_residual),
                                move.currency_id,
                                move.company_id,
                                line.date,
                            )

                        if move.currency_id.is_zero(amount):
                            continue

                        payments_widget_vals['content'].append({
                            'journal_name': line.ref or line.move_id.name,
                            'amount': amount,
                            'currency': move.currency_id.symbol,
                            'id': line.id,
                            'move_id': line.move_id.id,
                            'position': move.currency_id.position,
                            'digits': [69, move.currency_id.decimal_places],
                            'payment_date': fields.Date.to_string(line.date),
                        })
                    else:
                        pass


            if not payments_widget_vals['content']:
                continue

            move.invoice_outstanding_credits_debits_widget = json.dumps(payments_widget_vals)
            move.invoice_has_outstanding = True


    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount_show(self):
        print('Se va a computar el amount: ')
        for move in self:
            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed_show = 0.0
            total_untaxed_currency_show = 0.0
            total_tax_show = 0.0
            total_tax_currency_show = 0.0
            total_to_pay_show = 0.0
            total_residual_show = 0.0
            total_residual_currency_show = 0.0
            total_show = 0.0
            total_currency_show = 0.0
            currencies_show = move._get_lines_onchange_currency().currency_id

            for line in move.line_ids:
                if move._payment_state_matters():
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed_show amount.
                        total_untaxed_show += line.balance
                        total_untaxed_currency_show += line.amount_currency
                        total_show += line.balance
                        total_currency_show += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax_show += line.balance
                        total_tax_currency_show += line.amount_currency
                        total_show += line.balance
                        total_currency_show += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay_show += line.balance
                        total_residual_show += line.amount_residual
                        total_residual_currency_show += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total_show += line.balance
                        total_currency_show += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            if move.sum_account_sale == 1 or move.sum_account_purchase == 1:
                if move.is_primary_accountform_sale or move.is_primary_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 2 or move.sum_account_purchase == 4:
                if move.is_office_accountform_sale or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 3 or move.sum_account_purchase == 5:
                if move.is_primary_accountform_sale or move.is_primary_accountform_purchase or move.is_office_accountform_sale or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 4 or move.sum_account_purchase == 16:
                if move.is_ben_dis_accountform_sale or move.is_ben_dis_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 5 or move.sum_account_purchase == 17:
                if move.is_ben_dis_accountform_sale or move.is_ben_dis_accountform_purchase or move.is_primary_accountform_sale or move.is_primary_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 6 or move.sum_account_purchase == 20:
                if move.is_ben_dis_accountform_sale or move.is_ben_dis_accountform_purchase or move.is_office_accountform_sale or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_sale == 7:
                if move.sum_account_purchase == 21:
                    if move.is_primary_accountform_sale or move.is_primary_accountform_purchase or move.is_office_accountform_sale or move.is_office_accountform_purchase or move.is_ben_dis_accountform_sale or move.is_ben_dis_accountform_purchase:
                        move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                        move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                        move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                        move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                        move.amount_untaxed_signed_show = -total_untaxed_show
                        move.amount_tax_signed_show = -total_tax_show
                        move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                        move.amount_residual_signed_show = total_residual_show
                        move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                    else:
                        move.amount_untaxed_show = 0
                        move.amount_tax_show = 0
                        move.amount_total_show = 0
                        move.amount_residual_show = 0
                        move.amount_untaxed_signed_show = 0
                        move.amount_tax_signed_show = 0
                        move.amount_total_signed_show = 0
                        move.amount_residual_signed_show = 0
                        move.amount_total_in_currency_signed_show = 0
                elif move.sum_account_purchase == 31:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 3:
                if move.is_primary_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 7:
                if move.is_primary_accountform_purchase or move.is_insume_accountform_purchase or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 6:
                if move.is_office_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 8:
                if move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 2:
                if move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 9:
                if move.is_primary_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 10:
                if move.is_associated_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0      
            elif move.sum_account_purchase == 11:
                if move.is_primary_accountform_purchase or move.is_associated_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 12:
                if move.is_office_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 13:
                if move.is_primary_accountform_purchase or move.is_office_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 14:
                if move.is_office_accountform_purchase or move.is_associated_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 15:
                if move.is_primary_accountform_purchase or move.is_office_accountform_purchase or move.is_associated_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 18:
                if move.is_insume_accountform_purchase or move.is_ben_dis_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 19:
                if move.is_insume_accountform_purchase or move.is_primary_accountform_purchase or move.is_ben_dis_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 22:
                if move.is_office_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 23:
                if move.is_primary_accountform_purchase or move.is_office_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 24:
                if move.is_ben_dis_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 25:
                if move.is_primary_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 26:
                if move.is_ben_dis_accountform_purchase or move.is_insume_accountform_purchase or move.is_associated_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 27:
                if move.is_primary_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_associated_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 28:
                if move.is_associated_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 29:
                if move.is_primary_accountform_purchase or move.is_associated_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_office_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 30:
                if move.is_associated_accountform_purchase or move.is_office_accountform_purchase or move.is_ben_dis_accountform_purchase or move.is_insume_accountform_purchase:
                    move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                    move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                    move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                    move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                    move.amount_untaxed_signed_show = -total_untaxed_show
                    move.amount_tax_signed_show = -total_tax_show
                    move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                    move.amount_residual_signed_show = total_residual_show
                    move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
                else:
                    move.amount_untaxed_show = 0
                    move.amount_tax_show = 0
                    move.amount_total_show = 0
                    move.amount_residual_show = 0
                    move.amount_untaxed_signed_show = 0
                    move.amount_tax_signed_show = 0
                    move.amount_total_signed_show = 0
                    move.amount_residual_signed_show = 0
                    move.amount_total_in_currency_signed_show = 0
            elif move.sum_account_purchase == 31:
                move.amount_untaxed_show = sign * (total_untaxed_currency_show if len(currencies_show) == 1 else total_untaxed_show)
                move.amount_tax_show = sign * (total_tax_currency_show if len(currencies_show) == 1 else total_tax_show)
                move.amount_total_show = sign * (total_currency_show if len(currencies_show) == 1 else total_show)
                move.amount_residual_show = -sign * (total_residual_currency_show if len(currencies_show) == 1 else total_residual_show)
                move.amount_untaxed_signed_show = -total_untaxed_show
                move.amount_tax_signed_show = -total_tax_show
                move.amount_total_signed_show = abs(total_show) if move.move_type == 'entry' else -total_show
                move.amount_residual_signed_show = total_residual_show
                move.amount_total_in_currency_signed_show = abs(move.amount_total_show) if move.move_type == 'entry' else -(sign * move.amount_total_show)
            else:
                move.amount_untaxed_show = 0
                move.amount_tax_show = 0
                move.amount_total_show = 0
                move.amount_residual_show = 0
                move.amount_untaxed_signed_show = 0
                move.amount_tax_signed_show = 0
                move.amount_total_signed_show = 0
                move.amount_residual_signed_show = 0
                move.amount_total_in_currency_signed_show = 0

            currency_show = currencies_show if len(currencies_show) == 1 else move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move._payment_state_matters() and move.state == 'posted':
                if currency_show.is_zero(move.amount_residual_show):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency_show.compare_amounts(total_to_pay_show, total_residual_show) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state