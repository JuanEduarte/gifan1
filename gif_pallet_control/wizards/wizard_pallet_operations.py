from email.policy import default
from odoo import models, fields, _, api
from odoo.exceptions import UserError


class WizardPalletOperations(models.TransientModel):
    _name = 'wizard.pallet.operations'
    _description = 'Wizard de operaciones de tarimas'

    gif_pallet_qty = fields.Integer(string='Cantidad')
    gif_move_type = fields.Selection(string='Tipo de movimiento', selection=[
                            ('E','Egreso'),
                            ('P','Perdida'),
                            ('I','Ingreso'),
                            ('A','Adquisición')], default="I")
    gif_pallet_type = fields.Selection(string='Tipo de tarima', selection=[
                            ('E','Estandar'),
                            ('C','Chep'),
                            ('S','Smart'),
                            ('O','Otras')], default="E")
    partner_id = fields.Many2one('res.partner', string='Cliente')
    gif_date_history = fields.Datetime(string='Fecha de operación', default=lambda date: fields.Datetime.now())
    gif_pallete_id = fields.Many2one('gif.pallet.pallet', string="Tarima")

    @api.model
    def default_get(self, fields):
        rec = super(WizardPalletOperations, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['gif_pallete_id'] = id_ctx
        return rec

    def gif_set_tarimes(self):
        for record in self:
            values = {
                'gif_date_historic': record.gif_date_history,
                'gif_pallet_id': record.gif_pallete_id.id,
                'partner_id': record.partner_id.id
            }
            if record.gif_move_type in ['E', 'P']:
                values['stock_picking'] = 'MANUAL/OUT'
                values['gif_standard_before'] = record.gif_pallete_id.gif_counter_standard
                values['gif_chep_before'] = record.gif_pallete_id.gif_counter_chep
                values['gif_smart_before'] = record.gif_pallete_id.gif_counter_smart
                values['gif_other_before'] = record.gif_pallete_id.gif_counter_other
                if record.gif_pallet_type == 'C':
                    record.gif_pallete_id.gif_counter_chep -= record.gif_pallet_qty
                if record.gif_pallet_type == 'E':
                    record.gif_pallete_id.gif_counter_standard -= record.gif_pallet_qty
                if record.gif_pallet_type == 'S':
                    record.gif_pallete_id.gif_counter_smart -= record.gif_pallet_qty
                if record.gif_pallet_type == 'O':
                    record.gif_pallete_id.gif_counter_other -= record.gif_pallet_qty
                values['gif_standard_after'] = record.gif_pallete_id.gif_counter_standard
                values['gif_chep_after'] = record.gif_pallete_id.gif_counter_chep
                values['gif_smart_after'] = record.gif_pallete_id.gif_counter_smart
                values['gif_other_after'] = record.gif_pallete_id.gif_counter_other
            elif record.gif_move_type in ['I', 'A']:
                values['stock_picking'] = 'MANUAL/IN'
                values['gif_standard_before'] = record.gif_pallete_id.gif_counter_standard
                values['gif_chep_before'] = record.gif_pallete_id.gif_counter_chep
                values['gif_smart_before'] = record.gif_pallete_id.gif_counter_smart
                values['gif_other_before'] = record.gif_pallete_id.gif_counter_other
                if record.gif_pallet_type == 'C':
                    record.gif_pallete_id.gif_counter_chep += record.gif_pallet_qty
                if record.gif_pallet_type == 'E':
                    record.gif_pallete_id.gif_counter_standard += record.gif_pallet_qty
                if record.gif_pallet_type == 'S':
                    record.gif_pallete_id.gif_counter_smart += record.gif_pallet_qty
                if record.gif_pallet_type == 'O':
                    record.gif_pallete_id.gif_counter_other += record.gif_pallet_qty
                values['gif_standard_after'] = record.gif_pallete_id.gif_counter_standard
                values['gif_chep_after'] = record.gif_pallete_id.gif_counter_chep
                values['gif_smart_after'] = record.gif_pallete_id.gif_counter_smart
                values['gif_other_after'] = record.gif_pallete_id.gif_counter_other
            else:
                raise UserError(_("Necesitas selecciona el tipo de movimiento y tipo de tarima."))
            record.gif_pallete_id.gif_history_pallet.create(values)