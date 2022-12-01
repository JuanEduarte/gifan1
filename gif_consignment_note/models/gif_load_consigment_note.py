from odoo import models, fields, api, _
import pandas as pd
import base64



class GifloadNote(models.Model):
    _name = 'gif.load.note'

    name = fields.Char(string='Reporte de Carta Porte',index=True, default=lambda self: _('New'))
    file = fields.Binary(string='Suba su archivo')
    IdOrigen             = fields.Char(string='Id de origen')
    RFCOrigen            = fields.Char(string='RFCOrigen')
    Origen               = fields.Char(string='Origen')
    NumRegIdTribO        = fields.Char(string='NumRegIdTribO')
    FechaSalida          = fields.Char(string='FechaSalida')
    HoraSalida           = fields.Char(string='HoraSalida')
    DistanciaOrigen      = fields.Char(string='DistanciaOrigen')
    CalleOrigen          = fields.Char(string='CalleOrigen')
    NumExtOrigen         = fields.Char(string='NumExtOrigen')
    NumIntOrigen         = fields.Char(string='NumIntOrigen')
    ColoniaOrigen        = fields.Char(string='ColoniaOrigen')
    LocalidadOrigen      = fields.Char(string='LocalidadOrigen')
    ReferenciaOrigen     = fields.Char(string='ReferenciaDestino')
    MunicipioOrigen      = fields.Char(string='MunicipioDestino')
    EstadoOrigen         = fields.Char(string='EstadoDestino')
    PaisOrigen           = fields.Char(string='PaisDestino')
    CPOrigen             = fields.Char(string='CPDestino')
    IdDestino            = fields.Char(string='Id de destino')
    RFCDestino           = fields.Char(string='RFCDestino')
    Destino              = fields.Char(string='Destino')
    NumRegIdTribD        = fields.Char(string='NumRegIdTribD')
    FechaLlegada         = fields.Char(string='FechaLlegada')
    HoraLlegada          = fields.Char(string='FechaLlegada')
    DistanciaDestino     = fields.Char(string='DistanciaDestino')
    CalleDestino         = fields.Char(string='CalleDestino')
    NumExtDestino        = fields.Char(string='NumExtDestino')
    NumIntDestino        = fields.Char(string='NumIntDestino')
    ColoniaDestino       = fields.Char(string='ColoniaDestino')
    LocalidadDestino     = fields.Char(string='LocalidadDestino')
    ReferenciaDestino    = fields.Char(string='ReferenciaDestino')
    MunicipioDestino     = fields.Char(string='MunicipioDestino')
    EstadoDestino        = fields.Char(string='EstadoDestino')
    PaisDestino          = fields.Char(string='PaisDestino')
    CPDestino            = fields.Char(string='CPDestino')

    ConfType              = fields.Many2one(comodel_name='l10n_mx_edi.vehicle', string='Configuracion del vehiculo')
    PermisoSCT            = fields.Char(string='PermisoSCT')
    NoPermiso             = fields.Char(string='NoPermiso')
    Configuracinvehicular = fields.Char(string='Configuracinvehicular')
    Placas                = fields.Char(string='Placas')
    Modelo                = fields.Char(string='Modelo')
    Remolque1             = fields.Char(string='Remolque1')
    Placas1               = fields.Char(string='Placas1')
    Remolque2             = fields.Char(string='Remolque2')
    Placas2               = fields.Char(string='Placas2')
    AseguradoraCivil      = fields.Char(string='AseguradoraCivil')
    PolizaCivil           = fields.Char(string='PolizaCivil')
    AseguradoraMedioAmb   = fields.Char(string='AseguradoraMedioAmb')
    PolizaMedioAmb        = fields.Char(string='PolizaMedioAmb')
    AseguradoraCarga      = fields.Char(string='AseguradoraCarga')
    Polizacarga           = fields.Char(string='Polizacarga')
    PrimaSeguro           = fields.Char(string='PrimaSeguro')
    
    CartaPorte_page        = fields.One2many(comodel_name='consignment.note.report', inverse_name='Origin_report_data', string='Page de la carta')
    FigurasTransporte_page = fields.One2many(comodel_name='figuras.transporte.page', inverse_name='FigurasTransporte_report', string='Page de las figuras de transporte', store=True)
    
    
    @api.model
    def create(self, vals):
      if vals.get('name', _('New')) == _('New'):
        vals['name'] = self.env['ir.sequence'].next_by_code('gif.load.note') or _('New')
      result = super(GifloadNote, self).create(vals)
      return result
    
    @api.onchange('ConfType')
    def _onchange_ConfType(self):
      for record in self:
        if  self.ConfType.trailer_ids:
          if self.ConfType.trailer_ids[0]:
            record.Remolque1 = self.ConfType.trailer_ids[0].sub_type
            record.Placas1 = self.ConfType.trailer_ids[0].name
          else: pass
          if self.ConfType.trailer_ids[1]:
            record.Remolque2 = self.ConfType.trailer_ids[1].sub_type
            record.Placas2 = self.ConfType.trailer_ids[1].name
          else: pass
        
        record.PermisoSCT = self.ConfType.transport_perm_sct
        record.NoPermiso = self.ConfType.name
        record.Configuracinvehicular = self.ConfType.vehicle_config
        record.Placas = self.ConfType.vehicle_licence
        record.Modelo = self.ConfType.vehicle_model
        
   
        
        record.AseguradoraCivil = self.ConfType.transport_insurer
        record.PolizaCivil = self.ConfType.transport_insurance_policy
        record.AseguradoraMedioAmb = self.ConfType.environment_insurer
        record.PolizaMedioAmb = self.ConfType.environment_insurance_policy
        
        origin = self.env['res.partner'].search([('id','=','7')])
        
      for i in self.ConfType.figure_ids:
        
        figure_line = self.env['figuras.transporte.page'].create([{
          'FigurasTransporte_report': self.id,
          'TipoFigura': i.type,
          'RFC': origin.vat,
          'Nombre': origin.name,
          'licencia':origin.l10n_mx_edi_operator_licence,
          'Pais': origin.country_id.name,
        }])


    def files_data(self):
        list1 = []
        
        for record in self:
            list1.append((record.id, record.ConfType.name, record.PermisoSCT))
            data = record.file
            file_contents = base64.decodestring(data)
            xlsx = pd.ExcelFile(file_contents, engine='openpyxl')
            df = pd.read_excel(xlsx, sheet_name='CartaPorte')
         
            for i in df.index:
              typef = self.env['l10n_mx_edi.vehicle'].search([('id', '=', 7)])
              report_rel = self.env['consignment.note.report'].create([{
                'Origin_report_data' : self.id,
                'BienesTransp'       : df[['BienesTransp'][0]][i],
                'ClaveSTCC'          : df[['Clave STCC'][0]][i],
                'Mercancia'          : df[['Mercancia'][0]][i],
                'Cantidad'           : df[['Cantidad'][0]][i],
                'ClaveUnidad'        : df[['ClaveUnidad'][0]][i],
                'Unidad'             : df[['Unidad'][0]][i],
                'Dimensiones'        : df[['Dimensiones'][0]][i],
                'MaterialPeligroso'  : df[['MaterialPeligroso'][0]][i],
                'CveMaterialPeligroso': df[['CveMaterialPeligroso'][0]][i],
                'Embalaje'           : df[['Embalaje'][0]][i],
                'PesoEnKg'           : df[['PesoEnKg'][0]][i],
                'ValorMercancia'     : df[['ValorMercancia'][0]][i],
                'Moneda'             : df[['Moneda'][0]][i],
                'FraccionArancelaria': df[['FraccionArancelaria'][0]][i],
                'UUIDComercioExt'    : df[['UUIDComercioExt'][0]][i],
                'Pedimento'          : df[['Pedimento'][0]][i],
              }])

            
        self.IdOrigen          = df[['Id de origen'][0]][0]
        self.RFCOrigen         = df[['RFCOrigen'][0]][0]
        self.Origen            = df[['Origen'][0]][0]
        self.NumRegIdTribO     = df[['NumRegIdTribO'][0]][0]
        self.FechaSalida       = df[['FechaSalida'][0]][0]
        self.HoraSalida        = df[['HoraSalida'][0]][0]
        self.DistanciaOrigen   = df[['DistanciaOrigen'][0]][0]
        self.CalleOrigen       = df[['CalleOrigen'][0]][0]
        self.NumExtOrigen      = df[['NumExtOrigen'][0]][0]
        self.NumIntOrigen      = df[['NumIntOrigen'][0]][0]
        self.ColoniaOrigen     = df[['ColoniaOrigen'][0]][0]
        self.LocalidadOrigen   = df[['LocalidadOrigen'][0]][0]
        self.ReferenciaOrigen  = df[['ReferenciaOrigen'][0]][0]
        self.MunicipioOrigen   = df[['MunicipioOrigen'][0]][0]
        self.EstadoOrigen      = df[['EstadoOrigen'][0]][0]
        self.PaisOrigen        = df[['PaisOrigen'][0]][0]
        self.CPOrigen          = df[['CPOrigen'][0]][0]
        self.IdDestino         = df[['Id de destino'][0]][0]
        self.RFCDestino        = df[['RFC de Destino'][0]][0]
        self.Destino           = df[['Destino'][0]][0]
        self.NumRegIdTribD     = df[['NumRegIdTribD'][0]][0]
        self.FechaLlegada      = df[['FechaLlegada'][0]][0]
        self.HoraLlegada       = df[['HoraLlegada'][0]][0]
        self.DistanciaDestino  = df[['DistanciaDestino'][0]][0]
        self.CalleDestino      = df[['CalleDestino'][0]][0]
        self.NumExtDestino     = df[['NumExtDestino'][0]][0]
        self.NumIntDestino     = df[['NumIntDestino'][0]][0]
        self.ColoniaDestino    = df[['ColoniaDestino'][0]][0]
        self.LocalidadDestino  = df[['LocalidadDestino'][0]][0]
        self.ReferenciaDestino = df[['ReferenciaDestino'][0]][0]
        self.MunicipioDestino  = df[['MunicipioDestino'][0]][0]
        self.EstadoDestino     = df[['EstadoDestino'][0]][0]
        self.PaisDestino       = df[['PaisDestino'][0]][0]
        self.CPDestino         = df[['CPDestino'][0]][0]
    
    Dta1 = []
    Dta2 = []
    Dta3 = []
    @api.onchange('ConfType')
    def get_full_data(self):
      for record in self:
        for i in record.CartaPorte_page:
          self.Dta1.append((
                            self.IdOrigen,
                            self.RFCOrigen,
                            self.Origen,
                            self.NumRegIdTribO,
                            self.FechaSalida,
                            self.HoraSalida,
                            self.DistanciaOrigen,
                            self.CalleOrigen,
                            self.NumExtOrigen,
                            self.NumIntOrigen,
                            self.ColoniaOrigen,
                            self.LocalidadOrigen,
                            self.ReferenciaOrigen,
                            self.MunicipioOrigen,
                            self.EstadoOrigen,
                            self.PaisOrigen,
                            self.CPOrigen,
                            self.IdDestino,
                            self.RFCDestino,
                            self.Destino,
                            self.NumRegIdTribD,
                            self.FechaLlegada,
                            self.HoraLlegada,
                            self.DistanciaDestino,
                            self.CalleDestino,
                            self.NumExtDestino,
                            self.NumIntDestino,
                            self.ColoniaDestino,
                            self.LocalidadDestino,
                            self.ReferenciaDestino,
                            self.MunicipioDestino,
                            self.EstadoDestino,
                            self.PaisDestino,
                            self.CPDestino,
                            i.BienesTransp, 
                            i.ClaveSTCC,
                            i.Mercancia,
                            i.Cantidad,
                            i.ClaveUnidad,
                            i.Unidad,
                            i.Dimensiones,
                            i.MaterialPeligroso,
                            i.CveMaterialPeligroso,
                            i.Embalaje,
                            i.PesoEnKg,
                            i.ValorMercancia,
                            i.Moneda,
                            i.FraccionArancelaria,
                            i.UUIDComercioExt,
                            i.Pedimento,
                            ))
                 
        for j in record.FigurasTransporte_page:
          self.Dta2.append((
            j.TipoFigura,
            j.RFC,
            j.Nombre,
            j.licencia,
            j.Pais,
            j.NumRegIdTribO,
            j.ParteTransporte,
          ))
           
      self.Dta3.append((
            self.PermisoSCT,           
            self.NoPermiso,            
            self.Configuracinvehicular,
            self.Placas,              
            self.Modelo,               
            self.Remolque1,            
            self.Placas1,              
            self.Remolque2,           
            self.Placas2,              
            self.AseguradoraCivil,     
            self.PolizaCivil,          
            self.AseguradoraMedioAmb,  
            self.PolizaMedioAmb,       
            self.AseguradoraCarga,     
            self.Polizacarga,          
            self.PrimaSeguro,          
      ))
      
      
      df  = pd.DataFrame(self.Dta1, columns=['Id de origen','RFCOrigen','Origen','NumRegIdTribO','FechaSalida','HoraSalida','DistanciaOrigen','CalleOrigen','NumExtOrigen','NumIntOrigen','ColoniaOrigen','LocalidadOrigen','ReferenciaOrigen','MunicipioOrigen','EstadoOrigen','PaisOrigen','CPOrigen',    'Id de destino','RFC de Destino','Destino','NumRegIdTribD','FechaLlegada', 'HoraLlegada','DistanciaDestino','CalleDestino','NumExtDestino','NumIntDestino','ColoniaDestino','LocalidadDestino','ReferenciaDestino','MunicipioDestino','EstadoDestino','PaisDestino','CPDestino','BienesTransp','Clave STCC','Mercancia', 'Cantidad','ClaveUnidad','Unidad','Dimensiones','MaterialPeligroso','CveMaterialPeligroso','Embalaje','PesoEnKg','ValorMercancia','Moneda','FraccionArancelaria','UUIDComercioExt','Pedimento'])
      df1 = pd.DataFrame(self.Dta2, columns=['TipoFigura','RFC','Nombre','licencia','Pais','NumRegIdTribO','ParteTransporte'])
      df2 = pd.DataFrame(self.Dta3, columns=['PermisoSCT','NoPermiso','Configuracinvehicular','Placas','Modelo','Remolque1','Placas1','Remolque2','Placas2','AseguradoraCivil','PolizaCivil','AseguradoraMedioAmb','PolizaMedioAmb','AseguradoraCarga','Polizacarga','PrimaSeguro'])
          
      with pd.ExcelWriter('data.xlsx', engine='xlsxwriter') as writer:
          df.to_excel (writer,  sheet_name='CartaPorte')
          df1.to_excel(writer, sheet_name='FigurasTransporte')
          df2.to_excel(writer, sheet_name='Transporte')
      writer.close()
      
      
      encoded = base64.b64encode(open(writer, 'rb').read())
      
      record.file = encoded
      
      
      
             #######Modelos de tablas o pages#######

  #*****************Descripcion de origen, destino y Prooductos**************
    class ModuleName(models.Model):
        _name = 'consignment.note.report'
        _description = 'Visualizacion de Hoja de la carta porte del archivo cargado'


        Origin_report_data = fields.Many2one(comodel_name='gif.load.note', string='Carta Porte Data')
        
        BienesTransp         = fields.Char(string='BienesTransp')
        ClaveSTCC            = fields.Char(string='Clave STCC')       
        Mercancia            = fields.Char(string='Mercancia')
        Cantidad             = fields.Char(string='Cantidad')
        ClaveUnidad          = fields.Char(string='ClaveUnidad')
        Unidad               = fields.Char(string='Unidad')
        Dimensiones          = fields.Char(string='Dimensiones')
        MaterialPeligroso    = fields.Char(string='MaterialPeligroso')
        CveMaterialPeligroso = fields.Char(string='CveMaterialPeligroso')
        Embalaje             = fields.Char(string='Embalaje')
        PesoEnKg             = fields.Char(string='PesoEnKg')
        ValorMercancia       = fields.Char(string='ValorMercancia')
        Moneda               = fields.Char(string='Moneda')
        FraccionArancelaria  = fields.Char(string='FraccionArancelaria')
        UUIDComercioExt      = fields.Char(string='UUIDComercioExt')
        Pedimento            = fields.Char(string='Pedimento')

        

#*****************Descripcion de Figuras de transporte**************
    class FigurasTransporte(models.Model):
        _name = 'figuras.transporte.page'
        _description = 'Page de el reporte de las figurs de transporte'

        def values_fig(self):
          typef = self.env['res.partner'].search([('partner_id.name', 'ilike', 'fermont')])
        
        FigurasTransporte_report = fields.Many2one(comodel_name='gif.load.note', string='Figuras de trasnporte')
                
        TipoFigura      = fields.Selection(string='TipoFigura', selection=[('01', 'Operador'), ('02', 'Propietario'),('03', 'Arrendador'),('04', 'Notificado')])
        RFC             = fields.Char(string='RFC')
        Nombre          = fields.Char(string='Nombre')
        licencia        = fields.Char(string='licencia')
        Pais            = fields.Char(string='Pais')
        NumRegIdTribO   = fields.Char(string='NumRegIdTribO')
        ParteTransporte = fields.Char(string='ParteTransporte')    
                
       
