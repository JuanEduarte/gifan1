from odoo import api, fields, models

class WizardShowGroups(models.TransientModel):
    _name = 'wizard.show.groups'
    _description = 'Asignar una empresa a un grupo'

    partners_id = fields.Many2one('res.partner', domain="[('is_company', '=', True)]",string="Empresa a asociar")

    def assign_company(self):
        for record in self:
            grp_id = self.env.context.get('active_id',False)
            record.partners_id.group_id = grp_id
