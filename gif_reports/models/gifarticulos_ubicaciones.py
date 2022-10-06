from odoo import api, fields, models
from datetime import datetime


class ArticulosUbicaciones(models.Model):
	_name = 'gif.articulos.ubicaciones'
	_description = 'Creara una nueva vista de arbol donde se mostraran campos especifios de los productos poara ordenarlos de acuerdo a su ubicacion'
 
 
def _default_code_time(self):
			"""Función para calcular el código de tiempo."""
			code_time = datetime.now().strftime('%Y%m%d_%H%M%S')
			return code_time

def _default_active_company(self):
	"""Función que recupera el nombre de la compañia activa."""
	company_id = self.env.company.id
	return self.env['res.company'].search([('id','=', company_id)])

	name = fields.Char(string='Reporte de Artículos por Ubicaciones')
	company = fields.Many2one('res.company', string="Compañía", readonly=True, store=True, default = _default_active_company)
	date = fields.Date(string="Fecha", readonly=True, store=True, default = datetime.now())
 
 
 


