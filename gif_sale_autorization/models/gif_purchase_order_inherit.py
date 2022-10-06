from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar'),('sent',)], string="Status", index=True, readonly=True, default='draft')
    is_approve = fields.Boolean(compute='_is_approve')
    is_admin_office_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_primary_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_ben_dis_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_discount_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_associated_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_insume_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)

    is_primary_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_insume_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_office_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_associated_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_ben_dis_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_discount_purchaseform = fields.Boolean(compute='_purchaseform_calculate')

    gif_purchase_currency = fields.Float(default=0.0, string="Tasa Técnica",compute="_calculate_currency_purchase_sa",store=True)
    gif_purchase_inverse_currency = fields.Float(default=0.0, string="MXN por Unidad",compute="_calculate_currency_purchase_sa",store=True)

    gif_real_validator = fields.Float(default=0.0,compute="_gif_calculate_real_validator_ev")
    gif_temp_validator = fields.Float(default=0.0,compute="_onchange_currency_id_purchase_sa",string="Tasa de cambio")
    

    @api.onchange('currency_id')
    def _onchange_currency_id_purchase_sa(self):
        for record in self:
            try:
                if record.gif_own_currency_check_purchase == True:
                    record.gif_temp_validator = record.gif_own_inverse_currency_purchase
                else:
                    record.gif_temp_validator = record.currency_id.inverse_rate
            except:
                record.gif_temp_validator = record.currency_id.inverse_rate
    

    @api.depends('gif_purchase_currency','gif_purchase_inverse_currency')
    def _calculate_currency_purchase_sa(self):
        for record in self:
            try: 
                if record.gif_own_currency_check_purchase ==True:
                    record.gif_purchase_inverse_currency = record.gif_own_inverse_currency_purchase
                elif record.currency_id.inverse_rate != 0:
                    record.gif_purchase_currency = record.currency_id.rate
                    record.gif_purchase_inverse_currency = record.currency_id.inverse_rate
                else:
                    record.gif_purchase_currency = 1
                    record.gif_purchase_inverse_currency = 1
            except:
                if record.currency_id.inverse_rate != 0:
                    record.gif_purchase_currency = record.currency_id.rate
                    record.gif_purchase_inverse_currency = record.currency_id.inverse_rate
                else:
                    record.gif_purchase_currency = 1
                    record.gif_purchase_inverse_currency = 1
    
    def _gif_calculate_real_validator_ev(self):
        if self.gif_purchase_inverse_currency != 0:
            self.gif_real_validator = self.gif_purchase_inverse_currency
        else:
            self.gif_real_validator = 1
    
    

    # @api.onchange('tipificacion_compra')
    def _purchaseform_calculate(self):
        for record in self:
            record.is_discount_purchaseform = False
            if record.tipificacion_compra.id == 1:
                record.is_primary_purchaseform = True
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 2:
                print('Es de tipo insumo')
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = True
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 3:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = True
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 4:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = True
            elif record.tipificacion_compra.id == 5:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = True
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            else:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False

    def _is_approve_purchase(self):
        for record in self:
            user_group = []
            add_user = self.env.uid
            groups_i = self.env['res.groups'].search([('name','ilike','Validador')])
            for grupo in groups_i:
                if add_user in grupo.users.ids:
                    user_group.append(grupo.name)
            if user_group:
                for user in user_group:
                    if record.is_primary_purchaseform:
                        if 'Validador Transacciones Egreso Productos Primarios' in user:
                            record.is_admin_primary_purchase = True
                            record.is_admin_office_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_discount_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_office_purchaseform:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user:
                            record.is_admin_office_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_ben_dis_purchaseform:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user:
                            record.is_admin_ben_dis_purchase = True
                            record.is_admin_discount_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_insume_purchaseform:
                        if 'Validador Transacciones Egreso Productos Insumos' in user:
                            record.is_admin_insume_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_associated_purchaseform:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = True
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
            else:
                record.is_admin_discount_purchase = False
                record.is_admin_ben_dis_purchase = False
                record.is_admin_primary_purchase = False
                record.is_admin_office_purchase = False
                record.is_admin_associated_purchase = False
                record.is_admin_insume_purchase = False

    def button_confirm(self):
        for record in self:
            go_to_approve = False
            for line in record.order_line:
                temp = line.price_unit
                if line.product_template_id.descount_selector == "1":
                    fixed = line.d_f_id_purchases
                    porc = 0
                    if temp > fixed:
                        if temp >= 0:
                            if record.is_primary_purchaseform and record.is_admin_primary_purchase:
                                pass
                            elif record.is_office_purchaseform and record.is_admin_office_purchase:
                                pass
                            elif record.is_ben_dis_purchaseform and record.is_admin_ben_dis_purchase:
                                pass
                            elif record.is_associated_purchaseform and record.is_admin_associated_purchase:
                                pass
                            elif record.is_insume_purchaseform and record.is_admin_insume_purchase:
                                pass
                            else:
                                go_to_approve = True
                        else:
                            raise UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
                    else:
                        pass
                elif line.product_template_id.descount_selector == "2":
                    porc = line.d_p_id_purchases
                    fixed = 0
                    if  temp > porc:
                        if temp>= 0:
                            if record.is_primary_purchaseform and record.is_admin_primary_purchase:
                                pass
                            elif record.is_office_purchaseform and record.is_admin_office_purchase:
                                pass
                            elif record.is_ben_dis_purchaseform and record.is_admin_ben_dis_purchase:
                                pass
                            elif record.is_associated_purchaseform and record.is_admin_associated_purchase:
                                pass
                            elif record.is_insume_purchaseform and record.is_admin_insume_purchase:
                                pass
                            else:
                                go_to_approve = True
                        else:
                            raise UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
                    else:
                        pass
            if go_to_approve == True:
                print('Se va approve')
                record.state = 'to_approve'
            else:
                print('Pasa')
                res = super(PurchaseOrder, self).button_approve()
                return res

    def authorize_purchase_primary(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_office(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_insume(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_associated(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_ben_dis(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res

    def go_back_purchase(self):
        for record in self:
            record.state="draft"

    @api.onchange('requisition_id')
    def _purchase_type_inherit_ps(self):
        for record in self:
            record.tipificacion_compra = record.requisition_id.tipificacion_requisition
            for line in record.order_line:
                if line.product_template_id.partners_details_purchase:
                    for p in line.product_template_id.partners_details_purchase:
                        if record.partner_id.name ==  p.partner_purchase.name:
                            line.product_uom = p.partner_uom_purchase

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_template_id = fields.Many2one('product.template')
    d_p_id_purchases = fields.Float(compute='_compute_pp_purchases')
    d_f_id_purchases = fields.Float(compute='_compute_pf_purchases')

    gif_difference_purchase = fields.Float(string="Cantidad",default=0.0 ,compute='_is_difference_purchase_sa')
    gif_is_different_purchase = fields.Boolean(string="Varia",default=False,compute='_is_difference_purchase_sa')

    @api.constrains('product_uom','product_template_id')
    def _check_uom_and_product_gif(self):
        has_to_pass = False
        uom_pass = False
        for record in self:
            if record.product_template_id.partners_details_purchase:
                for p in record.product_template_id.partners_details_purchase:
                    if record.order_id.partner_id.name in p.partner_purchase.name:
                        has_to_pass = True
                    else:
                        has_to_pass = False
                    if record.product_uom == p.partner_uom_purchase:
                        uom_pass = True
                        break
                    else:
                        uom_pass = False
            else:
                raise ValidationError(_('Este producto no tiene proveedores asignados.'))

        if has_to_pass == False:
            raise ValidationError(_('Este producto no tiene proveedores asignados.'))
        if uom_pass == False:
            raise ValidationError(_('La unidad de medida de la orden no coincide con la unidad de medida del producto.'))
    
    @api.onchange('product_template_id')
    def _onchange_product_template_id_reset_order_line_sa(self):
        for record in self:
            if record.product_template_id.name == False or record.product_template_id.detailed_type == 'product':
                gif_pasa = True
                pass
            else:
                if record.product_template_id.partners_details_purchase:
                    for p in record.product_template_id.partners_details_purchase:
                        if record.order_id.partner_id.name == p.partner_purchase.name:
                            gif_pasa = True
                            break
                        else:
                            gif_pasa = False
                else:
                    gif_pasa = False
            if gif_pasa == False:
                record.product_template_id = None
                raise UserError(_('Este Proveedor no tiene precios asignados a este producto.'))
            else:
                pass
    

    @api.onchange('product_uom')
    def _compute_pp_purchases(self):
        for record in self:
            if record.product_template_id.d_p < 0 or record.product_template_id.standard_price < 0:
                raise UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
            else:
                if record.product_template_id.d_p > 100:
                    raise UserError(_('El descuento porcentual no puede ser mayor a 100.'))
                else:
                    if record.product_template_id.partners_details_purchase:
                        for p in record.product_template_id.partners_details_purchase:
                            if record.order_id.partner_id.name == p.partner_purchase.name:
                                if record.order_id.gif_temp_validator:
                                    print('Temp validator en el costo: ',record.order_id.gif_temp_validator)
                                    cost = p.partner_price_purchase/record.order_id.gif_temp_validator
                                    currency_discount = record.product_template_id.d_p/record.order_id.gif_temp_validator
                                else:
                                    cost = p.partner_price_purchase
                                    currency_discount = record.product_template_id.d_p
                                record.d_p_id_purchases = ((currency_discount/100) * cost) + cost
                                break
                            # else:
                            #     raise UserError(_('Este Proveedor no tiene precios asignados a este producto.'))
                        



    @api.onchange('product_uom')
    def _compute_pf_purchases(self):
        for record in self:
            if record.product_template_id.d_f < 0 or record.product_template_id.standard_price < 0:
                raise UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
            else:
                if record.product_template_id.partners_details_purchase:
                    for p in record.product_template_id.partners_details_purchase:
                        if record.order_id.partner_id.name == p.partner_purchase.name:
                            if record.order_id.gif_temp_validator:
                                cost = p.partner_price_purchase/record.order_id.gif_temp_validator
                                record.d_f_id_purchases = cost + ((record.product_template_id.d_f)/record.order_id.gif_temp_validator)
                            else:
                                cost = p.partner_price_purchase
                                record.d_f_id_purchases = cost + record.product_template_id.d_f
                            break
                        



    @api.depends('product_template_id')
    def _give_ids(self):
        for record in self:
            record.d_p = record.product_template_id.d_p_id_purchases

    @api.onchange('product_uom')
    def product_purchase_change(self):
        for record in self:
            if record.order_id.requisition_id:
                pass
            else:
                coin_name = False
                for partner_purchase in record.product_template_id.partners_details_purchase:
                    if  record.order_id.partner_id.name == partner_purchase.partner_purchase.name:
                        record.product_uom = partner_purchase.partner_uom_purchase
                        record.price_unit = partner_purchase.partner_price_purchase
                        print('1')
                        if record.product_uom == partner_purchase.partner_uom_purchase:
                            record.product_uom = None
                            record.product_uom = partner_purchase.partner_uom_purchase
                            record.price_unit = partner_purchase.partner_price_purchase
                            coin_name = partner_purchase.currency_purchase.name
                            break
                            print('2')
                if record.order_id.currency_id and record.order_id.gif_temp_validator != 0:
                    # try:
                        #print('try')
                    if coin_name != False:
                        print('Coin name: ',coin_name)
                        if coin_name == 'MXN' and record.order_id.currency_id.name == 'USD':
                            if record.order_id.gif_temp_validator != 1.0:
                                record.price_unit = record.price_unit / record.order_id.gif_temp_validator
                            else:
                                divisa = self.env['res.currency'].search([('name','=','USD')])
                                if divisa:
                                    record.price_unit = record.price_unit / divisa.rate_ids[0].inverse_company_rate
                        elif coin_name == 'USD' and record.order_id.currency_id.name == 'MXN':
                            print(record.order_id.gif_temp_validator)
                            if record.order_id.gif_temp_validator != 1.0:
                                record.price_unit = record.price_unit * record.order_id.gif_temp_validator 
                            else:
                                divisa = self.env['res.currency'].search([('name','=','USD')])
                                if divisa:
                                    record.price_unit = record.price_unit * divisa.rate_ids[0].inverse_company_rate
                    else:
                        record.price_unit = record.price_unit / record.order_id.gif_temp_validator
                    # except:
                    #     print('except')
                    #     record.price_unit = record.price_unit / record.order_id.gif_temp_validator
                    print('3')
                    
    @api.onchange('name')
    def _onchange_name_sale_autorization_purchase(self):
        for record in self:
            if record.order_id.requisition_id:
                pass
            else:
                for partner_purchase in record.product_template_id.partners_details_purchase:
                    if  record.order_id.partner_id.name == partner_purchase.partner_purchase.name:
                        record.product_uom = partner_purchase.partner_uom_purchase
                        record.price_unit = partner_purchase.partner_price_purchase
                        print('4')
                if record.order_id.currency_id and record.order_id.gif_temp_validator != 0:
                    record.price_unit = record.price_unit / record.order_id.gif_temp_validator
                    print('5')
    
    @api.depends('product_qty')
    def _compute_amount_sale_autorization(self):
        if self.order_id.requisition_id:
            pass
        else:
            for line in self:
                for partner_purchase in line.product_template_id.partners_details_purchase:
                    if  line.order_id.partner_id.name == partner_purchase.partner_purchase.name:
                            line.product_uom = partner_purchase.partner_uom_purchase
                            line.price_unit = partner_purchase.partner_price_purchase
                            print('6')
                if line.order_id.currency_id and line.order_id.gif_temp_validator != 0:
                    line.price_unit = line.price_unit / line.order_id.gif_temp_validator
                    print('7')

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity_purchase_sale_autorization(self):
        if self.order_id.requisition_id:
            pass
        else:
            for line in self:
                for partner_purchase in line.product_template_id.partners_details_purchase:
                    if  line.order_id.partner_id.name == partner_purchase.partner_purchase.name:
                            line.product_uom = partner_purchase.partner_uom_purchase
                            line.price_unit = partner_purchase.partner_price_purchase
                            print('8')
                if line.order_id.currency_id and line.order_id.gif_temp_validator != 0:
                    line.price_unit = line.price_unit / line.order_id.gif_temp_validator
                    print('9')
  
    @api.onchange('price_unit')
    def _is_difference_purchase_sa(self):
        for record in self:
            if record.product_template_id.partners_details_purchase:
                for p in record.product_template_id.partners_details_purchase:
                    if record.order_id.partner_id.name == p.partner_purchase.name:
                        if record.product_template_id.descount_selector == "2" or record.product_template_id.descount_selector == "1":
                                if record.price_unit > record.d_p_id_purchases or record.price_unit < record.d_p_id_purchases:
                                    if record.order_id.gif_temp_validator != 0:
                                        record.gif_is_different_purchase = True
                                        if p.currency_purchase.name == 'MXN' and record.order_id.currency_id.name == 'USD':
                                            print('Producto en pesos orden en USD')
                                            if record.order_id.gif_temp_validator != 1.0:
                                                print('Diferente a 1')
                                                print(record.order_id.gif_temp_validator)
                                                record.gif_difference_purchase = record.price_unit - (p.partner_price_purchase / record.order_id.gif_temp_validator)
                                                print('Difference: ',record.gif_difference_purchase)
                                                break
                                            else:
                                                print('Aqui busca divisa')
                                                divisa = self.env['res.currency'].search([('name','=','USD')])
                                                if divisa:
                                                    print('Deberia de ser esto')
                                                    record.gif_difference = record.price_unit - (p.partner_price_purchase / divisa.rate_ids[0].inverse_company_rate)
                                                    print('Difference: ',record.gif_difference)
                                                    break
                                        elif p.currency_purchase.name == 'USD' and record.order_id.currency_id.name == 'MXN':
                                            if record.order_id.gif_temp_validator != 1.0:
                                                record.gif_difference_purchase = record.price_unit - (p.partner_price_purchase * record.order_id.gif_temp_validator)
                                            else:
                                                divisa = self.env['res.currency'].search([('name','=','USD')])
                                                if divisa:
                                                    record.gif_difference_purchase = record.price_unit - (p.partner_price_purchase * divisa.rate_ids[0].inverse_company_rate)
                                        else:
                                            record.gif_is_different_purchase = True
                                            record.gif_difference_purchase = record.price_unit - p.partner_price_purchase
                                            break
                                else:
                                    print('Luego llega aquí')
                                    record.gif_is_different_purchase = False
                                    record.gif_difference_purchase = 0
                        # elif record.product_template_id.descount_selector == "1":
                        #     if  record.price_unit > record.d_f_id_purchases or record.price_unit < record.d_p_id_purchases:
                        #         if record.order_id.gif_temp_validator != 0:
                        #             record.gif_is_different_purchase = True
                        #             ##############33
                        #             record.gif_difference_purchase = record.price_unit - (p.partner_price_purchase/record.order_id.gif_temp_validator)
                        #             break
                        #         else:
                        #             record.gif_is_different_purchase = True
                        #             record.gif_difference_purchase = record.price_unit - p.partner_price_purchase
                        #             break
                        #     else:
                        #         record.gif_difference_purchase = 0
                        #         record.gif_is_different_purchase = False
                        
                        else:
                            print('2 d')
                            record.gif_difference_purchase = 0
                    else:
                        print('3 d')
                        record.gif_difference_purchase = 0
                        record.gif_is_different_purchase = False
            else:
                record.gif_difference_purchase = 0
                record.gif_is_different_purchase = False