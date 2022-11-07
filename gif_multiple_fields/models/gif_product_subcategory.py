from odoo import api, fields, models


class GifProductSubcategory(models.Model):
    _name = 'gif.product.subcategory'
    _description = 'Gifan Subcategoria del producto'

    name = fields.Char(string='Nombre')
    gif_subcategory_active = fields.Boolean(string='Activo',default=True)
    
    
