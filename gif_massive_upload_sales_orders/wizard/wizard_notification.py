from odoo import fields, models

class WizardNotification(models.TransientModel):
    _name = 'wizard.notification'
    _description = 'Notificación general.'

    text_notification = fields.Text(string="Atención", readonly=True)

    def refresh(self):
        pass