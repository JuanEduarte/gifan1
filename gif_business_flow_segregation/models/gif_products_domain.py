from odoo import api, fields, models


class ProductsDomain(models.Model):
    _name = 'gif.products.domain'
    _description = 'Dominio de los productos'

    name = fields.Char(string='Nombre')
