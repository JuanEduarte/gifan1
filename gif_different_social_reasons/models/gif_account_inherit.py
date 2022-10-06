from odoo import api, fields, models



class AccountMove(models.Model):
    _inherit = 'account.move'

    group_s = fields.Many2one(string="Grupos", related="partner_id.group_id",store=True)

class AccountPayment(models.Model):
    _inherit = "account.payment"

    group_s = fields.Many2one(string="Grupos", related="partner_id.group_id",store=True)

