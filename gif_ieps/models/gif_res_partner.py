
#from email.policy import default
from cgi import print_arguments
from odoo import api, fields, models

#Campos
class GifProductTemplate(models.Model):
     _inherit="product.template"

     gif_ieps_active = fields.Boolean(string = "Desglosar IEPS en factura")
     gif_ieps_type_sale = fields.Selection(string='Tipo de IEPS para ventas', default='%',selection=[('%', 'Porcentual'),('$', 'Fijo')])
     gif_ieps_value_sale = fields.Float(string='Valor de IEPS para ventas', default=0.0)
     gif_ieps_type_purchase = fields.Selection(string='Tipo de IEPS para compras', default='%',selection=[('%', 'Porcentual'),('$', 'Fijo')])
     gif_ieps_value_purchase = fields.Float(string='Valor de IEPS para compras', default=0.0)
     
     
     @api.onchange('gif_ieps_value_sale','gif_ieps_type_sale')
     def _verificaValorIEPS_ventas(self):
          if self.gif_ieps_type_sale == '%':
               if 0.0 < self.gif_ieps_value_sale < 100.0:
                    print("Valor del IEPS porcentual para ventas:",self.gif_ieps_value_sale)
               else:
                    self.gif_ieps_value_sale = 0.0
          else:
               if self.gif_ieps_value_sale < 0.0:
                    self.gif_ieps_value_sale = 0.0


     @api.onchange('gif_ieps_value_purchase','gif_ieps_type_purchase')
     def _verificaValorIEPS_compras(self):
          if self.gif_ieps_type_purchase == '%':
               if 0.0 < self.gif_ieps_value_purchase < 100.0:
                    print("Valor del IEPS porcentual para compras:",self.gif_ieps_value_purchase)
               else:
                    self.gif_ieps_value_purchase = 0.0
          else:
               if self.gif_ieps_value_purchase < 0.0:
                    self.gif_ieps_value_purchase = 0.0




#Agrega un campo en Contactos para dar la oṕcion de desglosar el IEPS o no en Sale, Purchase y Account
class GifResPartner(models.Model):
     _inherit="res.partner"

     gif_ieps_desglose = fields.Boolean(string = "Desglosar IEPS")



#Bibliotecas para intentar modificar el XML de la vista y así ocultar o mostrar
#el campo del IEPS
from lxml import etree
import json


class GifSaleOrderLine(models.Model):
     _inherit="sale.order.line"
     
     gif_IepsDisplay = fields.Boolean(related='order_id.gif_IepsDisplay')
     gif_SaleOrderIeps = fields.Float(string='IEPS',readonly=True,store=True)
     gif_SaleOrderIepsChar = fields.Char(string='IEPS Char',readonly=True,store=True)


class GifSaleOrder(models.Model):
     _inherit="sale.order"

     gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS',default=True)
     
     @api.onchange('order_line')
     def _ShowIeps(self):
          for record in self:
               for line in record.order_line:
                    producto = self.env['product.template'].search([('id','=',line.product_template_id.id)])
                    #print("Producto IEPSs: Sale(Type)=",producto.gif_ieps_type_sale," Sale(value)=",producto.gif_ieps_value_sale,
                    #" Purchase(Type)=",producto.gif_ieps_type_purchase," Purchase(value)=",producto.gif_ieps_value_purchase)
                    line.gif_SaleOrderIeps = producto.gif_ieps_value_sale
                    if producto.gif_ieps_type_sale == '%':
                         line.gif_SaleOrderIepsChar = str(producto.gif_ieps_value_sale)+' % ($ '+str(line.price_unit*(producto.gif_ieps_value_sale/100))+')'
                    else:
                         line.gif_SaleOrderIepsChar = '$ '+str(producto.gif_ieps_value_sale)
     

     #Al cambio en el valor del cliente se obtiene el valor del campo gif_ieps_desglose para saber si se
     #desglosa en IEPS o no
     @api.onchange('partner_id')
     def _IepsDisplay(self):
          for record in self:
               display = self.env['res.partner'].search([('id','=',record.partner_id.id)]).gif_ieps_desglose
               print("DISPLAY: ",display)
               record.gif_IepsDisplay = display
               self = self.with_context(gif_IepsDisplay = display)
               self.order_line = self.order_line.with_context(gif_IepsDisplay = display)




class GifPurchaseOrder(models.Model):
     _inherit="purchase.order"

     gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS_AM',default=False)

     @api.onchange('partner_id')
     def _IepsDisplay(self):
          for record in self:
               display = self.env['res.partner'].search([('id','=',record.partner_id.id)]).gif_ieps_desglose
               print("DISPLAY: ",display)
               record.order_line.gif_IepsDisplay = display
               print("\n\nVALOR DEL DISPLAY:",record.order_line.gif_IepsDisplay)


     '''
     @api.model
     def fields_view_get(self, view_id=None, view_type=False, context=None,toolbar=False, submenu=False):
          res = super(GifPurchaseOrder,self).fields_view_get(view_id=view_id, view_type=view_type,toolbar=toolbar, submenu=submenu)
          if view_type == 'form':
               #for node in doc.xpath("//field[@name='order_line']"):
               #     node.set('invisible', 'True')
               #     res['arch'] = etree.tostring(doc)
               doc = etree.XML(res['fields']['order_line']['views']['tree']['arch'])
               node = doc.xpath("//field[@name='gif_PurchaseOrderIeps']")
               node = node[0]
               print("\nNode:",node)
               node.set('invisible','1')
               print("\nNode Invisible:",etree.tostring(node))
               res['fields']['order_line']['views']['tree']['arch'] = etree.tostring(doc)
          return res
     '''

class GifPurchaseOrderLine(models.Model):
     _inherit="purchase.order.line"
     
     gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS',default=True)
     gif_PurchaseOrderIeps = fields.Float(string='IEPS',readonly=True)





class GifAccountMove(models.Model):
     _inherit="account.move"

     @api.onchange('partner_id')
     def _IepsDisplay(self):
          for record in self:
               display = self.env['res.partner'].search([('id','=',record.partner_id.id)]).gif_ieps_desglose
               print("DISPLAY: ",display)
               record.invoice_line_ids.gif_IepsDisplay = display
               print("\n\nVALOR DEL DISPLAY:",record.invoice_line_ids.gif_IepsDisplay)


class GifAccountMoveLine(models.Model):
     _inherit="account.move.line"

     gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS',default=True)
     gif_AccountMoveIeps = fields.Float(string='IEPS',readonly=True)
