from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit= 'sale.order' 

    gif_sale_fill_rate= fields.Boolean(string="Fill Rate", related='partner_id.gif_fill_rate', store=True )

    gif_sale_kanban_show = fields.Selection(string="Fill Rate", selection=[('1', 'Fill Rate'), ('0', 'None')], compute='get_fill_rate_kanban')

    @api.depends('gif_sale_fill_rate')
    def get_fill_rate_kanban(self):
        for record in self:
            if record.gif_sale_fill_rate == True:
                record.gif_sale_kanban_show = "1"
            else:
                record.gif_sale_kanban_show = "0"