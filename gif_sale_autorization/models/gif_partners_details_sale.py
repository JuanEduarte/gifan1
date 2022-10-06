from odoo import api, fields, models


class GifPartnersDetails(models.Model):
    _name = 'gif.partners.details'
    _description = 'Partners Descriptions'

    partner = fields.Many2one(comodel_name='res.partner', string='Socio')
    partner_price = fields.Float(string='Precio')
    partner_uom = fields.Many2one(comodel_name='uom.uom', string='Unidad Medida')
    bar_code = fields.Char(string='Código de Barras del Cliente')
    individual_code = fields.Char(string='Código Individual del Cliente')
    product_tmp_id = fields.Many2one(comodel_name='product.template', string='Producto')
    # currency_sale = fields.Selection(string='Moneda', selection=[('MXN', 'MXN'), ('USD', 'USD'),])
    currency_sale = fields.Many2one(comodel_name='res.currency', string='Moneda')
    