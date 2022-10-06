from odoo import api,fields,models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tipificacion_venta = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', required=True, store=True)
    change = fields.Boolean(default=False,compute="_calculate")
    amount_tax_show = fields.Monetary(string='Taxes', compute='_amount_all_show')
    amount_untaxed_show = fields.Monetary(string='Untaxed Amount', compute='_amount_all_show')
    groups_i = fields.Many2many(related='user_id.groups_id', string='String')
    amount_total_show = fields.Monetary(string='Total', compute='_amount_all_show')
    is_office = fields.Boolean(compute='_is_office')
    is_primary = fields.Boolean(compute='_is_primary')
    is_ben_dis = fields.Boolean(compute='_is_ben_dis')
    suma = fields.Integer(default=0,compute="_is_show")


    @api.onchange('change')
    def _is_office(self):
        for record in self:
            if record.tipificacion_venta.name == 'Productos de Oficina':
                record.is_office = True
            else:
                record.is_office = False
    
    @api.onchange('change')
    def _is_primary(self):
        for record in self:
            if record.tipificacion_venta.name == 'Productos Primarios':
                record.is_primary = True
            else:
                record.is_primary = False

    @api.onchange('change')
    def _is_ben_dis(self):
        for record in self:
            if record.tipificacion_venta.name == 'Descuentos y Beneficios':
                record.is_ben_dis = True
            else:
                record.is_ben_dis = False

    @api.depends('change')
    def _calculate(self):
        if self.change == False:
            self.change = True
            

    @api.onchange('change')
    def _is_show(self):
        for record in self:
            record.suma = 0
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
                            record.suma = record.suma + 1
                    elif 'Transacciones Ingreso Productos de Oficina' in user:
                        if 'Validador Transacciones Ingreso Productos de Oficina' in user:
                            pass
                        else:
                            record.suma = record.suma + 2
                    elif 'Transacciones Ingreso Descuentos y Beneficios' in user:
                        if 'Validador Transacciones Ingreso Descuentos y Beneficios' in user:
                            pass
                        else:
                            record.suma = record.suma + 4
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

    @api.onchange('tipificacion_venta')
    def onchange_reset_orderline(self):
        for record in self:
            record.order_line = None

    @api.onchange('change')
    @api.depends('order_line.price_total')
    def _amount_all_show(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed_show = amount_tax_show = 0.0
            if order.suma == 7:
                for line in order.order_line:
                    if order.is_primary or order.is_office or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 1:
                for line in order.order_line:
                    if order.is_primary:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                        break
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 2:
                for line in order.order_line:
                    if order.is_office:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 4:
                for line in order.order_line:
                    if order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0     
            elif order.suma == 3:
                for line in order.order_line:
                    if order.is_primary or order.is_office:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 5:
                for line in order.order_line:
                    if order.is_primary or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0 
            elif order.suma == 6:
                for line in order.order_line:
                    if order.is_office or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0       
            order.update({
                'amount_untaxed_show': amount_untaxed_show,
                'amount_tax_show': amount_tax_show,
                'amount_total_show': amount_untaxed_show + amount_tax_show,
            })
            

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty')
    def onchange_type_product(self):
        for record in self:
            res = {}
            temp = record.order_id.tipificacion_venta.id
            res['domain'] = {'product_template_id': [('product_type_sale', '=', str(temp))]}
            return res


    
    