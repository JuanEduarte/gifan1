from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit="account.payment.register"