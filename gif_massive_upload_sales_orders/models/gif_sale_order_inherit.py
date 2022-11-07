from odoo import models, fields, api

class GifSaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    gif_partner_code = fields.Char(string="Código cliente")
    gif_partner_shipping_code = fields.Char(string="Código dirección de entrega")
    gif_init_date = fields.Date(string="Fecha de inicio")
    gif_supplier_code = fields.Char(string="Número de proveedor")

# class GifSaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'

#     price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True, inverse='_compute_amount')

#     # def _set_price(self):
#     #     self.write({'price_unit': self.price_subtotal/self.product_uom_qty })


class GifResPartner(models.Model):
    _inherit = 'res.partner'

    def default_warehouse(self):
        return self.env['stock.warehouse'].search([])[0].id
        
    gif_default_warehouse = fields.Many2one('stock.warehouse', string="Almcén por defecto", default=default_warehouse)


class GifSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('partner_id.ref','partner_id.gif_default_warehouse ')
    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.gif_partner_code = self.partner_id.ref if self.partner_id.ref else False
        self.warehouse_id = self.partner_id.gif_default_warehouse if self.partner_id.gif_default_warehouse else False