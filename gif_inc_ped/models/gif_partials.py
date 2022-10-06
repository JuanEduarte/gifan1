from odoo import api, fields, models


class GIFPartials(models.Model):
    _name = 'gif.partials'
    _description = 'Partidas'

    name = fields.Char(string='Name')
    gif_part_no = fields.Integer(string='Partida No.')
    gif_no_igi = fields.Float(string='Importe sin IGI')
    gif_imp_igi = fields.Float(string='Importe IGI')

    gif_rel_pedi = fields.Many2one(comodel_name='gif.pediments')
    
    
    
    
