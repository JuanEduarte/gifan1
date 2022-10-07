from odoo import fields, models, api,_


class GifDeliveriRoutes(models.Model):
  _name = 'gif.delivery.routes'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _description = 'Rutas'

  name                  = fields.Char    (string='Ruta de entrega', required=True, copy=False, index=True, default=lambda self: _('New'))
  distribution_route    = fields.Integer (string='Ruta de distribucion', default=0, store=True )
  customer              = fields.Many2one('res.partner', string='Cliente',store=True , required=True) 
  type1                 = fields.Boolean (string='Rutas de factura', default=False, store = True)
  type2                 = fields.Boolean (string='Rutas de movimientos', default=False,store = True) 
  date                  = fields.Datetime(string='Fecha', required=True)
  carrier               = fields.Many2one('res.company', string='Transportista')
  vehicle_number        = fields.Many2one('fleet.vehicle', string='N° de veiculo')
  plates                = fields.Char    (string='Matriculas', compute='_onchange_vehicle_number')
  flete                 = fields.Integer (string='flete pactado', required=True)
  seguros               = fields.Integer (string='importe de maniobras', required=True)
  maniobras             = fields.Integer (string='Importe de seguros', required=True)
  total                 = fields.Float   (string='Total', compute = '_onchange_custom')
  child_ids             = fields.Many2one('res.partner', string='Direccion de entrega')
  mov                   =fields.Selection(string='Tipo de movimiento', selection=[('internal','Translados Internos'),('internal','Recolecciones'),('3','Paquetes'),('outgoing','Entregas')], store=True)
  evidence              = fields.Image   ('Suba su imagen de evidencia', max_width=100, max_height=100, verify_resolution=False)
  
  
  gif_personal_details  = fields.One2many(comodel_name='gif.personal.details', inverse_name='gif_personal_id', string='Detalles del personal')
  gif_routes_details    = fields.One2many(comodel_name='gif.routes.details', inverse_name='gif_delivery_id', string='Detalles de las rutas', store=True)
  gif_routes_movements  = fields.One2many(comodel_name='gif.movements.details', inverse_name='gif_delivery_mov', string='Detalles de movimientos', store=True)
  gif_account_move = fields.One2many(comodel_name = 'account.move', inverse_name= 'Route' ,  string='campo de validacion', store=True)

  
  @api.model
  def create(self, vals):
      if vals.get('name', _('New')) == _('New'):
        vals['name'] = self.env['ir.sequence'].next_by_code('gif.delivery.routes') or _('New')
      result = super(GifDeliveriRoutes, self).create(vals)
      return result

  @api.onchange('customer')
  def _onchange_move_select(self):
    for record in (self): 
      if record.customer:
        stock_picking_ids = self.env['stock.picking'].search([('partner_id.name', '=', record.customer.name)])
        for i in stock_picking_ids:
          pass
      else:
        stock_picking_ids = self.env['stock.picking'].search([('partner_id', '=', False)])
        for i in stock_picking_ids:
          pass
        
  @api.onchange('customer')
  def _onchange_customer_select(self):
    for record in (self): 
      for i in record.customer:
        return {'domain':{'child_ids':[('id', 'in', record.customer.child_ids.ids)]}}


  @api.onchange('child_ids')
  def _onchange_customer(self):
    a = 0
    b = 0
    for record in (self):
     if len(record.gif_routes_details) == 0:
        for i in record.customer.invoice_ids:
          if i.state == 'posted' and record.child_ids == i.partner_shipping_id: 
            b =+ 1
            a = a + i.amount_total
            #record.total = a
            invoice_rel =self.env['gif.routes.details'].create([{
              'gif_delivery_id': record.id,
              'invoice': i.id,
              'order': i.invoice_origin,
              'importe': i.amount_total,
              'client': i.partner_id.name,
              'secuence': b,
            }])
          else:
            a = 0
            b = ""
    else:
        pass
      
      
  @api.onchange('mov')
  def _onchange_movement(self):
    for record in (self):
          b = 0
          if record.customer:
            stock_picking_ids = self.env['stock.picking'].search([('partner_id.name', '=', record.customer.name)])
            #print('abc#########', stock_picking_ids)
            for i in stock_picking_ids:
              if i.picking_type_id.code == record.mov:
                print('abc#########', i.name, i.state, i.picking_type_code, i.picking_type_id.name)
                print('####### DONE')
                b = b+1
                inv_rel =self.env['gif.movements.details'].create([{
                  'gif_delivery_mov': record.id,
                  'name': i.name,
                  'type' : i.picking_type_id.name, 
                  'origin_doc': i.origin,
                  'secuence': b,
                    }])
              else:
                pass
    
  @api.onchange('customer')
  def _onchange_child_id(self):
    for record in (self):
     if len(record.gif_routes_details) == 0:
        for i in record.customer.invoice_ids:
          if i.state == 'posted' and i.invoice_origin and record.child_ids == i.partner_shipping_id: 
            invoice_rel =self.env['account.move'].create([{
              'Route': record.id,
              'route_id': i.id,
            }])
    else:
        pass

  @api.onchange('child_ids')
  def _onchange_custom(self):
    for record in (self):
        a = 0
        for i in record.customer.invoice_ids:
          if   i.state == 'posted' and record.child_ids == i.partner_shipping_id : 
            a = a + i.amount_total
          record.total= a
        
  @api.onchange('vehicle_number')
  def _onchange_vehicle_number(self):
    for record in self:
      if record.vehicle_number:
        record.plates = record.vehicle_number.license_plate
      else:
        record.plates =''
        
  def action_report(self):
   return self.env.ref('gif_delivery_routes.action_report_delivery_routes').report_action(self)


