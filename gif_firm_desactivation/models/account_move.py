# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models,_
from psycopg2 import OperationalError
from odoo.tools.float_utils import float_repr
from odoo.addons.l10n_mx_edi.models.account_move import AccountMove as OriginalAccountMove
from odoo.addons.account_edi.models.account_edi_document import AccountEdiDocument as OriginalAccountEdiDocument

class AccountMove(models.Model):
    _inherit = "account.move"

    gif_firm_flag = fields.Boolean(
        string='Control de Pac', 
        default=True,
        help="Campo utilizado para evitar el timbrado de la factura.")

    def l10n_mx_edi_update_sat_status(self):
        '''Synchronize both systems: Odoo & SAT to make sure the invoice is valid.
        '''
        _logger.info("############################################### self = %s",self)
        # res = super(AccountMove, self).l10n_mx_edi_update_sat_status()
        
        for move in self:
            if not move.gif_firm_flag:
                _logger.info("############################################### se timbra")
                supplier_rfc = move.l10n_mx_edi_cfdi_supplier_rfc
                customer_rfc = move.l10n_mx_edi_cfdi_customer_rfc
                total = float_repr(move.l10n_mx_edi_cfdi_amount, precision_digits=move.currency_id.decimal_places)
                uuid = move.l10n_mx_edi_cfdi_uuid
                try:
                    status = self.env['account.edi.format']._l10n_mx_edi_get_sat_status(supplier_rfc, customer_rfc, total, uuid)
                except Exception as e:
                    move.message_post(body=_("Failure during update of the SAT status: %(msg)s", msg=str(e)))
                    continue

                if status == 'Vigente':
                    move.l10n_mx_edi_sat_status = 'valid'
                elif status == 'Cancelado':
                    move.l10n_mx_edi_sat_status = 'cancelled'
                elif status == 'No Encontrado':
                    move.l10n_mx_edi_sat_status = 'not_found'
                else:
                    move.l10n_mx_edi_sat_status = 'none'
            else:
                _logger.info("############################################### no timbrar")

    def action_process_edi_web_services(self):
        if not self.gif_firm_flag:
            _logger.info("############################################### procesar documentos")
            docs = self.edi_document_ids.filtered(lambda d: d.state in ('to_send', 'to_cancel') and d.blocking_level != 'error')
            docs._process_documents_web_services()
        else:
            _logger.info("############################################### no procesar docs")

    OriginalAccountMove.l10n_mx_edi_update_sat_status=l10n_mx_edi_update_sat_status
    OriginalAccountMove.action_process_edi_web_services=action_process_edi_web_services


class AccountEdiDocument(models.Model):
    _inherit = 'account.edi.document'

    def _process_documents_web_services(self, job_count=None, with_commit=True):
        ''' Post and cancel all the documents that need a web service.

        :param job_count:   The maximum number of jobs to process if specified.
        :param with_commit: Flag indicating a commit should be made between each job.
        :return:            The number of remaining jobs to process.
        '''
        all_jobs = self.filtered(lambda d: d.edi_format_id._needs_web_services())._prepare_jobs()
        jobs_to_process = all_jobs[0:job_count] if job_count else all_jobs

        for documents, doc_type in jobs_to_process:
            move_to_lock = documents.move_id
            attachments_potential_unlink = documents.attachment_id.filtered(lambda a: not a.res_model and not a.res_id)
            if not move_to_lock.gif_firm_flag:
                _logger.info("############################################### procesar documentos2")
                try:
                    with self.env.cr.savepoint(flush=False):
                        self._cr.execute('SELECT * FROM account_edi_document WHERE id IN %s FOR UPDATE NOWAIT', [tuple(documents.ids)])
                        self._cr.execute('SELECT * FROM account_move WHERE id IN %s FOR UPDATE NOWAIT', [tuple(move_to_lock.ids)])

                        # Locks the attachments that might be unlinked
                        if attachments_potential_unlink:
                            self._cr.execute('SELECT * FROM ir_attachment WHERE id IN %s FOR UPDATE NOWAIT', [tuple(attachments_potential_unlink.ids)])

                        self._process_job(documents, doc_type)
                except OperationalError as e:
                    if e.pgcode == '55P03':
                        _logger.debug('Another transaction already locked documents rows. Cannot process documents.')
                    else:
                        raise e
                else:
                    if with_commit and len(jobs_to_process) > 1:
                        self.env.cr.commit()
            else:
                _logger.info("############################################### no procesar docs2")

        return len(all_jobs) - len(jobs_to_process)


    OriginalAccountEdiDocument._process_documents_web_services=_process_documents_web_services

