
from datetime import datetime
from odoo import api, fields, models
from pytz import timezone

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

    @api.onchange('expiration_date')
    def onchange_expiration_date(self):
        for record in self:
            # now_dt = datetime.now(timezone(self.env.user.tz))
            if self.expiration_date:
                record.lot_name = str(self.expiration_date.astimezone(timezone(self.env.user.tz)).date()).replace('-','')

