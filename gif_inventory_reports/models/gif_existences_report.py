from odoo import models, fields, api


class GifExistencesReport(models.Model):
    _name = 'gif.existences.report'
    _inherit = 'gif.base.report'
    _description = 'Existence reports'
    # _order = 'id desc'

    title    = fields.Char(string="Titulo", default="Consulta de existencias por producto")
    product  = fields.Many2one('product.product', string="Producto a consultar:",
                    domain=[("type", "in", ["consu", "product"])])

    #product_existence = fields.One2many('gif.product.existence','report_id',string="Productos")

    existences = fields.One2many('gif.product.centralized','report_id_exs')
                                    #compute='_compute_existences')

    @api.onchange('product')
    @api.depends('code_time')
    def _compute_existences(self):
        for record in self:

            cnt = self.env['gif.product.centralized'].search_count([('code_time','like',record.code_time)])
            if cnt == 0:
                p_ids = self.create_product_centralized(record.code_time, record.product)
                record.existences = [(6,0,p_ids)]
            else:
                ids = self.env['gif.product.centralized'].search([('code_time','like',record.code_time)]).ids
                record.existences = [(4,ids)]

                p_ids = self.create_product_centralized(record.code_time, record.product)
                record.existences = [(6,0,p_ids)]

                # record.existences = [(6,0,ids)]
    

    
    def create_product_centralized(self, code_time, product_id):

        products_ids = []
        reserved_qty = self.get_reserved_qty(product_id)

        for quant in self.env['stock.quant'].search([('product_id.id','=',product_id.id)]):
            warehouse_id = self.env['stock.location'].browse(quant.location_id.id).warehouse_id
            if not warehouse_id: continue
            
            vals = {
                'warehouse'       : warehouse_id.id,
                'product'         : product_id.id,
                'description_sale': product_id.description_sale,
                #'reserved_qty'    : abs(quant.inventory_diff_quantity),
                'available_qty'   : quant.quantity,
                # 'gif_pallets'     : 0,  
                'avg_cost'        : product_id.standard_price,
                'code_time'       : code_time,
            }

            vals['ext_avg_cost'] = vals['available_qty'] * vals['avg_cost']
            vals['reserved_qty'] = reserved_qty.get(quant.lot_id.name,0)

            # if quant.product_tmpl_id.packaging_ids:
            #     for pack in quant.product_tmpl_id.packaging_ids:
            #         vals['gif_pallets'] = quant.quantity // pack.qty ################# (?)

            #         product_quant = self.env['gif.product.centralized'].create(vals)
            #         products_ids.append(product_quant.id)
            # else:
            product_quant = self.env['gif.product.centralized'].create(vals)
            products_ids.append(product_quant.id)
        
        return products_ids




