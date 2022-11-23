import base64
import os  
import zipfile
import pandas as pd
from odoo import api, fields, models


class ConsignmentNote(models.TransientModel):
    _name = 'gif.consignment.note'
    _description = 'Creaciion de archivo exel con la informacion requerida de la carta porte'

    Invoice_id = fields.Many2one('account.move', string='Id de factura' )
    Partner_id = fields.Many2one('res.partner', string='Id de cliente')
    inverse_account_move = fields.Many2one('account.move', string='factura')

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
    get_template = fields.Binary('Template')

    invoice_ids = []

    @api.model
    def default_get(self, fields):
        rec = super(ConsignmentNote, self).default_get(fields)
        id_ctx = self.env.context.get('active_ids', False)
        rec['Invoice_id'] = id_ctx
        for i in id_ctx:
          if i not in self.invoice_ids:
            self.invoice_ids.append(i)
        return rec
          

    def create_report(self):
      for record in self:
        
        for folder, subfolders, files in os.walk('/odoo/custom/addons/Report_data/'):
          for file in files:
            os.remove('/odoo/custom/addons/Report_data/'+file)
        
        for i in self.invoice_ids:
          Dta = []
          Inv = self.env['account.move'].search([('id','=', i)])
          for record in self:
            originPartner = self.env['res.partner'].search([('name','ilike','GIFAN INTERNACIONAL S DE RL DE CV')])
            if Inv:
              for j in Inv.invoice_line_ids:
                originInvoice = self.env['sale.order'].search([('name','=',Inv.invoice_origin)])
                Qty_done = self.env['stock.picking'].search([('origin','=',originInvoice.name),('picking_type_code','ilike','outgoing')])
                i=Inv
                Dta.append((
          ########DATOS DEL ORIGEN##########
              record.IdDestino,
              originPartner.vat,
              originPartner.name,
              record.NumRegIdTribO,
              record.FechaSalida,
              record.HoraSalida,
              record.DistanciaOrigen,
              originPartner.street_name,
              originPartner.street_number,
              originPartner.street_number2,
              originPartner.l10n_mx_edi_colony,
              originPartner.l10n_mx_edi_locality_id.name,
              originPartner.ref,
              originPartner.city_id.name,
              originPartner.state_id.name,
              originPartner.country_id.name,
              originPartner.zip,
                      
          ########DATOS DEL DESTINO##########
              record.IdOrigen,
              i.partner_id.vat,
              i.partner_id.name,
              record.NumRegIdTribD,
              record.FechaLlegada,
              record.HoraLlegada,
              record.DistanciaDestino,
              i.partner_id.street_name,
              i.street_number,
              i.street_number2,
              i.partner_id.l10n_mx_edi_colony,
              i.partner_id.l10n_mx_edi_locality_id.name,
              i.partner_id.ref,
              i.partner_id.city_id.name,
              i.partner_id.state_id.name,
              i.partner_id.country_id.name,
              i.partner_id.zip,
              
          ########DATOS DEL PRODUCTO##########
              j.product_id.name,
              j.product_id.ClaveSTCC, 
              j.product_id.description_sale,
              Qty_done.move_line_ids_without_package.qty_done,
              Qty_done.move_line_ids_without_package.product_uom_id.unspsc_code_id.code,
              Qty_done.move_line_ids_without_package.product_uom_id.category_id.name,
              j.product_id.volume,
              j.product_id.gif_hazard_active,
              j.product_id.	l10n_mx_edi_hazardous_material_code,
              j.product_id.l10n_mx_edi_hazard_package_type,
              j.product_id.weight,
              originInvoice.order_line.price_subtotal,
              i.currency_id.name,
              j.product_id.l10n_mx_edi_tariff_fraction_id,
              i.gif_invoice_uuid,
              j.l10n_mx_edi_customs_number
              ))
          string = i.name
          new_string = string.replace('/', "")
            
          df = pd.DataFrame(Dta, columns=['Id de origen','RFCOrigen','Origen','NumRegIdTribO','FechaSalida','HoraSalida','DistanciaOrigen','CalleOrigen','NumExtOrigen','NumIntOrigen','ColoniaOrigen','LocalidadOrigen','ReferenciaOrigen','MunicipioOrigen','EstadoOrigen','PaisOrigen','CPOrigen',    'Id de destino','RFC de Destino','Destino','NumRegIdTribD','FechaLlegada', 'HoraLlegada','DistanciaDestino','CalleDestino','NumExtDestino','NumIntDestino','ColoniaDestino','LocalidadDestino','ReferenciaDestino','MunicipioDestino','EstadoDestino','PaisDestino','CPDestino','BienesTransp','Clave STCC','Mercancia', 'Cantidad','ClaveUnidad','Unidad','Dimensiones','MaterialPeligroso','CveMaterialPeligroso','Embalaje','PesoEnKg','ValorMercancia','Moneda','FraccionArancelaria','UUIDComercioExt','Pedimento'])
          df1 = pd.DataFrame( columns=['TipoFigura','RFC','Nombre','licencia','Pais','NumRegIdTribO','ParteTransporte'])
          df2 = pd.DataFrame( columns=['PermisoSCT','NoPermiso','Configuracinvehicular','Placas','Modelo','Remolque1','Placas1','Remolque2','Placas2','AseguradoraCivil','PolizaCivil','AseguradoraMedioAmb','PolizaMedioAmb','AseguradoraCarga','Polizacarga','PrimaSeguro'])
          
          with pd.ExcelWriter('/odoo/custom/addons/Report_data/'+ new_string +'.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer,  sheet_name='CartaPorte')
            df1.to_excel(writer, sheet_name='FigurasTransporte')
            df2.to_excel(writer, sheet_name='Transporte')
          
      
        
        
        fantasy_zip = zipfile.ZipFile('/odoo/custom/addons/Report_data/'+ new_string + '.zip', 'w')
        for folder, subfolders, files in os.walk('/odoo/custom/addons/Report_data/'):
          for file in files:
            if file.endswith('.xlsx'):
              fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), '/odoo/custom/addons/Report_data/'), compress_type = zipfile.ZIP_DEFLATED)     
        fantasy_zip.close()
        
        xb = open("/odoo/custom/addons/Report_data/"+ new_string + '.zip', 'rb').read()
        base64_encoded = base64.b64encode(xb).decode('UTF-8')
        self.get_template = base64_encoded
        

      return {
            'type': 'ir.actions.act_window',
            'res_model': 'gif.consignment.note',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id':self.id,
            }

   