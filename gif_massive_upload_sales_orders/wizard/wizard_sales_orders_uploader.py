from http import client
import re
import csv
from xml.dom import ValidationErr
import openpyxl
import base64
from io import BytesIO
from io import StringIO
from pytz import timezone
from datetime import date, datetime as dt, timedelta
from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, api

class WizardSalesOrdersUploader(models.TransientModel):
    _name = 'wizard.sales.orders.uploader'
    _description = 'Cargador de órdenes de venta.'
    # id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    # gif_massive_upload_sales_orders.access_wizard_sales_orders_uploader,access_wizard_sales_orders_uploader,gif_massive_upload_sales_orders.model_wizard_sales_orders_uploader,,1,1,1,1
    
    name = fields.Char(string='Nombre del archivo')
    orders_file = fields.Binary('Archivo', required=True)

    gif_load_type = fields.Selection(selection = [('sor','Soriana'),
                                                ('frk','City Fresko Vallejo'),
                                                ('che','Chedraui'),
                                                ('liv','Liverpool'),
                                                ('heb','HEB'),
                                                ('csv','Carga genérica CSV'),
                                                ],
                                    required=True,
                                    string="Tipo de carga")


    gif_order_date = fields.Date(string="Fecha de pedido")
    gif_init_date = fields.Date(string="Fecha de inicio")
    gif_cancel_date = fields.Date(string="Fecha de cancelación")
    gif_supplier_code = fields.Char(string="Número de proveedor")

    gif_customer = fields.Many2one('res.partner',string="Cliente")
    gif_customer_code = fields.Char(string="Codigo de cliente")
    gif_delivery_dir = fields.Many2one('res.partner',string="Dirección de entrega")
    gif_delivery_dir_code = fields.Char(string="Código de dirección de entrega")
    gif_order = fields.Char(string="Número de pedido")

    gif_tfv = fields.Many2one('gif.tipificaciones.ventas',
        default = lambda self: self.env['gif.tipificaciones.ventas'].search([('name','=','Productos Primarios')]))

    gif_tag = fields.Many2one('crm.tag',
        default = lambda self: self.env['crm.tag'].search([('name','=','Carga masiva')]))

    gif_isValid = fields.Boolean(default=False)

    gif_content_file = []
    delivery_address_not_found = []
    products_not_found = []
    invalid_products = []

    gif_sale_order_lines = []       # Productos
    """[{key:val},{...},...]"""


    def upload_files(self):
        for record in self:
            values = self.gif_create_orders()
            return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.onchange('gif_customer')
    def onchange_customer(self):
        if self.gif_load_type == 'csv':
            self.gif_customer_code = self.gif_customer.ref if self.gif_customer else False

    @api.onchange('gif_delivery_dir')
    def onchange_delivery_dir(self):
        if self.gif_load_type == 'csv':
            self.gif_delivery_dir_code = self.gif_delivery_dir.ref if self.gif_delivery_dir else False


    @api.onchange('gif_load_type')
    def get_customer(self):
        """Función que recupera el cliente por defecto establecido en las fichas de cliente de cargas masivas."""

        self.clear_fields()

        customers = self.env['default.customers'].search([])
        
        if not customers:
            raise UserError('No exiten fichas de cliente por defecto.')

        if customers[-1]:
            if self.gif_load_type == 'sor':
                self.gif_customer = customers[-1].gif_partner_soriana
            
            elif self.gif_load_type == 'frk':
                self.gif_customer = customers[-1].gif_partner_cityfresko
            
            elif self.gif_load_type == 'che':
                self.gif_customer = customers[-1].gif_partner_chedraui

            elif self.gif_load_type == 'liv':
                self.gif_customer = customers[-1].gif_partner_liverpool
            
            elif self.gif_load_type == 'heb':
                self.gif_customer = customers[-1].gif_partner_heb

            else:
                self.gif_customer = False

            self.gif_customer_code = self.gif_customer.ref if self.gif_customer else False
            self.gif_delivery_dir_code = self.gif_delivery_dir if self.gif_delivery_dir else False

        else:
            raise UserError('No exiten fichas de cliente por defecto.')


    @api.onchange('orders_file')
    def clear_fields(self):
        """Función que limpia los campos cuando se selecciona un nuevo archivo."""
        self.gif_content_file.clear()
        self.delivery_address_not_found.clear()
        self.products_not_found.clear()
        self.invalid_products.clear()
        self.gif_sale_order_lines.clear()

        self.gif_order = None
        self.gif_order_date = None
        self.gif_init_date = None
        self.gif_cancel_date = None
        self.gif_supplier_code = None

        self.gif_delivery_dir = None
        self.gif_delivery_dir_code = None
        self.gif_isValid = False

    def _check_product(self,upc):
        """Función que valida la existencia de un producto y si se puede vender al cliente."""

        name = str(upc)
        # Buscamos el producto por código de barras
        product = self.env['product.product'].search([('barcode','=',name)])
        
        if len(product) > 1:
            raise ValidationError("El código %s está establecido para varios productos." % name)

        if not product:
            # Buscamos el producto por código de barras o individual del cliente
            details_id = self.env['gif.partners.details'].search(['|',('bar_code','=',name),('individual_code','=',name)])
            """Lo activo?"""
            # if len(details_id) > 1:
            #     raise ValidationError("El código %s está establecido para varios clientes." % name)

            product_id = details_id[0].product_tmp_id.product_variant_id.id
            product = self.env['product.product'].browse(product_id)
            
        
        if not product:
            self.products_not_found.append(str(upc))
            return (False,False)

        partner_details = self.env['gif.partners.details'].search([
                             ('product_tmp_id','=', product.product_tmpl_id.id),
                             ('partner','=', self.gif_customer.id) ])
        
        if not partner_details:
            self.invalid_products.append(f'{product.barcode} - {product.name}\n')
            return (False,False)
        
        # return (product, partner_details)
        return (product, partner_details)

    def read_soriana(self):
        """Función que recupera los datos del archivo con formato para Soriana"""
        # Encabezado
        self.gif_supplier_code = self.gif_content_file[0][1]
        self.gif_order = self.gif_content_file[0][3]

        self.gif_order_date = self.get_date(self.gif_content_file[1][1])
        self.gif_init_date = self.get_date(self.gif_content_file[5][0])
        self.gif_cancel_date = self.get_date(self.gif_content_file[5][1])
        
        shops = list(map(lambda x: int(x), self.gif_content_file[5][2].split(',')))

        # Buscamos la direccion de entrega
        for a,b,shop,*_ in self.gif_content_file:

            if str(shop).isnumeric():
                if shop in shops:
                    continue        # Tienda
            else:
                continue            # Otro

            # Direccion de entrega
            del_dir = self.env['res.partner'].search([('type','=','delivery'),('ref','=',str(shop))])
            
            if not del_dir and str(shop) not in self.delivery_address_not_found:
                self.delivery_address_not_found.append(str(shop))
                continue
            
            self.gif_delivery_dir = del_dir.id
            self.gif_delivery_dir_code = del_dir.ref
            break
        
        if not self.gif_delivery_dir:
            raise ValidationError('No se encontró ninguna dirección de entrega.')

        # Buscamos las lineas de productos
        for prov,ped,dir,qty,upc,uc,precost,*_ in self.gif_content_file:
            if str(dir) == self.gif_delivery_dir_code:
                
                product, partner_details = self._check_product(upc)
                if not product:
                    continue

                order_line = {
                    'product_template_id': product.product_tmpl_id.id,
                    'product_uom_qty': float(qty),
                    'product_uom': partner_details.partner_uom.id,
                    # 'price_subtotal': float(row[6]),
                    'name':product.product_tmpl_id.description_sale,
                    'product_id':product.id,
                }
                order_line['price_unit'] = round(float(precost) / order_line['product_uom_qty'], 2)

                self.gif_sale_order_lines.append(order_line)

    def read_fresko(self):
        """Función que recupera los datos del archivo con formato para City Fresko"""
        
        # Se busca el encabezado de la orden
        for mod, dir, ped, prov, status, ordt, indt, cldt,*_ in self.gif_content_file:
            
            if mod == "DE" and str(dir).isnumeric():

                # Direccion de entrega
                del_dir = self.env['res.partner'].search([('type','=','delivery'),('ref','=',str(dir))])
                
                if not del_dir:
                    self.delivery_address_not_found.append(str(dir))
                    continue
                
                self.gif_order = ped
                self.gif_supplier_code = prov
                self.gif_order_date = self.get_date(ordt)
                self.gif_init_date = self.get_date(indt)
                self.gif_cancel_date = self.get_date(cldt)

                self.gif_delivery_dir = del_dir.id
                self.gif_delivery_dir_code = del_dir.ref

                break
        
        # Se buscan las lineas de productos
        for mod,ped, dir,upc,e,f,g,qty,*_ in self.gif_content_file:

            if mod == "DD" and str(dir).isnumeric() and str(dir) == self.gif_delivery_dir_code:

                product, partner_details = self._check_product(upc)
                if not product:
                    continue

                order_line = {
                    'product_template_id': product.product_tmpl_id.id,
                    'product_uom_qty': float(qty),
                    'product_uom': partner_details.partner_uom.id,
                    'name':product.product_tmpl_id.description_sale,
                    'product_id':product.id,
                    'price_unit':partner_details.partner_price,
                }

                self.gif_sale_order_lines.append(order_line)
     
    def read_chedraui(self):
        """Función que recupera los datos del archivo con formato EDI para Chedraui."""
        
        order_pat = re.compile('BGM\+.*\+(\d{9})')
        date_order_pat = re.compile('DTM\+137:(\d{8}):.*')
        date_init_pat = re.compile('DTM\+2:(\d{8}):.*')
        date_cancel_pat = re.compile('DTM\+61:(\d{8}):.*')

        supplier_code_pat = re.compile('NAD\+BY\++(\d+)')
        delivery_code_pat = re.compile('NAD\+ST\+(\d+)')

        product_pat = re.compile('LIN\++(\d+):.*')
        qty_pat = re.compile('QTY\+21:(\d+)')
        price_pat = re.compile('MOA\+146:(\d+\.?\d*)')

        # split_by_order = re.compile('UNH.+')
        order,*_ = self.gif_content_file

        self.gif_order = order_pat.search(order).group(1)
        products = product_pat.findall(order)
        qtys = qty_pat.findall(order)
        prices = price_pat.findall(order)
        self.gif_order_date = self.get_date(date_order_pat.search(order).group(1))
        self.gif_init_date = self.get_date(date_init_pat.search(order).group(1))
        self.gif_cancel_date = self.get_date(date_cancel_pat.search(order).group(1))
        self.gif_supplier_code = supplier_code_pat.search(order).group(1)
        self.gif_delivery_dir_code = delivery_code_pat.search(order).group(1)

        # Direccion de entrega
        del_dir = self.env['res.partner'].search([('type','=','delivery'),('ref','=',self.gif_delivery_dir_code)])
        
        if not del_dir and str(self.gif_delivery_dir_code) not in self.delivery_address_not_found:
            self.delivery_address_not_found.append(self.gif_delivery_dir_code)
            raise ValidationError('No se encontró la dirección de entrega: '+ self.gif_delivery_dir_code)
        
        self.gif_delivery_dir = del_dir.id
        self.gif_delivery_dir_code = del_dir.ref

        # Lineas de productos
        for upc,qty,subtot in zip(products, qtys, prices):
            
            product, partner_details = self._check_product(upc)
            if not product:
                continue

            order_line = {
                'product_template_id': product.product_tmpl_id.id,
                'product_uom_qty': float(qty),
                'product_uom': partner_details.partner_uom.id,
                'name':product.product_tmpl_id.description_sale,
                'product_id':product.id,
                # 'price_unit':partner_details.partner_price,
                'price_subtotal': float(subtot),
            }
            order_line['price_unit'] = float(subtot) / order_line['product_uom_qty']

            self.gif_sale_order_lines.append(order_line)

    def read_heb(self):
        """Función que recupera los datos del archivo con formato para HEB"""
        #Encabezado
        for row in self.gif_content_file:
            
            if row[0] == 'Numero de Proveedor:':
                self.gif_supplier_code = row[1]
            
            elif row[0] == 'Facturar a:':
                # self.gif_delivery_dir_code = row[5]
                self.gif_order_date = self.get_date(row[7])
                
                # Direccion de entrega
                del_dir = self.env['res.partner'].search([('type','=','delivery'),('ref','=',str(row[5])),('parent_id','=',self.gif_customer.id)])
                
                if not del_dir and str(row[5]) not in self.delivery_address_not_found:
                    # self.delivery_address_not_found.append(str(row[5]))
                    raise ValidationError('No se encontró la dirección de entrega: '+ str(row[5]))

                self.gif_delivery_dir = del_dir.id
                self.gif_delivery_dir_code = del_dir.ref

            elif re.match('Direcci.n:', row[0]):
                self.gif_init_date = self.get_date(row[7])
            
            elif row[0] == 'Municipio:':
                self.gif_cancel_date = self.get_date(row[7])


        # Lineas de producto
        for ref,upc,desc,qty,*_,importe in self.gif_content_file:

            if str(ref).isnumeric() and str(upc).isnumeric():
                
                product, partner_details = self._check_product(upc)
                if not product:
                    continue

                order_line = {
                    'product_template_id': product.product_tmpl_id.id,
                    'product_uom_qty': float(qty),
                    'product_uom': partner_details.partner_uom.id,
                    'name':product.product_tmpl_id.description_sale,
                    'product_id':product.id,
                    # 'price_unit':partner_details.partner_price,
                }
                order_line['price_unit'] = float(importe) / order_line['product_uom_qty']

                self.gif_sale_order_lines.append(order_line)

    def read_generic_csv(self):
        """Función que recupera los datos de un archivo CSV genérico."""
        
        # Se busca el encabezado de la orden para recuperar fechas
        for mod, or_dt, in_dt, cl_dt,*_ in self.gif_content_file:
            
            if mod == "DE" and str(or_dt).isnumeric():
                self.gif_order_date = self.get_date(or_dt)
                self.gif_init_date = self.get_date(in_dt)
                self.gif_cancel_date = self.get_date(cl_dt)
                break
        
        # Se buscan las lineas de productos
        for mod,upc,qty,subt,*_ in self.gif_content_file:
            print(mod,upc,qty,subt,*_)
            if mod == "DD" and str(upc).isnumeric():# and str(dir) == self.gif_delivery_dir_code:
                
                product, partner_details = self._check_product(upc)
                if not product:
                    continue

                order_line = {
                    'product_template_id': product.product_tmpl_id.id,
                    'product_uom_qty': float(qty),
                    'product_uom': partner_details.partner_uom.id,
                    'name':product.product_tmpl_id.description_sale,
                    'product_id':product.id,
                    # 'price_subtotal':float(subt)
                    # 'price_unit':partner_details.partner_price,
                }
                order_line['price_unit'] = round(float(subt) / order_line['product_uom_qty'], 2)

                self.gif_sale_order_lines.append(order_line)

    def read_file(self):
        """Función que identifica el tipo de archivo y almacena su contenido en una lista."""
        for record in self:

            record.gif_content_file.clear()

            # Excel
            if '.xlsx' in record.name.lower():
                try:
                    wb = openpyxl.load_workbook(filename = BytesIO(base64.b64decode(record.orders_file)), read_only = True)
                    ws = wb.active
                    record.gif_content_file.extend([r for r in ws.iter_rows(values_only=True) if any(r)])
                except:
                    raise ValidationError('Error al abrir el archivo (xlsx).')

            # CSV
            elif '.csv' in record.name.lower():
                try:
                    file = csv.reader(StringIO(base64.b64decode(record.orders_file).decode(errors='ignore')))
                    record.gif_content_file.extend(file)
                except:
                    raise ValidationError('Error al abrir el archivo (csv).')
            
            # TXT
            elif '.txt' in record.name.lower():
                try:
                    file = base64.b64decode(record.orders_file).decode("utf-8")
                    # file_lines = file.split("\n")
                    record.gif_content_file.append(file)
                except:
                    raise ValidationError('Error al abrir el archivo (txt).')

            # Otro
            else:
                raise UserError('Tipo de archivo no admitido.')

    def preview_files(self):
        """Función que recupera la información para previsualización."""
        
        if self.gif_load_type == 'csv' and '.csv' not in self.name.lower():
            raise UserError("Seleccione un archivo con extensión CSV.")

        if self.gif_load_type == 'che' and '.txt' not in self.name.lower():
            raise UserError("Seleccione un archivo con extensión TXT.")

        self.read_file()
        
        self.gif_sale_order_lines.clear()

        try:
            if self.gif_load_type == 'sor':
                self.read_soriana()
            
            elif self.gif_load_type == 'frk':
                self.read_fresko()

            elif self.gif_load_type == 'che':
                self.read_chedraui()

            elif self.gif_load_type == 'heb':
                self.read_heb()

            elif self.gif_load_type == 'csv':
                self.read_generic_csv()

            if not all([
                self.gif_supplier_code,
                self.gif_order_date,
                self.gif_init_date,
                self.gif_cancel_date,
                self.gif_delivery_dir,
                self.gif_delivery_dir_code]):
                raise ValidationError("El archivo no contiene el formato indicado para este cliente.")

        except Exception as e:
            raise ValidationError(e)

        # Validacion de direccion de entrega        
        if self.delivery_address_not_found:
            dirs = ', '.join(set(self.delivery_address_not_found))
            raise ValidationError("No se encontró la dirección de entrega: "+dirs)
        
        # Validacion de existencia de productos
        if self.products_not_found:
            prods = ', '.join(set(self.products_not_found))
            raise ValidationError("No se encontraron los siguientes prouctos:\n"+prods)
        
        # Validacion de venta de productos al cliente
        if self.invalid_products:
            prods = ', '.join(set(self.invalid_products))
            raise ValidationError(f"El cliente {self.gif_customer.name} no se encuentra en la lista de socios de los siguientes productos:\n{prods}")

        self.gif_isValid = True

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.sales.orders.uploader',
            'view_mode': 'form',
            'res_id':self.id,
            'target': 'new',
            }

    def gif_create_orders(self):
        """Función que crea la orden de venta."""
        
        # Varifica que se haya leido el archivo.
        if not self.gif_isValid:
            self.preview_files()

        # Valores de la orden
        vals = {
            'partner_id': self.gif_customer.id,
            'gif_partner_code': self.gif_customer_code,
            'gif_supplier_code':self.gif_supplier_code,
            'origin':self.gif_order,
            'validity_date':self.gif_cancel_date,
            'gif_init_date':self.gif_init_date,
            # 'date_order': self.gif_order_date,#.astimezone(timezone(self.env.user.tz)),
            'date_order': self.with_user_timezone(self.gif_order_date),
            'tipificacion_venta':self.gif_tfv.id,
            'tag_ids':[(4,self.gif_tag.id)],
            'warehouse_id': self.gif_customer.gif_default_warehouse.id,
            'partner_shipping_id':self.gif_delivery_dir.id,
            'gif_partner_shipping_code':self.gif_delivery_dir_code,
        }
        so = self.env['sale.order'].create(vals)
        
        # Se crean las lineas de orden
        for line_vals in self.gif_sale_order_lines:
            so.order_line = [(0,0,line_vals)]

    def with_user_timezone(self, date_time):
        """Funcion que recibe una fecha (obj. date o datetime) y devuelve un datetime con la diferencia de zona horaria del usuario aplicada.
            params:
                date_time - Date o datetime en tiempo UTC

                return - Datetime con diferencia de zona horaria
        """
        # Convertimos a datetime
        dttm = fields.Datetime.to_datetime(date_time)
        # Obtenemos la diferencia de horas
        hrs_dif = str(dttm.astimezone(timezone(self.env.user.tz))).split('-')[-1].split(':')[0]
        delta = timedelta(hours=int(hrs_dif))
        return dttm + delta

    def get_date(self, sdate):
        """Funcion que transforma una cadena de texto, que representa una fecha en cualquier formato, a un objeto tipo fecha.
        
            params:
                sdate - Cadena de texto que representa una fecha
            
            return:
                date - Objeto tipo fecha
        """
        pattern1 = '(\d{4})\D?(\d{2})\D?(\d{2})' # ISO (aaaa)(mm)(dd)
        pattern2 = '(\d{2})\D?(\d{2})\D?(\d{4})' # Comun (dd)(mm)(aaaa)
        
        try:
            try:
                a,m,d = re.search(pattern1, str(sdate)).groups()
                if int(m) > 12:
                    raise ValidationError("Modelo de fecha incorrecto")
                    # d,m,a = re.search(pattern2, sdate).groups()
            except:
                d,m,a = re.search(pattern2, str(sdate)).groups()
        except:
            raise ValidationErr("No se pudo leer la fecha: "+ str(sdate))

        try:
            date = dt.strptime('/'.join([d,m,a]), '%d/%m/%Y')
            return date
        except:
            raise ValidationErr("No se pudo leer la fecha: "+ str(sdate))
