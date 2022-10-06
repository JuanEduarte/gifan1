from odoo import api,fields,models

class PurchaseOrderPS(models.Model):
    _inherit = 'purchase.order'

    tipificacion_compra = fields.Many2one(comodel_name='gif.tipificaciones.compras', string='Tipo de Compra')
    change = fields.Boolean(default=False,compute="_calculate")
    is_office_purchase = fields.Boolean(compute='_is_office_purchase')
    is_primary_purchase = fields.Boolean(compute='_is_primary_purchase')
    is_ben_dis_purchase = fields.Boolean(compute='_is_ben_dis_purchase')
    is_discount_purchase = fields.Boolean(compute='_is_ben_dis_purchase')
    is_insume_purchase = fields.Boolean(compute='_is_insume_purchase')
    is_associated_purchase = fields.Boolean(compute='_is_associated_purchase')
    sum_purchase_order = fields.Integer(default=0,compute="_is_show")

    @api.depends('change')
    def _calculate(self):
        if self.change == False:
            self.change = True

    @api.onchange('change')
    def _is_office_purchase(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos de Oficina':
                record.is_office_purchase = True
            else:
                record.is_office_purchase = False
    
    @api.onchange('change')
    def _is_primary_purchase(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos Primarios':
                record.is_primary_purchase = True
            else:
                record.is_primary_purchase = False

    @api.onchange('change')
    def _is_ben_dis_purchase(self):
        for record in self:
            if record.tipificacion_compra.name == 'Descuentos y Beneficios':
                record.is_ben_dis_purchase = True
                record.is_discount_purchase = True
                
            else:
                record.is_ben_dis_purchase = False
                record.is_discount_purchase = False
    
    @api.onchange('change')
    def _is_associated_purchase(self):
        for record in self:
            if record.tipificacion_compra.name == 'Gastos Asociados':
                record.is_associated_purchase = True
            else:
                record.is_associated_purchase = False

    @api.onchange('change')
    def _is_insume_purchase(self):
        for record in self:
            if record.tipificacion_compra.name == 'Productos Insumos':
                record.is_insume_purchase = True
            else:
                record.is_insume_purchase = False
    
    

    @api.onchange('change')
    def _is_show(self):
        for record in self:
            record.sum_purchase_order = 0
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
                            record.sum_purchase_order = record.sum_purchase_order + 1
                    elif 'Transacciones Egreso Productos de Oficina' in user:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user:
                            pass
                        else:
                            record.sum_purchase_order = record.sum_purchase_order + 4
                    elif 'Transacciones Egreso Descuentos y Beneficios' in user:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user:
                            pass
                        else:
                            record.sum_purchase_order = record.sum_purchase_order + 16
                    elif 'Transacciones Egreso Productos Insumos' in user:
                        if 'Validador Transacciones Egreso Productos Insumos' in user:
                            pass
                        else:
                            record.sum_purchase_order = record.sum_purchase_order + 2
                    elif 'Transacciones Egreso Gastos Asociados' in user:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user:
                            pass
                        else:
                            record.sum_purchase_order = record.sum_purchase_order + 8
            x = 1
    
#Insumos: is_insume_purchase |Primarios: is_primary_purchase |Oficina: is_office_purchase |DesBen: is_ben_dis_purchase |Gastos: is_associated_purchase
    @api.onchange('partner_id')
    def onchange_type_product(self):
        self.tipificacion_compra = None
        self.requisition_id = None
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

    @api.onchange('tipificacion_compra','partner_id')
    def onchange_reset_orderline(self):
        for record in self:
            if(record.requisition_id):
                pass
            else:
                try:
                    record.order_line = None
                except:
                    pass
            
            
class PurchaseOrderLinePS(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty')
    def onchange_type_product(self):
        for record in self:
            res = {}
            temp = record.order_id.tipificacion_compra.id
            res['domain'] = {'product_template_id': [('product_type_purchase', '=', str(temp))]}
            return res
 