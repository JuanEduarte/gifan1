from odoo import api, fields, models


class TipificacionesComprasPS(models.Model):
    _name = 'gif.tipificaciones.compras'
    _description = 'Modelo de segregación y tipificación egreso'

    name = fields.Char(string='Nombre')

