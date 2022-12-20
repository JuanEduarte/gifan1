# -*- coding: utf-8 -*-
from odoo import api, models, _
import base64
import re
from num2words import num2words
from lxml import etree
from lxml.objectify import fromstring
from xml.etree.ElementTree import tostring

class GifAccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    # -------------------------------------------------------------------------
    # CFDI: Helpers
    # -------------------------------------------------------------------------

    def get_other_vals(self, move):
        
        saleOrder = self.env['sale.order'].search([('name','=',move.invoice_origin)], limit=1)
        
        if saleOrder:
            # Dates
            init_date = saleOrder.gif_init_date
            cancel_date = saleOrder.validity_date
            # Origin
            sale_order_origin = saleOrder.origin
            # Provider
            supplier_code = saleOrder.gif_supplier_code
            
        else:
            init_date = None
            cancel_date = None
            supplier_code = None
            sale_order_origin = None


        # Products quantity
        cnt = {}
        for line in move.invoice_line_ids:
            cnt[line.product_id.name] = cnt.get(line.product_id.name, 0) + 1


        # Payment terms
        payment_terms = move.invoice_payment_term_id
        term = payment_terms.line_ids.filtered(lambda t: t.value == 'balance')

        if term:
            if len(term) == 1:
                payment_term_days = term.days
            else:
                payment_term_days = term[0].days
        else:
            payment_term_days = 0


        # Company full direction
        company = move.company_id

        company_direction = company.street_number + \
                    company.street_number2 + \
                    company.l10n_mx_edi_colony + \
                    company.city + \
                    company.state_id.name + \
                    'CP' + company.zip
        company_direction.upper()
        

        vals = {
            'init_date':init_date,
            'cancel_date':cancel_date,
            'products_cnt': len(cnt),
            'sale_order_id':saleOrder,
            'supplier_code': supplier_code,
            'sale_order_origin':sale_order_origin,
            'payment_term_days':payment_term_days,
            'company_direction':company_direction,
            'no_identify':None
        }

        return vals

    

    @api.model
    def _l10n_mx_edi_cfdi_append_addenda(self, move, cfdi, addenda):
        ''' Append an additional block to the signed CFDI passed as parameter.
        :param move:    The account.move record.
        :param cfdi:    The invoice's CFDI as a string.
        :param addenda: The addenda to add as a string.
        :return cfdi:   The cfdi including the addenda.
        '''
        # addenda_values = {'record': move, 'cfdi': cfdi}

        def num2word(num, currency_name):
            unit = {'MXN':'PESO', 'USD':'DOLAR', 'EUR':'EURO'}
            units = {'MXN':'PESOS', 'USD':'DOLARES', 'EUR':'EUROS'}
            
            u = units if int(num) > 1 else unit

            unit = num2words( int(num), lang='es', to='currency')
            unit = re.sub('euro(s)?', u.get(currency_name,''), unit)

            ns = str(num)
            subunit = ns[ns.find('.')+1 :]
            
            curr = {'MXN':'M.N.'}.get(currency_name,'')
            total = "%s %s/100 %s" %(unit, subunit, curr)
            return total.upper()


        cfdi_values = {
            **self._l10n_mx_edi_get_invoice_cfdi_values(move),
            **self.get_other_vals(move),
            'num2word':num2word
        }
        cfdi_values["only_date"] = cfdi_values['cfdi_date'].split('T')[0]
        
        #print(cfdi_values)
        
        addenda = addenda._render(cfdi_values).strip()
        # addenda = addenda._render(values=addenda_values).strip()
        # print(addenda)
        
        if not addenda:
            return cfdi

        cfdi_node = fromstring(cfdi)
        addenda_node = fromstring(addenda)
        version = cfdi_node.get('Version')

        if 'Complemento' in addenda_node.tag:
            ns = {'detallista':"http://www.sat.gob.mx/detallista"}
            complement_node = cfdi_node.find('{http://www.sat.gob.mx/cfd/%s}Complemento' % version[0])
            complement_node.set('detallista',"http://www.sat.gob.mx/detallista")

            detallista_node = addenda_node.find('detallista:detallista', ns)
            complement_node.append(detallista_node)

        elif 'Addenda' in addenda_node.tag:
            addenda_node.tag = '{http://www.sat.gob.mx/cfd/%s}Addenda' % version[0]

        # Add a root node Addenda if not specified explicitly by the user.
        elif addenda_node.tag != '{http://www.sat.gob.mx/cfd/%s}Addenda' % version[0]:
            node = etree.Element(etree.QName('http://www.sat.gob.mx/cfd/%s' % version[0], 'Addenda'))
            node.append(addenda_node)
            addenda_node = node

        cfdi_node.append(addenda_node)
        #return etree.tostring(cfdi_node, pretty_print=True, xml_declaration=True, encoding='UTF-8')