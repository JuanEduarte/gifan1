from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil import relativedelta
import string
import re


class SalesReportsWizard(models.TransientModel):

    _name = 'sales.reports.wizard'
    
    name = fields.Char(string='name')
    start_date = fields.Date(string='Fecha de inicio', default=str(datetime.now() + relativedelta.relativedelta(months=-2, day=1, days=-1))[:10])
    end_date = fields.Date(string='Fecha de termino', default=datetime.today())
    client_param1 = fields.Char(string='Primer rango de cliente')
    client_param2 = fields.Char(string='Segundo rango de cliente')
    product_param1 = fields.Char(string='Primer rango de productos')
    product_param2 = fields.Char(string='Segundo rango de productos ')
    
    moves = []
    
    
    def get_sale_report(self):
      by_date = self.env['sale.order'].search([('create_date', '<=', self.end_date),('create_date', '>=', self.start_date)])
      print(by_date)
      if self.client_param1 == False and self.client_param2 == False:    
        for i in by_date:
          print(i)
          self.moves.append(i)
      
      elif self.client_param1 and self.client_param2 == False:
        print('#### UN SOLO PARAMETRO DE CLIENTE')
        clients_name = []
        self.moves.clear()
        for i in by_date:
          clients_name.append(i.partner_id.name)
        dato = '^'+(str(self.client_param1)).upper()
        filtradas = [p for p in clients_name if  re.match(dato, (p.upper()))]
        
        for j in filtradas:
          res = self.env['sale.order'].search([('partner_id.name', '=', j)])
        self.moves.append(res)
        #print('*** REGRESA', self.moves)

      elif self.client_param1 and self.client_param2:
        orders = []
        self.moves.clear()
        for i in string.ascii_lowercase:
          if string.ascii_lowercase.index(i) >= string.ascii_lowercase.index(self.client_param1) and string.ascii_lowercase.index(i) <= string.ascii_lowercase.index(self.client_param2):
            for order in by_date:
              if order.partner_id.name.startswith(i.upper()):
                self.moves.append(order)
                orders.append(order.partner_id.name)
              else:
                pass
        orders1 = sorted(orders)
        for k in orders1:
          print('*******',k)
          
      print('moves',self.moves)
      
      