from odoo import api, fields, models

class GifProductCategory(models.Model):
    _name = 'gif.product.category'
    _description = 'Categoria del producto de Gifan'

    name = fields.Char(string='Nombre')
    gif_category_active = fields.Boolean(string='Activo',default=True)
    
