
from odoo import api, fields, models


class GitStockPicking(models.Model):
    _inherit="stock.move.line"

    gif_unidad_stock=fields.Many2one('uom.uom', domain="[('category_id', '=', product_uom_category_id)]")


    @api.onchange('qty_done')
    def gif_unidad(self):
        for record in self:
            if record.qty_done > 0.1:
                record.gif_unidad_stock = 1 
        
    @api.onchange('gif_unidad_stock')
    def gif_unidad_oculto(self):
        for record in self:
                record.product_uom_id = record.gif_unidad_stock





