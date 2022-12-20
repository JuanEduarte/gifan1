from odoo import api, fields, models


class GifPartnersDetails(models.Model):
    _name = 'gif.partners.details'
    _description = 'Partners Descriptions'

    '''
        Se crea el modelo de la tabla de clientes (ventas) en productos.
    '''

    partner = fields.Many2one(comodel_name='res.partner', string='Socio')
    partner_price = fields.Float(string='Precio',digits=(12,4))
    partner_uom = fields.Many2one(comodel_name='uom.uom', string='Unidad Medida')
    bar_code = fields.Char(string='Código de Barras del Cliente')
    individual_code = fields.Char(string='Código Individual del Cliente')
    product_tmp_id = fields.Many2one(comodel_name='product.template', string='Producto')
    currency_sale = fields.Many2one(comodel_name='res.currency', string='Moneda')
    gif_partner_code_sale = fields.Char(string='Código de Cliente')

    @api.onchange('gif_partner_code_sale')
    def _onchange_gif_partner_code_sale(self):
        for record in self:
            if record.gif_partner_code_sale != False:
                cliente = self.env['res.partner'].search([('ref','ilike',record.gif_partner_code_sale)])
                if cliente.id != False:
                    record.partner = cliente.id
                else:
                    continue
    
    
    