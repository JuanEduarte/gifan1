from odoo import models, fields
import re


class GifDiarySalesReport(models.Model):
    _name = 'gif.diary.sales.report'
    _inherit = 'gif.base.report'
    _order = 'id desc'

    name = fields.Char(default="Reporte de Ventas Diario", readonly=True, store=True)
    lines = fields.One2many('gif.line.diary.sales', 'report_id', store=True)

    # Entradas

    search_type = fields.Selection([('1','Cliente'),('2','Producto')], string="Consultar por:", default = '1')

    init_time = fields.Datetime(string="Fecha de inicio")
    final_time = fields.Datetime(string="Fecha de fin")

    init_range = fields.Char(string="Nombre / Desde")
    final_range = fields.Char(string="Hasta")

    def valid_inputs(self):
        for record in self:

            if not record.init_range:   #Vacío
                print("Todos los clientes")
                return 1

            elif record.init_range and record.final_range: # Rango
                init_match = re.match('[A-Z]{1}\*$', record.init_range, re.I)
                final_match = re.match('[A-Z]{1}\*$', record.final_range, re.I)

                if init_match and final_match:
                    print("Busqueda por rangos")
                    return 2

                else:
                    print("Rango incorrecto")
            
            else:   # Nombre
                print("Busqueda por nombre")
                return 3



    def get_customers(self):
        for record in self:
            
            search_range = self.valid_inputs()

            if search_range == 1:
                customers = self.env['res.partner'].search([("customer_rank", ">", 0)])
                return customers

            elif search_range == 2:
                i = str(record.init_range)[0]
                f = str(record.final_range)[0]
                pattern = f"^[{i}|{f}].*"
                customers = self.env['res.partner'].search([("customer_rank", ">", 0)])
                customers = [customer for customer in customers if re.match(pattern, customer.name, re.I)]
                return customers

            elif search_range == 3:
                customer = self.env['res.partner'].search([("customer_rank", ">", 0),('name','ilike',record.init_range)])
                return customer
                
            else:
                print("Algo malo paso")
                return False


    def compute_lines(self):
        for record in self:    
            for customer in self.get_customers():
                print(customer.name)
                vals = {}

                vals['gif_customer'] = customer.id
                
                goals = self.env['gif.goals'].search([('gif_customer','like', customer.name)])

                # for goal in goals:
                #     vals['gif_brand'] = goal.gif_brand
                #     vals['gif_goal'] = goal.gif_goal
                    
                record.lines = [(0,0,vals)]
            


class GifLineDiarySales(models.Model):
    _name = 'gif.line.diary.sales'

    report_id = fields.Many2one('gif.diary.sales.report', store=True)

    gif_customer = fields.Many2one('res.partner', string="Cliente", readonly=True)
    gif_supplier = fields.Char(string="Proveedor", readonly=True)
    gif_brand = fields.Char(string="Marca", readonly=True)
    gif_goal = fields.Float(string="Float", readonly=True)
    gif_smpy = fields.Float(string="SMPY", readonly=True)
    gif_smpy_meta = fields.Float(string="SMPY/META", readonly=True)
    gif_total_fact = fields.Float(string="TOTAL FACT", readonly=True)
    gif_total_canc = fields.Float(string="TOTAL CANC", readonly=True)
    gif_total_dev = fields.Float(string="TOTAL DEV", readonly=True)
    gif_total_desc = fields.Float(string="TOTAL DESC", readonly=True)
    gif_shtd = fields.Float(string="SHTD", readonly=True)
    gif_openord = fields.Float(string="OPENORD", readonly=True)
    gif_pps = fields.Float(string="PPS", readonly=True)
    gif_shtd_openord = fields.Float(string="SHTD + OPENORD", readonly=True)
    gif_pmonth = fields.Float(string="PMONTH", readonly=True)
    gif_p3month = fields.Float(string="P3MONTH", readonly=True)
    gif_p6month = fields.Float(string="P6MONTH", readonly=True)
    gif_p12month = fields.Float(string="P12MONTH", readonly=True)




