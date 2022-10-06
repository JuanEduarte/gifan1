from odoo import api, fields, models

class GifExpirationDateReport(models.Model):
    _name = 'gif.expiration.date.report'
    _inherit = 'gif.base.report'
    _description = 'Expiration Date reports'
    _order = 'id desc'

    title        = fields.Char(string="Titulo", default="Reporte Caducidades por Artículo Global")
    products     = fields.One2many('gif.product.centralized','report_id_expd', string="Productos existentes", store=True)
                                    # compute='compute_products')


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

        for product in self.env['product.product'].search([
                        ("type", "in", ["consu", "product"])]):
            
            for quant in self.env['stock.quant'].search([('product_id','=',product.id)]):
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id: continue

                vals = {
                    'warehouse'       : warehouse_id.id,
                    'product'         : product.id,
                    'description_sale': quant.product_id.description_sale,
                    'pricing'         : quant.product_tmpl_id.gif_brand_ids.gif_brand_name,
                    'barcode_upc'     : quant.product_id.barcode,
                    'barcode_dun14'   : quant.lot_id.name,
                    'gif_description_product' : product.name,
                    'reserved_qty'    : quant.reserved_quantity,
                    'available_qty'   : quant.product_id.qty_available,
                    'gif_located'     : 0,
                    'gif_expiration_130' : 0,
                    'gif_prc'         : 0,
                    'gif_pcc'         : 0,
                    'gif_ppd'         : 0,
                    'gif_pc'          : 0,
                    'code_time'       : code_time,
                }
                
                product_quant = self.env['gif.product.centralized'].create(vals)
                products_ids.append(product_quant.id)
        
        return products_ids


