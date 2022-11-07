from odoo import models, fields 

class GifProductBrand(models.Model):
    _name = 'gif.product.brand'
    _description = 'Marcas de productos'

    '''
        Se crea el modelo y los campos para las marcas.
    '''

    name = fields.Char(string='Nombre de marca', required=True)
    gif_brand_active = fields.Boolean(string='Activo', default=True)
    # product_id = fields.One2many('product.template', 'gif_brand_ids')