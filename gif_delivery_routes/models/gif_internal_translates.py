from email.policy import default
from odoo.exceptions import UserError
from odoo import fields, models, api,_


class GifInternalRoutes(models.Model):
  _name = 'gif.internal.translates'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _description = 'Rutas'

  name                  = fields.Char    (string='Ruta de entrega', required=True, copy=False, index=True, default=lambda self: _('New'))
  distribution_route    = fields.Integer (string='Ruta de distribucion', default=0, store=True )
  customer              = fields.Many2one('res.partner', string='Cliente',store=True , required=True) 
  date                  = fields.Datetime(string='Fecha', required=True)
  carrier               = fields.Many2one('res.company', string='Transportista')
  vehicle_number        = fields.Many2one('fleet.vehicle', string='N° de veiculo')
  plates                = fields.Char    (string='Matriculas', compute='_onchange_vehicle_number')
  flete                 = fields.Integer (string='flete pactado', required=True)
  seguros               = fields.Integer (string='importe de maniobras', required=True)
  maniobras             = fields.Integer (string='Importe de seguros', required=True)
  mov                   =fields.Selection(string='Tipo de movimiento', selection=[('internal','Translados Internos'),('colect','Recolecciones'),('outgoing','Entregas')],  store=True)
  evidence              = fields.Image   ('Suba su imagen de evidencia', max_width=100, max_height=100, verify_resolution=False)
  state                 =fields.Selection([('draft','Borrador'),('done','Hecho'),('confirm','Confirmado'),('cancel','Cancelado')], default='draft', string='Status' )
  array1                =fields.Char     (string='a', compute='_onchange_gif_routes_details')
  array2                =fields.Char     (string='b', compute='_onchange_gif_routes_details')
  
    
  gif_personal_details  = fields.One2many(comodel_name='gif.personal.details',  inverse_name='gif_personal_id',  string='Detalles del personal')
  gif_routes_movements  = fields.One2many(comodel_name='gif.movements.details', inverse_name='gif_delivery_mov', string='Detalles de movimientos', store=True)
  gif_account_move      = fields.One2many(comodel_name = 'account.move', inverse_name= 'Route' ,  string='campo de validacion', store=True)
  
  frst_invoice = []
  lst_invoice  = []
  trd_invoice  = []
  
  
  @api.onchange('gif_routes_movements')
  def _onchange_gif_routes_details(self):
    for record in self:
      self.frst_invoice.clear()
      self.lst_invoice.clear()
      for i in record.gif_routes_movements:          
         self.frst_invoice.append(i.id)
      
      record.array1 = self.frst_invoice
        
      for i in record.gif_routes_movements:
          self.lst_invoice.append(i.id)   
      record.array2 = self.lst_invoice
     
  def action_draft(self):
    self.state='draft'    
  
  def action_done(self):
    self.state='done'
    if self.state:
      for i in self.gif_routes_movements.name:
          self.trd_invoice.append(i)
        

  def action_confirm(self):
    if not self.gif_routes_movements:
     raise UserError(('Debe haber registros en las lineas de detalles de movimientos'))
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
   
  @api.onchange('customer')
  def _onchange_customer_select(self):
    for record in (self): 
      for i in record.customer:
        return {'domain':{'child_ids':[('id', 'in', record.customer.child_ids.ids)]}}


 
  @api.onchange('mov')
  def _onchange_movement(self):
    for record in (self):
          b = 0
          if record.customer:
            stock_picking_ids = self.env['stock.picking'].search([('partner_id.name', '=', record.customer.name)])
            for i in stock_picking_ids:
              if i.picking_type_id.code == record.mov and i.state=='done':
                print('abc#########', i.name, i.state, i.picking_type_code, i.picking_type_id.name)
                print('####### DONE')
                b = b+1
                inv_rel =self.env['gif.movements.details'].create([{
                  'gif_delivery_mov': record.id,
                  'name': i.name,
                  'typee' : i.picking_type_id.name, 
                  'client': i.partner_id.name,
                  'origin_doc': i.origin,
                  'secuence': b,
                    }])
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
      
class GifmovementsDetails(models.Model):
  _name = 'gif.movements.details'
  _description = 'Detalles de los movimientos'
  
  gif_delivery_mov = fields.Many2one(comodel_name='gif.internal.translates')
  secuence = fields.Char(string='Secuencia')
  name = fields.Char(comodel= 'stock.picking', string='Nombre')
  typee = fields.Char(string='Tipo')
  client = fields.Char(string='Cliente')
  origin_doc  = fields.Char(string='Documento de origen')
  cobrado  = fields.Char(string='Cobrado')
  state =fields.Selection([('draft','Borrador'),('done','Hecho'),('confirm','Confirmado'),('cancel','Cancelado')], default='draft', string='Status' )
  
  
  '''@api.onchange('invoice')
  def _onchange_invoice(self):
    a=0
    for record in self:
      a=a+1
      if record.name:
        record.secuence = a
      else:
        pass'''
      
  @api.onchange('gif_delivery_mov.state')
  def _onchange_mov_field(self):
    for record in (self): 
      record.state = record.gif_delivery_mov.state

class ValidationInvoiceField(models.Model):
  _inherit = 'account.move'
  
  route_id = fields.Char(string='Rutas')