from odoo import api,fields,models

class TipificacionesVentas(models.Model):
    _name = 'gif.tipificaciones.ventas'
    _description = 'Modelo de segregación y tipificación ingresos'

    name = fields.Char(string='Nombre')
