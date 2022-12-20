from odoo import api, fields, models
import json
from odoo.tools.misc import formatLang

class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS_AM',default=False)

    gif_tax_totals_json = fields.Char(compute='_compute_gif_tax_totals_json')

    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    def  _compute_gif_tax_totals_json(self):
        def gif_compute_taxes(order_line):
            return order_line.taxes_id._origin.gif_compute_all(**order_line._prepare_compute_all_values())

        account_move = self.env['account.move']
        for order in self:
            gif_subtotal = 0
            for line in order.order_line:
                gif_subtotal += line.gif_price_subtotal_ieps
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, gif_compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, gif_subtotal, order.currency_id)
            order.gif_tax_totals_json = json.dumps(tax_totals)

    @api.onchange('partner_id')
    def _show_purchase_ieps(self):
        for record in self:
            if record.partner_id.id != False:
                if record.partner_id.gif_ieps_desglose == True:
                    record.gif_IepsDisplay = True
                else:
                    record.gif_IepsDisplay = False
            else:
                record.gif_IepsDisplay = False
    

    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    def  _compute_tax_totals_json(self):
        ieps = 0.0
        for line in self.order_line:
            if line.gif_PurchaseOrderIeps != 0 and line.gif_PurchaseOrderIeps != False:
                ieps = ieps + line.gif_PurchaseOrderIeps

        def compute_taxes(order_line):
            return order_line.taxes_id._origin.compute_all(**order_line._prepare_compute_all_values())


        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            tax_totals['allow_tax_edition'] = True
            currency = order.currency_id
            order.tax_totals_json = json.dumps(tax_totals)

class PurchaseOrderLine(models.Model):
    _inherit="purchase.order.line"
     
    gif_IepsDisplayOL = fields.Boolean(string='DisplayFieldIEPS',compute='_get_purchase_ieps_ol')
    gif_PurchaseOrderIeps = fields.Float(string='IEPS',store=True)#compute='_onchange_price_unit_gif_ieps'
    gif_price_unit_ieps = fields.Float(string='Gif Price Unit',compute='_gif_onchange_price_unit_ieps')
    gif_price_subtotal_ieps = fields.Float(string='Gif Price Subtotal',compute='_gif_onchange_price_subtotal_ieps')
    gif_tax_id_ieps = fields.Char(string='Gif Tax',compute='_gif_onchange_tax_id_ieps')

    @api.onchange('taxes_id')
    def _gif_onchange_tax_id_ieps(self):
        for record in self:
            if len(record.taxes_id) > 0:
                string_ieps = ""
                for tax in record.taxes_id:
                    if 'IEPS' in tax.name:
                        continue
                    else:
                        string_ieps = string_ieps +' ' + tax.description or tax.name
                record.gif_tax_id_ieps = string_ieps
            else:
                record.gif_tax_id_ieps = False

    @api.onchange('price_subtotal','gif_PurchaseOrderIeps')
    def _gif_onchange_price_subtotal_ieps(self):
        for record in self:
            if record.price_subtotal != False:
                record.gif_price_subtotal_ieps = record.price_subtotal + record.gif_PurchaseOrderIeps
            else:
                record.gif_price_subtotal_ieps = 0

    @api.onchange('price_unit','gif_PurchaseOrderIeps')
    def _gif_onchange_price_unit_ieps(self):
        for record in self:
            if record.price_unit != False:
                record.gif_price_unit_ieps = (record.price_subtotal + record.gif_PurchaseOrderIeps) / record.product_qty
            else:
                record.gif_price_unit_ieps = 0
    
    

    @api.onchange('product_template_id')
    def _get_purchase_ieps_ol(self):
        for record in self:
            if record.order_id.partner_id.gif_ieps_desglose == True:
                record.gif_IepsDisplayOL = True
                break
            else:
                record.gif_IepsDisplayOL = False

    def _prepare_compute_all_values(self):
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'currency': self.order_id.currency_id,
            'quantity': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
            'ieps':  self.gif_PurchaseOrderIeps,
        }

    

    @api.onchange('price_unit','product_qty')
    def _onchange_price_unit_gif_ieps(self):
        for record in self:
            if record.product_template_id.gif_type_ieps != False:
                if record.product_template_id.gif_type_ieps == '2':
                    record.gif_PurchaseOrderIeps = record.product_template_id.gif_ieps_purchase_fij * record.product_uom.ratio * record.product_qty
                elif record.product_template_id.gif_type_ieps == '1':
                    amount = 0
                    for i in record.taxes_id:
                        if 'IEPS' in i.name:
                            amount = i.amount
                            break
                    if amount != 0:
                        record.gif_PurchaseOrderIeps = record.price_subtotal * (amount / 100)
                    else:
                        record.gif_PurchaseOrderIeps = 0
                if 'USD' in record.order_id.currency_id.name:
                        record.gif_PurchaseOrderIeps = record.gif_PurchaseOrderIeps / record.order_id.gif_own_inverse_currency_purchase
                record.gif_PurchaseOrderIeps = 0

            record._compute_amount()

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _prepare_account_move_line(self,move=False):
        res = super(PurchaseOrderLine,self)._prepare_account_move_line()
        res['gif_AccountMoveIeps'] = self.gif_PurchaseOrderIeps
        return res

    