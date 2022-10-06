from platform import release
from odoo import api, fields, models


class Stockmove(models.Model):
    _inherit="stock.move"

    gif_stock_move=fields.Boolean(string="Fill Rate", related="partner_id.gif_fill_rate",store=True)

    gif_stockm_kanban_show = fields.Selection(string="Fill Rate", selection=[('1', 'Fill Rate'), ('0', 'None')], compute='get_fill_rate_kanban')

    @api.depends('gif_stock_move')
    def get_fill_rate_kanban(self):
        for record in self:
            if record.gif_stock_move == True:
                record.gif_stockm_kanban_show = "1"
            else:
                record.gif_stockm_kanban_show = "0"