class GifPersonalDetails(models.Model):
  _name = 'gif.personal.details'
  _description = 'Detalles del personal'
  
  gif_personal_id = fields.Many2one(comodel_name='gif.delivery.routes')
  employe_name    = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True)
  employe_type    = fields.Char    (string='Tipo de empleado', compute='_onchange_employe_type')
  employe_id      = fields.Char    (string='ID de personal', compute='_onchange_employe_type')
  secuence = fields.Char           (string='Secuencia', compute='_onchange_secuence_compute')
  
  
  @api.onchange('employe_name')
  def _onchange_employe_type(self):
    try:
      for record in self:
        if record.employe_name:
          record.employe_type = record.employe_name.job_title
          record.employe_id = record.employe_name.barcode
        else:
         record.employe_type = ''
         record.employe_id = ''
    except:
      record.employe_type = ''
      record.employe_id = ''
      
      
  
  @api.onchange('employe_name')
  def _onchange_secuence_compute(self):
    a=0
    for record in self:
      if record.employe_name:
       a = a+1
       record.secuence=a

class GifRoutesDetails(models.Model):
  _name = 'gif.routes.details'
  _description = 'Detalles de las rutas'
  
  gif_delivery_id = fields.Many2one(comodel_name='gif.delivery.routes')
  secuence = fields.Char(string='Secuencia', compute='_onchange_invoice')
  invoice  = fields.Many2one(comodel_name='account.move', string='Factura')
  fiscal = fields.Char(string='fiscal')
  client = fields.Char(string='Cliente', compute='_onchange_invoice')
  importe  = fields.Char(string='Importe', compute='_onchange_invoice')
  order = fields.Char(string = 'Orden de venta', compute='_onchange_invoice')
  cobrado  = fields.Char(string='Cobrado')
  
  
  @api.onchange('invoice')
  def _onchange_invoice(self):
    a=0
    for record in self:
      a=a+1
      if record.invoice:
        record.importe = record.invoice.amount_total
        record.order = record.invoice.invoice_origin
        record.client = record.invoice.partner_id.name
        record.secuence = a
      else:
        record.importe = ''
        record.order = ''
        record.client = ''
        record.secuence = a
        
  @api.depends('gif_delivery_id.customer')
  @api.onchange('invoice')
  def _onchange_customer_selec(self):
    for record in (self): 
      return {'domain':{'invoice':[('partner_id', '=', record.gif_delivery_id.customer.id),('state', '=', 'posted')]}}
       
class GifmovementsDetails(models.Model):
  _name = 'gif.movements.details'
  _description = 'Detalles de los movimientos'
  
  gif_delivery_mov = fields.Many2one(comodel_name='gif.delivery.routes')
  secuence = fields.Char(string='Secuencia')
  name = fields.Char(string='Nombre', store=True)
  type = fields.Char(string='Tipo')
  client = fields.Char(string='Cliente')
  origin_doc  = fields.Char(string='Domcumento de origen')
  cobrado  = fields.Char(string='Cobrado')
  
  
  @api.onchange('invoice')
  def _onchange_invoice(self):
    a=0
    for record in self:
      a=a+1
      if record.name:
        record.secuence = a
      else:
        pass

class ValidationInvoiceField(models.Model):
  _inherit = 'account.move'
  
  Route = fields.Many2one(comodel_name='gif.routes.details')
  route_id = fields.Char(string='Rutas')