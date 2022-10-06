from odoo import models,api,fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    gif_own_inverse_currency_purchase = fields.Float(string='Tasa Manual',digits=(12,12))
    gif_own_currency_check_purchase = fields.Boolean(string='Encender Tasa de Cambio')
    gif_wr_code = fields.Char(default='')

    @api.onchange('currency_id')
    def _onchange_currency_id_write_code_gcc(self):
        if self.gif_wr_code == '':
            self.gif_wr_code = self.currency_id.name
        else:
            pass
    
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
            divisa = self.env['res.currency'].search([('name','=','USD')])
            # self.pricelist_id.currency_id.inverse_rate = self.gif_own_inverse_currency
            self.gif_purchase_inverse_currency = self.gif_own_inverse_currency_purchase
            self.gif_temp_validator = self.gif_own_inverse_currency_purchase
            divisa.rate_ids[0].inverse_company_rate = self.gif_own_inverse_currency_purchase
    
    
