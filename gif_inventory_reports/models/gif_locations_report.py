from odoo import models, fields, api
import datetime as dt
import dateutil.parser as dp

class GifLocationsReport(models.Model):
    _name = 'gif.locations.report'
    _inherit = 'gif.base.report'
    _description = 'Location reports'
    _order = 'id desc'

    title    = fields.Char(string="Titulo", default="Reporte de artículos por ubicaciones")
    products = fields.One2many('gif.product.centralized','report_id_loc', string="Productos existentes", store=True)
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
        ids = 0

        for product_id in self.env['product.product'].search([
                        ("type", "in", ["consu", "product"]), ("qty_available", ">", 0)]):

            # Ultimo movimiento
            moves_line = self.env['stock.move.line'].search([('product_id','=',product_id.id)])
            last_date = max([(ml.date, ml.id) for ml in moves_line])
            # move_line = self.env['stock.move.line'].browse(last_date[1])

            total_lot_qty = 0
            
            for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id: continue

                vals = {
                    'warehouse'       : warehouse_id.id,
                    'product'         : product_id.id,
                    'description_sale': product_id.description_sale,
                    'gif_location'    : quant.location_id.barcode,
                    'gif_expiration_date' : quant.lot_id.expiration_date,
                    'barcode_dun14'   : quant.lot_id.name,
                    'reserved_qty'    : quant.reserved_quantity,
                    'available_qty'   : quant.available_quantity,
                    'last_move'       : dp.parse(str(last_date[0])).date(),
                    'code_time'       : code_time,
                    'gif_id'          : ids,
                }
                
                total_lot_qty += vals['available_qty']

                product_quant = self.env['gif.product.centralized'].create(vals)
                products_ids.append(product_quant.id)
                ids += 1
            
            total_quant = self.env['gif.product.centralized'].create(
                {'available_qty':total_lot_qty,
                'code_time':code_time,
                'gif_id':ids,
                'reserved_qty':None,
                'gif_total_ex':"Total",
                })
            products_ids.append(total_quant.id)
            ids += 1

        return products_ids



