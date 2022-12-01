from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.move'
    
    file_data = fields.Binary('Archivo', required=True,)
    file_name = fields.Char('nombre del archivo')
    gif_journal = fields.Many2one( comodel_name='account.journal', string='Diario')
    confirm = fields.Char(string='Confirmar')
    memo = fields.Char(string='Memo')
    
       