from odoo import models,api,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_actual_currency(self):
        divisa = self.env['res.currency'].search([('name','=','USD')])
        return divisa.rate_ids[0].inverse_company_rate

    gif_own_currency_check_sale = fields.Boolean(string='Encender Tasa de Cambio')
    gif_write_code = fields.Char(default="")
    gif_own_inverse_currency = fields.Float(string='Tasa Manual',digits=(12,12),default=_get_actual_currency)

    gif_is_usd = fields.Boolean(compute='_gif_is_usd')

    @api.onchange('pricelist_id')
    def _gif_is_usd(self):
        for record in self:
            if record.pricelist_id.currency_id.name != False:
                if 'USD' in record.pricelist_id.currency_id.name:
                    record.gif_is_usd = True
                else:
                    record.gif_is_usd = False
            else:
                    record.gif_is_usd = False
    
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id_write_name_gcc(self):
        self.gif_write_code = self.pricelist_id.currency_id.name
    
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
            # self.gif_own_currency_check_sale = True
            divisa = self.env['res.currency'].search([('name','=','USD')])
            self.gif_sale_inverse_currency = self.gif_own_inverse_currency
            divisa.rate_ids[0].inverse_company_rate = self.gif_own_inverse_currency
            

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder,self)._prepare_invoice()
        if self.gif_own_inverse_currency > 0:
            invoice_vals['gif_own_inverse_currency_account'] = self.gif_own_inverse_currency
            invoice_vals['gif_own_currency_check_account'] = self.gif_own_currency_check_sale
        return invoice_vals
    
