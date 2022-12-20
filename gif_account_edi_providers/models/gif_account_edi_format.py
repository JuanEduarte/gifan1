
from unittest import result
from odoo import api, fields, models, tools, _
from odoo.tools.xml_utils import _check_with_xsd

import requests
import base64
# from lxml.objectify import fromstring
from lxml.etree import fromstring
from lxml import etree
from io import BytesIO

import string
import re
import logging


_logger = logging.getLogger(__name__)


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    

    def _l10n_mx_edi_get_ekomercio_credentials(self, move):
        return self._l10n_mx_edi_get_ekomercio_credentials_company(move.company_id)

    def _l10n_mx_edi_get_ekomercio_credentials_company(self, company):
        ''' Return the company credentials for PAC: ekomercio. Does not depend on a recordset
        '''
        if company.l10n_mx_edi_pac_test_env:
            return {
                'username': 'pruebas01',
                'password': 'Ekomercio.1',
                'sign_url': 'https://edixcfdisecuretest.ekomercio.com/WSCFDBuilderPlusTurbo/WSCFDBuilderPlus.asmx',
                'cancel_url': '',
            }
        else:
            if not company.l10n_mx_edi_pac_username or not company.l10n_mx_edi_pac_password:
                return {
                    'errors': [_("The username and/or password are missing.")]
                }

            return {
                'username': company.l10n_mx_edi_pac_username,
                'password': company.l10n_mx_edi_pac_password,
                'sign_url': '',
                'cancel_url': '',
            }

    def _l10n_mx_edi_ekomercio_sign(self, move, credentials, cfdi):
        return self._l10n_mx_edi_ekomercio_sign_service(credentials, cfdi)

    def _l10n_mx_edi_ekomercio_sign_service(self, credentials, cfdi):
        ''' Send the CFDI XML document to Ekomercio for signature. Does not depend on a recordset
        '''

        url = credentials['sign_url']
        template = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <getCFDI xmlns="http://edixcfdisecure.ekomercio.com/">
                <usuario>{user}</usuario>
                <password>{password}</password>
                <xmlFirmado><![CDATA[{data}]]></xmlFirmado>
                </getCFDI>
            </soap:Body>
            </soap:Envelope>"""

        soap_env = template.format(user=credentials['username'], password=credentials['password'], data=cfdi.decode('UTF-8'))
        #soap_env = template.format(user=credentials['username'], password=credentials['password'], data=cadena_chain)
        print(soap_env)
        headers = {'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': 'http://edixcfdisecure.ekomercio.com/getCFDI'}#,
                    # 'Content-Length': str(len(template))}

        try:
            soap_xml = requests.post(url, data=soap_env, headers=headers, timeout=20)
            
        except requests.exceptions.RequestException as req_e:
            return {'errors': [str(req_e)]}


        cfdiResult_patt = "<getCFDIResult>(.*)</getCFDIResult>"

        xml_str = str(soap_xml.content.decode('utf-8'))
        xml_str = xml_str.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;","&").strip()

        cfdiResult = re.search(cfdiResult_patt, xml_str, re.DOTALL).group(1)
        print("edi.format:\n", cfdiResult)
        response = fromstring(cfdiResult.encode('utf-8'))

        if response.tag == "Error":
            code = response.find('ErrorCode').text
            msg = response.find('ErrorMessage').text

            errors = []
            if code:
                errors.append(_("Code : %s") % code)
            if msg:
                errors.append(_("Message : %s") % msg)
            return {'errors': errors}

        cfdi_signed = cfdiResult
        if cfdi_signed:
            cfdi_signed = cfdi_signed.encode('utf-8')

        return {
            'cfdi_signed': cfdi_signed,
            'cfdi_encoding': 'str',
        }

    # def _l10n_mx_edi_ekomercio_cancel(self, move, credentials, cfdi):
    #     uuid_replace = move.l10n_mx_edi_cancel_invoice_id.l10n_mx_edi_cfdi_uuid
    #     return self._l10n_mx_edi_ekomercio_cancel_service(move.l10n_mx_edi_cfdi_uuid, move.company_id, credentials,
    #                                                    uuid_replace=uuid_replace)

    # def _l10n_mx_edi_ekomercio_cancel_service(self, uuid, company, credentials, uuid_replace=None):
    #     ''' Cancel the CFDI document with PAC: ekomercio. Does not depend on a recordset
    #     '''
    #     # certificates = company.l10n_mx_edi_certificate_ids
    #     # certificate = certificates.sudo().get_valid_certificate()
    #     # cer_pem = certificate.get_pem_cer(certificate.content)
    #     # key_pem = certificate.get_pem_key(certificate.key, certificate.password)
    #     url = credentials['sign_url']
    #     template = """<?xml version="1.0" encoding="utf-8"?>
    #         <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    #             <soap:Body>
    #                 <cancelarCFDI xmlns="http://edixcfdisecure.ekomercio.com/">
    #                     <usuario>{user}</usuario>
    #                     <password>{password}</password>
    #                     <rfcEmisor>{rfc}</rfcEmisor>
    #                     <uuid>{uuid}</uuid>
    #                 </cancelarCFDI>
    #             </soap:Body>
    #         </soap:Envelope>"""

    #     soap_env = template.format(user=credentials['username'], password=credentials['password'], rfc=company.vat, uuid=uuid)

    #     headers = {'Content-Type': 'text/xml; charset=utf-8',
    #                 'SOAPAction': 'http://edixcfdisecure.ekomercio.com/cancelarCFDI',
    #                     'Content-Length': str(len(template))}

    #     try:
    #         soap_xml = requests.post(url, data=soap_env, headers=headers, timeout=20)
    #         print(soap_xml.status_code)

           

    #         # transport = Transport(timeout=20)
    #         # client = Client(credentials['cancel_url'], transport=transport)
    #         # factory = client.type_factory('apps.services.soap.core.views')
    #         # uuid_type = factory.UUID()
    #         # uuid_type.UUID = uuid
    #         # uuid_type.Motivo = "01" if uuid_replace else "02"
    #         # if uuid_replace:
    #         #     uuid_type.FolioSustitucion = uuid_replace
    #         # docs_list = factory.UUIDArray(uuid_type)
    #         # response = client.service.cancel(
    #         #     docs_list,
    #         #     credentials['username'],
    #         #     credentials['password'],
    #         #     company.vat,
    #         #     cer_pem,
    #         #     key_pem,
    #         # )

    #     except Exception as e:
    #         return {
    #             'errors': [_("The Ekomercio service failed to cancel with the following error: %s", str(e))],
    #         }
 

    #     cfdiResult_patt = "<cancelarCFDIResult>(.*)</cancelarCFDIResult>"

    #     xml_str = str(soap_xml.content.decode('utf-8'))
    #     xml_str = xml_str.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;","&").strip()

    #     cfdiResult = re.search(cfdiResult_patt, xml_str, re.DOTALL).group(1)
    #     print(cfdiResult)
    #     response = fromstring(cfdiResult.encode('utf-8'))

    #     if response.tag == "Error":
    #         code = response.find('ErrorCode').text
    #         msg = response.find('ErrorMessage').text

    #         errors = []
    #         if code:
    #             errors.append(_("Code : %s") % code)
    #         if msg:
    #             errors.append(_("Message : %s") % msg)
    #         return {'errors': errors}

    #     # if not getattr(response, 'Folios', None):
    #     #     code = getattr(response, 'CodEstatus', None)
    #     #     msg = _("Cancelling got an error") if code else _('A delay of 2 hours has to be respected before to cancel')
    #     # else:
    #     #     code = getattr(response.Folios.Folio[0], 'EstatusUUID', None)
    #     #     cancelled = code in ('201', '202')  # cancelled or previously cancelled
    #     #     # no show code and response message if cancel was success
    #     #     code = '' if cancelled else code
    #     #     msg = '' if cancelled else _("Cancelling got an error")

    #     return {'success': True}

    def _l10n_mx_edi_ekomercio_sign_invoice(self, invoice, credentials, cfdi):
        return self._l10n_mx_edi_ekomercio_sign(invoice, credentials, cfdi)

    def _l10n_mx_edi_ekomercio_cancel_invoice(self, invoice, credentials, cfdi):
        # return self._l10n_mx_edi_ekomercio_cancel(invoice, credentials, cfdi)
        return {'errors':['La cancelación de EDI no está disponible.']}

    def _l10n_mx_edi_ekomercio_sign_payment(self, move, credentials, cfdi):
        return self._l10n_mx_edi_ekomercio_sign(move, credentials, cfdi)

    def _l10n_mx_edi_ekomercio_cancel_payment(self, move, credentials, cfdi):
        # return self._l10n_mx_edi_ekomercio_cancel(move, credentials, cfdi)
        return {'errors':['La cancelación de EDI no está disponible.']}

