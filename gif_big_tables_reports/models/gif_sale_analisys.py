from odoo import models, fields


class GifSaleAnalisys(models.Model):
    _name = 'gif.sale.analisys'

    #report_id = fields.Many2one('gif.report', store=True)

    gif_customer_id = fields.Many2one('res.partner', string="Cliente", readonly=True)
    
    gif_product_id = fields.Many2one('product.product', string="Producto", readonly=True)
    gif_supplier = fields.Char(string="Proveedor", readonly=True)
    gif_brand = fields.Char(string="Marca", readonly=True)
    gif_goal = fields.Float(string="Meta", readonly=True)
    gif_smpy = fields.Float(string="SMPY", readonly=True)
    gif_smpy_meta = fields.Float(string="SMPY/META", readonly=True)
    gif_total_fact = fields.Float(string="TOTAL FACT", readonly=True)
    gif_total_canc = fields.Float(string="TOTAL CANC", readonly=True)
    gif_total_dev = fields.Float(string="TOTAL DEV", readonly=True)
    gif_total_desc = fields.Float(string="TOTAL DESC", readonly=True)
    gif_shtd = fields.Float(string="SHTD", readonly=True)
    gif_openord = fields.Float(string="OPENORD", readonly=True)
    gif_pps = fields.Float(string="PPS", readonly=True)
    gif_shtd_openord = fields.Float(string="SHTD + OPENORD", readonly=True)
    gif_pmonth = fields.Float(string="PMONTH", readonly=True)
    gif_p3month = fields.Float(string="P3MONTH", readonly=True)
    gif_p6month = fields.Float(string="P6MONTH", readonly=True)
    gif_p12month = fields.Float(string="P12MONTH", readonly=True)




