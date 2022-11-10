import pandas as pd
from styleframe import StyleFrame, Styler, utils
from odoo import api, fields, models


class ConsignmentNote(models.Model):
    _name = 'gif.consignment.note'
    _description = 'Creaciion de archivo exel con la informacion requerida de la carta porte'

    Invoice_id = fields.Many2one('account.move', string='Id de factura',
                                 context="{'Invoice_id': context.get('Invoice_id', False)}")
    Partner_id = fields.Many2one('res.partner', string='Id de cliente')
    inverse_account_move = fields.Many2one('account.move', strng='factura')

    IdOrigen = fields.Char(string='Id de origen')
    NumRegIdTribO = fields.Char(string='Número de registro Tributario')
    FechaSalida = fields.Date(string='Fecha de salida')
    HoraSalida = fields.Datetime(string='Hora de salida')
    DistanciaOrigen = fields.Integer(string='Distancia origen')
    IdDestino = fields.Char(string='Id de destino')
    NumRegIdTribD = fields.Char(string='Número de registro Tributario')
    FechaLlegada = fields.Date(string='Fecha de llegada')
    HoraLlegada = fields.Datetime(string='Hora de llegada')
    DistanciaDestino = fields.Integer(string='Distancia destino')
    UUIDComercioExt = fields.Integer(string='UUID de Comercio exterior')


    @api.model
    def default_get(self, fields):
        rec = super(ConsignmentNote, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['Invoice_id'] = id_ctx
        return rec

    def create_report(self):
      for record in self:
        if record.Invoice_id:
          print (record.Invoice_id.invoice_line_ids.name)
          i=record.Invoice_id
          Dta = {
        #'Partner_id': i.partner_id.name,
        'Id de origen': record.IdOrigen,
        'RFCOrigen': i.partner_id.vat,
        'Origen': i.partner_id.name,
        'NumRegIdTribO': record.NumRegIdTribD,
        'FechaSalida': record.FechaSalida,
        'HoraSalida':   record.HoraSalida,
        'DistanciaOrigen': record.DistanciaOrigen,
        'CalleOrigen': i.partner_id.street_name,
        'NumExtOrigen': 0,
        'NumIntOrigen': 0,
        'ColoniaOrigen': i.partner_id.l10n_mx_edi_colony,
        'LocalidadOrigen': i.partner_id.l10n_mx_edi_locality_id.name,
        'ReferenciaOrigen': i.partner_id.ref,
        'MunicipioOrigen': i.partner_id.city_id.name,
        'EstadoOrigen': i.partner_id.state_id.name,
        'PaisOrigen': i.partner_id.country_id.name,
        'CPOrigen': i.partner_id.zip,
        }
          
        
          print('ppppppppAAA', self.Invoice_id)
          df = pd.DataFrame([Dta], index= [0])
          default_style = Styler(font_size=7) 
          sf = StyleFrame(df, styler_obj=default_style)
         
          sf.apply_headers_style(styler_obj=Styler(bold=False,
                                         bg_color=utils.colors.blue,
                                         font_size=7))
          
          sf.to_excel('/odoo/custom/addons/Report_data/carta3.xlsx').save()
