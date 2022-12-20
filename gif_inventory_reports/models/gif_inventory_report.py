from odoo import api, fields, models
import datetime as dt
import dateutil.parser as dp

#gif_inventory_reports.access_gif_inventory_report,access_gif_inventory_report,gif_inventory_reports.model_gif_inventory_report,,1,1,1,1

class GifInventoryReport(models.Model):
    _name = 'gif.inventory.report'
    _inherit = 'gif.base.report'
    _description = 'Inventory reports'
    _order = 'id desc'

    title        = fields.Char(string="Título", default="Existencia por Artículo")
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

            if not product_id.name == '80319735':
                continue

            incoming_moves = self.env['stock.move.line'].search([
                ('product_id', '=', product_id.id),
                ('state', '=', 'done'),
                ('picking_code', '=', 'incoming')])
            
            # print("in",incoming_moves)

            outgoing_moves = self.env['stock.move.line'].search([
                ('product_id', '=', product_id.id),
                ('state', '=', 'done'),
                ('picking_code', '=', 'outgoing')])

            # print("out",outgoing_moves)

            incoming_qtys = {}
            for move in incoming_moves:
                origin = self.env['purchase.order'].search([('name','=',move.origin)])
                provider = origin.partner_id
                incoming_qtys[provider.id] = incoming_qtys.get(provider.id,0) + move.qty_done

            # outgoing_qtys = {}
            # for move in outgoing_moves:
            #     origin = self.env['sale.order'].search([('name','=',move.origin)])
            #     client = origin.partner_id
            #     outgoing_qtys[client.id] = outgoing_qtys.get(client.id,0) + move.qty_done

            

            
            print("Product:", product_id.name)
            print("Recepciones:",incoming_qtys)
            # print("Entregas:", outgoing_qtys)

            moves_line = self.env['stock.move.line'].search([('product_id','=',product_id.id)])

            # Ultimo movimiento
            try:
                last_date = max([(ml.date, ml.id) for ml in moves_line])
            except:
                last_date = None
            
            break
            for quant in self.env['stock.quant'].search([('product_id','=',product_id.id)]):
                # Almacén
                warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
                if not warehouse_id:
                    print("Not ws:", quant.location_id.name )
                    continue

                for detail in quant.product_tmpl_id.partners_details_purchase:
                    seller = detail.partner_purchase.id




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
                    'pricing'           : quant.product_tmpl_id.gif_brand_ids.name,
                    'last_move'         : dp.parse(str(last_date[0])).date()
                }
                
                vals['ext_avg_cost'] = vals['available_qty'] * vals['avg_cost']

                for detail in quant.product_tmpl_id.partners_details_purchase:
                    
                    vals['seller'] = detail.partner_purchase.id
                    product_quant = self.env['gif.product.centralized'].create(vals)
                    products_ids.append(product_quant.id)
        
        return products_ids


