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
      Id_de_origen = []
      for record in self:
        originPartner = self.env['res.partner'].search([('name','ilike','GIFAN INTERNACIONAL S DE RL DE CV')])
        if record.Invoice_id:
          for j in record.Invoice_id.invoice_line_ids:
            originInvoice = self.env['sale.order'].search([('name','=',record.Invoice_id.invoice_origin)])
            Qty_done = self.env['stock.picking'].search([('origin','=',originInvoice.name),('picking_type_code','ilike','outgoing')])
            i=record.Invoice_id
           
           
            Dta = {
      ########DATOS DEL ORIGEN##########
          'Id de origen': record.IdDestino,
          'RFCOrigen': originPartner.vat,
          'Origen': originPartner.name,
          'NumRegIdTribO': record.NumRegIdTribO,
          'FechaSalida': record.FechaSalida,
          'HoraSalida':   record.HoraSalida,
          'DistanciaOrigen': record.DistanciaOrigen,
          'CalleOrigen': originPartner.street_name,
          'NumExtOrigen': 0,
          'NumIntOrigen': 0,
          'ColoniaOrigen': originPartner.l10n_mx_edi_colony,
          'LocalidadOrigen': originPartner.l10n_mx_edi_locality_id.name,
          'ReferenciaDestino': originPartner.ref,
          'MunicipioDestino': originPartner.city_id.name,
          'EstadoDestino': originPartner.state_id.name,
          'PaisDestino': originPartner.country_id.name,
          'CPDestino': originPartner.zip,
                  
      ########DATOS DEL DESTINO##########
          'Id de destino': record.IdOrigen,
          'RFC de Destino': i.partner_id.vat,
          'Destino': i.partner_id.name,
          'NumRegIdTribO': record.NumRegIdTribD,
          'FechaLlegada': record.FechaLlegada,
          'HoraLlegada':   record.HoraLlegada,
          'DistanciaDestino': record.DistanciaDestino,
          'CalleDestino': i.partner_id.street_name,
          'NumExtDestino': 0,
          'NumIntDestino': 0,
          'ColoniaDestino': i.partner_id.l10n_mx_edi_colony,
          'LocalidadDestino': i.partner_id.l10n_mx_edi_locality_id.name,
          'ReferenciaDestino': i.partner_id.ref,
          'MunicipioDestino': i.partner_id.city_id.name,
          'EstadoDestino': i.partner_id.state_id.name,
          'PaisDestino': i.partner_id.country_id.name,
          'CPDestino': i.partner_id.zip,
          
      ########DATOS DEL PRODUCTO##########
          'BienesTransp':j.product_id.name,
          #'ClaveSTCC': record.,
          'Mercancia':j.product_id.description_sale,
          'Cantidad': Qty_done.move_line_ids_without_package.qty_done,
          'ClaveUnidad':Qty_done.move_line_ids_without_package.product_uom_id.unspsc_code_id.code,
          'Unidad':Qty_done.move_line_ids_without_package.product_uom_id.category_id.name,
          'Dimensiones':j.product_id.volume,
          'MaterialPeligroso':j.product_id.gif_hazard_active,
          'CveMaterialPeligroso':j.product_id.	l10n_mx_edi_hazardous_material_code,
          'Embalaje':j.product_id.l10n_mx_edi_hazard_package_type,
          'PesoEnKg':j.product_id.weight,
          'ValorMercancia':originInvoice.order_line.price_subtotal,
          'Moneda':i.currency_id.name,
          'FraccionArancelaria':j.product_id.l10n_mx_edi_tariff_fraction_id,
          'UUIDComercioExt':i.gif_invoice_uuid,
          'Pedimento':j.l10n_mx_edi_customs_number,
          
          }
            
        
          print('##########', self.Invoice_id)
          df = pd.DataFrame([Dta], index= [0])
          default_style = Styler(font_size=7) 
          sf = StyleFrame(df, styler_obj=default_style)
         
          sf.apply_headers_style(styler_obj=Styler(bold=False,
                                         bg_color=utils.colors.blue,
                                         font_size=7))
          
          sf.to_excel('/odoo/custom/addons/Report_data/carta7.xlsx').save()
