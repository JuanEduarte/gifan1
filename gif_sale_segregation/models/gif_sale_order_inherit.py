from odoo import api,fields,models


class SaleOrderSS(models.Model):
    _inherit = 'sale.order'

    tipificacion_venta = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', required=True, store=True)
    change = fields.Boolean(default=False,compute="_calculate")
    is_office_sale = fields.Boolean(compute='_is_office_sale')
    is_primary_sale = fields.Boolean(compute='_is_primary_sale')
    is_ben_dis_sale = fields.Boolean(compute='_is_ben_dis_sale')
    sum_sale_order = fields.Integer(default=0,compute="_is_show")


    @api.onchange('change')
    def _is_office_sale(self):
        for record in self:
            if record.tipificacion_venta.name == 'Productos de Oficina':
                record.is_office_sale = True
            else:
                record.is_office_sale = False
    
    @api.onchange('change')
    def _is_primary_sale(self):
        for record in self:
            if record.tipificacion_venta.name == 'Productos Primarios':
                record.is_primary_sale = True
            else:
                record.is_primary_sale = False

    @api.onchange('change')
    def _is_ben_dis_sale(self):
        for record in self:
            if record.tipificacion_venta.name == 'Descuentos y Beneficios':
                record.is_ben_dis_sale = True
            else:
                record.is_ben_dis_sale = False

    @api.depends('change')
    def _calculate(self):
        if self.change == False:
            self.change = True
            

    @api.onchange('change')
    def _is_show(self):
        for record in self:
            record.sum_sale_order = 0
            x = 0
            user_group = []
            add_user = self.env.uid
            groups_i = self.env['res.groups'].search([('name','ilike','Transacciones Ingreso')])
            for grupo in groups_i:
                if add_user in grupo.users.ids:
                    user_group.append(grupo.name)
            for user in user_group:
                if x == 0:
                    if 'Transacciones Ingreso Productos Primarios' in user:
                        if 'Validador Transacciones Ingreso Productos Primarios' in user:
                            pass
                        else:
                            record.sum_sale_order = record.sum_sale_order + 1
                    elif 'Transacciones Ingreso Productos de Oficina' in user:
                        if 'Validador Transacciones Ingreso Productos de Oficina' in user:
                            pass
                        else:
                            record.sum_sale_order = record.sum_sale_order + 2
                    elif 'Transacciones Ingreso Descuentos y Beneficios' in user:
                        if 'Validador Transacciones Ingreso Descuentos y Beneficios' in user:
                            pass
                        else:
                            record.sum_sale_order = record.sum_sale_order + 4
            x = 1
                    

    @api.onchange('partner_id')
    def onchange_type_sale(self):
        for record in self:
            res_v = {}
            add_user = record.user_id
            grupo = self.env['res.groups'].search([('users','=',add_user.id)])
            tipi_ventas_id =[]
            for g in grupo:
                if(g.name == 'Transacciones Ingreso Productos Primarios'):
                    tipi_ventas_id.append(1)
                elif(g.name == 'Transacciones Ingreso Productos de Oficina'):
                    tipi_ventas_id.append(2)
                elif(g.name == 'Transacciones Ingreso Descuentos y Beneficios'):
                    tipi_ventas_id.append(3)
            res_v['domain'] = {'tipificacion_venta': [('id', 'in', tipi_ventas_id)]}
            size = len(tipi_ventas_id)
            if size == 1:
                record.tipificacion_venta = tipi_ventas_id[0]
            return res_v

    @api.onchange('tipificacion_venta','partner_id')
    def onchange_reset_orderline(self):
        for record in self:
            try:
                record.order_line = None
            except:
                pass


class SaleOrderLineSS(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty')
    def onchange_type_product(self):
        for record in self:
            res = {}
            temp = record.order_id.tipificacion_venta.id
            res['domain'] = {'product_template_id': [('product_type_sale', '=', str(temp))]}
            return res


    
    