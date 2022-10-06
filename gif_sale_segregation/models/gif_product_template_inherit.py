from odoo import api,fields,models


class ProductTemplateSS(models.Model):
    _inherit = 'product.template'
    
    # product_type_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', store=True)
    product_type_sale = fields.Selection(string='Tipo de Venta', selection=
    [('1', 'Productos primarios'),
     ('2', 'Productos de oficina'),
     ('3', 'Descuentos y beneficios')])
    

    
    
