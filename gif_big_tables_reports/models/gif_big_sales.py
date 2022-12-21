from odoo import api, fields, models

class GifBigSales(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        res = super(GifBigSales, self).action_confirm()
        print("Self sale:", self)
        self.create_big_sales()
        return res

    def create_big_sales(self):
        
        sale_vals = {
            'gif_customer_id': self.partner_id,
            'gif_customer': self.partner_id.name,
            'gif_name': self.name,
            'gif_state': self.state,
            'gif_date': None,
            'gif_init_date': self.date_order,
            'gif_currency_id': self.price_list.currency_id,
            'gif_subtotal_without_taxes': self.amount_untaxed_show,
            'gif_iva_tax':None,
            'gif_ieps_tax':None,
            'gif_total':None,
        }

        lines_vals = []
        for line in self.order_line:
            line_vals = {
            'gif_product_id': line.product_template_id.product_variant_id.id,
            'gif_product': line.product_temlate_id.product_variant_id.name,
            'gif_description': line.product_temlate_id.product_variant_id.description_sale,
            'gif_quantity': line.product_uom_quantity,
            'gif_uom_id':line.product_uom.id,
            'gif_balance_multiplicator':None,
            'gif_total_quantity':line.gif_total_units,
            'gif_unit_price':line.price_unit,
            'gif_price_per_piece': line.price_unit / line.gif_total_units,
            'gif_iva_per_unit':None,
            'gif_ieps_per_unit':None,
            'gif_subtotal':line.price_subtotal
            }

            lines_vals.append(line_vals)

        for line_vals in lines_vals:
            self.env['gif.big.sales'].create( sale_vals.update(line_vals) )



class GifBigTableSalesReceptions(models.Model):
    _name = 'gif.big.sales.receptions'
    _description = 'Table to save all Odoo sales receptions.'

     # Reception
    gif_sale_order_id = fields.Many2one('sale.order', string="Orden de venta")
    gif_product_id = fields.Many2one('product.product', string="Producto")
    
    gif_incoming_picking_id = fields.Many2one('stock.picking', string="Recepción")
    gif_inpick_date = fields.Datetime(string="Fecha de creación recep.")
    gif_inpick_init_date = fields.Datetime(string="Fecha de confirmación recep.")
    gif_expiration_date = fields.Date(string="Fecha de caducación")
    gif_lot_id = fields.Many2one('stock.production.lot', string="Lote")
    gif_qty_done = fields.Float(string="Recibidos")
    gif_qty_missing = fields.Float(string="Faltantes")


class GifBigTableSales(models.Model):
    _name = 'gif.big.sales'
    _description = 'Table to save all Odoo sales.'

    # Customer
    gif_customer_id = fields.Many2one('res.partner', string="Cliente")
    gif_customer = fields.Char(string="Nombre del Cliente")

    # Sale
    gif_name = fields.Char(string="Orden de compra")
    gif_state = fields.Char(string="Estado")
    gif_date = fields.Datetime(string="Fecha de creación")
    gif_init_date = fields.Datetime(string="Fecha de confirmación")
    gif_currency_id = fields.Many2one('res.currency', string="Moneda")
    gif_subtotal_without_taxes = fields.Float(string="Importe sin impuestos")
    gif_iva_tax = fields.Boolean(string="Impuesto IVA")
    gif_ieps_tax = fields.Boolean(string="Impuesto IEPS")
    gif_total = fields.Float(string="Total")
    
    # Lines
    gif_product_id = fields.Many2one('product.product', string="Producto")
    gif_product = fields.Char(string="Nombre del producto")
    gif_description = fields.Char(string="Descripción de venta")
    gif_quantity = fields.Float(string="Cantidad")
    gif_uom_id = fields.Many2one('uom.uom',string="Unidad de medida")
    gif_balance_multiplicator = fields.Float(string="Factor de multiplicación")
    gif_total_quantity = fields.Float(string="Unidades totales")
    gif_unit_price = fields.Float(string="Precio unitario")
    gif_price_per_piece = fields.Float(string="Precio por pieza")
    gif_iva_per_unit = fields.Float(string="IVA x Unidad")
    gif_ieps_per_unit = fields.Float(string="IEPS x Unidad")
    gif_subtotal = fields.Float(string="Importe sin impuestos")
