from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    gif_real_stock1 = fields.Float(
        string=' Cantidad Real Entregada', compute='suma_resultado')
    gif_real_stockpicking = fields.Float(string='Cantidad Entregada')
    related_type = fields.Many2one(comodel_name='stock.picking')
    gif_total_units = fields.Float(
    string=' Unidades totales', compute='total_units')
    unit_type = fields.Many2one(comodel_name='uom.uom')

    def suma_resultado(self):
        for record in self:
            print(record.state)
            entregas = record.order_id.picking_ids
            print(entregas)
            counter = 0
            for entrega in entregas:
                for line in entrega.move_line_ids_without_package:
                    print(line.gif_real_stockpicking)
                    counter += line.gif_real_stockpicking

            record.gif_real_stock1 = counter

    def total_units(self):
        for record in self:
          record.gif_total_units = record.product_uom.ratio * record.product_uom_qty
