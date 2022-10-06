from odoo import fields, models

class GifProductBrand(models.Model):
    _name = 'gif.product.brand'
    _description = 'Marcas de productos'
    _rec_name = 'gif_brand_name'

    gif_brand_name = fields.Char(string='Nombre de marca', required=True)
    gif_brand_active = fields.Boolean(string='Activo', default=True)
    product_id = fields.One2many('product.template', 'gif_brand_ids')