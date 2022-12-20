from odoo import models, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    gif_firm_flag = fields.Boolean(
        string='Control de PAC', 
        default=False,
        help="Campo utilizado para evitar el timbrado de la factura.")
