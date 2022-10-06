from odoo import models, fields


class ModuleName(models.Model):
  _inherit = 'account.move'
  
  Route = fields.Many2one(comodel_name='gif.delivery.routes')
  route_id = fields.Char(strting='Ruta')
  
  
  def asigned_route(self):
    for record in self:
      for l in record.Route:
      
          print (l.name)
          print (l)
          print (l)
       
        
      
    