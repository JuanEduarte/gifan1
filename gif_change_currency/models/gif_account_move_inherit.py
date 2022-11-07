from odoo import models,fields,api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_actual_currency(self):
        divisa = self.env['res.currency'].search([('name','=','USD')])
        return divisa.rate_ids[0].inverse_company_rate

    gif_own_currency_check_account = fields.Boolean(string='Encender Tasa Manual')
    gif_own_inverse_currency_account = fields.Float(string='Tasa de Cambio',digits=(12,12),default=_get_actual_currency)
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
    def _onchange_currency_id_gcc(self):
        self.gif_wr_code = self.currency_id.name

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids_gcc(self):
        try:
            if self.type_of_purchase.id != False:
                for record in self.invoice_line_ids:
                    for detail in record.product_id.partners_details_purchase:
                        if detail.currency_purchase:
                            if self.gif_wr_code == 'MXN' and detail.currency_purchase.name == 'MXN':
                                self.gif_own_currency_check_account = False
                            else:
                                self.gif_own_currency_check_account = True
                            break
                        else:
                            self.gif_own_currency_check_account = False
            elif self.type_of_sale.id != False:
                for record in self.invoice_line_ids:
                    for detail in record.product_id.partners_details:
                        if detail.currency_sale:
                            if self.gif_wr_code == 'MXN' and detail.currency_sale.name == 'MXN':
                                self.gif_own_currency_check_account = False
                            else:
                                self.gif_own_currency_check_account = True
                            break
                        else:
                            self.gif_own_currency_check_account = False
        except Exception as e:
            self.gif_own_currency_check_account = False
            print('Error: ',e)

    @api.onchange('gif_own_inverse_currency_account')
    def _onchange_gif_own_inverse_currency_account_gcc(self):
        if self.gif_own_inverse_currency_account > 0:
            self.gif_own_currency_check_account = True
            divisa = self.env['res.currency'].search([('name','=','USD')])
            self.gif_temp_account = self.gif_own_inverse_currency_account
            divisa.rate_ids[0].inverse_company_rate = self.gif_own_inverse_currency_account
            try:
                for line in self.line_ids:
                    line._onchange_amount_currency()
            except Exception as e:
                print('Error: ',e)

    @api.onchange('date', 'currency_id')
    def _onchange_currency(self):
        currency = self.currency_id or self.company_id.currency_id

        if self.is_invoice(include_receipts=True):
            if self.gif_own_inverse_currency_account != 0:
                pass
            else:
                for line in self._get_lines_onchange_currency():
                    line.currency_id = currency
                    line._onchange_currency()
        else:
            for line in self.line_ids:
                line._onchange_currency()

        self._recompute_dynamic_lines(recompute_tax_base_amount=True)
    
    

class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        res = super(AccountMoveReversal,self).reverse_moves()
        if self.move_ids.gif_own_inverse_currency_account > 0:
            divisa = self.env['res.currency'].search([('name','=','USD')])
            if divisa:
                divisa.rate_ids[0].inverse_company_rate = self.move_ids.gif_own_inverse_currency_account
        try:
            return res
        except Exception as e:
            print('Error: ')
            print(e)
    
