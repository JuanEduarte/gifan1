from odoo import models, fields


class GifResPartner(models.Model):
    _inherit = 'res.partner'

    gif_provider_id = fields.Char(string="No. Proveedor", help="Número de proveedor con el cual el cliente tiene registrado a GIFAN.")
