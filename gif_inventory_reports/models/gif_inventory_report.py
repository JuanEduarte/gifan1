from odoo import api, fields, models
import datetime as dt
import dateutil.parser as dp

#gif_inventory_reports.access_gif_inventory_report,access_gif_inventory_report,gif_inventory_reports.model_gif_inventory_report,,1,1,1,1

class GifInventoryReport(models.Model):
    _name = 'gif.inventory.report'
    _inherit = 'gif.base.report'
    _description = 'Inventory reports'
    _order = 'id desc'

    title        = fields.Char(string="Titulo", default="Reporte de inventario")
    products     = fields.One2many('gif.product.centralized','report_id_inv', string="Productos existentes",store=True)
    
    @api.depends('code_time')
    def compute_products(self):
        for record in self:
            
            if len(record.products) == 0:
                p_ids = self.create_product_centralized(record.code_time)
                record.products = [(6,0,p_ids)]

            else:
                remove_ids = self.env['gif.product.centralized'].search([('code_time','like',record.code_time)]).unlink()
                p_ids = self.create_product_centralized(record.code_time)
                record.products = [(6,0,p_ids)]



    def create_product_centralized(self, code_time):
        """Función que crea los registros de cada producto."""
        products_ids = []
        
        for product_id in self.env['product.product'].search([
                        ("type", "in", ["consu", "product"])]):
            # Reservado
            reserved_qty = self.get_reserved_qty(product_id)

            try:
                # Ultimo movimiento
                moves_line = self.env['stock.move.line'].search([('product_id','=',product_id.id)])
                last_date = max([(ml.date, ml.id) for ml in moves_line])
            except:
                last_date = None
            
            for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id: continue


                vals = {
                    'expiration_date' : product_id.use_expiration_date,
                    'barcode_upc'     : product_id.barcode,
                    'barcode_dun14'   : quant.lot_id.name,
                    'description_sale': product_id.description_sale,
                    'avg_cost'        : product_id.standard_price,
                    'product'         : product_id.id,
                    'warehouse'       : warehouse_id.id,
                    'code_time'       : code_time,
                    'subtype_product' : quant.product_tmpl_id.gif_subtypeprod,
                    'reserved_qty'    : quant.reserved_quantity,
                    'available_qty'     : quant.available_quantity,
                    'to_receive'        : 0,
                    'pricing'           : quant.product_tmpl_id.gif_brand_ids.gif_brand_name,
                    'last_move'         : dp.parse(str(last_date[0])).date()
                }
                
                vals['ext_avg_cost'] = vals['available_qty'] * vals['avg_cost']

                for detail in quant.product_tmpl_id.partners_details_purchase:
                    
                    vals['seller'] = detail.partner_purchase.id
                    product_quant = self.env['gif.product.centralized'].create(vals)
                    products_ids.append(product_quant.id)
        
        return products_ids


