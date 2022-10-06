from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit= 'account.payment' 

    gif_account_pay_fill_rate= fields.Boolean(string="Fill Rate", related='partner_id.gif_fill_rate', store=True)
    gif_account_pay_change = fields.Boolean(string="Checar", default=False, compute='change_view')
    gif_account_batch_fill_rate=fields.Boolean(string="Fill Rate", related='partner_id.gif_fill_rate', store=True)
    


    @api.depends('gif_account_pay_fill_rate')
    def change_view(self):
        for record in  self:
            if record.gif_account_pay_fill_rate == True:
                if record.partner_type=='customer':
                    record.gif_account_pay_change = True
                else:
                    record.gif_account_pay_change = False

            return record.gif_account_pay_change