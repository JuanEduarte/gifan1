
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


    def _l10n_mx_edi_export_invoice_cfdi(self, invoice):
        ''' Create the CFDI attachment for the invoice passed as parameter.

        :param move:    An account.move record.
        :return:        A dictionary with one of the following key:
        * cfdi_str:     A string of the unsigned cfdi of the invoice.
        * error:        An error if the cfdi was not successfuly generated.
        '''


        # == CFDI values ==
        cfdi_values = self._l10n_mx_edi_get_invoice_cfdi_values(invoice)
        cfdi_values["only_date"] = cfdi_values['cfdi_date'].split('T')[0]
        cfdi_values["only_hour"] = cfdi_values['cfdi_date'].split('T')[1]
        cfdi_values["tax_tr"] = "TR"
        cfdi_values["tax_re"] = "RE"
        cfdi_values["state"] = 1.00

        cfd_types = {
            'out_invoice':'FA', # Factura
            'out_refund' :'NC', # Nota de crédito
        }

        cfdi_values['typeCFD'] = cfd_types.get( cfdi_values['record'].move_type, '')

        cfdi_values['TradingPartner_Prov'] = cfdi_values['customer'].gif_provider_id


        # for k,v in cfdi_values.items():
        #     print(k,':',v)

        qweb_template, xsd_attachment = self._l10n_mx_edi_get_invoice_templates()
        #qweb_template_ek = self.env.ref('gif_account_edi_providers.ekcfdiv40')
        # xsd_attachment = self.sudo().env.ref('l10n_mx_edi.xsd_cached_cfdv40_xsd', False)


        # == Generate the CFDI ==
        cfdi = qweb_template._render(cfdi_values)
        #cfdi_ek = qweb_template_ek._render(cfdi_values)
        
        decoded_cfdi_values = invoice._l10n_mx_edi_decode_cfdi(cfdi_data=cfdi)
        #decoded_cfdi_values_ek = invoice._l10n_mx_edi_decode_cfdi(cfdi_data=cfdi_ek)

        cfdi_cadena_crypted = cfdi_values['certificate'].sudo().get_encrypted_cadena(decoded_cfdi_values['cadena'])
        #cfdi_cadena_crypted = cfdi_values['certificate'].sudo().get_encrypted_cadena(decoded_cfdi_values_ek['cadena'])
        print('\n')
        print("Cadena:", decoded_cfdi_values['cadena'])
        print('\n')
        #print("CadenaEKO:", decoded_cfdi_values_ek['cadena'])

        decoded_cfdi_values['cfdi_node'].attrib['Sello'] = cfdi_cadena_crypted

        # == Optional check using the XSD ==
        xsd_datas = base64.b64decode(xsd_attachment.datas) if xsd_attachment else None

        res = {
            'cfdi_str': etree.tostring(decoded_cfdi_values['cfdi_node'], pretty_print=True, xml_declaration=True, encoding='UTF-8'),
        }

        if xsd_datas:
            try:
                with BytesIO(xsd_datas) as xsd:
                    _check_with_xsd(decoded_cfdi_values['cfdi_node'], xsd)
            except (IOError, ValueError):
                _logger.info(_('The xsd file to validate the XML structure was not found'))
            except Exception as e:
                print("Errors??")
                res['errors'] = str(e).split('\\n')

        return res
