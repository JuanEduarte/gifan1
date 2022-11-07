import base64
from ensurepip import version
from shutil import move
import requests
from pprint import pprint
from io import BytesIO
from zipfile import ZipFile
from lxml import etree
from lxml.objectify import fromstring
import re
from odoo import fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class WizardXmlUpdater(models.TransientModel):
    _name = 'wizard.xml.updater'
    _description = 'Cargador de archivos XML'

    name = fields.Char(string='Nombre del archivo')
    xml_files = fields.Binary('Archivos XML')

    num_files_upload = fields.Integer(default=0)
    num_files_duplicated = fields.Integer(default=0)

    def upload_files(self):
        for record in self:
            values = self.gif_upload_files()
            #return {'type': 'ir.actions.client', 'tag': 'reload'}
            txt_upload = "Se subieron %s archivos a la plataforma exitosamente. \n" % (record.num_files_upload)
            txt_duplicated = "Se omitieron %s archivos por duplicidad. Favor de revisar." % (record.num_files_duplicated)

            return {
                'name': 'Notificación de carga XML',
                'context':{'default_text_notification':txt_upload + txt_duplicated},
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.notification.reload',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                }

    def gif_upload_files(self):
        for record in self:
            zip_file = base64.decodebytes(record.xml_files)
            zipfile = ZipFile(BytesIO(zip_file), "r")

            # NSMAP = {
            #     'xsi':'http://www.w3.org/2001/XMLSchema-instance',
            #     'cfdi':'http://www.sat.gob.mx/cfd/3',
            #     'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
            # }

            values = {}
            for file in zipfile.namelist():
                if '.xml' in file:

                    _file = zipfile.open(file).read()
                    fact_b64 = base64.b64encode(_file)
                    file_xml_tree_root = etree.fromstring(_file)
                    file_str = _file.decode('UTF-8')

                    # NSMAP
                    xsi_re = re.search('xsi="(\S*)"', file_str)
                    cfdi_re = re.search('cfdi="(\S*)"', file_str)
                    tfd_re = re.search('tfd="(\S*)"', file_str)

                    if not all([xsi_re, cfdi_re, tfd_re]):
                        raise ValidationError(f'El archivo {file} no contiene algunos de los siguientes valores: xsi, cfdi, tfd.')

                    NSMAP = {
                        'xsi': xsi_re.group(1),
                        'cfdi': cfdi_re.group(1),
                        'tfd': tfd_re.group(1)
                    }

                    # # Busqueda de UUID
                    complement = file_xml_tree_root.find("cfdi:Complemento", NSMAP)
                    stamp = complement.find("tfd:TimbreFiscalDigital", NSMAP)
                    uuid = stamp.attrib['UUID']
                    timdate = stamp.attrib['FechaTimbrado']

                    # Duplicidad
                    xml_files = self.env['gif.purchase.xml.updater'].search([('gif_uuid','=',uuid)])

                    if xml_files:
                        # Ya existe
                        record.num_files_duplicated += 1
                        continue

                    # Busqueda de Emisor
                    emisor = file_xml_tree_root.find("cfdi:Emisor", NSMAP)
                    rfc_emisor = emisor.attrib['Rfc']
                    name_emisor = emisor.attrib['Nombre']

                    # Busqueda de Receptor
                    receptor = file_xml_tree_root.find("cfdi:Receptor", NSMAP)
                    rfc_receptor = receptor.attrib['Rfc']
                    name_receptor = receptor.attrib['Nombre']

                    # Busqueda de Datos de Factura
                    total = file_xml_tree_root.attrib['Total']
                    name = file_xml_tree_root.attrib['Serie']
                    folio = file_xml_tree_root.attrib['Folio']

                    if '/' in file:
                        fname = file.split('/')[1]
                    else:
                        fname = file

                    invoice_data = {
                        'name': name+folio,
                        'gif_uuid': uuid,
                        'gif_rfc_issuer': rfc_emisor,
                        'gif_name_issuer': name_emisor,
                        'gif_rfc_receiver': rfc_receptor,
                        'gif_name_receiver': name_receptor,
                        'gif_file_type': file.split('.')[-1],
                        'gif_total': total,
                        'gif_filename': fname,
                        'gif_date_timb': timdate.replace('T', ' '),
                        'gif_attachment_64': fact_b64,
                        'gif_attachment_raw': _file,
                        }

                    invoice_data['gif_status'] = self.validate_xml_sat(invoice_data['gif_rfc_issuer'], 
                                        invoice_data['gif_rfc_receiver'], 
                                        invoice_data['gif_total'], 
                                        invoice_data['gif_uuid'])

                    xml_model = self.env['gif.purchase.xml.updater'].create(invoice_data)
                    
                    attached = self.env['ir.attachment'].create({
                                    'name': fname,
                                    'type': 'binary',
                                    'datas': base64.b64encode(_file),
                                    'store_fname': fname,
                                    'res_model': 'gif.purchase.xml.updater',
                                    'res_id': xml_model.id,
                                    'mimetype': 'application/xml'
                                })

                    record.num_files_upload += 1

                    values[name] = invoice_data
                    
                    # Asociacion de XML a factura o al pago
                    try:
                        move_id = self.env['account.move'].search([('gif_invoice_uuid','=',uuid),('move_type','=','in_invoice')])
                        if move_id:
                            move_id.attachment_updater(xml_model)
                        else:
                            payment_id = self.env['account.payment'].search([('gif_payment_uuid','=',uuid),('payment_type','=','outbound')])
                            if payment_id:
                                payment_id.attachment_updater(xml_model)
                    except:
                        pass
            
            for file in zipfile.namelist():
                if '.pdf' in file:
                    _file = zipfile.open(file).read()
                    
                    if '/' in file:
                        fname = file.split('/')[1]
                    else:
                        fname = file

                    fname = fname.replace('.pdf','')
                    
                    # Duplicidad
                    pdf_files = self.env['ir.attachment'].search([('name','=',fname)])
                    if pdf_files:
                        # Ya existe
                        record.num_files_duplicated += 1
                        continue
                    
                    xml_model = self.env['gif.purchase.xml.updater'].search([('gif_uuid','like',fname)])

                    attached = self.env['ir.attachment'].create({
                                    'name': fname,
                                    'type': 'binary',
                                    'datas': base64.b64encode(_file),
                                    'store_fname': fname,
                                    'res_model': 'gif.purchase.xml.updater',
                                    'res_id': xml_model.id,
                                    'mimetype': 'application/pdf'
                                })

                    record.num_files_upload += 1

                    xml_model.update({'gif_attachment_pdf':_file,
                                        'gif_pdf':True})

                    # Asociacion de XML a factura o al pago
                    
                    try:
                        move_id = self.env['account.move'].search([('gif_invoice_uuid','=',uuid),('move_type','=','in_invoice')])
                        if len(move_id) == 1:
                            move_id.attachment_updater(xml_model)
                        else:
                            payment_id = self.env['account.payment'].search([('gif_payment_uuid','=',uuid),('payment_type','=','outbound')])
                            if len(payment_id) == 1:
                                payment_id.attachment_updater(xml_model)
                    except:
                        pass

            return values



    def validate_xml_sat(self, supplier_rfc, customer_rfc, total, uuid):
        url = 'https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc?wsdl'
        headers = {'SOAPAction': 'http://tempuri.org/IConsultaCFDIService/Consulta', 'Content-Type': 'text/xml; charset=utf-8'}
        template = """<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:ns0="http://tempuri.org/" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <ns1:Body>
                <ns0:Consulta>
                    <ns0:expresionImpresa>${data}</ns0:expresionImpresa>
                </ns0:Consulta>
            </ns1:Body>
        </SOAP-ENV:Envelope>"""
        namespace = {'a': 'http://schemas.datacontract.org/2004/07/Sat.Cfdi.Negocio.ConsultaCfdi.Servicio'}
        params = '?re=%s&amp;rr=%s&amp;tt=%s&amp;id=%s' % (
            tools.html_escape(supplier_rfc or ''),
            tools.html_escape(customer_rfc or ''),
            total or 0.0, uuid or '')
        soap_env = template.format(data=params)
        #An exception might be raised here and should be managed by the calling function
        soap_xml = requests.post(url, data=soap_env, headers=headers, timeout=20)
        # print(soap_xml.text)
        response = fromstring(soap_xml.text)
        fetched_status = response.xpath('//a:Estado', namespaces=namespace)
        status = fetched_status[0] if fetched_status else ''
        return status