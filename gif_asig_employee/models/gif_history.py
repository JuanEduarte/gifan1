from odoo import api, fields, models


class GifHistory(models.Model):
    _name = 'gif.history'
    _description = 'Historico de Empleados'

    name = fields.Char(string='Referencia')
    gif_date_planned_start = fields.Date(string='Fecha Programada')
    gif_product_id = fields.Many2one('product.product', 'Producto')
    gif_duration_expected = fields.Float (string="Duración Esperada")
    gif_duration = fields.Float(string="Duración Real")
    gif_state= fields.Selection(string='Estado', default='draft',selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ])
    gif_total_before =fields.Integer(string="Total Antes")
    gif_linea_before =fields.Integer(string="Linea Antes")
    gif_linea_after =fields.Integer(string="Linea Despues")
    gif_dps_before =fields.Integer(string="Disponibles Antes")
    gif_dps_after = fields.Integer(string="Disponibles Despues") 
    gif_traslate_emp = fields.Integer(string="Trasladar Empleados")
    gif_traslate_des = fields.Char(string="Destino De Traslado") 

