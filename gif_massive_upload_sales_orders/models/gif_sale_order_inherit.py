from odoo import models, fields, api

class GifSaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    gif_partner_code = fields.Char(string="Código cliente")
    gif_partner_shipping_code = fields.Char(string="Código dirección de entrega")
    gif_init_date = fields.Date(string="Fecha de inicio")
    gif_supplier_code = fields.Char(string="Número de proveedor")


    @api.depends('partner_id.ref','partner_id.gif_default_sale_warehouse ')
    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.gif_partner_code = self.partner_id.ref if self.partner_id.ref else False
        self.warehouse_id = self.partner_id.gif_default_sale_warehouse if True else False

    @api.onchange('partner_shipping_id')
    def _onchange_partner_shipping(self):
        self.gif_partner_shipping_code = self.partner_shipping_id.ref if self.partner_shipping_id.ref else False


class GifResPartner(models.Model):
    _inherit = 'res.partner'

    def default_warehouse(self):
        return self.env['stock.warehouse'].search([])[0].id
        
    def default_picking(self):
        return self.env['stock.picking.type'].search([])[0].id

    gif_default_sale_warehouse = fields.Many2one('stock.warehouse', string="Almcén de venta", default=default_warehouse)
    gif_default_purchase_warehouse = fields.Many2one('stock.picking.type', string="Almcén de compra", default=default_picking)


class GifPurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    @api.depends('partner_id.gif_default_purchase_warehouse')
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id.gif_default_purchase_warehouse:
            self.picking_type_id = self.partner_id.gif_default_purchase_warehouse