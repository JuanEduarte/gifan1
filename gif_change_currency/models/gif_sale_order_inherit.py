from odoo import models,api,fields


class GifSaleOrder(models.Model):
    _inherit = 'sale.order'

    gif_own_currency_check_sale = fields.Boolean(string='Encender Tasa de Cambio')
    gif_write_code = fields.Char(default="")
    gif_own_inverse_currency = fields.Float(string='Tasa Manual',digits=(12,12))
    
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id_write_name_gcc(self):
        if self.gif_write_code == "":
            self.gif_write_code = self.pricelist_id.currency_id.name
        else:
            pass
    
    ##Si ponen el tipo de cambio, se va con él, si no tiene que ir con odoo
    ## Al poner el tipo de cambio manual, se tiene que ir a actualizar al ultimo que tiene odoo con ese valor.

    @api.onchange('order_line')
    def _is_own_check(self):
        try:
            for record in self.order_line:
                for detail in record.product_template_id.partners_details:
                    if detail.currency_sale:
                        if self.gif_write_code == 'MXN' and detail.currency_sale.name == 'MXN':
                            self.gif_own_currency_check_sale = False
                        else:
                            self.gif_own_currency_check_sale = True
        except:
            self.gif_own_currency_check_sale = False

    @api.onchange('gif_own_inverse_currency')
    def _onchange_gif_own_inverse_currency_gcc(self):
        if self.gif_own_inverse_currency > 0:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            # self.pricelist_id.currency_id.inverse_rate = self.gif_own_inverse_currency
            self.gif_sale_inverse_currency = self.gif_own_inverse_currency
            divisa.rate_ids[0].inverse_company_rate = self.gif_own_inverse_currency
    

    
