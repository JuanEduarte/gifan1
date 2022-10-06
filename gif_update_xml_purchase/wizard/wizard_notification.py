from odoo import fields, models

class WizardNotificationReload(models.TransientModel):
    _name = 'wizard.notification.reload'
    _description = 'Notificación de archivos subidos o duplicados.'

    text_notification = fields.Text(string="Atención", readonly=True)

    def refresh(self):
        return {'type': 'ir.actions.client', 'tag': 'reload'}


class WizardNotification(models.TransientModel):
    _name = 'wizard.notification'
    _description = 'Notificación general.'

    text_notification = fields.Text(string="Atención", readonly=True)

    def refresh(self):
        return True