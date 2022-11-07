from odoo import api, fields, models


class GifProductType(models.Model):
    _name = 'gif.product.type'
    _description = 'Gifan Tipo de Producto'

    name = fields.Char(string='Nombre')
    gif_type_active = fields.Boolean(string='Activo', default = True)
    
