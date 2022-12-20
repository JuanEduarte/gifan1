# -*- coding: utf-8 -*-

import base64
import logging
import ssl
import subprocess
import tempfile
from datetime import datetime
from lxml import etree, objectify

_logger = logging.getLogger(__name__)

from pytz import timezone

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

def str_to_datetime(dt_str, tz=timezone('America/Mexico_City')):
    return tz.localize(fields.Datetime.from_string(dt_str))



class Certificate(models.Model):
    _inherit = 'l10n_mx_edi.certificate'

    @api.model
    def _get_cadena_chain(self, xml_tree, xslt_path):
        """ Use the provided XSLT document to generate a pipe-delimited string
        :param xml_tree: the source lxml document
        :param xslt_path: Path to the XSLT document
        :return: string
        """
        cadena_transformer = etree.parse(tools.file_open(xslt_path))
        print("cadena_transformer",cadena_transformer)
        return str(etree.XSLT(cadena_transformer)(xml_tree))

    def _gif_certify_and_stamp(self, xml_content_str, xslt_path):
        """ Appends the Sello stamp, certificate, and serial number to CFDI documents
        :param xml_content_str: The XML document string to certify and stamp
        :param xslt_path: Path to the XSLT used to generate the cadena chain (pipe delimited string of important values)
        :return: A string of the XML with appended attributes: NoCertificado, Certificado, Sello
        """
        # TODO: replace function _l10n_mx_edi_add_digital_stamp in l10n_mx_reports/models/trial_balance.py (fix module dependencies too)
        # TODO: improve functions _l10n_mx_edi_export_payment_cfdi & _l10n_mx_edi_export_invoice_cfdi in l10n_mx_edi/models/account_edi_format.py
        self.ensure_one()
        print("???????????")
        if not xml_content_str:
            return None
        tree = objectify.fromstring(xml_content_str)
        tree.attrib['NoCertificado'] = self.serial_number
        tree.attrib['Certificado'] = self.get_data()[0]
        print(tree)
        cadena_chain = self._get_cadena_chain(tree, xslt_path)
        return cadena_chain
