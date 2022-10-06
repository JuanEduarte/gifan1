from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit= 'account.move' 

    gif_account_fill_rate= fields.Boolean(string="Fill Rate", related='partner_id.gif_fill_rate', store=True)
    gif_account_change = fields.Boolean(string="Fill Rate", default=False, compute='change_view')


    @api.depends('gif_account_fill_rate')
    def change_view(self):
        for record in  self:
            if record.gif_account_fill_rate == True:
                if record.move_type=='out_invoice' or record.move_type=='out_refund' or record.move_type=='out_receipt' :
                    record.gif_account_change = True
                else:
                    record.gif_account_change = False

            return record.gif_account_change

