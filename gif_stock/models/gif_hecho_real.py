from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    gif_real_stock1= fields.Float(string=' Cantidad Real Entregada' ,compute= 'suma_resultado')
    gif_real_stockpicking= fields.Float(string='Cantidad Entregada')
    related_type = fields.Many2one(comodel_name='stock.picking')
    gif_total_units= fields.Float(string=' Unidades totales', compute='unidades_totales') 
    unit_type= fields.Many2one(comodel_name='uom.uom')

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
            
            record.gif_real_stock1 =  counter

    def unidades_totales(self): 
        for record in self:
            unit = record.product_uom.name
            if unit == 'Tarima':
                res= record.product_uom_qty * 50
                record.gif_total_units=res
            if unit == 'Empaque':
                res= record.product_uom_qty * 20
                record.gif_total_units=res
            if unit == 'Docenas':
                res= record.product_uom_qty * 12
                record.gif_total_units=res
            if unit == 'Unidades':
                res= record.product_uom_qty * 1
                record.gif_total_units=res
                
              
    

    