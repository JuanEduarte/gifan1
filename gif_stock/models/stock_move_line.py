from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    gif_real_stockpicking= fields.Float(string='Cantidad Entregada')
    # gif_real_stock2 = fields.Float(string='Cantidad Real',compute="_calcule_salida")
    gif_real_stock = fields.Float(string='Cantidad Real Entregada',compute="_calcule_salida")
    # gif_real = fields.Char(related='gif_real_stock.gif_real_stock1')
    gif_real_type = fields.Char(string='Picking Name', compute="calcule_valor")
    gif_real = fields.Float(string='Entregado Real', compute='equalization', readonly=False )
    

    def _calcule_salida(self):
        for record in self:
            total=self.env['stock.move.line']
            total_productos=total.search_count([('product_id','=',record.product_id.id)])
            total = record.picking_id
            print(total)
            print("#############")
            counter = 0
            for total in total:
                for line in total.move_line_ids_without_package:
                    print(line.gif_real_stockpicking)
                    counter += line.gif_real_stockpicking
            
            record.gif_real_stock =  counter



    def calcule_valor(self):
        for record in self:
            if record.picking_id.picking_type_id.id:
                record.gif_real_type = record.picking_id.picking_type_id.code
            else:
                record.gif_real_type = ''

            print(record.gif_real_type)
    
    def equalization(self):
        for record in self:
            if record.picking_id.gif_select_all == True:
                res = record.qty_done 
            else:
                res = 0
            record.gif_real= res
                
        