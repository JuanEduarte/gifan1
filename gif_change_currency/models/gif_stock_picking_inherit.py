from odoo import models, api, fields


class Picking(models.Model):
    _inherit = 'stock.picking'

    def _get_actual_currency(self):
        divisa = self.env['res.currency'].search([('name','=','USD')])
        return divisa.rate_ids[0].inverse_company_rate

    gif_check_currency = fields.Boolean(string='Encender Tasa Manual')
    gif_custom_currency = fields.Float(string='Tasa de Cambio Manual',default=_get_actual_currency)

    @api.onchange('gif_custom_currency')
    def _onchange_gif_custom_currency(self):
        if self.gif_custom_currency > 0:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            if divisa:
                divisa.rate_ids[0].inverse_company_rate = self.gif_custom_currency

    def button_validate(self):
        if self.gif_custom_currency > 0:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            if divisa:
                divisa.rate_ids[0].inverse_company_rate = self.gif_custom_currency
        res = super(Picking,self).button_validate()
        return res
    
    
    
