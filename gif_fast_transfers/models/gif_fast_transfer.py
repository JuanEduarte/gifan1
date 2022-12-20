from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class GifFastTransfer(models.Model):
    _name = 'gif.fast.transfer'
    _description = 'Modelo para agilizar las transferencias.'

    name = fields.Char(string='Nombre')
    company_id = fields.Many2one(comodel_name='res.company', string='Compañia',default=lambda self: self.env.company.id)
    gif_type = fields.Selection(string='Tipo de movimiento', selection=[('purchase', 'Recepción'), ('sale', 'Entrega'),('transfer','Traslado')],readonly=True,copy=False,index=True,default='transfer')
    state = fields.Selection(string='Estado', selection=[('draft', 'Borrador'), ('done', 'Confirmado'),('cancel','Cancelado')],readonly=True,copy=False,index=True,default='draft')
    gif_sale_order = fields.Many2one(comodel_name='sale.order', string='Orden de Venta')
    gif_purchase_order = fields.Many2one(comodel_name='purchase.order', string='Orden de Compra')
    gif_fast_capture = fields.One2many(comodel_name='gif.fast.capture', inverse_name='gif_relation', string='Captura')
    gif_origin = fields.Char(string='Documento Origen')
    gif_picking = fields.Many2one(comodel_name='stock.picking', string='Movimiento')
    gif_transfer_type = fields.Selection(string='Tipo de traslado', selection=[('1', 'Normal'), ('2', 'Total'),],default='1')
    gif_ubi_origin = fields.Many2one(comodel_name='stock.location', string='Ubicación Origen')
    gif_ubi_dest = fields.Many2one(comodel_name='stock.location', string='Ubicación Destino')

    @api.onchange('gif_ubi_dest')
    def _onchange_gif_ubi_dest(self):
        for record in self:
            if record.gif_transfer_type == '2':
                if len(record.gif_ubi_dest.quant_ids) > 0:
                    raise ValidationError('Solo se puede hacer un traslado total a una ubicación vacía.')
                else:
                    if len(record.gif_ubi_origin.quant_ids) > 0:
                        for quant in record.gif_ubi_origin.quant_ids:
                            if quant.product_tmpl_id.active == True:
                                lineas = self.env['gif.fast.capture'].create({
                                    'gif_product_code': quant.product_tmpl_id.barcode or quant.product_tmpl_id.default_code,
                                    'gif_product': quant.product_tmpl_id.id,
                                    'gif_location_code': record.gif_ubi_dest.barcode,
                                    'gif_date': quant.removal_date,
                                    'gif_lot': quant.lot_id.name,
                                    'gif_qty': quant.available_quantity,
                                    'gif_relation': self.id,
                                })
                    else:
                        raise ValidationError('La ubicación Origen está vacía.')
            
    @api.model 
    def create(self, vals): 
        vals['name'] =self.env['ir.sequence'].next_by_code('gif.fast.transfer.name')      
        return super(GifFastTransfer, self).create(vals)
    
    def send_info(self):
        try:
            if self.gif_type == 'purchase':
                picking = self.env['stock.picking'].search([('origin','=',self.gif_purchase_order.name)])
                if picking:
                    # if len(self.gif_fast_capture) != len(picking.move_ids_without_package):
                    #     print('Error')
                    #     raise ValidationError('La cantidad de productos no coincide. En el documento hay: %s y la orden de entrega tiene: %s'%(len(self.gif_fast_capture),len(picking.move_ids_without_package)))
                    for record in self.gif_fast_capture:
                        for line in picking.move_ids_without_package:
                            if record.gif_product.id == line.product_id.id:
                                move = picking.move_line_ids.new({
                                    'product_id': record.gif_product.id,
                                    'location_id': picking.location_id.id,
                                    'location_dest_id': record.gif_location.id,
                                    'lot_name': record.gif_lot,
                                    'expiration_date': record.gif_date,
                                    'qty_done': record.gif_qty,
                                    'product_uom_id': record.gif_product.uom_id.id,
                                })
                                if move:
                                    picking.move_line_nosuggest_ids += move
                                    print(picking.move_line_nosuggest_ids)
            elif self.gif_type == 'sale':
                picking = self.env['stock.picking'].search([('id','=',self.gif_picking.id)])
                if picking:
                    for record in self.gif_fast_capture:
                        for line in picking.move_ids_without_package:
                            if record.gif_product.id == line.product_id.id:
                                line.update({
                                    'quantity_done': record.gif_qty,
                                })
            elif self.gif_type == 'transfer':
                type = self.env['stock.picking.type'].search([('name','ilike','Transferencias Internas')])
                picking_order = self.env['stock.picking'].create([{
                    # 'partner_id': ,
                    'picking_type_id': type.id,
                    'location_id': self.gif_ubi_origin.id,
                    'location_dest_id': self.gif_ubi_dest.id,
                    'scheduled_date': datetime.today(),
                    'date_done': datetime.today(),
                    # 'user_id': vendedor.id,
                }])
                for record in self.gif_fast_capture:
                    if picking_order.id != False:
                        picking_move = self.env['stock.move'].create([{
                            'name': record.gif_product.name,
                            'date': datetime.today(),
                            # 'scheduled_date': datetime.datetime.strptime(data['pedido']['fecha_servicio'], '%Y-%m-%d %H:%M:%S'),
                            'picking_id': picking_order.id,
                            'location_id': self.gif_ubi_origin.id,
                            'location_dest_id': self.gif_ubi_dest.id,
                            'product_id': record.gif_product.id,
                            'product_uom': record.gif_product.uom_id.id,
                            'product_uom_qty': record.gif_qty,
                            # 'qty_done': record.gif_qty,
                        }])
                        # 
                        # for line in picking_order.
                        lote = self.env['stock.production.lot'].search([('product_id','=',record.gif_product.id),('name','=',record.gif_lot)])
                        picking_line = self.env['stock.move.line'].create([{
                            'move_id': picking_move.id,
                            'picking_id': picking_order.id,
                            'product_id': record.gif_product.id,
                            'product_uom_id': record.gif_product.uom_id.id,
                            'location_id': self.gif_ubi_origin.id,
                            'location_dest_id': self.gif_ubi_dest.id,
                            'qty_done': record.gif_qty,
                            'cct_expiration_date': record.gif_date,
                            'lot_id': lote.id,
                            'gif_real_stockpicking': record.gif_qty,
                        }])
                        try:
                            picking_order.action_confirm()
                            picking_order.button_validate()
                            # try:
                            #     if not picking_order.env.context.get('button_validate_picking_ids'):
                            #         print('If not')
                            #         picking_order = picking_order.with_context(button_validate_picking_ids=picking_order.ids)
                            #     res = picking_order._pre_action_done_hook()
                            #     if res is not True:
                            #         print('Aquí retorna el res')
                            #         print('Vamos a asignarle la orden') 
                            #         expiry = self.env['expiry.picking.confirmation'].search([])
                            #         wizard = self.env['expiry.picking.confirmation'].search([('picking_ids','in',picking_order.ids)])
                            #         print('Otra prueba')
                            #         picking_to_validate = expiry.env.context.get('button_validate_picking_ids')
                            #         if picking_to_validate:
                            #             print('If la variable nueva')
                            #             expiry.process()
                            #             print('Se intento por otro lado')
                            #         print('Se los dimos al wizard')
                            #         wizard.process()
                            # except Exception as e:
                            #     print('Error del wizard: ',e)
                        except Exception as e:
                            print('El error: ',e)
                self.gif_picking = picking_order.id
            else:
                return True
            print('Se logro')
            self.state = 'done'
        except Exception as e:
            raise ValidationError(e)

    @api.constrains('gif_fast_capture')
    def gif_check_qty(self):
        if self.gif_type == 'purchase':
            big_error = "Algunos productos tienen cantidades mayores: "
            sum_total = {}
            for record in self.gif_fast_capture:
                key = str(record.gif_product.id)
                if key not in sum_total:
                    sum_total[key] = record.gif_qty
                else:
                    sum_total[key] = sum_total[key] + record.gif_qty
                print('El dict hasta ahora: ',sum_total)
            for line in self.gif_purchase_order.order_line:
                totales = line.product_qty * line.product_uom.factor_inv
                if sum_total[str(line.product_template_id.id)] > totales:
                    excedente = sum_total[str(line.product_template_id.id)] - totales
                    error = '\nEl producto: ' + line.product_template_id.name + ' tiene: '+str(excedente)+ ' unidades de más.'
                    big_error = big_error + error
            if big_error != "Algunos productos tienen cantidades mayores: ":
                raise ValidationError(big_error)
        

    @api.ondelete(at_uninstall=True)
    def _delete_registers(self):
        for record in self:
            if record.state == 'done':
                raise UserError('No puedes borrar registros que estén concluidos.')