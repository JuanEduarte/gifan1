from odoo import models,fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # gif_listprice = fields.Boolean(string='Con lista de Precios')
    gif_procter_1 = fields.Char(string='AGRUPACIÓN PROCTER 1')
    gif_procter_2 = fields.Char(string='AGRUPACIÓN PROCTER 2')
    
    
    
