from odoo import api, fields, models


class GifPartnersDetails(models.Model):
    _name = 'gif.partners.details.purchase'
    _description = 'Partners Descriptions'

    '''
        Se crea el modelo de la tabla de proveedores (compras) en productos.
    '''

    partner_purchase = fields.Many2one(comodel_name='res.partner', string='Socio')
    partner_price_purchase = fields.Float(string='Precio',digits=(12,4))
    partner_uom_purchase = fields.Many2one(comodel_name='uom.uom', string='Unidad Medida')
    bar_code_purchase = fields.Char(string='Código de Barras del Proveedor')
    individual_code_purchase = fields.Char(string='Código Individual del Proveedor')
    product_tmp_id_purchase = fields.Many2one(comodel_name='product.template', string='Producto')
    currency_purchase  = fields.Many2one(comodel_name='res.currency', string='Moneda')
    gif_partner_code_purchase = fields.Char(string='Código de Cliente')

    @api.onchange('gif_partner_code_purchase')
    def _onchange_gif_partner_code_purchase(self):
        for record in self:
            if record.gif_partner_code_purchase != False:
                cliente = self.env['res.partner'].search([('ref','ilike',record.gif_partner_code_purchase)])
                if cliente.id != False:
                    record.partner_purchase = cliente.id
                else:
                    continue
    