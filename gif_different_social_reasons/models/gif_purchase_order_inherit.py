from odoo import api,fields,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    group_s = fields.Many2one(string="Grupos", related="partner_id.group_id",store=True)
