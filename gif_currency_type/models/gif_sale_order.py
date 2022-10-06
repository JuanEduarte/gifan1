from odoo import models, fields
class GifSaleOrder(models.Model):
    _inherit = 'sale.order'
    coin_type = fields.Many2one('sale.order', string='Tipo de Moneda')