from odoo import models, fields


class CCTStockQuant(models.Model):
    _inherit = 'stock.quant'

    cct_expiration_date = fields.Datetime("Fecha de caducidad", related="lot_id.expiration_date" )#compute='compute_exp_date')


class CCTStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    cct_expiration_date = fields.Datetime("Fecha de caducidad", related="lot_id.expiration_date" )