from odoo import models,api,fields


class PurchaseRequistionPs(models.Model):
    _inherit = 'purchase.requisition'

    tipificacion_requisition = fields.Many2one(comodel_name='gif.tipificaciones.compras', string='Tipo de Compra')
    change = fields.Boolean(default=False,compute="_calculate")
    is_office_requisition = fields.Boolean(compute='_is_office_requisition')
    is_primary_requisition = fields.Boolean(compute='_is_primary_requisition')
    is_ben_dis_requisition = fields.Boolean(compute='_is_ben_dis_requisition')
    is_discount_requisition = fields.Boolean(compute='_is_ben_dis_requisition')
    is_insume_requisition = fields.Boolean(compute='_is_insume_requisition')
    is_associated_requisition = fields.Boolean(compute='_is_associated_requisition')
    sum_requisition_order = fields.Integer(default=0,compute="_is_show")

    @api.depends('change')
    def _calculate(self):
        if self.change == False:
            self.change = True

    def _is_office_requisition(self):
        for record in self:
            if record.tipificacion_requisition.name == 'Productos de Oficina':
                record.is_office_requisition = True
            else:
                record.is_office_requisition = False

    def _is_primary_requisition(self):
        for record in self:
            if record.tipificacion_requisition.name == 'Productos Primarios':
                record.is_primary_requisition = True
            else:
                record.is_primary_requisition = False
    def _is_ben_dis_requisition(self):
        for record in self:
            if record.tipificacion_requisition.name == 'Descuentos y Beneficios':
                record.is_ben_dis_requisition = True
                record.is_discount_requisition = True
                
            else:
                record.is_ben_dis_requisition = False
                record.is_discount_requisition = False

    def _is_associated_requisition(self):
        for record in self:
            if record.tipificacion_requisition.name == 'Gastos Asociados':
                record.is_associated_requisition = True
            else:
                record.is_associated_requisition = False
    def _is_insume_requisition(self):
        for record in self:
            if record.tipificacion_requisition.name == 'Productos Insumos':
                record.is_insume_requisition = True
            else:
                record.is_insume_requisition = False
    
    

    @api.onchange('change')
    def _is_show(self):
        for record in self:
            record.sum_requisition_order = 0
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
                            record.sum_requisition_order = record.sum_requisition_order + 1
                    elif 'Transacciones Egreso Productos de Oficina' in user:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user:
                            pass
                        else:
                            record.sum_requisition_order = record.sum_requisition_order + 4
                    elif 'Transacciones Egreso Descuentos y Beneficios' in user:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user:
                            pass
                        else:
                            record.sum_requisition_order = record.sum_requisition_order + 16
                    elif 'Transacciones Egreso Productos Insumos' in user:
                        if 'Validador Transacciones Egreso Productos Insumos' in user:
                            pass
                        else:
                            record.sum_requisition_order = record.sum_requisition_order + 2
                    elif 'Transacciones Egreso Gastos Asociados' in user:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user:
                            pass
                        else:
                            record.sum_requisition_order = record.sum_requisition_order + 8
            x = 1
    
#Insumos: is_insume_requisition |Primarios: is_primary_requisition |Oficina: is_office_requisition |DesBen: is_ben_dis_requisition |Gastos: is_associated_requisition
    @api.onchange('vendor_id')
    def onchange_type_product(self):
        for record in self:
            res_v = {}
            add_user = record.user_id
            grupo = self.env['res.groups'].search([('users','=',add_user.id)])
            tipi_requisitions_id =[]
            for g in grupo:
                if(g.name == 'Transacciones Egreso Productos de Oficina'):
                    tipi_requisitions_id.append(3)
                elif(g.name == 'Transacciones Egreso Gastos Asociados'):
                    tipi_requisitions_id.append(4)
                elif(g.name == 'Transacciones Egreso Productos Insumos'):
                    tipi_requisitions_id.append(2)
                elif(g.name == 'Transacciones Egreso Productos Primarios'):
                    tipi_requisitions_id.append(1)
                elif(g.name == 'Transacciones Egreso Descuentos y Beneficios'):
                    tipi_requisitions_id.append(5)
            res_v['domain'] = {'tipificacion_requisition': [('id', 'in', tipi_requisitions_id)]}
            size = len(tipi_requisitions_id)
            if size == 1:
                record.tipificacion_requisition = tipi_requisitions_id[0]
            return res_v

    @api.onchange('tipificacion_requisition','vendor_id')
    def onchange_reset_orderline(self):
        for record in self:
            try:
                record.order_line = None
            except:
                pass

class PurchaseOrderLinePS(models.Model):
    _inherit = 'purchase.requisition.line'

    @api.onchange('product_qty')
    def onchange_type_product(self):
        for record in self:
            res = {}
            temp = record.requisition_id.tipificacion_requisition.id
            res['domain'] = {'product_id': [('product_type_purchase', '=', str(temp))]}
            return res
            



