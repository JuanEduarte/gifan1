from odoo import api, fields, models


class GifBigTable(models.Model):
    _name = 'gif.big.sales'
    _description = 'Table to save all Odoo sales.'

    # Customer
    gif_customer_id = fields.Many2one('res.partner', string="Cliente")

    # Sale
    gif_name = fields.Char(string="Orden de compra")
    gif_date = fields.Datetime(string="Fecha de creación")
    gif_init_date = fields.Datetime(string="Fecha de confirmación")
    gif_currency_id = fields.Many2one('res.currency', string="Moneda")
    gif_subtotal_without_taxes = fields.Float(string="Importe sin impuestos")
    gif_iva_tax = fields.Boolean(string="Impuesto IVA")
    gif_iva_percent = fields.Float(string="Porcentaje IVA")
    gif_iva_amount = fields.Float(string="Valor IVA")
    gif_ieps_tax = fields.Boolean(string="Impuesto IEPS")
    gif_ieps_percent = fields.Float(string="Porcentaje IEPS")
    gif_ieps_amount = fields.Float(string="Valor IEPS")
    gif_total = fields.Float(string="Total")
    
    # Lines
    gif_product_id = fields.Many2one('product.product', string="Producto")
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
    
    # Reception
    gif_incoming_picking_id = fields.Many2one('stock.picking', string="Recepción")
    gif_inpick_date = fields.Datetime(string="Fecha de creación recep.")
    gif_inpick_init_date = fields.Datetime(string="Fecha de confirmación recep.")
    gif_expiration_date = fields.Date(string="Fecha de caducación")
    gif_lot_id = fields.Many2one('stock.production.lot', string="Lote")
    gif_qty_done = fields.Float(string="Recibidos")
    gif_qty_missing = fields.Float(string="Faltantes")
