from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gif_def_loc_in = fields.Many2one(comodel_name='stock.location', string='Ubicación por defecto Recepción')
    gif_def_loc_out= fields.Many2one(comodel_name='stock.location', string='Ubicación por defecto Entrega')
    
