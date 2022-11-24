import pandas as pd
import csv, requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError



class GifConsigmentNoteButton(models.Model):
    _inherit = 'account.move'
    
    
    def get_data(self):
      print ('selfff',self)
      dirs = []
      for record in self:
        if record.state != 'posted':
          raise UserError(("Las factura "+record.name+" No esta en estado publicado"))
        else: 
          dirs.append(record.partner_shipping_id)
      print(dirs)
      unique = list(dict.fromkeys(dirs))
    
      print(unique)
      l = len(unique)
      if l != 1:
        raise UserError(("Las facturas seleccionadas no tienen la misma direccion de entrega, verifique su seleccion!"))
      elif l == 1 :
        create = {
              'type': 'ir.actions.act_window',
              'res_model': 'gif.consignment.note',
              'target': 'new',
              'view_mode': 'form',
              }
        return create
      else:
        return False
      
     
