from odoo import models, api, fields


class AccountMovePS(models.Model):
    _inherit = 'account.move'

    change_account_purchase = fields.Boolean(default=False,compute="_change_purchase")
    is_primary_accountform_purchase = fields.Boolean(default=False,compute="_define_purchase")
    is_office_accountform_purchase = fields.Boolean(default=False,compute="_define_purchase")
    is_ben_dis_accountform_purchase = fields.Boolean(default=False,compute="_define_purchase")
    is_insume_accountform_purchase = fields.Boolean(default=False,compute="_define_purchase")
    is_associated_accountform_purchase = fields.Boolean(default=False,compute="_define_purchase")

    is_primary_purchase = fields.Boolean(default=False,compute="_define_purchase",store=True)
    is_office_purchase = fields.Boolean(default=False,compute="_define_purchase",store=True)
    is_discount_purchase = fields.Boolean(default=False,compute="_define_purchase",store=True)
    is_insume_purchase = fields.Boolean(default=False,compute="_define_purchase",store=True)
    is_associated_purchase = fields.Boolean(default=False,compute="_define_purchase",store=True)
    
    sum_account_purchase = fields.Integer(default=0, compute="_calculate_account_purchase")
    type_of_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', store=True)
    type_of_purchase = fields.Many2one(comodel_name='gif.tipificaciones.compras', string='Tipo de Compra',store=True)
    # payment_type_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta', store=True)
    payment_type_purchase = fields.Selection(string='Tipo de Pago', selection=
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
    def _onchange_type_of_purchase(self):
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

    @api.onchange('partner_id')
    def _onchange_partner_id_changedomainpurchase(self):
        for record in self:
            res_ap = {}
            add_user_ap = record.user_id
            grupo_ap = self.env['res.groups'].search([('users','=',add_user_ap.id)])
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

    @api.onchange('change_account_purchase')
    def _onchange_field_type_of_purchase(self):
        for record in self:
            if record.type_of_purchase.id == 1:
                record.payment_type_purchase = '1'
            elif record.type_of_puchase.id == 2:
                record.payment_type_purchase = '2'
            elif record.type_of_purchase.id == 3:
                record.payment_type_purchase = '3'
            elif record.type_of_purchase.id == 4:
                record.payment_type_purchase = '4'
            elif record.type_of_purchase == 5:
                record.payment_type_purchase = '5'


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
    
    @api.depends('sum_account_purchase')
    def _calculate_account_purchase(self):
        for record in self:
            record.sum_account_purchase = 0
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
                            record.sum_account_purchase = record.sum_account_purchase + 1
                    elif 'Transacciones Egreso Productos de Oficina' in user_p:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user_p:
                            pass
                        else:
                            record.sum_account_purchase = record.sum_account_purchase + 4
                    elif 'Transacciones Egreso Descuentos y Beneficios' in user_p:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user_p:
                            pass
                        else:
                            record.sum_account_purchase = record.sum_account_purchase + 16
                    elif 'Transacciones Egreso Productos Insumos' in user_p:
                        if 'Validador Transacciones Egreso Productos Insumos' in user_p:
                            pass
                        else:
                            record.sum_account_purchase = record.sum_account_purchase + 2
                    elif 'Transacciones Egreso Gastos Asociados' in user_p:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user_p:
                            pass
                        else:
                            record.sum_account_purchase = record.sum_account_purchase + 8
            y = 1
            return record.sum_account_purchase

    @api.depends('change_account_purchase')
    def _change_purchase(self):
        for record in self:
            if record.change_account_purchase == False:
                record.change_account_purchase = True
            if record.change_account_purchase == True:
                record.change_account_purchase = False
    
    def _define_purchase(self):
        for record in self:
            record.is_primary_purchase = False
            record.is_office_purchase = False
            record.is_discount_purchase = False
            record.is_insume_purchase = False
            record.is_associated_purchase = False
            record.is_insume_accountform_purchase = False
            record.is_primary_accountform_purchase = False
            record.is_ben_dis_accountform_purchase = False
            record.is_office_accountform_purchase = False
            record.is_associated_accountform_purchase = False
            primarys_purchase = self.env['purchase.order'].search([('tipificacion_compra.name','=','Productos Primarios')])
            offices_purchase = self.env['purchase.order'].search([('tipificacion_compra.name','=','Productos de Oficina')])
            discounts_purchase = self.env['purchase.order'].search([('tipificacion_compra.name','=','Descuentos y Beneficios')])
            insumes_purchase = self.env['purchase.order'].search([('tipificacion_compra.name','=','Productos Insumos')])
            associateds_purchase = self.env['purchase.order'].search([('tipificacion_compra.name','=','Gastos Asociados')])
            #Estas son las condiciones de compras:
            if primarys_purchase:
                for primary_p in primarys_purchase:
                    if (primary_p.name == record.invoice_origin):
                        record.is_primary_accountform_purchase = True
                        record.payment_type_purchase = '1'
                        record.type_of_purchase = 1
                        break
                    else:
                        if record.type_of_purchase:
                            if record.type_of_purchase.id == 1:
                                record.is_primary_accountform_purchase = True
                                break
                            else:
                                record.is_primary_accountform_purchase= False
                        else:
                            record.is_primary_accountform_purchase = False
            else:
                if record.type_of_purchase:
                    if record.type_of_purchase.id == 1:
                        record.is_primary_accountform_purchase = True
                        break
                    else:
                        record.is_primary_accountform_purchase = False
                else:
                    record.is_primary_accountform_purchase = False
            if discounts_purchase:
                for discount_p in discounts_purchase:
                    if (discount_p.name == record.invoice_origin):
                        record.is_ben_dis_accountform_purchase = True
                        record.payment_type_purchase = '5'
                        record.type_of_purchase = 5
                        break
                    else:
                        if record.type_of_purchase:
                            if record.type_of_purchase.id == 5:
                                record.is_ben_dis_accountform_purchase = True
                                break
                            else:
                                record.is_ben_dis_accountform_purchase = False
                        else:
                            record.is_ben_dis_accountform_purchase = False
            else:
                if record.type_of_purchase:
                    if record.type_of_purchase.id == 5:
                        record.is_ben_dis_accountform_purchase = True
                        break
                    else:
                        record.is_ben_dis_accountform_purchase = False
                else:
                    record.is_ben_dis_accountform_purchase = False
            if offices_purchase:
                for office_p in offices_purchase:
                    if (office_p.name == record.invoice_origin):
                        record.is_office_accountform_purchase = True
                        record.payment_type_purchase = '3'
                        record.type_of_purchase = 3
                        break
                    else:
                        if record.type_of_purchase:
                            if record.type_of_purchase.id == 3:
                                record.is_office_accountform_purchase = True
                                break
                            else:
                                record.is_office_accountform_purchase = False
                        else:
                            record.is_office_accountform_purchase = False
            else:
                if record.type_of_purchase:
                    if record.type_of_purchase.id == 3:
                        record.is_office_accountform_purchase = True
                        break
                    else:
                        record.is_office_accountform_purchase = False
                else:
                    record.is_office_accountform_purchase = False
            if insumes_purchase:
                for insume_p in insumes_purchase:
                    if (insume_p.name == record.invoice_origin):
                        record.is_insume_accountform_purchase = True
                        record.payment_type_purchase = '2'
                        record.type_of_purchase = 2
                        break
                    else:
                        if record.type_of_purchase:
                            if record.type_of_purchase.id == 2:
                                record.is_insume_accountform_purchase = True
                                break
                            else:
                                record.is_insume_accountform_purchase = False
                        else:
                            record.is_insume_accountform_purchase = False
            else:
                if record.type_of_purchase:
                    if record.type_of_purchase.id == 2:
                        record.is_insume_accountform_purchase = True
                        break
                    else:
                        record.is_insume_accountform_purchase = False
                else:
                    record.is_insume_accountform_purchase = False
            if associateds_purchase:
                for associated_p in associateds_purchase:
                    if (associated_p.name == record.invoice_origin):
                        record.is_associated_accountform_purchase = True
                        record.payment_type_purchase = '4'
                        record.type_of_purchase = 4
                        break
                    else:
                        if record.type_of_purchase:
                            if record.type_of_purchase.id == 4:
                                record.is_associated_accountform_purchase = True
                                break
                            else:
                                record.is_associated_accountform_purchase = False
                        else:
                            record.is_associated_accountform_purchase = False
            else:
                if record.type_of_purchase:
                    if record.type_of_purchase.id == 4:
                        record.is_associated_accountform_purchase = True
                        break
                    else:
                        record.is_associated_accountform_purchase = False
                else:
                    record.is_associated_accountform_purchase = False
            if record.payment_type_purchase and record.type_of_purchase.id == False:
                if record.payment_type_purchase == '1':
                    record.type_of_purchase = 1
                elif record.payment_type_purchase == '2':
                    record.type_of_purchase = 2
                elif record.payment_type_purchase == '3':
                    record.type_of_purchase = 3
                elif record.payment_type_purchase == '4':
                    record.type_of_purchase = 4
                elif record.payment_type_purchase == '5':
                    record.type_of_purchase = 5

    @api.onchange('partner_id')
    def _onchange_partner_id_changetype_purchase(self):
        for record in self:
            try:
                res_ap = {}
                add_user = record.user_id
                grupo_move_p = self.env['res.groups'].search([('users','=',add_user.id)])
                type_account_id_p =[]
                for g_move_p in grupo_move_p:
                    if(g_move_p.name == 'Transacciones Egreso Productos de Oficina'):
                        type_account_id_p.append(3)
                    elif(g_move_p.name == 'Transacciones Egreso Gastos Asociados'):
                        type_account_id_p.append(4)
                    elif(g_move_p.name == 'Transacciones Egreso Productos Insumos'):
                        type_account_id_p.append(2)
                    elif(g_move_p.name == 'Transacciones Egreso Productos Primarios'):
                        type_account_id_p.append(1)
                    elif(g_move_p.name == 'Transacciones Egreso Descuentos y Beneficios'):
                        type_account_id_p.append(5)
                res_ap['domain'] = {'type_of_purchase': [('id','in',type_account_id_p)]}
                return res_ap
            except:
                pass

    @api.onchange('type_of_purchase','partner_id')
    def onchange_reset_orderlinee(self):
        for record in self:
            try:
                record.invoice_line_ids = None
            except:
                pass

    class AccountMoveOrderLinePS(models.Model):
        _inherit = 'account.move.line'

        @api.onchange('quantity')
        def onchange_type_of_product_changedomainpurchase(self):
            for record in self:
                if record.move_id.type_of_purchase:
                    res = {}
                    temp = record.move_id.type_of_purchase.id
                    res['domain'] = {'product_id': [('product_type_purchase', '=', str(temp))]}
                    return res
                elif record.move_id.payment_type_sale:
                    try: 
                        res = {}
                        temp = record.move_id.payment_type_sale
                        res['domain'] = {'product_id': [('product_type_sale', '=', str(temp))]}
                        return res
                    except: 
                        pass
    
