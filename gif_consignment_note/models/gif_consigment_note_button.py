import pandas as pd
import csv, requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError



class GifConsigmentNoteButton(models.Model):
    _inherit = 'account.move'
    
    def get_data(self):
      ctx = self.env['gif.consignment.note'].with_context(Invoice_id=self.id)._context
      for record in self:
        print('***********', record.id)
      create = {
            'type': 'ir.actions.act_window',
            'res_model': 'gif.consignment.note',
            'target': 'new',
            'view_mode': 'form',
            'context': ctx,
            }
      print(create)
      return create
      
     
