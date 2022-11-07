from odoo import api, fields, models


class GifSetPartials(models.Model):
    _name = 'gif.set.partials'
    _description = 'Modelo para definir las partidas'

    name = fields.Char(string='Nombre')
    gif_part_prod = fields.Many2one(comodel_name='product.template', string='IGI',domain=[('gif_is_igi','=',True)])
    gif_part_porc = fields.Integer(string='Porcentaje')
    gif_rel_part_part = fields.Many2one(comodel_name='gif.pediments')
    gif_part_num_set = fields.Integer(string='No. Partida')
    
    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gif_is_igi = fields.Boolean(string='Es IGI')
    split_method_landed_cost = fields.Selection(selection_add=[('igi','IGI'),('equal',)],ondelete={'igi': 'set default'},default='equal')
    gif_porc_igi = fields.Integer(string='Porcentaje IGI')
    
    

    
