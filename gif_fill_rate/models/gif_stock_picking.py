
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit='stock.picking'

    gif_stock_fill_rate = fields.Boolean(string="Con Fill Rate", related='partner_id.gif_fill_rate', store=True )

    gif_stock_kanban_show = fields.Selection(string="Fill Rate", selection=[('1', 'Fill Rate'), ('0', 'None')], compute='get_fill_rate_kanban')

    @api.depends('gif_stock_fill_rate')
    def get_fill_rate_kanban(self):
        for record in self:
            if record.gif_stock_fill_rate == True:
                record.gif_stock_kanban_show = "1"
            else:
                record.gif_stock_kanban_show = "0"