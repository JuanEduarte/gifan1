from odoo import api, fields, models

#Campos
class GifProductTemplate(models.Model):
    _inherit="product.template"

    gif_ieps_active = fields.Boolean(string = "Desglosar IEPS en factura")
    gif_ieps_type_sale = fields.Selection(string='Tipo de IEPS para ventas', default='%',selection=[('%', 'Porcentual'),('$', 'Fijo')])
    gif_ieps_value_sale = fields.Float(string='Valor de IEPS para ventas', default=0.0)
    gif_ieps_type_purchase = fields.Selection(string='Tipo de IEPS para compras', default='%',selection=[('%', 'Porcentual'),('$', 'Fijo')])
    gif_ieps_value_purchase = fields.Float(string='Valor de IEPS para compras', default=0.0)
    
    
    @api.onchange('gif_ieps_value_sale','gif_ieps_type_sale')
    def _verificaValorIEPS_ventas(self):
        if self.gif_ieps_type_sale == '%':
            if 0.0 < self.gif_ieps_value_sale < 100.0:
                print("Valor del IEPS porcentual para ventas:",self.gif_ieps_value_sale)
            else:
                self.gif_ieps_value_sale = 0.0
        else:
            if self.gif_ieps_value_sale < 0.0:
                self.gif_ieps_value_sale = 0.0


    @api.onchange('gif_ieps_value_purchase','gif_ieps_type_purchase')
    def _verificaValorIEPS_compras(self):
        if self.gif_ieps_type_purchase == '%':
            if 0.0 < self.gif_ieps_value_purchase < 100.0:
                print("Valor del IEPS porcentual para compras:",self.gif_ieps_value_purchase)
            else:
                self.gif_ieps_value_purchase = 0.0
        else:
            if self.gif_ieps_value_purchase < 0.0:
                self.gif_ieps_value_purchase = 0.0
