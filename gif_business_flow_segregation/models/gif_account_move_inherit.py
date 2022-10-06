from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    change_account = fields.Boolean(default=False,compute="_change")
    

    @api.depends('change_account')
    def _change(self):
        print('El change')
        # for record in self:
            # print(record.account_root_id)
            # print(record.commercial_partner_id.name)
            # print(record.journal_id.name)
            # print(record.highest_name)
        self.change_account = True

    # @api.onchange('journal_id')
    # def _onchange_change(self):
    #     print('Este es conta')
    #     for record in self:
    #         print('Se hace: ')
    #         print(record.company_currency_id)
    #         print(record.commercial_partner_id)
    
    
    
