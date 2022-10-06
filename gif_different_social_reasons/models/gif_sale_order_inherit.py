from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    group_s = fields.Many2one(string="Grupos", related="partner_id.group_id",store=True)