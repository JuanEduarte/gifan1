from odoo import api, fields, models


class GifPartnersDetails(models.Model):
    _name = 'gif.partners.details.purchase'
    _description = 'Partners Descriptions'

    partner_purchase = fields.Many2one(comodel_name='res.partner', string='Socio')
    partner_price_purchase = fields.Float(string='Precio')
    partner_uom_purchase = fields.Many2one(comodel_name='uom.uom', string='Unidad Medida')
    bar_code_purchase = fields.Char(string='Código de Barras del Proveedor')
    individual_code_purchase = fields.Char(string='Código Individual del Proveedor')
    product_tmp_id_purchase = fields.Many2one(comodel_name='product.template', string='Producto')
    currency_purchase  = fields.Many2one(comodel_name='res.currency', string='Moneda')
    