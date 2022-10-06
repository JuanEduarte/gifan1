from odoo import api, fields, models,_


class GifInventory(models.Model):
    _name = 'gif.inventory'
    _description = 'Campos que lleva el inventario Ciclico'

    gif_rel = fields.Many2one(comodel_name='gif.cyc.inventory')   
    # state = fields.Selection(string='Status', selection=[('draft', 'Borrador'), ('first_c','Primer Conteo'),('second_c','Segundo Conteo'),('third_c','Tercer Conteo'),('done', 'Confirmado'),('canceled','Cancelado')],readonly=True,copy=False,index=True,tracking=3,default='draft')
    state = fields.Selection(string='Status', selection=[('draft', 'Borrador'),('done', 'Confirmado'),('canceled','Cancelado')],readonly=True,copy=False,index=True,tracking=3,default='draft')
    gif_location = fields.Many2one(comodel_name='stock.location', string='Ubicación',compute="_onchange_code_ubi")
    gif_product = fields.Many2one(comodel_name='product.template', string='Producto',compute="_onchange_gif_product")
    gif_qty = fields.Integer(string='Cantidad')
    gif_uom = fields.Many2one(comodel_name='uom.uom', string='Unidad de medida',compute="_onchange_gif_product")
    code_prod = fields.Char(string='CdB Producto')
    code_ubi = fields.Char(string='CdB Ubicación')
    gif_real_inv = fields.Integer(string='Cantidad en Sistema')
    gif_check = fields.Boolean(string='Consistente',compute="_check_check")
    # gif_sec_count = fields.Integer(string='Segundo Conteo')
    # gif_trd_count = fields.Integer(string='Tercer Conteo')
    
    @api.onchange('code_prod')
    def _onchange_gif_product(self):
        for record in self:
            if record.code_prod:
                product = record.env['product.template'].search([('barcode','=',record.code_prod)])
                inventary = record.env['stock.quant'].search([('location_id','=',record.gif_location.id)])
                record.gif_product = product.id
                record.gif_uom = product.uom_id
                for i in inventary:
                    if i.product_id.name == product.name:
                        record.gif_real_inv = i.inventory_quantity_auto_apply
                        break
                    else:
                        pass
            else:
                record.gif_product = False
                record.gif_uom = False

    @api.onchange('code_ubi')
    def _onchange_code_ubi(self):
        for record in self:
            if record.code_ubi:
                ubi = self.env['stock.location'].search([('barcode','=',record.code_ubi)])
                record.gif_location = ubi.id
            else:
                record.gif_location = False
    
    @api.onchange('gif_qty')
    def _check_check(self):
        for record in self:
            if record.gif_qty == record.gif_real_inv:
                record.gif_check = True
            else:
                record.gif_check = False

    
    
    
