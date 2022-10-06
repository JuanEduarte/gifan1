from odoo import api, fields, models
import datetime as dt

class GifDetailsExpirationDateReport(models.Model):
    _name = 'gif.details.expiration.date.report'
    _inherit = 'gif.base.report'
    _description = 'Details Expiration Date reports'
    _order = 'id desc'

    title        = fields.Char(string="Titulo", default="Reporte de Detalle de Caducidades")
    products     = fields.One2many('gif.product.centralized','report_id_dexpd', string="Productos existentes", store=True)
                                    # compute='_compute_stock_products')


    # @api.depends('code_time')
    # def _compute_stock_products(self):
    #     """Función que filtra y asigna los productos a mostrar en el reporte."""
        
    #     for record in self:
                
    #         cnt = self.env['gif.product.centralized'].search_count([('code_time','like',record.code_time)])
    #         if cnt == 0:
    #             p_ids = self.create_product_centralized(record.code_time)
    #             record.products = [(6,0,p_ids)]
    #         else:
    #             ids = self.env['gif.product.centralized'].search([('code_time','like',record.code_time)]).ids
    #             record.products = [(6,0,ids)]

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
                        ("type", "in", ["consu", "product"]), ("qty_available", ">", 0)]):
            
            for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id: continue
                
                try:
                    rem_days = (quant.lot_id.expiration_date - dt.datetime.now()).days 
                except:
                    rem_days = False

                vals = {
                    'product'         : product_id.id,
                    'description_sale': product_id.description_sale,
                    'pricing'         : quant.product_tmpl_id.gif_brand_ids.gif_brand_name,
                    'barcode_upc'     : product_id.barcode,
                    'gif_expiration_date': quant.lot_id.expiration_date,
                    'gif_remaining_exp_days' : rem_days,
                    'gif_qty_oh'      : quant.available_quantity,
                    'code_time'       : code_time,
                }
                
                product_quant = self.env['gif.product.centralized'].create(vals)
                products_ids.append(product_quant.id)
        
        return products_ids


