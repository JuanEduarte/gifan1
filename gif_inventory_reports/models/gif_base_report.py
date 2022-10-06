from odoo import api, fields, models
import datetime as dt
#from datetime import datetime

class GifBaseReport(models.Model):
    _name = 'gif.base.report'
    _description = 'Basic header for reports.'

    
    def _default_code_time(self):
        """Función para calcular el código de tiempo."""
        code_time = (dt.datetime.now() - dt.timedelta(hours=5)).strftime('%Y%m%d_%H%M%S')
        return code_time


    def _default_active_company(self):
        """Función que recupera el nombre de la compañia activa."""
        company_id = self.env.company.id
        return self.env['res.company'].search([('id','=', company_id)])

    def _default_date(self):
        return dt.datetime.now()

  # Encabezado    
    code_time    = fields.Char(store=True, default=_default_code_time)
    name         = fields.Char(default="New",string="Reporte", readonly=True, store=True, compute='_compute_name_report')
    company_name = fields.Many2one('res.company', string="Compañía", readonly=True, store=True, default = _default_active_company)
    date         = fields.Date(string="Fecha", readonly=True, store=True, default =_default_date)
    # datetime     = fields.Datetime(string="Fecha y hora", readonly=True, store=True, default = lambda d : dt.datetime.now())
    # date         = fields.Date(string="Fecha", readonly=True, store=True, default = dt.datetime.now())
    title        = fields.Char(string="Titulo")

    @api.depends('code_time')
    def _compute_name_report(self):
        """Función para computar el nombre del reporte con base en el código de tiempo."""
        for record in self:
            # record.name = "Reporte de Inventario " + str(record.code_time)
            print("Create date: ",record.create_date)
            # record.name = "Reporte de Inventario " + record.code_time
            record.name = f'{record.title} {record.code_time}'


    # def get_reserved_qty(self, product):
    #     """Función para calcular la cantidad reservada por lotes de un producto."""
    #     for record in self:
    #         reserved_qty = {}
    #         for sale in self.env['sale.order'].search([('state','like','done')]):
                
    #             stock_picking = self.env['stock.picking'].search([('origin','like',sale.name),('state','like','assigned')])
    #             if not stock_picking:
    #                 continue

    #             for picking in stock_picking:
    #                 #moves = [move for move in picking.move_lines if move.product_id.id == product.id and move.forecast_availability ]

    #                 moves = self.env['stock.move'].search(
    #                     [('picking_id','=',picking.id),('product_id','=',product.id),('forecast_availability','>','0')])

    #                 for line in moves.move_line_ids:
    #                 # for line in moves:
    #                     reserved_qty[line.lot_id.name] = reserved_qty.get(line.lot_id.name,0) + line.product_uom_qty
    #         # print(reserved_qty)
    #         return reserved_qty


    def get_reserved_qty(self, product):
        """Función para calcular la cantidad reservada por lotes de un producto."""
        for record in self:
            reserved_qty = {}

            # Movimientos cuyo producto sea el que buscamos y el estado de su picking sea "Listo"
            moves = self.env['stock.move'].search([('product_id','=',product.id),('picking_id.state','like','assigned')])
            
            # Movimientos que tienen una cantidad reservada
            moves_lst = [move for move in moves if move.forecast_availability]

            for move in moves_lst:
                order_sale = self.env['sale.order'].search([('state','like','done'),('name','like',move.picking_id.origin)])
                
                # Confirmación de factura
                if order_sale:
                    for line in move.move_line_ids:
                        reserved_qty[line.lot_id.name] = reserved_qty.get(line.lot_id.name,0) + line.product_uom_qty

            return reserved_qty