from odoo import api, fields, models
import datetime as dt

class GifInvoinceExpirationReport(models.Model):
    _name = 'gif.invoice.expiration.report'
    _inherit = 'gif.base.report'
    _description = 'Invoince Expiration reports'
    _order = 'id desc'

    title        = fields.Char(string="Titulo", default="Reporte de Facturación Caducidades")
    products     = fields.One2many('gif.product.centralized','report_id_invc', string="Productos existentes", store=True)
                                    #compute='_compute_stock_products')

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
        vals = {}
        # Facturas de cliente publicadas.
        for invoice in self.env['account.move'].search([('move_type','like','out_invoice'),('state','like','post')]):
            vals['gif_invoice'] = invoice.name
            vals['gif_pps_no'] = invoice.invoice_origin # Orden de venta origen

            # Lotes
            lot_ids = []
            moves = self.env['stock.move'].search(
                [('picking_id.origin','like',invoice.invoice_origin),('picking_id.state','in',('assigned','done'))])
            
            for move in moves:
                for line in move.move_line_ids:
                    lot_ids.append(line.lot_id.name)


            vals['gif_pricing_group'] = None

            vals['gif_cust_no'] = None
            vals['gif_ship_name'] = None
            vals['gif_inv_date'] = invoice.invoice_date



            # print("Factura",invoice.name)
            for line in invoice.invoice_line_ids:
                vals['product'] = line.product_id.id
                vals['description_sale'] = line.product_id.description_sale
                vals['barcode_dun14'] = None
                vals['gif_inv_exp_date'] = None
                vals['gif_inv_qty'] = line.quantity
                vals['gif_total_lot_prod'] = None

                product_quant = self.env['gif.product.centralized'].create(vals)
                products_ids.append(product_quant.id)



        # for product_id in self.env['product.product'].search([
        #                 ("type", "in", ["consu", "product"]), ("qty_available", ">", 0)]):
            
        #     for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
        #         warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
        #         if not warehouse_id: continue
                
        #         try:
        #             rem_days = (quant.lot_id.expiration_date - dt.datetime.now()).days 
        #         except:
        #             rem_days = False

        #         vals = {
        #             'product'         : product_id.id,
        #             'description_sale': product_id.description_sale,
        #             'pricing'         : quant.product_tmpl_id.gif_brand_ids.gif_brand_name,
        #             'barcode_upc'     : product_id.barcode,
        #             'gif_expiration_date': quant.lot_id.expiration_date,
        #             'gif_remaining_exp_days' : rem_days,
        #             'gif_qty_oh'      : quant.available_quantity,
        #             'code_time'       : code_time,
        #         }
                
        #         product_quant = self.env['gif.product.centralized'].create(vals)
        #         products_ids.append(product_quant.id)
        
        return products_ids


