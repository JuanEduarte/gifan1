from odoo import models, fields
import re
from odoo.exceptions import ValidationError


class GifDiarySalesReport(models.Model):
    _name = 'gif.diary.sales.report'
    _inherit = 'gif.base.report'
    _order = 'id desc'

    name = fields.Char(default="Reporte de Ventas Diario", readonly=True, store=True)
    lines = fields.Many2many('gif.sale.analisys', store=True)

    # Entradas

    search_type = fields.Selection([('1','Cliente'),('2','Producto')], string="Consultar por:", default = '1')

    init_time = fields.Datetime(string="Fecha de inicio")
    final_time = fields.Datetime(string="Fecha de fin")

    init_range = fields.Char(string="Nombre / Desde")
    final_range = fields.Char(string="Hasta")

    def valid_inputs(self):
        for record in self:

            # Fecha
            if record.init_time > record.final_time:
                raise ValidationError("La fecha de inicio debe ser menor a la fecha de finalización.")

            # Todos
            if not record.init_range:
                #print("Todos los clientes")
                return 1
            
            # Rango
            elif record.init_range and record.final_range:
                init_match = re.match('[A-Z]{1}\*$', record.init_range, re.I)
                final_match = re.match('[A-Z]{1}\*$', record.final_range, re.I)

                if init_match and final_match:
                    #print("Busqueda por rangos")
                    return 2

                else:
                    #print("Rango incorrecto")
                    raise ValidationError("Rango incorrecto")

            elif record.init_range and not record.final_range:
                init_match = re.match('[\w]+\*$', record.init_range, re.I)
                
                # Patron
                if init_match:
                    #print("Busqueda por patron")
                    return 4
                
                # Nombre
                else:
                    #print("Busqueda por nombre")
                    return 3



    def get_customers(self):
        for record in self:
            
            search_range = self.valid_inputs()

            # Todos
            if search_range == 1:
                customers = self.env['res.partner'].search([("customer_rank", ">", 0)])
                return customers

            # Rango
            elif search_range == 2:
                i = str(record.init_range)[0]
                f = str(record.final_range)[0]
                pattern = f"^[{i}-{f}].*"
                customers = self.env['res.partner'].search([("customer_rank", ">", 0)])
                customers = customers.filtered(lambda c: re.match(pattern, c.name, re.I))
                return customers

            # Nombre
            elif search_range == 3:
                customer = self.env['res.partner'].search([("customer_rank", ">", 0),('name','ilike',record.init_range)])
                return customer

            # Patrón
            elif search_range == 4:
                init = str(record.init_range).replace('*','.*')
                pattern = f"^{init}"
                customers = self.env['res.partner'].search([("customer_rank", ">", 0)])
                customers = customers.filtered(lambda c: re.match(pattern, c.name, re.I))
                return customers
                
            else:
                #print("Algo malo paso")
                return False
    
    def get_products(self):
        for record in self:
            
            search_range = self.valid_inputs()

            # Todos los productos
            if search_range == 1:
                products = self.env['product.product'].search([])
                return products
            
            # Rango
            elif search_range == 2:
                i = str(record.init_range)[0]
                f = str(record.final_range)[0]
                pattern = f"^[{i}-{f}].*"
                products = self.env['product.product'].search([])
                products = products.filtered(lambda c: re.match(pattern, c.name, re.I))
                return products

            # Nombre
            elif search_range == 3:
                product = self.env['product.product'].search([('name','ilike',record.init_range)])
                return product

            # Patrón
            elif search_range == 4:
                init = str(record.init_range).replace('*','.*')
                pattern = f"^{init}"
                products = self.env['res.partner'].search([])
                products = products.filtered(lambda c: re.match(pattern, c.name, re.I))
                return products
                
            else:
                #print("Algo malo paso")
                return False


    def compute_lines(self):
        for record in self:
            
            # Por cliente
            if record.search_type == '1':
                for customer in self.get_customers():
                    print(customer.name)
                    vals = {}

                    vals['gif_customer'] = customer.id
                    
                    # goals = self.env['gif.goals'].search([('gif_customer','like', customer.name)])

                    # for goal in goals:
                    #     vals['gif_brand'] = goal.gif_brand
                    #     vals['gif_goal'] = goal.gif_goal
                        
                    record.lines = [(0,0,vals)]
            
            # Por producto
            elif record.search_type == '2':
                for product in self.get_products():
                    print(product)
                    record.lines = [(0,0,{'gif_product':product.id})]


