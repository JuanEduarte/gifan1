from odoo import models, fields


class GifSaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    gif_partner_code = fields.Char(string="Código cliente")
    gif_partner_shipping_code = fields.Char(string="Código dirección de entrega")
    gif_init_date = fields.Char(string="Fecha de inicio")
    gif_supplier_code = fields.Char(string="Número de proveedor")
    