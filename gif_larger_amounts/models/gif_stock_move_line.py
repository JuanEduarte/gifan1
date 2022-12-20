
from datetime import date, datetime as dt, timedelta

from odoo import api, fields, models
from pytz import timezone

class GitStockPicking(models.Model):
    _inherit="stock.move.line"

    gif_unidad_stock=fields.Many2one('uom.uom', domain="[('category_id', '=', product_uom_category_id)]")

    
    @api.onchange('qty_done')
    def gif_unidad(self):
        for record in self:
            if record.qty_done > 0.1:
                record.gif_unidad_stock = 1 
        
    @api.onchange('gif_unidad_stock')
    def gif_unidad_oculto(self):
        for record in self:
                record.product_uom_id = record.gif_unidad_stock

    
    @api.onchange('expiration_date')
    def onchange_expiration_date(self):
        for record in self:
            if self.expiration_date:
                self.expiration_date = self.with_user_timezone(self.expiration_date)
                record.lot_name = str(self.with_user_timezone(self.expiration_date).date()).replace('-','')

    def with_user_timezone(self, date_time):
        """Funcion que recibe una fecha (obj. date o datetime) y devuelve un datetime con la diferencia de zona horaria del usuario aplicada.
            params:
                date_time - Date o datetime en tiempo UTC

                return - Datetime con diferencia de zona horaria
        """
        # Convertimos a datetime
        dttm = fields.Datetime.to_datetime(date_time)
        # Obtenemos la diferencia de horas
        hrs_dif = str(dttm.astimezone(timezone(self.env.user.tz))).split('-')[-1].split(':')[0]
        delta = timedelta(hours=int(hrs_dif))
        return dttm + delta