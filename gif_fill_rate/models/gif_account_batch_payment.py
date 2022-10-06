from platform import release
from odoo import api, fields, models


class AccountBatchPayment(models.Model):
    _inherit="account.batch.payment"

    
    gif_account_batch_fill_rate= fields.Boolean(string="Fill Rate", release='partner_id.gif_fill_rate', store=True)
