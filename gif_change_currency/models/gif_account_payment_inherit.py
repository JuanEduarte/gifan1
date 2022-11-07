from odoo import models,api,fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _get_actual_currency(self):
        divisa = self.env['res.currency'].search([('name','=','USD')])
        return divisa.rate_ids[0].inverse_company_rate

    gif_manual_currency = fields.Boolean(string='Habilitar Tasa Manual',default=False)
    gif_inverse_currency = fields.Float(string='Tasa Manual',digits=(12,12),default=_get_actual_currency)
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
    def _onchange_currency_id_gcc(self):
        try:
            if self.currency_id.name == 'USD':
                self.gif_manual_currency = True
        except:
            self.gif_manual_currency = False

    @api.onchange('gif_inverse_currency')
    def _onchange_gif_inverse_currency(self):
        if self.gif_inverse_currency > 0 and self.gif_manual_currency == True:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            divisa.rate_ids[0].inverse_company_rate = self.gif_inverse_currency

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    gif_manual_currency = fields.Boolean(string='Habilitar Tasa Manual',default=False)
    gif_inverse_currency = fields.Float(string='Tasa Manual')

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
    def _onchange_currency_id_gcc(self):
        try:
            if self.currency_id.name == 'USD' and self.line_ids.move_id.gif_own_inverse_currency_account > 0:
                self.gif_manual_currency = True
                self.gif_inverse_currency = self.line_ids.move_id.gif_own_inverse_currency_account
        except:
            self.gif_manual_currency = False

    @api.onchange('gif_inverse_currency')
    def _onchange_gif_inverse_currency(self):
        if self.gif_inverse_currency > 0 and self.gif_manual_currency == True:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            divisa.rate_ids[0].inverse_company_rate = self.gif_inverse_currency
            self._compute_amount()
    

    

    
    
    
    
    
    
