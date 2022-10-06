from odoo import fields,api,models

class AccountMoveSS(models.Model):
    _inherit = 'account.payment'

    change_account_sale = fields.Boolean(default=False,compute="_change_sale")
    is_primary_sale = fields.Boolean(default=False,compute="_define_sale")
    is_office_sale = fields.Boolean(default=False,compute="_define_sale")
    is_ben_dis_sale = fields.Boolean(default=False,compute="_define_sale")
    is_discount_sale = fields.Boolean(default=False,compute="_define_sale")
    sum_payment_sale = fields.Integer(default=0, compute="_calculate_payment_sale")
    payment_type_sale = fields.Selection(string='Tipo de Pago', selection=
    [('1', 'Productos primarios'),
    ('2', 'Productos de oficina'), 
    ('3', 'Descuentos y beneficios')], compute="_onchange_type_of_sale",inverse='_inverse_sale',store=True)
    type_of_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', store=True)

    @api.onchange('type_of_sale')
    def _onchange_type_of_sale(self):
        for record in self:
            if record.type_of_sale.id == 1:
                record.payment_type_sale = '1'
            elif record.type_of_sale.id == 2:
                record.payment_type_sale = '2'
            elif record.type_of_sale.id == 3:
                record.payment_type_sale = '3'

    def _inverse_sale(self):
        for record in self:
            if record.payment_type_sale != False:
                pass
            else:
                pass
            return record.payment_type_sale

    @api.onchange('partner_id')
    def _onchange_partner_id_changetype_sale(self):
        for record in self:
            try:
                res_as = {}
                add_user = record.user_id
                grupo_move_s = self.env['res.groups'].search([('users','=',add_user.id)])
                type_account_id_s =[]
                for g_move_s in grupo_move_s:
                    if(g_move_s.name == 'Transacciones Ingreso Productos Primarios'):
                        type_account_id_s.append(1)
                    elif(g_move_s.name == 'Transacciones Ingreso Productos de Oficina'):
                        type_account_id_s.append(2)
                    elif(g_move_s.name == 'Transacciones Ingreso Descuentos y Beneficios'):
                        type_account_id_s.append(3)
                res_as['domain'] = {'type_of_sale': [('id', 'in',type_account_id_s)]}
                return res_as
            except:
                pass
    
    def _calculate_payment_sale(self):
        for record in self:
            record.sum_payment_sale = 0
            x = 0
            user_group_s = []
            add_user = self.env.uid
            groups_s = self.env['res.groups'].search([('name','ilike','Transacciones Ingreso')])
            for grupo_s in groups_s:
                if add_user in grupo_s.users.ids:
                    user_group_s.append(grupo_s.name)
            for user_s in user_group_s:
                if x == 0:
                    if 'Transacciones Ingreso Productos Primarios' in user_s:
                        if 'Validador Transacciones Ingreso Productos Primarios' in user_s:
                            pass
                        else:
                            record.sum_payment_sale = record.sum_payment_sale + 1
                    elif 'Transacciones Ingreso Productos de Oficina' in user_s:
                        if 'Validador Transacciones Ingreso Productos de Oficina' in user_s:
                            pass
                        else:
                            record.sum_payment_sale = record.sum_payment_sale + 2
                    elif 'Transacciones Ingreso Descuentos y Beneficios' in user_s:
                        if 'Validador Transacciones Ingreso Descuentos y Beneficios' in user_s:
                            pass
                        else:
                            record.sum_payment_sale = record.sum_payment_sale + 4
            x = 1

    @api.depends('change_account_sale')
    def _change_sale(self):
        for record in self:
            if record.change_account_sale == False:
                record.change_account_sale = True
            if record.change_account_sale == True:
                record.change_account_sale = False
    
    def _define_sale(self):
        for record in self:
            record.is_primary_sale = False
            record.is_office_sale = False
            record.is_discount_sale = False
            record.is_ben_dis_sale = False
            primarys_sale = self.env['sale.order'].search([('tipificacion_venta.name','=','Productos Primarios')])
            offices_sale = self.env['sale.order'].search([('tipificacion_venta.name','=','Productos de Oficina')])
            ben_diss_sale = self.env['sale.order'].search([('tipificacion_venta.name','=','Descuentos y Beneficios')])
            #Estas son las condiciones de venta:
            if primarys_sale:
                for primary_s in primarys_sale:
                    if (primary_s.name == record.invoice_origin):
                        record.payment_type_sale = '1'
                        record.type_of_sale = 1
                        record.is_primary_sale = True
                        break
                    else:
                        if record.type_of_sale or record.payment_type_sale:
                            if record.type_of_sale.id == 1 or record.payment_type_sale == '1':
                                record.is_primary_sale = True
                                break
                            else:
                                record.is_primary_sale = False
                        else:
                            record.is_primary_sale = False
            else:
                if record.type_of_sale or record.payment_type_sale:
                    if record.type_of_sale.id == 1 or record.payment_type_sale == '1':
                        record.is_primary_sale = True
                        break
                    else:
                        record.is_primary_sale = False
                else:
                    record.is_primary_sale = False
            if offices_sale:
                for office_s in offices_sale:
                    if(office_s.name == record.invoice_origin):
                        record.type_of_sale = 2
                        record.payment_type_sale = '2'
                        record.is_office_sale = True
                        break
                    else:
                        if record.type_of_sale or record.payment_type_sale:
                            if record.type_of_sale.id == 2 or record.payment_type_sale == '2':
                                record.is_office_sale = True
                                break
                            else:
                                record.is_office_sale = False
                        else:
                            record.is_office_sale = False
            else:
                if record.type_of_sale or record.payment_type_sale:
                    if record.type_of_sale.id == 2 or record.payment_type_sale == '2':
                        record.is_office_sale = True
                        break
                    else:
                        record.is_office_sale = False
                else:
                    record.is_office_sale = False
            if ben_diss_sale:
                for ben_dis_s in ben_diss_sale:
                    if(ben_dis_s.name == record.invoice_origin):
                        record.type_of_sale = 3
                        record.payment_type_sale = '3'
                        record.is_ben_dis_sale = True
                        break
                    else:
                        if record.type_of_sale or record.payment_type_sale:
                            if record.type_of_sale.id == 3 or record.payment_type_sale == '3':
                                record.is_ben_dis_sale = True
                                break
                            else:
                                record.is_ben_dis_sale = False
                        else:
                            record.is_ben_dis_sale = False
            else:
                if record.type_of_sale or record.payment_type_sale:
                    if record.type_of_sale.id == 3 or record.payment_type_sale == '3':
                        record.is_ben_dis_sale = True
                    else:
                        record.is_ben_dis_sale = False
                else:
                    record.is_ben_dis_sale = False
            if record.type_of_sale.id == False and record.payment_type_sale:
                if record.payment_type_sale == '1':
                    record.type_of_sale = 1
                elif record.payment_type_sale == '2':
                    record.type_of_sale = 2
                elif record.payment_type_sale == '3':
                    record.type_of_sale = 3