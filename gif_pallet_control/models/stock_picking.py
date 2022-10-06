from email.policy import default
from odoo import models, fields, api
from datetime import datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    gif_picking_code = fields.Boolean(string='Codigo de picking', default=False)
    gif_pallet_standard = fields.Integer(string='Tarima Estandar', default=0)
    gif_pallet_chep = fields.Integer(string='Tarima Chep', default=0)
    gif_pallet_smart = fields.Integer(string='Tarima Smart', default=0)
    gif_pallet_other = fields.Integer(string='Tarima Otra', default=0)

    def button_validate(self):
        print(self)
        for record in self:
            if record.picking_type_id.code == 'incoming':
                record._add_pallets()
                res= super(StockPicking,self).button_validate()
                return res
            elif record.picking_type_id.code == 'outgoing':
                record._remove_pallets()
                res= super(StockPicking,self).button_validate()
                return res
            else:
                print('Native action')
                res= super(StockPicking,self).button_validate()
                return res
        print('Dentro del Picking')
        res= super(StockPicking,self).button_validate()
        return res
    
    def _add_pallets(self):
        for record in self:
            pallet = self.env['gif.pallet.pallet'].search([('company_id', '=', record.company_id.id)])
            values = {
                'gif_date_historic': datetime.now(),
                'gif_pallet_id': pallet.id,
                'partner_id': record.partner_id.id,
                'stock_picking': record.name,
                'gif_standard_before': pallet.gif_counter_standard,
                'gif_chep_before': pallet.gif_counter_chep,
                'gif_smart_before': pallet.gif_counter_smart,
                'gif_other_before': pallet.gif_counter_other,
            }
            pallet.gif_counter_standard += record.gif_pallet_standard
            pallet.gif_counter_chep += record.gif_pallet_chep
            pallet.gif_counter_smart += record.gif_pallet_smart
            pallet.gif_counter_other += record.gif_pallet_other

            # std = pallet.gif_counter_standard + record.gif_pallet_standard
            # chep = pallet.gif_counter_chep + record.gif_pallet_chep
            # smart = pallet.gif_counter_smart + record.gif_pallet_smart
            values.update({
                'gif_standard_after': pallet.gif_counter_standard,
                'gif_chep_after': pallet.gif_counter_chep,
                'gif_smart_after': pallet.gif_counter_smart,
                'gif_other_after': pallet.gif_counter_other,
                # 'gif_standard_after': std,
                # 'gif_chep_after': chep,
                # 'gif_smart_after': smart,
            })
            print(values)
            pallet.gif_history_pallet.create(values)
            return True

    def _remove_pallets(self):
        for record in self:
            pallet = self.env['gif.pallet.pallet'].search([('company_id', '=', record.company_id.id)])
            values = {
                'gif_date_historic': datetime.now(),
                'gif_pallet_id': pallet.id,
                'partner_id': record.partner_id.id,
                'stock_picking': record.name,
                'gif_standard_before': pallet.gif_counter_standard,
                'gif_chep_before': pallet.gif_counter_chep,
                'gif_smart_before': pallet.gif_counter_smart,
            }
            pallet.gif_counter_standard -= record.gif_pallet_standard
            pallet.gif_counter_chep -= record.gif_pallet_chep
            pallet.gif_counter_smart -= record.gif_pallet_smart
            pallet.gif_counter_other -= record.gif_pallet_other

            # std = pallet.gif_counter_standard - record.gif_pallet_standard
            # chep = pallet.gif_counter_chep - record.gif_pallet_chep
            # smart = pallet.gif_counter_smart - record.gif_pallet_smart
            values.update({
                'gif_standard_after': pallet.gif_counter_standard,
                'gif_chep_after': pallet.gif_counter_chep,
                'gif_smart_after': pallet.gif_counter_smart,
                # 'gif_standard_after': std,
                # 'gif_chep_after': chep,
                # 'gif_smart_after': smart,
            })
            print(values)
            pallet.gif_history_pallet.create(values)
            return True

    def read(self, fields=None, load='_classic_read'):
        for record in self:
            if record.picking_type_id.id != 0:
                if record.picking_type_id.code in ['incoming', 'outgoing']:
                    record.gif_picking_code = True
                else:
                    record.gif_picking_code = False
            res = super(StockPicking,self).read(fields,load)
            return res

    @api.onchange('picking_type_id')
    def _get_picking_code(self):
        for record in self:
            if record.picking_type_id.code in ['incoming', 'outgoing']:
                record.gif_picking_code = True
                print(record.gif_picking_code)
            else:
                record.gif_picking_code = False
                print(record.gif_picking_code)