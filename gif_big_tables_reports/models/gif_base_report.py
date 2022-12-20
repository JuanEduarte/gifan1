from odoo import api, fields, models
from datetime import datetime as dt, timedelta
from pytz import timezone





class GifBaseReport(models.Model):
    _name = 'gif.base.report'
    _description = 'Basic header for reports.'

    
    def _default_code_time(self):
        """Función para calcular el código de tiempo."""
        #code_time = (dt.datetime.now() - dt.timedelta(hours=5)).strftime('%Y%m%d_%H%M%S')
        code_time = self.with_user_timezone(dt.now()).strftime('%Y%m%d_%H%M%S')
        return code_time


    def _default_active_company(self):
        """Función que recupera el nombre de la compañia activa."""
        company_id = self.env.company.id
        return self.env['res.company'].search([('id','=', company_id)])

    def _default_date(self):
        return dt.now()

    def with_user_timezone(self, date_time):
        """Funcion que recibe una fecha (obj. date o datetime) y devuelve un datetime con la diferencia de zona horaria del usuario aplicada.
            params:
                date_time: Date o datetime en tiempo UTC

            return:
                date_time: Datetime con diferencia de zona horaria
        """
        # Convertimos a datetime
        dttm = fields.Datetime.to_datetime(date_time)
        # Obtenemos la diferencia de horas
        hrs_dif = str(dttm.astimezone(timezone(self.env.user.tz))).split('-')[-1].split(':')[0]
        delta = timedelta(hours=int(hrs_dif))
        return dttm + delta

  # Encabezado    
    code_time    = fields.Char(store=True, default=_default_code_time)
    name         = fields.Char(default="New",string="Reporte", readonly=True, store=True, compute='_compute_name_report')
    company_name = fields.Many2one('res.company', string="Compañía", readonly=True, store=True, default = _default_active_company)
    date         = fields.Date(string="Fecha", readonly=True, store=True, default =_default_date)
    title        = fields.Char(string="Titulo")

    @api.depends('code_time')
    def _compute_name_report(self):
        """Función para computar el nombre del reporte con base en el código de tiempo."""
        for record in self:
            print("Create date bigs: ",record.create_date)
            record.name = f'{record.title} {record.code_time}'