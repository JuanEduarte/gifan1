# from dataclasses import fields
from odoo import models,fields
class GifPackagingType(models.Model):
    _inherit="product.packaging"
    gif_packbed= fields.Char(string = "N° Empaques por Cama")
    gif_numbt=fields.Char(string='N° Camas por Tarima')
    gif_packagesxt=fields.Char(string='N° Empaques por Tarima')