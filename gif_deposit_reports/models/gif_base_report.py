from odoo import api, fields, models
import datetime as dt
#from datetime import datetime

class GifBaseReport(models.Model):
    _name = 'gif.base.report'
    _description = 'Basic header for reports.'

    
    def _default_code_time(self):
        """Función para calcular el código de tiempo."""
        code_time = (dt.datetime.now() - dt.timedelta(hours=5)).strftime('%Y%m%d_%H%M%S')
        return code_time


    def _default_active_company(self):
        """Función que recupera el nombre de la compañia activa."""
        company_id = self.env.company.id
        return self.env['res.company'].search([('id','=', company_id)])

    def _default_date(self):
        return dt.datetime.now()

  # Encabezado    
    code_time    = fields.Char(store=True, default=_default_code_time)
    #name         = fields.Char(readonly=True, store=True)
    company_name = fields.Many2one('res.company', string="Compañía", readonly=True, store=True, default = _default_active_company)
    date         = fields.Date(string="Fecha", readonly=True, store=True, default =_default_date)

