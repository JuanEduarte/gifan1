from odoo import api, fields, models


class GifBusinessLine(models.Model):
    _name = 'gif.business.line'
    _description = 'GIFAN Línea de negocio'

    name = fields.Char(string='Nombre')
    gif_active_line = fields.Boolean(string='Activo',default=True)
    
