
from odoo import api, fields, models
import json


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    gif_memo = fields.Char(string="Memo")
    gif_payment_lines = fields.One2many('account.payment','payment_id', string ="Payment lines")
    gif_account_payment_ids = fields.Many2many('account.payment', string="Pagos Desglosados", compute='_get_payment_move')

    def _get_payment_move(self):
        for record in self:
            payments = self.env['account.payment'].search([('ref', 'ilike', record.name)])
            if record.state not in ['cancel','draft']:
                pagos = [(6, 0, payments.ids)]
                record.update({'gif_account_payment_ids': pagos})
            else:
                record.gif_account_payment_ids = False
            
            

    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_reconciled_info(self):
        for record in self:
            res= super(AccountMove,self)._compute_payments_widget_reconciled_info()
            json = record._get_reconciled_info_JSON_values()
            for payment in json:
                pago = self.env['account.payment'].search([('id', '=', payment['account_payment_id'])])
                pago.ref = record.name
                record.payment_id = pago.payment_id  

            return res
            