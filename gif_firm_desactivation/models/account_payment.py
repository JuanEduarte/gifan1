# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models,_
from odoo.addons.account_edi.models.account_payment import AccountPayment as OriginalAccountPayment
from odoo.addons.l10n_mx_edi.models.account_payment import AccountPayment as OriginalAccountPaymentL

class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_process_edi_web_services(self):
        moves = self.env["account.move"].search([("name","=",self.ref)])
        for move in moves:
            self.move_id.gif_firm_flag=move.gif_firm_flag
        _logger.info("############################################### flag 1=%s",self.move_id.gif_firm_flag)
        if not self.move_id.gif_firm_flag:
            return self.move_id.action_process_edi_web_services()

    def action_retry_edi_documents_error(self):
        self.ensure_one()
        moves = self.env["account.move"].search([("name","=",self.ref)])
        for move in moves:
            self.move_id.gif_firm_flag=move.gif_firm_flag
        _logger.info("############################################### flag 2=%s",self.move_id.gif_firm_flag)
        if not self.move_id.gif_firm_flag:
            return self.move_id.action_retry_edi_documents_error()

    OriginalAccountPayment.action_process_edi_web_services = action_process_edi_web_services
    OriginalAccountPayment.action_retry_edi_documents_error = action_retry_edi_documents_error

    def l10n_mx_edi_update_sat_status(self):
        moves = self.env["account.move"].search([("name","=",self.ref)])
        for move in moves:
            self.move_id.gif_firm_flag=move.gif_firm_flag
        _logger.info("############################################### flag 3=%s",self.move_id.gif_firm_flag)
        if not self.move_id.gif_firm_flag:
            return self.move_id.l10n_mx_edi_update_sat_status()

    def action_l10n_mx_edi_force_generate_cfdi(self):
        moves = self.env["account.move"].search([("name","=",self.ref)])
        for move in moves:
            self.move_id.gif_firm_flag=move.gif_firm_flag
        _logger.info("############################################### flag 3=%s",self.move_id.gif_firm_flag)
        if not self.move_id.gif_firm_flag:
            self.l10n_mx_edi_force_generate_cfdi = True
            self.move_id._update_payments_edi_documents()

    OriginalAccountPaymentL.l10n_mx_edi_update_sat_status=l10n_mx_edi_update_sat_status
    OriginalAccountPaymentL.action_l10n_mx_edi_force_generate_cfdi=action_l10n_mx_edi_force_generate_cfdi