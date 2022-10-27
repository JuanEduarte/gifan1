from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    gif_total_units = fields.Char(string='Unidades reales', compute='total_units')
    
    def total_units(self):
        for record in self:
          record.gif_total_units = record.product_uom.ratio  * record.product_uom_qty
          
          
          
class AccountOrder(models.Model):
    _inherit = 'account.move.line'
    
    gif_total_units = fields.Char(string='Unidades reales', compute='total_units')
    
    def total_units(self):
        for record in self:
          record.gif_total_units = record.product_uom_id.ratio * record.quantity
          
          
          
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    gif_total_units = fields.Char(string='Unidades reales', compute='total_units')
    
    def total_units(self):
        for record in self:
          record.gif_total_units = record.product_uom.ratio * record.product_qty
                


class real_qty_delivery(models.Model):
    _inherit = 'account.move.line'
    
    
    @api.onchange("qty_done")
    def _onchange_field(self):
        for record in self:
            pass

