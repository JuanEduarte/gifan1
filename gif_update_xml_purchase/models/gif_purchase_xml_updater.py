from cmath import atan
from odoo import api, fields, models
import requests
from odoo import fields, models, tools
from lxml.objectify import fromstring

class GifPurchaseXMLUpdater(models.Model):
    _name = 'gif.purchase.xml.updater'
    _description = 'Modelo de subida de xml'
    _order = 'id desc'

    name = fields.Char(string='Factura')
    gif_rfc_issuer = fields.Char(string='RFC Emisor')
    gif_name_issuer = fields.Char(string='Nombre Emisor')
    gif_rfc_receiver = fields.Char(string='RFC Receptor')
    gif_name_receiver = fields.Char(string='RFC Receptor')
    gif_filename = fields.Char(string='Nombre del archivo')
    gif_file_type = fields.Char(string='Tipo')
    gif_uuid = fields.Char(string='UUID')
    gif_total = fields.Float(string='Total a pagar')
    gif_account_move = fields.Many2one('account.move', string='Factura')
    gif_account_payment = fields.Many2one('account.payment', string='Pago')
    gif_attachment_64 = fields.Binary(string='XML base64')
    gif_attachment_raw = fields.Binary(string='XML RAW')
    gif_date_timb = fields.Datetime(string='Fecha de timbrado')
    gif_status = fields.Char(string='Estatus SAT')
    gif_duplicidad = fields.Boolean(string='Duplicidad')
    gif_attachment_pdf = fields.Binary(string="PDF Raw")
    gif_pdf = fields.Boolean(string="PDF")

    def gif_validate_cfdi(self):
        for record in self:
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
                tools.html_escape(record.gif_rfc_issuer or ''),
                tools.html_escape(record.gif_rfc_receiver or ''),
                record.gif_total or 0.0, record.gif_uuid or '')
            soap_env = template.format(data=params)
            #An exception might be raised here and should be managed by the calling function
            soap_xml = requests.post(url, data=soap_env, headers=headers, timeout=20)
            # print(soap_xml.text)
            response = fromstring(soap_xml.text)
            fetched_status = response.xpath('//a:Estado', namespaces=namespace)
            status = fetched_status[0] if fetched_status else ''
            record.gif_status = status

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('full_code'):
                name = f'{record.name} / {record.gif_uuid} / ${record.gif_total}'
            else:
                name = record.name
            result.append((record.id,name))
        return result
