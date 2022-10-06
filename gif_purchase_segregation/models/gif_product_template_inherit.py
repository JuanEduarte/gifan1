from odoo import api,fields,models


class ProductTemplatePS(models.Model):
    _inherit = 'product.template'

    product_type_purchase = fields.Selection(string='Tipo de Compra', selection=
    [('1', 'Productos primarios'),
    ('2', 'Productos insumos'),
    ('3', 'Productos de oficina'), 
    ('4', 'Gastos asociados'),
    ('5', 'Descuentos y beneficios')])
    

    
    
