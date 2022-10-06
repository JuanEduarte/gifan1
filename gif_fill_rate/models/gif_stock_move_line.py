from platform import release
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit="stock.move.line"    
    
    
    gif_stock_move_line = fields.Boolean(string="Fill Rate", related="picking_partner_id.gif_fill_rate", store=True)

    gif_stockml_kanban_show = fields.Selection(string="Fill Rate", selection=[('1', 'Fill Rate'), ('0', 'None')], compute='get_fill_rate_kanban')

    @api.depends('gif_stock_move_line')
    def get_fill_rate_kanban(self):
        for record in self:
            if record.gif_stock_move_line == True:
                record.gif_stockml_kanban_show = "1"
            else:
                record.gif_stockml_kanban_show = "0"