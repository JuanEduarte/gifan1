from odoo import fields,api,models

class AccountMovePS(models.Model):
    _inherit = 'account.batch.payment'

    change_account_purchase = fields.Boolean(default=False,compute="_change_purchase")
    is_primary_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    is_office_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    is_ben_dis_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    is_insume_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    is_discount_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    is_associated_purchase = fields.Boolean(default=False,compute="_define_batch_purchase")
    sum_batch_purchase = fields.Integer(default=0, compute="_calculate_batch_purchase")
    type_of_purchase = fields.Many2one(comodel_name='gif.tipificaciones.compras')
    type_of_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', store=True)
    payment_type_purchase = fields.Selection(string='Tipo de compra', selection=
    [('1', 'Productos primarios'),
    ('2', 'Productos insumos'),
    ('3', 'Productos de oficina'), 
    ('4', 'Gastos asociados'),
    ('5', 'Descuentos y beneficios')], compute="_type_purchase",inverse='_inverse_purchase',store=True)
    payment_type_sale = fields.Selection(string='Tipo de Pago', selection=
    [('1', 'Productos primarios'),
    ('2', 'Productos de oficina'), 
    ('3', 'Descuentos y beneficios')], compute="_type_sale",inverse='_inverse_sale',store=True)

    @api.onchange('type_of_purchase')
    def _onchange__type_purchase_batch(self):
        for record in self:
            if record.type_of_purchase.id == 1:
                record.payment_type_purchase = '1'
            elif record.type_of_purchase.id == 2:
                record.payment_type_purchase = '2'
            elif record.type_of_purchase.id == 3:
                record.payment_type_purchase = '3'
            elif record.type_of_purchase.id == 4:
                record.payment_type_purchase = '4'
            elif record.type_of_purchase.id == 5:
                record.payment_type_purchase = '5'

    @api.onchange('journal_id')
    def _onchange_journal_id_changedomainpurchase(self):
        for record in self:
            res_ap = {}
            add_user_ap = self.env.uid
            grupo_ap = self.env['res.groups'].search([('users','=',add_user_ap)])
            type_of_purchase_id =[]
            for g_ap in grupo_ap:
                if(g_ap.name == 'Transacciones Egreso Productos de Oficina'):
                    type_of_purchase_id.append(3)
                elif(g_ap.name == 'Transacciones Egreso Gastos Asociados'):
                    type_of_purchase_id.append(4)
                elif(g_ap.name == 'Transacciones Egreso Productos Insumos'):
                    type_of_purchase_id.append(2)
                elif(g_ap.name == 'Transacciones Egreso Productos Primarios'):
                    type_of_purchase_id.append(1)
                elif(g_ap.name == 'Transacciones Egreso Descuentos y Beneficios'):
                    type_of_purchase_id.append(5)
            res_ap['domain'] = {'type_of_purchase': [('id', 'in', type_of_purchase_id)]}
            return res_ap

    def _inverse_purchase(self):
        for record in self:
            if record.payment_type_purchase != False:
                pass
            else:
                pass
            return record.payment_type_purchase

    @api.onchange('change_account_purchase')
    def _type_purchase(self):
        for record in self:
            if record.payment_type_purchase != False:
                if record.type_of_purchase.id == 1:
                    record.payment_type_purchase = '1'
                elif record.type_of_purchase.id == 2:
                    record.payment_type_purchase = '2'
                elif record.type_of_purchase.id == 3:
                    record.payment_type_purchase = '3'
                elif record.type_of_purchase.id == 4: 
                    record.payment_type_purchase = '4'
                elif record.type_of_purchase.id == 5:
                    record.payment_type_purchase = '5'
                    
            else:
                if record.type_of_purchase:
                    record.type_of_purchase.id = record.type_of_purchase.id
                else:
                    pass
    
    def _calculate_batch_purchase(self):
        for record in self:
            record.sum_batch_purchase = 0
            y = 0
            user_group_p = []
            add_user_p = self.env.uid
            groups_p = self.env['res.groups'].search([('name','ilike','Transacciones Egreso')])
            for grupo_p in groups_p:
                if add_user_p in grupo_p.users.ids:
                    user_group_p.append(grupo_p.name)
            for user_p in user_group_p:
                if y == 0:
                    if 'Transacciones Egreso Productos Primarios' in user_p:
                        if 'Validador Transacciones Egreso Productos Primarios' in user_p:
                            pass
                        else:
                            record.sum_batch_purchase = record.sum_batch_purchase + 1
                    elif 'Transacciones Egreso Productos de Oficina' in user_p:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user_p:
                            pass
                        else:
                            record.sum_batch_purchase = record.sum_batch_purchase + 4
                    elif 'Transacciones Egreso Descuentos y Beneficios' in user_p:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user_p:
                            pass
                        else:
                            record.sum_batch_purchase = record.sum_batch_purchase + 16
                    elif 'Transacciones Egreso Productos Insumos' in user_p:
                        if 'Validador Transacciones Egreso Productos Insumos' in user_p:
                            pass
                        else:
                            record.sum_batch_purchase = record.sum_batch_purchase + 2
                    elif 'Transacciones Egreso Gastos Asociados' in user_p:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user_p:
                            pass
                        else:
                            record.sum_batch_purchase = record.sum_batch_purchase + 8
            y = 1

    @api.depends('change_account_purchase')
    def _change_purchase(self):
        for record in self:
            if record.change_account_purchase == False:
                record.change_account_purchase = True
            if record.change_account_purchase == True:
                record.change_account_purchase = False
    
    def _define_batch_purchase(self):
        for record in self:
            record.is_primary_purchase = False
            record.is_ben_dis_purchase = False
            record.is_discount_purchase = False
            record.is_office_purchase = False
            record.is_insume_purchase = False
            record.is_associated_purchase = False
            if record.type_of_purchase:
                if record.type_of_purchase.id == 1:
                    record.is_primary_purchase = True
                    break
                elif record.type_of_purchase.id == 5:
                    record.is_ben_dis_purchase = True
                    break
                elif record.type_of_purchase.id == 3:
                    record.is_office_purchase = True
                    break
                elif record.type_of_purchase.id == 2:
                    record.is_insume_purchase = True
                    break
                elif record.type_of_purchase.id == 4:
                    record.is_associated_purchase = True
                    break