from odoo import api, fields, models


class GifProductCentralized(models.Model):
    _name = 'gif.product.centralized'
    _description = 'Product fields centralized.'
    _order = 'id desc'

    
    # Comun
    warehouse        =  fields.Many2one('stock.warehouse', string="Almacén")
    product          =  fields.Many2one('product.product', string="Producto")
    description_sale =  fields.Text(string="Descripción", readonly=True)

    # Reporte de inventario    
    expiration_date  =  fields.Boolean(string = "Caducidad", readonly=True)#, compute='_retrive')
    barcode_upc      =  fields.Char(string="UPC", readonly=True)
    barcode_dun14    =  fields.Char(string="DUN14", readonly=True)         # Lote
    avg_cost         =  fields.Float(string="Costo promedio", readonly=True)

    seller           =  fields.Many2one('res.partner', string="Proveedor")

    code_time        =  fields.Char(string="code_time", store=True)
    report_id_exs    =  fields.Many2one('gif.existences.report', string="Reporte",ondelete='cascade')
    report_id_inv    =  fields.Many2one('gif.inventory.report', string="Reporte",ondelete='cascade')
    report_id_loc    =  fields.Many2one('gif.locations.report', string="Reporte",ondelete='cascade')
    report_id_expd   =  fields.Many2one('gif.expiration.date.report', string="Reporte",ondelete='cascade')
    report_id_dexpd  =  fields.Many2one('gif.details.expiration.date.report', string="Reporte",ondelete='cascade')
    report_id_invc   =  fields.Many2one('gif.invoice.expiration.report', string="Reporte",ondelete='cascade')
    report_id_wahs   =  fields.Many2one('gif.warehouse.report', string="Reporte",ondelete='cascade')
    report_id_brd    =  fields.Many2one('gif.brand.report', string="Reporte",ondelete='cascade')

    subtype_product  =  fields.Char(string="Subtipo", readonly=True)
    reserved_qty     =  fields.Float(string="Reservado", readonly=True)
    available_qty    =  fields.Float(string="Disponible", readonly=True)
    to_receive       =  fields.Float(string="En recibo", readonly=True)
    ext_avg_cost     =  fields.Float(string="Costo promedio extendido", readonly=True)
    pricing          =  fields.Char(string="Marca", readonly=True)
    last_move        =  fields.Char(string="Último movimiento", readonly=True)

    # Reporte de existencias
    gif_pallets          =  fields.Integer(string="Cajas", readonly=True)

    # Reporte de ubicaciones
    gif_location = fields.Char(string="Ubicación", readonly=True)
    gif_expiration_date = fields.Date(string="Caducidad", readonly=True) #Por lote
    gif_total_ex = fields.Char(string="Total", readonly=True)
    gif_id = fields.Integer(store=True)

    # Reporte por caducidad
    gif_description_product = fields.Char(string="Descripción")
    gif_located = fields.Char(string="Ubicación")
    gif_expiration_130 = fields.Float(string="Disponible +130") # Fecha de caducidad > 130 dias
    gif_prc = fields.Float(string="Riesgo (PRC)") # Fecha de caducidad ...
    gif_pcc = fields.Float(string="Caducidad comercial (PCC)") # Fecha de caducidad ...
    gif_ppd = fields.Float(string="Donación (PPD)") # Fecha de caducidad ...
    gif_pc = fields.Float(string="Caducidad (PC)") # Fecha de caducidad ...

    # Reporte detalles de caducidad
    gif_remaining_exp_days = fields.Integer(string="Días de caducidad")
    # gif_remaining_exp_days = fields.Integer(string="Días de caducidad") # Pendiente: Parecido pero diferente
    gif_qty_oh = fields.Float(string="QTY_OH")


    # Reporte facturación caducidades
    gif_invoice = fields.Char(string="Documento")
    gif_pps_no = fields.Char(string="PPS NO")
    gif_cust_no = fields.Char(string="Cust NO.")
    gif_ship_name = fields.Char(string="Ship name")
    gif_cust_po = fields.Char(string="Cust PO")
    gif_inv_date = fields.Date(string="Fecha")
    gif_pricing_group = fields.Char(string="Pricing-Group")
    gif_inv_exp_date = fields.Date(string="Caducidad")
    gif_inv_qty = fields.Float(string="Cant. entregada")
    gif_total_lot_prod = fields.Float(string="Total")

    # Reporte por almacén
    gif_partner_purchase = fields.Char(string="Proveedor")
    gif_warehouse_existences = fields.Float(string="Existencias")
    gif_unit_cost = fields.Float(string="Costo Unitario")
    gif_total_cost = fields.Float(string="Costo Total")
    gif_cellar = fields.Float(string="Bodegas")
    gif_brand =  fields.Char(string="Marca", readonly=True)

    # Inventario por marca


