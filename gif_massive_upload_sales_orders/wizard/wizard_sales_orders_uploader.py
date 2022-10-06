import base64
from io import BytesIO
from io import StringIO
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import openpyxl
import csv

class WizardSalesOrdersUploader(models.TransientModel):
    _name = 'wizard.sales.orders.uploader'
    _description = 'Cargador de órdenes de venta.'
    # id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    # gif_massive_upload_sales_orders.access_wizard_sales_orders_uploader,access_wizard_sales_orders_uploader,gif_massive_upload_sales_orders.model_wizard_sales_orders_uploader,,1,1,1,1

    name = fields.Char(string='Nombre del archivo')
    xlsx_files = fields.Binary('Archivo')

    gif_load_type = fields.Selection(selection = [('sor','Soriana'),
                                                ('frk','City Fresko Vallejo'),
                                                ('chd','Chedraui'),
                                                ('lpl','Liverpool'),
                                                ('um0','Carga masiva de Pedidos'),
                                                ('um1','Carga masiva de Pedidos EDI'),
                                                ],
                                    required=True,
                                    string="Tipo de carga")


    gif_order_date = fields.Char(string="Fecha de pedido")
    gif_init_date = fields.Char(string="Fecha de inicio")
    gif_cancel_date = fields.Char(string="Fecha de cancelación")
    gif_order = fields.Char(string="Número de pedido")
    gif_supplier_code = fields.Char(string="Número de proveedor")

    gif_lines = fields.One2many('wizard.sales.orders.uploader.line','gif_loader_id',string="Órdenes de venta",
                                readonly=True, limit=10)

    gif_sales_orders = {}

    def upload_files(self):
        for record in self:
            values = self.gif_upload_files()
            return {'type': 'ir.actions.client', 'tag': 'reload'}

    # @api.onchange('xlsx_files')
    def preview_files(self):
        """Función que recupera la información para previsualización."""
        for record in self:
            if not record.xlsx_files:
                raise UserError('Seleccione un archivo')
            
            try:
                wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(record.xlsx_files)), read_only=True)
                ws = wb.active
            except:
                # Intenta leer con archivo vacio
                pass
            else:
                tfv = self.env['gif.tipificaciones.ventas'].search([('name','=','Productos Primarios')]).id
                # delivery_addres_ref_not_found = []

                if record.gif_load_type == 'sor':
                    delivery_addres_ref_not_found = self.soriana_uploader(ws, tfv)
                
                elif record.gif_load_type == 'frk':
                    #delivery_addres_ref_not_found = self.fresko_uploader(ws, tfv)
                    pass


                # print("Dict len:", len(record.gif_sales_orders))
                if delivery_addres_ref_not_found:
                    dirs = ', '.join(delivery_addres_ref_not_found)
                    raise ValidationError("No se encontraron las siguientes direcciones de entrega:\n"+dirs)
                    #return self.notification("No se encontraron las siguientes direcciones de entrega:\n"+dirs)

            return {
                # 'name': 'Nootificación',
                # 'context':{'default_text_notification'},
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.sales.orders.uploader',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id':self.id,
                'target': 'new',
                }

    def soriana_uploader(self, ws, tfv):
        for record in self:
            delivery_addres_ref_not_found = []
            # self.gif_sales_orders = {}
            # Encabezado
            nrow = 1
            for row in ws.iter_rows(min_row=1, max_row=6, min_col=None, max_col=None, values_only=True):
                
                if nrow == 1:
                    record.gif_supplier_code = row[1]
                    record.gif_order = row[3]

                elif nrow == 2:
                    record.gif_order_date = row[1]

                elif nrow == 6:
                    record.gif_init_date = row[0]
                    record.gif_cancel_date = row[1]

                nrow += 1

            
            for row in ws.iter_rows(min_row=None, max_row=None, min_col=None, max_col=None, values_only=True):
                
                # Debe tener un numero de pedido
                if str(row[1]) != str(record.gif_order):
                    continue

                # Solo se leen 1 vez
                if row[2] in record.gif_sales_orders.keys() or str(row[2]) in delivery_addres_ref_not_found:
                    continue
                
                # Direccion de entrega
                del_dir = record.env['res.partner'].search([('parent_id','!=',False),('ref','=',str(row[2]))])
                if not del_dir:
                    delivery_addres_ref_not_found.append(str(row[2]))
                    continue

                # Visualizaciones
                vals = {
                    'gif_delivery_dir_code': row[2],
                    'gif_delivery_dir': del_dir.id,
                    'gif_customer': del_dir.parent_id.id,
                    'gif_customer_code': del_dir.parent_id.ref,
                }

                record.gif_lines = [(0,0,vals)]

                # Datos de ordenes
                record.gif_sales_orders[row[2]] = {
                    'vals':{
                        'partner_id': del_dir.parent_id.id,
                        'gif_partner_code': del_dir.parent_id.ref,
                        'partner_shipping_id':del_dir.id,
                        'gif_partner_shipping_code':del_dir.ref,
                        'gif_supplier_code':self.gif_supplier_code,
                        'origin':row[1],
                        'validity_date':None,
                        'gif_init_date':None,
                        # 'date_order':None,
                        'tipificacion_venta':tfv,
                        # 'state':'sale',
                    },
                    'lines':[],
                }

            return delivery_addres_ref_not_found

    def gif_upload_files(self):
        for record in self:
            try:
                wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(record.xlsx_files)), read_only=True)
                ws = wb.active
            except:
                # Intenta leer con archivo vacio
                pass
            else:
                if record.gif_load_type == 'sor':
                    sale_orders = {}
                    products_not_found = []

                    # Para cada linea de pedido
                    for row in ws.iter_rows(min_row=None, max_row=None, min_col=None, max_col=None, values_only=True):

                        sale_order = record.gif_sales_orders.get(row[2], False)

                        # Numero de pedido

                        if str(row[1]) != str(record.gif_order) or not sale_order:
                            continue
                        

                        product = self.env['product.product'].search([('barcode','=',row[4])])
                        if not product:
                            products_not_found.append(str(row[4]))
                            continue

                        partner_details = self.env['gif.partners.details'].search([
                                ('product_tmp_id','=', product.product_tmpl_id.id),
                                ('partner','=', sale_order['vals']['partner_id'])
                                ])

                        order_line = {
                            'product_template_id': product.product_tmpl_id.id,
                            'product_uom_qty': float(row[3]),
                            'product_uom': partner_details.partner_uom.id,
                            'price_subtotal': float(row[6]),
                            #'tax_id': product.product_tmpl_id.taxes_id.id,
                            'name':product.product_tmpl_id.description_sale,
                            # 'customer_lead':15.0,
                            'product_id':product.id,
                        }
                        order_line['price_unit'] = order_line['price_subtotal'] / order_line['product_uom_qty']

                        sale_order['lines'].append(order_line)

                    if products_not_found:
                        prod = ', '.join(products_not_found)
                        raise ValidationError("No se encontraron los siguientes productos:\n"+prod)

                    # for key, vals in record.gif_sales_orders.items():
                    #     print("Key:", key)
                    #     print("   Val", vals['vals'])
                    #     for line in vals['lines']:
                    #         print("   Line", line)
                
                self.create_orders()
    

    def create_orders(self):
        for id,order in self.gif_sales_orders.items():
            so = self.env['sale.order'].create(order.get('vals',{}))
            for line in order.get('lines',[]):
                so.order_line = [(0,0,line)]
        

                            
    def notification(self, msm):
        return {
            'name': 'Notificación',
            'context':{'default_text_notification':msm},
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.notification',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            }
                    

                        



class WizardSalesOrdersUploaderLine(models.TransientModel):
    _name = 'wizard.sales.orders.uploader.line'
    _description = 'Lineas de cargador de órdenes de venta.'

    gif_loader_id = fields.Many2one('wizard.sales.orders.uploader')

    gif_customer = fields.Many2one('res.partner',string="Cliente")
    gif_customer_code = fields.Char(string="Codigo de cliente")
    gif_delivery_dir = fields.Many2one('res.partner',string="Dirección de entrega")
    gif_delivery_dir_code = fields.Char(string="Código de Dirección de entrega")

