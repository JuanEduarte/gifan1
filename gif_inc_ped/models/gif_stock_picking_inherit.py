from odoo import models,fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    gif_has_pediment = fields.Boolean(default=False)
