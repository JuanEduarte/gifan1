from odoo import api, fields, models


class GifProductSubtype(models.Model):
    _name = 'gif.product.subtype'
    _description = 'Subtipo del Producto'

    name = fields.Char(string='Nombre')
    gif_subtype_active = fields.Boolean(string='Activo')
    
