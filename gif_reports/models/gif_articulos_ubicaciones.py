from odoo import api, fields, models
from datetime import datetime

class GifArticulosUbicaciones(models.Model):
		_name = 'gif.articulos.ubicaciones'
	 #_inherit = 'gif.base.report'
		_description = 'Reporte de articulos por ubicaiones'


		title = fields.Char(string="Titulo", default="Articulos por ubicaiones")


		@api.depends('code_time')
		def _compute_stock_products(self):
				"""Función que filtra y asigna los productos a mostrar en el reporte."""

				for record in self:
						cnt = self.env['gif.product.quant'].search_count([('code_time','like',record.code_time)])
						if cnt == 0:
								self.create_product_quant(record.code_time)
						ids = self.env['gif.product.quant'].search([('code_time','like',record.code_time)]).ids
						record.products = [(6,0,ids)]



		def create_product_quant(self, code_time):
					"""Función que crea los registros de cada producto."""

					for product in self.env['product.product'].search([("type", "in", ["consu", "product"]), ("qty_available", ">", 0)]):

						quants = self.env['stock.quant'].search([('product_id','=',product.id)])

						for record in quants:
								warehouse_id_q = int(self.env['stock.location'].browse(record.location_id.id).warehouse_id.id)
								if not warehouse_id_q: continue

								vals = {
											'expiration_date' : record.product_id.use_expiration_date,
											'barcode_upc'     : record.product_id.barcode,
											'barcode_dun14'   : record.lot_id.name,
											'description_sale': record.product_id.description_sale,
											'avg_cost'        : record.product_id.standard_price,
											'product_id'      : product.id,
											'warehouse_id'    : warehouse_id_q,
											'code_time'       : code_time,
											'seller_id'       : 0,
											'ubication'       : record.location_id,
									}

								for detail in record.product_tmpl_id.partners_details_purchase:

										vals['seller_id'] = detail.partner_purchase.id
										product_quant = self.env['gif.product.quant'].create(vals)