from odoo import api, fields, models


class GifPool(models.Model):
    _name = 'gif.sale.pool'
    _description = 'All lines of a confirmed invoices'

    gif_customer = fields.Many2one('res.partner', string="Cliente")
    gif_brand = fields.Many2one('gif.product.brand', string="Marca")
    gif_product = fields.Many2one('product.product', string="Producto")
    gif_total = fields.Float(string="Total")
    gif_date = fields.Date(string="Fecha")
    gif_month = fields.Char(string="Mes")
    gif_year = fields.Char(string="Año")

