from platform import release
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit ='stock.picking.batch'

    gif_stock_batch= fields.Boolean(string="Fill Rate", release="partner_id.gif_fill_rate",store=True)

    gif_stockp_kanban_show = fields.Selection(string="Fill Rate", selection=[('1', 'Fill Rate'), ('0', 'None')], compute='get_fill_rate_kanban')

    @api.depends('gif_stock_batch')
    def get_fill_rate_kanban(self):
        for record in self:
            if record.gif_stock_batch == True:
                record.gif_stockp_kanban_show = "1"
            else:
                record.gif_stockp_kanban_show = "0"