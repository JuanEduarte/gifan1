from odoo import models,api,fields,tools,_
from odoo.tools.float_utils import float_is_zero
from collections import defaultdict
from odoo.exceptions import UserError

class StockLandedCostLine(models.Model):
    _inherit = 'stock.landed.cost.lines'

    split_method = fields.Selection(selection_add=[('igi','IGI'),('equal',)],ondelete={'igi': 'set default'},default='equal')
    gif_part_qty = fields.Integer(default=0)
    gif_part_no = fields.Integer(default=0)
    gif_part_prod = fields.Char(string='')
    
    
class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    @api.onchange('l10n_mx_edi_customs_number')
    def _onchange_l10n_mx_edi_customs_number_gif_pediments(self):
        pediment = self.env['gif.pediments'].search([('name','=',self.l10n_mx_edi_customs_number)],limit=1)
        igi_dict = {}
        igi_dict2 = {}
        igi_price = {}
        igi_exit = []
        igi_value = {}
        if pediment and pediment.gif_prorrateado == False:
            self.ensure_one()
            self.picking_ids = pediment.gif_ped_stock
            if len(self.cost_lines) >= 1:
                for line in self.cost_lines:
                    line.price_unit = pediment.gif_total
            else:
                cost_des = self.env['product.product'].search([('name','=','Costo Destino')])
                self.update({
                    'cost_lines': [(0,0,{
                        'split_method': 'equal',
                        'price_unit': pediment.gif_total,
                        'product_id': cost_des,
                        'name': cost_des.name,
                        'account_id': cost_des.product_tmpl_id.get_product_accounts()['stock_input'].id,
                        })]
                    })

            for pline in pediment.gif_part_part_one:
                igi_dict[str(pline.gif_part_num_set)] = str(pline.gif_part_prod.name)
            for igline in pediment.gif_set_part:
                igi_dict2[str(igline.gif_part_no)] = str(igline.gif_imp_igi)
            for assign in pediment.gif_rel_doc_ped:
                if assign.gif_nm_part not in igi_exit:
                    igi_exit.append(assign.gif_nm_part)
                try:
                    igi_value[str(assign.gif_nm_part)] = igi_value[str(assign.gif_nm_part)] + assign.gif_total_ped
                except:
                    igi_value[str(assign.gif_nm_part)] = assign.gif_total_ped
            for value in igi_exit:
                total = 0
                for a in pediment.gif_rel_doc_ped:
                    if a.gif_nm_part == value:
                        total += 1
                igi_price[value] = total
            for iline in pediment.gif_rel_doc_ped:
                if iline.gif_nm_part != 0:
                    product = self.env['product.product'].search([('name','=',igi_dict[str(iline.gif_nm_part)])])
                    price = iline.gif_total_ped/(igi_value[str(iline.gif_nm_part)])
                    price_final = price * float(igi_dict2[str(iline.gif_nm_part)])
                    self.update({
                        'cost_lines': [(0,0,{
                            'split_method': 'igi',
                            'price_unit': price_final,
                            'product_id': product,
                            'name': product.name+' '+iline.gif_stock_product,
                            'account_id': product.product_tmpl_id.get_product_accounts()['stock_input'].id,
                            'gif_part_qty': iline.gif_stock_qty,
                            'gif_part_no': iline.gif_nm_part,
                            'gif_part_prod': iline.gif_stock_product,
                        })],
                    })
        else:
            self.cost_lines = None

    def get_valuation_lines(self):
        self.ensure_one()
        lines = []

        for move in self._get_targeted_move_ids():
            # it doesn't make sense to make a landed cost for a product that isn't set as being valuated in real time at real cost
            if move.product_id.cost_method not in ('fifo', 'average') or move.state == 'cancel' or not move.product_qty:
                continue
            vals = {
                'product_id': move.product_id.id,
                'move_id': move.id,
                'quantity': move.product_qty,
                'former_cost': sum(move.stock_valuation_layer_ids.mapped('value')),
                'weight': move.product_id.weight * move.product_qty,
                'volume': move.product_id.volume * move.product_qty
            }
            lines.append(vals)

        if not lines:
            target_model_descriptions = dict(self._fields['target_model']._description_selection(self.env))
            raise UserError(_("You cannot apply landed costs on the chosen %s(s). Landed costs can only be applied for products with FIFO or average costing method.", target_model_descriptions[self.target_model]))
        return lines

    def compute_landed_cost(self):
        AdjustementLines = self.env['stock.valuation.adjustment.lines']
        AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()

        towrite_dict = {}
        for cost in self.filtered(lambda cost: cost._get_targeted_move_ids()):
            rounding = cost.currency_id.rounding
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            ids = []
            for val_line_values in all_val_line_values:
                for cost_line in cost.cost_lines:
                    # print(val_line_values)
                    if cost_line.split_method == 'igi':
                        nombre = cost_line.product_id.name + ' '+ cost_line.gif_part_prod
                        producto = self.env['product.product'].search([('id','=',val_line_values['product_id'])])
                        prod_name = cost_line.product_id.name + ' '+producto.name
                        if nombre == cost_line.name and prod_name == cost_line.name:
                            #El nombre del producto es el mismo, cambiar
                            # if val_line_values['cost_line_id'] not in ids:
                            #     ids.append(val_line_values['cost_line_id'])
                            val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                            self.env['stock.valuation.adjustment.lines'].create(val_line_values)
                        else:
                            pass
                    else:
                        val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                        self.env['stock.valuation.adjustment.lines'].create(val_line_values)
                total_qty += val_line_values.get('quantity', 0.0)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += cost.currency_id.round(former_cost)
                total_line += 1
            for line in cost.cost_lines:
                value_split = 0.0
                for valuation in cost.valuation_adjustment_lines:
                    value = 0.0
                    if valuation.cost_line_id and valuation.cost_line_id.id == line.id:
                        if line.split_method == 'by_quantity' and total_qty:
                            per_unit = (line.price_unit / total_qty)
                            value = valuation.quantity * per_unit
                        elif line.split_method == 'by_weight' and total_weight:
                            per_unit = (line.price_unit / total_weight)
                            value = valuation.weight * per_unit
                        elif line.split_method == 'by_volume' and total_volume:
                            per_unit = (line.price_unit / total_volume)
                            value = valuation.volume * per_unit
                        elif line.split_method == 'equal':
                            value = (line.price_unit / total_line)
                        elif line.split_method == 'by_current_cost_price' and total_cost:
                            per_unit = (line.price_unit / total_cost)
                            value = valuation.former_cost * per_unit
                        elif line.split_method == 'igi':
                            value = (line.price_unit) 
                        else:
                            value = (line.price_unit / total_line)

                        if rounding:
                            value = tools.float_round(value, precision_rounding=rounding, rounding_method='UP')
                            fnc = min if line.price_unit > 0 else max
                            value = fnc(value, line.price_unit - value_split)
                            value_split += value

                        if valuation.id not in towrite_dict:
                            towrite_dict[valuation.id] = value
                        else:
                            towrite_dict[valuation.id] += value
        for key, value in towrite_dict.items():
            AdjustementLines.browse(key).write({'additional_landed_cost': value})
        return True

    def _check_sum(self):
        print('La funcion que checa')
        """ Check if each cost line its valuation lines sum to the correct amount
        and if the overall total amount is correct also """
        prec_digits = self.env.company.currency_id.decimal_places
        print('Prec digits: ',prec_digits)
        for landed_cost in self:
            total_amount = sum(landed_cost.valuation_adjustment_lines.mapped('additional_landed_cost'))
            print('Total amount: ',total_amount)
            if not tools.float_is_zero(total_amount - landed_cost.amount_total, precision_digits=prec_digits):
                print('Lande cost amount: ',landed_cost.amount_total)
                return False

            val_to_cost_lines = defaultdict(lambda: 0.0)
            for val_line in landed_cost.valuation_adjustment_lines:
                val_to_cost_lines[val_line.cost_line_id] += val_line.additional_landed_cost
            if any(not tools.float_is_zero(cost_line.price_unit - val_amount, precision_digits=prec_digits)
                   for cost_line, val_amount in val_to_cost_lines.items()):
                print('Retorna false 2')
                return False
        return True

    def button_validate(self):
        self._check_can_validate()
        cost_without_adjusment_lines = self.filtered(lambda c: not c.valuation_adjustment_lines)
        if cost_without_adjusment_lines:
            cost_without_adjusment_lines.compute_landed_cost()
        if not self._check_sum():
            raise UserError(_('Cost and adjustments lines do not match. You should maybe recompute the landed costs.'))

        for cost in self:
            cost = cost.with_company(cost.company_id)
            move = self.env['account.move']
            move_vals = {
                'journal_id': cost.account_journal_id.id,
                'date': cost.date,
                'ref': cost.name,
                'line_ids': [],
                'move_type': 'entry',
            }
            valuation_layer_ids = []
            cost_to_add_byproduct = defaultdict(lambda: 0.0)
            for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                remaining_qty = sum(line.move_id.stock_valuation_layer_ids.mapped('remaining_qty'))
                linked_layer = line.move_id.stock_valuation_layer_ids[:1]

                # Prorate the value at what's still in stock
                cost_to_add = (remaining_qty / line.move_id.product_qty) * line.additional_landed_cost
                if not cost.company_id.currency_id.is_zero(cost_to_add):
                    valuation_layer = self.env['stock.valuation.layer'].create({
                        'value': cost_to_add,
                        'unit_cost': 0,
                        'quantity': 0,
                        'remaining_qty': 0,
                        'stock_valuation_layer_id': linked_layer.id,
                        'description': cost.name,
                        'stock_move_id': line.move_id.id,
                        'product_id': line.move_id.product_id.id,
                        'stock_landed_cost_id': cost.id,
                        'company_id': cost.company_id.id,
                    })
                    linked_layer.remaining_value += cost_to_add
                    valuation_layer_ids.append(valuation_layer.id)
                # Update the AVCO
                product = line.move_id.product_id
                if product.cost_method == 'average':
                    cost_to_add_byproduct[product] += cost_to_add
                # Products with manual inventory valuation are ignored because they do not need to create journal entries.
                if product.valuation != "real_time":
                    continue
                # `remaining_qty` is negative if the move is out and delivered proudcts that were not
                # in stock.
                qty_out = 0
                if line.move_id._is_in():
                    qty_out = line.move_id.product_qty - remaining_qty
                elif line.move_id._is_out():
                    qty_out = line.move_id.product_qty
                move_vals['line_ids'] += line._create_accounting_entries(move, qty_out)
    
            # batch standard price computation avoid recompute quantity_svl at each iteration
            products = self.env['product.product'].browse(p.id for p in cost_to_add_byproduct.keys())
            for product in products:  # iterate on recordset to prefetch efficiently quantity_svl
                if not float_is_zero(product.quantity_svl, precision_rounding=product.uom_id.rounding):
                    product.with_company(cost.company_id).sudo().with_context(disable_auto_svl=True).standard_price += cost_to_add_byproduct[product] / product.quantity_svl

            move_vals['stock_valuation_layer_ids'] = [(6, None, valuation_layer_ids)]
            # We will only create the accounting entry when there are defined lines (the lines will be those linked to products of real_time valuation category).
            cost_vals = {'state': 'done'}
            if move_vals.get("line_ids"):
                move = move.create(move_vals)
                cost_vals.update({'account_move_id': move.id})
            cost.write(cost_vals)
            if cost.account_move_id:
                move._post()

            if cost.vendor_bill_id and cost.vendor_bill_id.state == 'posted' and cost.company_id.anglo_saxon_accounting:
                all_amls = cost.vendor_bill_id.line_ids | cost.account_move_id.line_ids
                for product in cost.cost_lines.product_id:
                    accounts = product.product_tmpl_id.get_product_accounts()
                    input_account = accounts['stock_input']
                    all_amls.filtered(lambda aml: aml.account_id == input_account and not aml.reconciled).reconcile()
        pediment = self.env['gif.pediments'].search([('name','=',self.l10n_mx_edi_customs_number)],limit=1)
        if pediment and pediment.gif_prorrateado == False:
            pediment.gif_prorrateado = True
            for picking in self.picking_ids:
                picking.gif_has_pediment = True
        return True