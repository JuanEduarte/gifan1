from odoo import models,api,fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_actual_currency(self):
        divisa = self.env['res.currency'].search([('name','=','USD')])
        return divisa.rate_ids[0].inverse_company_rate

    gif_own_inverse_currency_purchase = fields.Float(string='Tasa Manual',digits=(12,12),default=_get_actual_currency)
    gif_own_currency_check_purchase = fields.Boolean(string='Encender Tasa de Cambio',default=False)
    gif_wr_code = fields.Char(default='')

    gif_is_usd = fields.Boolean(compute='_gif_is_usd')

    @api.onchange('currency_id')
    def _gif_is_usd(self):
        for record in self:
            if record.currency_id.name != False:
                if 'USD' in record.currency_id.name:
                    record.gif_is_usd = True
                else:
                    record.gif_is_usd = False
            else:
                record.gif_is_usd = False

    @api.onchange('currency_id')
    def _onchange_currency_id_write_code_gcc(self):
        self.gif_wr_code = self.currency_id.name
    
    @api.onchange('order_line')
    def _onchange_order_line_gcc(self):
        try:
            for record in self.order_line:
                for detail in record.product_template_id.partners_details_purchase:
                    if detail.currency_purchase:
                        if self.gif_wr_code == 'MXN' and detail.currency_purchase.name == 'MXN':
                            self.gif_own_currency_check_purchase = False
                        else:
                            self.gif_own_currency_check_purchase = True
        except:
            self.gif_own_currency_check_purchase = False

    @api.onchange('gif_own_inverse_currency_purchase')
    def _onchange_gif_own_inverse_currency_purchase(self):
        if self.gif_own_inverse_currency_purchase > 0:
            self.gif_own_currency_check_purchase = True
            divisa = self.env['res.currency'].search([('name','=','USD')])
            self.gif_purchase_inverse_currency = self.gif_own_inverse_currency_purchase
            self.gif_temp_validator = self.gif_own_inverse_currency_purchase
            divisa.rate_ids[0].inverse_company_rate = self.gif_own_inverse_currency_purchase
    
    
    def _prepare_invoice(self):
        for order in self:
            invoice_vals = super(PurchaseOrder,order)._prepare_invoice()
            if self.gif_own_inverse_currency_purchase > 0:
                    invoice_vals['gif_own_inverse_currency_account'] = self.gif_own_inverse_currency_purchase
                    invoice_vals['gif_own_currency_check_account'] = self.gif_own_currency_check_purchase
        return invoice_vals

        