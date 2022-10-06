from odoo import api,fields,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tipificacion_compra = fields.Many2one(comodel_name='gif.tipificaciones.compras', string='Tipo de Compra', required=True)
    change = fields.Boolean(default=False,compute="_calculate")
    amount_tax_show = fields.Monetary(string='Taxes', compute='_amount_all_show')
    amount_untaxed_show = fields.Monetary(string='Untaxed Amount', compute='_amount_all_show')
    amount_total_show = fields.Monetary(string='Total', compute='_amount_all_show')
    is_office = fields.Boolean(compute='_is_office')
    is_primary = fields.Boolean(compute='_is_primary')
    is_ben_dis = fields.Boolean(compute='_is_ben_dis')
    is_insume = fields.Boolean(compute='_is_insume')
    is_associated = fields.Boolean(compute='_is_associated')
    suma = fields.Integer(default=0,compute="_is_show")

    @api.depends('change')
    def _calculate(self):
        if self.change == False:
            self.change = True

    @api.onchange('change')
    def _is_office(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos de Oficina':
                record.is_office = True
            else:
                record.is_office = False
    
    @api.onchange('change')
    def _is_primary(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos Primarios':
                record.is_primary = True
            else:
                record.is_primary = False

    @api.onchange('change')
    def _is_ben_dis(self):
        for record in self:
            if record.tipificacion_compra.name == 'Descuentos y Beneficios':
                record.is_ben_dis = True
            else:
                record.is_ben_dis = False
    
    @api.onchange('change')
    def _is_associated(self):
        for record in self:
            if record.tipificacion_compra.name == 'Gastos Asociados':
                record.is_associated = True
            else:
                record.is_associated = False

    @api.onchange('change')
    def _is_insume(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos Insumos':
                record.is_insume = True
            else:
                record.is_insume = False
    
    

    @api.onchange('change')
    def _is_show(self):
        for record in self:
            record.suma = 0
            x = 0
            user_group = []
            add_user = self.env.uid
            groups_i = self.env['res.groups'].search([('name','ilike','Transacciones Egreso')])
            for grupo in groups_i:
                if add_user in grupo.users.ids:
                    user_group.append(grupo.name)
            for user in user_group:
                if x == 0:
                    if 'Transacciones Egreso Productos Primarios' in user:
                        if 'Validador Transacciones Egreso Productos Primarios' in user:
                            pass
                        else:
                            record.suma = record.suma + 1
                    elif 'Transacciones Egreso Productos de Oficina' in user:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user:
                            pass
                        else:
                            record.suma = record.suma + 2
                    elif 'Transacciones Egreso Descuentos y Beneficios' in user:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user:
                            pass
                        else:
                            record.suma = record.suma + 4
                    elif 'Transacciones Egreso Productos Insumos' in user:
                        if 'Validador Transacciones Egreso Productos Insumos' in user:
                            pass
                        else:
                            record.suma = record.suma + 8
                    elif 'Transacciones Egreso Gastos Asociados' in user:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user:
                            pass
                        else:
                            record.suma = record.suma + 16
            x = 1

    @api.depends('order_line.price_total')
    def _amount_all_show(self):
        for order in self:
            amount_untaxed_show = amount_tax_show = 0.0
            if order.suma == 31:
                for line in order.order_line:
                    line._compute_amount()
                    amount_untaxed_show += line.price_subtotal
                    amount_tax_show += line.price_tax
            elif order.suma == 1:
                for line in order.order_line:
                    if order.is_primary:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
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
            elif order.suma == 8:
                for line in order.order_line:
                    if order.is_insume:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 16:
                for line in order.order_line:
                    if order.is_associated:
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
            elif order.suma == 9:
                for line in order.order_line:
                    if order.is_primary or order.is_insume:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 17:
                for line in order.order_line:
                    if order.is_primary or order.is_associated:
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
            elif order.suma == 10:
                for line in order.order_line:
                    if order.is_insume or order.is_office:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 24:
                for line in order.order_line:
                    if order.is_insume or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 12:
                for line in order.order_line:
                    if order.is_insume or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 18:
                for line in order.order_line:
                    if order.is_office or order.is_associated:
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
            elif order.suma == 20:
                for line in order.order_line:
                    if order.is_associated or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 11:
                for line in order.order_line:
                    if order.is_primary or order.is_insume or order.is_office:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 25:
                for line in order.order_line:
                    if order.is_primary or order.is_insume or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 13:
                for line in order.order_line:
                    if order.is_primary or order.is_insume or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 19:
                for line in order.order_line:
                    if order.is_primary or order.is_office or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 7:
                for line in order.order_line:
                    if order.is_primary or order.is_office or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 21:
                for line in order.order_line:
                    if order.is_primary or order.is_ben_dis or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 26:
                for line in order.order_line:
                    if order.is_insume or order.is_office or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 14:
                for line in order.order_line:
                    if order.is_insume or order.is_office or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 22:
                for line in order.order_line:
                    if order.is_ben_dis or order.is_office or order.is_associated:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 15:
                for line in order.order_line:
                    if order.is_primary or order.is_insume or order.is_office or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 23:
                for line in order.order_line:
                    if order.is_primary or order.is_associated or order.is_office or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 27:
                for line in order.order_line:
                    if order.is_associated or order.is_insume or order.is_office or order.is_primary:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 28:
                for line in order.order_line:
                    if order.is_associated or order.is_insume or order.is_ben_dis:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 29:
                for line in order.order_line:
                    if order.is_associated or order.is_insume or order.is_ben_dis or order.is_primary:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 30:
                for line in order.order_line:
                    if order.is_associated or order.is_insume or order.is_ben_dis or order.is_office:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.suma == 31:
                for line in order.order_line:
                    if order.is_associated or order.is_insume or order.is_ben_dis or order.is_office or order.is_primary:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id
            order.update({
                'amount_untaxed_show': currency.round(amount_untaxed_show),
                'amount_tax_show': currency.round(amount_tax_show),
                'amount_total_show': amount_untaxed_show + amount_tax_show,
            })
    
#Insumos: is_insume |Primarios: is_primary |Oficina: is_office |DesBen: is_ben_dis |Gastos: is_associated
    @api.onchange('partner_id')
    def onchange_type_product(self):
        for record in self:
            res_v = {}
            add_user = record.user_id
            grupo = self.env['res.groups'].search([('users','=',add_user.id)])
            tipi_compras_id =[]
            for g in grupo:
                if(g.name == 'Transacciones Egreso Productos de Oficina'):
                    tipi_compras_id.append(3)
                elif(g.name == 'Transacciones Egreso Gastos Asociados'):
                    tipi_compras_id.append(4)
                elif(g.name == 'Transacciones Egreso Productos Insumos'):
                    tipi_compras_id.append(2)
                elif(g.name == 'Transacciones Egreso Productos Primarios'):
                    tipi_compras_id.append(1)
                elif(g.name == 'Transacciones Egreso Descuentos y Beneficios'):
                    tipi_compras_id.append(5)
            res_v['domain'] = {'tipificacion_compra': [('id', 'in', tipi_compras_id)]}
            size = len(tipi_compras_id)
            if size == 1:
                record.tipificacion_compra = tipi_compras_id[0]
            return res_v

    @api.onchange('tipificacion_compra')
    def onchange_reset_orderline(self):
        for record in self:
            record.order_line = None
            
            
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty')
    def onchange_type_product(self):
        for record in self:
            res = {}
            temp = record.order_id.tipificacion_compra.id
            res['domain'] = {'product_template_id': [('product_type_purchase', '=', str(temp))]}
            return res