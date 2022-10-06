from odoo import models,api,fields,tools,_
from odoo.tools.float_utils import float_is_zero
from collections import defaultdict
from odoo.exceptions import UserError

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    @api.onchange('l10n_mx_edi_customs_number')
    def _onchange_l10n_mx_edi_customs_number_gif_pediments(self):
        pediment = self.env['gif.pediments'].search([('name','=',self.l10n_mx_edi_customs_number)],limit=1)
        if pediment:
            self.picking_ids = pediment.gif_ped_stock
            for line in self.cost_lines:
                line.price_unit = pediment.gif_total

    def compute_landed_cost(self):
        AdjustementLines = self.env['stock.valuation.adjustment.lines']
        AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()

        towrite_dict = {}
        for cost in self.filtered(lambda cost: cost._get_targeted_move_ids()):
            print('/////////////////////////////////')
            rounding = cost.currency_id.rounding
            print('Rounding: ',rounding)
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            for val_line_values in all_val_line_values:
                print('**********************************')
                print('Val line values: ',val_line_values)
                for cost_line in cost.cost_lines:
                    print('||||||||||||||||||||||||||||||||')
                    print('Cost line: ',cost_line)
                    val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                    self.env['stock.valuation.adjustment.lines'].create(val_line_values)
                total_qty += val_line_values.get('quantity', 0.0)
                print('Total qty: ',total_qty)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                print('Former cost: ',former_cost)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += cost.currency_id.round(former_cost)
                print('Total cost: ',total_cost)

                total_line += 1

            for line in cost.cost_lines:
                print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
                print('Line: ',line)
                value_split = 0.0
                for valuation in cost.valuation_adjustment_lines:
                    print('$$$$$$$$$$$$$$$$$$$$$$$$$')
                    print('Valuation: ',valuation)
                    value = 0.0
                    if valuation.cost_line_id and valuation.cost_line_id.id == line.id:
                        print('Valuation cost line: ',valuation.cost_line_id)
                        if line.split_method == 'by_quantity' and total_qty:
                            per_unit = (line.price_unit / total_qty)
                            print('Per unit: ',per_unit)
                            print('{} = {} / {}'.format(per_unit,line.price_unit,total_qty))
                            value = valuation.quantity * per_unit
                            print('Value: ',value)
                        elif line.split_method == 'by_weight' and total_weight:
                            per_unit = (line.price_unit / total_weight)
                            value = valuation.weight * per_unit
                        elif line.split_method == 'by_volume' and total_volume:
                            per_unit = (line.price_unit / total_volume)
                            value = valuation.volume * per_unit
                        elif line.split_method == 'equal':
                            value = (line.price_unit / total_line)
                            print('{} = {} / {}'.format(value,line.price_unit,total_line))
                        elif line.split_method == 'by_current_cost_price' and total_cost:
                            per_unit = (line.price_unit / total_cost)
                            value = valuation.former_cost * per_unit
                        else:
                            value = (line.price_unit / total_line)

                        if rounding:
                            print('If rounding: ',rounding)
                            value = tools.float_round(value, precision_rounding=rounding, rounding_method='UP')
                            print('Value: ',value)
                            fnc = min if line.price_unit > 0 else max
                            print('Fnc: ',fnc)
                            value = fnc(value, line.price_unit - value_split)
                            print('Value 2: ',value)
                            value_split += value
                            print('Value split: ',value_split)

                        if valuation.id not in towrite_dict:
                            towrite_dict[valuation.id] = value
                            print('If: ')
                            print('Towrite_dict: ',towrite_dict,towrite_dict[valuation.id])
                        else:
                            print('Else')
                            towrite_dict[valuation.id] += value
                            print('Towrite_dict: ',towrite_dict,towrite_dict[valuation.id])
        for key, value in towrite_dict.items():
            AdjustementLines.browse(key).write({'additional_landed_cost': value})
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
            print('Cost Date: ', cost.date)
            print('Cost Name: ', cost.name)
            valuation_layer_ids = []
            cost_to_add_byproduct = defaultdict(lambda: 0.0)
            for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                remaining_qty = sum(line.move_id.stock_valuation_layer_ids.mapped('remaining_qty'))
                print('Remaining qty: ',remaining_qty)
                linked_layer = line.move_id.stock_valuation_layer_ids[:1]
                print('Linked layer: ',linked_layer)

                # Prorate the value at what's still in stock
                cost_to_add = (remaining_qty / line.move_id.product_qty) * line.additional_landed_cost
                print('Cost to add: ')
                print('{} = ({} / {}) * {} '.format(cost_to_add,remaining_qty,line.move_id.product_qty,line.additional_landed_cost))
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
                    print('Linked later reamining value: ',linked_layer.remaining_value)
                    valuation_layer_ids.append(valuation_layer.id)
                    print('Valuation layer  id ',valuation_layer.id)
                # Update the AVCO
                product = line.move_id.product_id
                print('Product: ',product)
                if product.cost_method == 'average':
                    print('El metodo de costo del producto es promedio')
                    cost_to_add_byproduct[product] += cost_to_add
                    print('cost_to_add_byproduct[product]: ',cost_to_add_byproduct[product])
                # Products with manual inventory valuation are ignored because they do not need to create journal entries.
                if product.valuation != "real_time":
                    print('Su valoración es en tiempo real')
                    continue
                # `remaining_qty` is negative if the move is out and delivered proudcts that were not
                # in stock.
                qty_out = 0
                if line.move_id._is_in():
                    qty_out = line.move_id.product_qty - remaining_qty
                    print('Qty out if: ')
                    print('{} = {} - {}'.format(qty_out,line.move_id.product_qty,remaining_qty))
                elif line.move_id._is_out():
                    print('Qty out elif: ')
                    qty_out = line.move_id.product_qty
                    print('{} = {} '.format(qty_out,line.move_id.product_qty))
                move_vals['line_ids'] += line._create_accounting_entries(move, qty_out)
                print('Move vals: ')
                print('{} += {}'.format(move_vals['line_ids'],line._create_accounting_entries(move, qty_out)))

            # batch standard price computation avoid recompute quantity_svl at each iteration
            products = self.env['product.product'].browse(p.id for p in cost_to_add_byproduct.keys())
            for product in products:  # iterate on recordset to prefetch efficiently quantity_svl
                print('For product in products: ',product)
                if not float_is_zero(product.quantity_svl, precision_rounding=product.uom_id.rounding):
                    product.with_company(cost.company_id).sudo().with_context(disable_auto_svl=True).standard_price += cost_to_add_byproduct[product] / product.quantity_svl

            move_vals['stock_valuation_layer_ids'] = [(6, None, valuation_layer_ids)]
            # We will only create the accounting entry when there are defined lines (the lines will be those linked to products of real_time valuation category).
            cost_vals = {'state': 'done'}
            if move_vals.get("line_ids"):
                print('If move vals: ')
                move = move.create(move_vals)
                cost_vals.update({'account_move_id': move.id})
            cost.write(cost_vals)
            if cost.account_move_id:
                move._post()

            if cost.vendor_bill_id and cost.vendor_bill_id.state == 'posted' and cost.company_id.anglo_saxon_accounting:
                all_amls = cost.vendor_bill_id.line_ids | cost.account_move_id.line_ids
                print('All amls: ')
                print('{} = {} | {}'.format(all_amls,cost.vendor_bill_id.line_ids,cost.account_move_id.line_ids))
                for product in cost.cost_lines.product_id:
                    accounts = product.product_tmpl_id.get_product_accounts()
                    input_account = accounts['stock_input']
                    all_amls.filtered(lambda aml: aml.account_id == input_account and not aml.reconciled).reconcile()

        return True