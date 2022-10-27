from odoo import models, fields, api, _


class Gif_real_delivery(models.Model):
    _inherit = 'sale.order.line'
    
    real_qty = fields.Char(string="Cantidad real entregada")
    
    '''@api.onchange("state")
    def _onchange_field_state_condition(self):
        for record in self:
            if record.state = 'confirm':'''
                
              
            
            
