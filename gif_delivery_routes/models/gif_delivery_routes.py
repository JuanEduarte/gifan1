from email.policy import default
from odoo.exceptions import UserError
from odoo import fields, models, api,_


class GifDeliveriRoutes(models.Model):
  _name = 'gif.delivery.routes'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _description = 'Rutas'

  name                  = fields.Char    (string='Ruta de entrega', required=True, copy=False, index=True, default=lambda self: _('New'))
  distribution_route    = fields.Integer (string='Ruta de distribucion', default=0, store=True )
  customer              = fields.Many2one('res.partner', string='Cliente',store=True , required=True) 
  date                  = fields.Datetime(string='Fecha', required=True)
  carrier               = fields.Many2one('res.partner', string='Transportista')
  carrier_origin = fields.Selection(string='Origen del transportista', selection=[('intern', 'Interno'), ('extern', 'Externo')])  
  vehicle_number        = fields.Many2one('fleet.vehicle', string='N° de veiculo')
  plates                = fields.Char    (string='Matriculas', compute='_onchange_vehicle_number')
  flete                 = fields.Integer (string='flete pactado', required=True)
  seguros               = fields.Integer (string='importe de maniobras', required=True)
  maniobras             = fields.Integer (string='Importe de seguros', required=True)
  total                 = fields.Float   (string='Total', compute='_onchange_gif_routes_details' )
  child_ids             = fields.Many2one('res.partner', string='Direccion de entrega')
  evidence              = fields.Image   ('Suba su imagen de evidencia', max_width=100, max_height=100, verify_resolution=False)
  state                 =fields.Selection([('draft','Borrador'),('done','Hecho'),('confirm','Confirmado'),('cancel','Cancelado'),('return','Retornado')], default='draft', string='Status' )
  carrier_marca         =fields.Char(string='Marca del vehiculo')
  carrier_modelo        =fields.Char(string='Modelo del vehiculo')
  carrier_placas        =fields.Char(string='Placas del vehiculo')
  returned              =fields.Selection([('Delivery','Ruta entregada'),('Returned','Ruta regeresada'),('Partial','Parcialmente entregada')], string='Ruta retorno' )
  array1                =fields.Char     (string='a', compute='_onchange_gif_routes_details')
  array2                =fields.Char     (string='b', compute='_onchange_gif_routes_details')
  
    
  gif_personal_details  = fields.One2many(comodel_name='gif.personal.details',  inverse_name='gif_personal_id',  string='Detalles del personal')
  gif_routes_details    = fields.One2many(comodel_name='gif.routes.details',    inverse_name='gif_delivery_id',  string='Detalles de las rutas', store=True)
  gif_account_move      = fields.One2many(comodel_name = 'account.move', inverse_name= 'Route' ,  string='campo de validacion', store=True)
  
  frst_invoice = []
  lst_invoice  = []
  trd_invoice  = []
  
  
  @api.onchange('gif_routes_details')
  def _onchange_gif_routes_details(self):
    t = 0
    for record in self:
      self.frst_invoice.clear()
      self.lst_invoice.clear()
      for i in record.gif_routes_details.invoice:          
         self.frst_invoice.append(i.id)
         t += i.amount_total
      record.total = t
      record.array1 = self.frst_invoice
        
      for i in record.gif_routes_details.invoice:
          self.lst_invoice.append(i.id)   
      record.array2 = self.lst_invoice



 
  def action_draft(self):
    self.state='draft'    
  
  def action_done(self):
    self.state='done'
    if self.state:
      for i in self.gif_routes_details.invoice:
        self.trd_invoice.append(i.name)
        print('tipo:Ruta de factura')
    
  def action_confirm(self):
    if  not  self.gif_routes_details :
     raise UserError(('Debe haber registros en las lineas de detalles de rutas'))
   
    else:
      self.state='confirm'
      for record in self:
        for i in self.trd_invoice:
              nam = i
              for i in record.customer.invoice_ids:
                if i.name == nam:
                  i.route_id = record.name
        for i in record.customer.invoice_ids:
          if i.route_id == record.name and i.name not in self.trd_invoice:
            i.route_id = None
          else:
            pass

  def action_cancel(self):
    self.state='cancel'
    
  def action_return(self):
    self.state='return'
  



  @api.model
  def create(self, vals):
      if vals.get('name', _('New')) == _('New'):
        vals['name'] = self.env['ir.sequence'].next_by_code('gif.delivery.routes') or _('New')
      result = super(GifDeliveriRoutes, self).create(vals)
      return result




  @api.onchange("carrier_origin")
  def _onchange_carrier_origin(self):
    for record in self:
      if record.carrier_origin == 'intern':
        record.carrier = 13042
      
        
    
    
    
  @api.onchange('customer')
  def _onchange_customer_select(self):
    for record in (self): 
      for i in record.customer:
        return {'domain':{'child_ids':[('id', 'in', record.customer.child_ids.ids)]}}


  @api.onchange('child_ids')
  def _onchange_customer(self):
    b = 0
    for record in (self):
     if len(record.gif_routes_details) == 0:
        for i in record.customer.invoice_ids:
          if i.state == 'posted' and i.route_id == False and record.child_ids == i.partner_shipping_id: 
            b =+ 1
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
  validate = fields.Char(String='validar')
  state =fields.Selection([('draft','Borrador'),('done','Hecho'),('confirm','Confirmado'),('cancel','Cancelado')], default='draft', string='Status' )
  
  
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
        
  @api.onchange('gif_delivery_id.state')
  def _onchange_move_field(self):
    for record in (self): 
      record.state = record.gif_delivery_id.state
        
  @api.depends('gif_delivery_id.customer')
  @api.onchange('invoice')
  def _onchange_customer_select(self):
    selet=[]
    for record in (self): 
      for i in record.gif_delivery_id.lst_invoice:
        nam = i
        for i in record.gif_delivery_id.customer.invoice_ids:
          if nam == i.id:
            selet.append(i.name) 
               
      return {'domain':{'invoice':[('partner_id', '=', record.gif_delivery_id.customer.id),('state', '=', 'posted'), ('route_id', '=', None), ('name', 'ilike', '%FVMXN'), ('name', 'not in', selet)]}}

class ValidationInvoiceField(models.Model):
  _inherit = 'account.move'
  
  Route = fields.Many2one(comodel_name='gif.routes.details')
  route_id = fields.Many2one(string='Rutas')