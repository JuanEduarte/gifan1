import pandas as pd
import csv, requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import os
from os import remove



class GifConsigmentNoteButton(models.Model):
    _inherit = 'account.move'
    
    
    def get_data(self):
      
      for folder, subfolders, files in os.walk('/odoo/custom/addons/Report_data/'):
        
        if files:
          for file in files:
            
            ftr = ('/odoo/custom/addons/Report_data/'+file)
            
            remove(ftr)
        else: pass
        
      
      dirs = []
      for record in self:
        
        if record.state != 'posted':
          raise UserError(("Las factura "+record.name+" No esta en estado publicado"))
        else: 
          dirs.append(record.partner_shipping_id)
      
      unique = list(dict.fromkeys(dirs))
    
      
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
      
     
