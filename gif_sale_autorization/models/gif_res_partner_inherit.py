from odoo import models,fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gif_listprice = fields.Boolean(string='Con lista de Precios')
    
