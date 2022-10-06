from odoo import models, fields, api
import datetime as dt
import dateutil.parser as dp

class GifWarehouseReport(models.Model):
    _name = 'gif.warehouse.report'
    _inherit = 'gif.base.report'
    _description = 'Warehouse reports'
    _order = 'id desc'

    title    = fields.Char(string="Titulo", default="Reporte de Inventario por Almacén")
    products = fields.One2many('gif.product.centralized','report_id_wahs', string="Productos existentes", store=True)
                                #compute='compute_products')

    @api.depends('code_time')
    def compute_products(self):
        for record in self:
            
            if len(record.products) == 0:
                p_ids = self.create_product_centralized(record.code_time)
                record.products = [(6,0,p_ids)]
                # sorted(record.products, key=lambda x:  )

            else:
                remove_ids = self.env['gif.product.centralized'].search([('code_time','like',record.code_time)]).unlink()
                p_ids = self.create_product_centralized(record.code_time)
                record.products = [(6,0,p_ids)]


    def create_product_centralized(self, code_time):

        products_ids = []
        vals = {}

        for product_id in self.env['product.product'].search([("type", "in", ["consu", "product"])]):
            
            for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id: continue

                vals['gif_warehouse_existences'] = warehouse_id.name
                vals['gif_partner_purchase'] = None
                vals['product'] = product_id.id
                vals['description_sale']: product_id.description_sale
                vals['gif_brand'] = quant.product_tmpl_id.gif_brand_ids.gif_brand_name
                vals['gif_warehouse_existences'] = quant.available_quantity
                vals['gif_unit_cost'] = product_id.standard_price
                vals['gif_total_cost'] = vals['gif_unit_cost'] * vals['gif_warehouse_existences']
                vals['gif_cellar'] = None
                vals['code_time'] = code_time
                
               
                product_quant = self.env['gif.product.centralized'].create(vals)
                products_ids.append(product_quant.id)

        return products_ids



