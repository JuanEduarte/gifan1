from odoo import models, fields, api

class StockPickingLine(models.Model):
    _inherit = 'stock.picking'
    
    gif_real_stockpicking= fields.Float(string='Cantidad Entregada')
    # gif_ocultar= fields.Char(string=' Cantidad' ,compute='ocultar_resultado')
    gif_prueba_boton = fields.Boolean(string='prueba',default= False, compute='ocultar_resultado')
    gif_select_all= fields.Boolean(string='Seleccionar todos', default= False)

    
    @api.onchange('picking_type_id')
    def ocultar_resultado(self):
        for record in self:
            #resultado = self.env['stock.move.line'].search([('product_id','=',record.product_id.id)])
            print("##################################################################")
            for entrada in record.picking_type_id:  
                if entrada.name == 'Recolección' or entrada.name=='Órdenes de entrega':
                    print(entrada.name)
                    record.gif_prueba_boton = True
                else:
                    record.gif_prueba_boton = False
                
                
            print(record.gif_prueba_boton)
     
            