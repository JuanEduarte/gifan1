from odoo import api, fields, models


class GifCategory(models.Model):
    _name = 'gif.category'
    _description = 'Categoria del producto'

    name = fields.Char(string='Nombre')
    gif_category_active = fields.Boolean(string='Activo')
    
