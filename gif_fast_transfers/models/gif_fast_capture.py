from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class GifFastCapture(models.Model):
    _name = 'gif.fast.capture'
    _description = 'Modelo para la captura rapida de datos para traslados.'

    def _default_date(self):
        print('Default: ')
        print('Tipo: ',self.gif_relation.gif_type)
        if self.gif_relation.gif_type == 'transfer':
            return False
        else:
            today = datetime.today()
            one_year = today + relativedelta(years=1)
            default_date = one_year.replace(hour=6,minute=0,second=0)
            return default_date

    name = fields.Char(string='Nombre')
    company_id = fields.Many2one(comodel_name='res.company', string='Compañia',default=lambda self: self.env.company.id)
    gif_product = fields.Many2one(comodel_name='product.template', string='Producto',compute='_onchange_gif_product_code')
    gif_location_code = fields.Char(string='Código Ubicación')
    gif_location = fields.Many2one(comodel_name='stock.location', string='Ubicación',compute='_onchange_gif_location_code')
    gif_date = fields.Datetime(string='Fecha de  caducidad',default=_default_date)
    gif_lot = fields.Char(string='Numero de Lote')
    gif_lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', domain="[('product_id', '=', gif_product), ('company_id', '=', company_id)]", check_company=True)
    gif_qty = fields.Integer(string='Cantidad Recibida',default=0)
    gif_relation = fields.Many2one(comodel_name='gif.fast.transfer', string='Relación')
    gif_product_code = fields.Char(string='Código del Producto')
    gif_has_code = fields.Boolean(default=False)
    

    @api.onchange('gif_product_code')
    def _onchange_gif_product_code(self):
        try:
            id_purchase = []
            id_sale = []
            for record in self:
                producto = False
                if record.gif_product_code != False:
                    producto = record.env['product.template'].search(['|',('barcode','=',record.gif_product_code),('default_code','=',record.gif_product_code)])
                    if len(producto) != 0:
                        record.gif_product = producto.id
                    else:
                        producto = record.env['gif.partners.details'].search(['|',('bar_code','=',record.gif_product_code),('individual_code','=',record.gif_product_code)],limit=1)
                        if producto != False and len(producto) != 0:
                            record.gif_product = producto.product_tmp_id.id
                        else:
                            producto = record.env['gif.partners.details.purchase'].search(['|',('bar_code_purchase','=',record.gif_product_code),('individual_code_purchase','=',record.gif_product_code)],limit=1)
                            if producto != False and len(producto) != 0:
                                record.gif_product = producto.product_tmp_id_purchase.id
                            else:
                                record.gif_product = False
                    if record.gif_product != False:
                        if record.gif_relation.gif_type == 'transfer':
                            if record.gif_relation.gif_ubi_dest.id != False:
                                record.gif_location_code = record.gif_relation.gif_ubi_origin.barcode
                                record.gif_has_code = True
                        else:
                            if record.gif_relation.gif_type == 'purchase':
                                for line_p in record.gif_relation.gif_purchase_order.order_line:
                                    if line_p.product_template_id.id not in id_purchase:
                                        id_purchase.append(line_p.product_template_id.id)
                                if record.gif_product.id not in id_purchase:
                                    raise ValidationError('No puedes agregar productos que no están en la orden de compra.')
                                if record.gif_product.gif_def_loc_in.id != False and record.gif_location_code == False:
                                    record.gif_location_code = record.gif_product.gif_def_loc_in.barcode
                                    record.gif_has_code = True
                            elif record.gif_relation.gif_type == 'sale':
                                for line_s in record.gif_relation.gif_sale_order.order_line:
                                    if line_s.product_template_id.id not in id_sale:
                                        id_sale.append(line_s.product_template_id.id)
                                if record.gif_product.id not in id_sale:
                                    raise ValidationError('No puedes agregar productos uqe no están en la orden de venta.')
                                if record.gif_product.gif_def_loc_out.id != False and record.gif_location_code == False:
                                    record.gif_location_code = record.gif_product.gif_def_loc_out.barcode
                                    record.gif_has_code = True
                else:
                    record.gif_product = False
        except Exception as e:
            print('Error: ',e)

    @api.onchange('gif_location_code')
    def _onchange_gif_location_code(self):
        for record in self:
            if record.gif_location_code:
                ubi = self.env['stock.location'].search([('barcode','=',record.gif_location_code)])
                record.gif_location = ubi.id
            else:
                record.gif_location = False

    @api.onchange('gif_date')
    def onchange_gif_date(self):
        for record in self:
            if self.gif_date:
                # self.gif_date = self.with_user_timezone(self.gif_date)
                record.gif_lot = str(self.gif_date.date()).replace('-','')

    @api.onchange('gif_qty')
    def _onchange_gif_qty(self):
        # print('Reinicio')
        gif_id = []
        order_id = []
        for record in self:
            print('Linea: ',record.gif_lot)
            if record.gif_relation.gif_type == 'purchase':
                prefijo = 'recibir'
                ubi_string = 'orden.'
                for line in record.gif_relation.gif_purchase_order.order_line:
                    total_units = 0
                    order_id.append(line.product_template_id.id)
                    gif_id.append(record.gif_product.id)
                    if line.product_template_id.id == record.gif_product.id:
                        total_units = line.product_qty * line.product_uom.factor_inv
                        if  total_units < record.gif_qty:
                            raise ValidationError('No puedes recibir más productos de los solicitados.')
            elif record.gif_relation.gif_type == 'sale':
                prefijo = 'entregar'
                ubi_string = 'orden.'
                for line in record.gif_relation.gif_sale_order.order_line:
                    order_id.append(line.product_template_id.id)
                    gif_id.append(record.gif_product.id)
                    # total_units = line.product_qty * line.product_uom.factor_invs
            elif record.gif_relation.gif_type == 'transfer':
                prefijo = 'trasladar'
                ubi_string = 'ubicación origen.'
                for line in record.gif_relation.gif_ubi_origin.quant_ids:
                    order_id.append(line.product_tmpl_id.id)
                    gif_id.append(record.gif_product.id)
                    if line.product_tmpl_id.id == record.gif_product.id and line.removal_date == record.gif_date:
                        if record.gif_qty > line.available_quantity:
                            raise ValidationError('No puedes trasladar más unidades de las que tienes.')
        if len(gif_id) > 0:
            for g in gif_id:
                if g not in order_id and g != False:
                    string = 'No puedes '+ prefijo +' productos que no están en la ' + ubi_string
                    raise ValidationError(string)
    
    
    