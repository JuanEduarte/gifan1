# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models,_
import base64


class AccountMove(models.Model):
	_inherit = "account.move"

	gif_firm_flag = fields.Boolean(
		string='Control de PAC', 
		default=False,
		help="Campo utilizado para evitar el timbrado de la factura.")


	"""
	Sobreescribimos el método para que no se genere el timbrado
	sobre una factura que tiene encendida la bandera 'Saldos Iniciales'

	El código agregado se encuentra entre las líneas de comentarios
	# Líneas añadidas
	...
	# Fin líneas añadidas
	"""
	def l10n_mx_edi_update_pac_status(self):
		for record in self:
			_logger.info("######################################## status= %s",record.l10n_mx_edi_pac_status)
		res = super(AccountMove, self).l10n_mx_edi_update_pac_status()
		return res


	def _l10n_mx_edi_retry(self):
		'''Try to generate the cfdi attachment and then, sign it.
		'''
		_logger.info("######################################## self 2= %s",self)
		version = self.l10n_mx_edi_get_pac_version()
		for inv in self:

			# Líneas añadidas *
			# Unícamente se hace la muestra del mensaje sobre la acción 
			# de inhibir el timbrado de la factura
			if inv.gif_firm_flag:
				inv.message_post(
					body=_('Intencionalmente se inhibe el timbrado por ser de saldos iniciales'))
				continue
			# Fin líneas añadidas *
			_logger.info("######################################## %s",inv.ref)

			cfdi_values = inv._l10n_mx_edi_create_cfdi()
			error = cfdi_values.pop('error', None)
			cfdi = cfdi_values.pop('cfdi', None)
			if error:
				# cfdi failed to be generated
				inv.l10n_mx_edi_pac_status = 'retry'
				inv.message_post(body=error, subtype='account.mt_invoice_validated')
				_logger.error('The CFDI generated for the invoice %s is not valid: %s' % (inv.name, str(error)))
				continue
			# cfdi has been successfully generated
			inv.l10n_mx_edi_pac_status = 'to_sign'
			filename = ('%s-%s-MX-Invoice-%s.xml' % (
				inv.journal_id.code, inv.name, version.replace('.', '-'))).replace('/', '')
			ctx = self.env.context.copy()
			ctx.pop('default_type', False)
			inv.l10n_mx_edi_cfdi_name = filename
			attachment_id = self.env['ir.attachment'].with_context(ctx).create({
				'name': filename,
				'res_id': inv.id,
				'res_model': inv._name,
				'datas': base64.encodestring(cfdi),
				'description': 'Mexican invoice',
				})
			inv.message_post(
				body=_('CFDI document generated (may be not signed)'),
				attachment_ids=[attachment_id.id],
				subtype='account.mt_invoice_validated')
			inv._l10n_mx_edi_sign()

	"""
	Realizamos el cálculo de las líneas del asiento contable ( debit y credit)
	con base en la fecha en la cual se confirmó el pedido de compra
	"""
	# @api.model
	# def create(self, vals):
	# 	update_vals = self.update_values_dict(vals)
	# 	vals.update(update_vals)
	# 	# Cargamos el CFDI origen para saldos iniciales
	# 	# if vals.get('sgt_opening_balances', False) and vals.get('sgt_l10n_mx_edi_origin', False):
	# 	# 	vals['l10n_mx_edi_origin'] = vals.get('sgt_l10n_mx_edi_origin')
	# 	res = super(AccountMove, self).create(vals)
	# 	if res.journal_id.currency_id and res.currency_id.id != res.journal_id.currency_id.id:
	# 		res.select_journal_by_currency()
	# 	# if res.int_opening_balances:
	# 	# 	res.action_post()
	# 	return res

	# def write(self, vals):
	# 	res = super(AccountMove, self).write(vals)
	# 	_logger.info("###################################### write= %s",self)
	# 	_logger.info("###################################### vals= %s",vals)
	# 	_logger.info("###################################### opening= %s",self.int_opening_balances)
	# 	return res

	# def update_values_dict(self, vals):
	# 	if vals.get('type', False) == 'entry':
	# 		stock_move_id = vals.get('stock_move_id', False)
	# 		if stock_move_id:
	# 			stock_move = self.env['stock.move'].browse([stock_move_id])
	# 			if stock_move and stock_move.purchase_line_id:
	# 				purchase_order = stock_move.purchase_line_id.order_id
	# 				vals['purchase_id'] = purchase_order.id

	# 				line_ids = vals.get('line_ids', False)
	# 				if line_ids and purchase_order:
	# 					for line in line_ids:
	# 						values = line[2]
	# 						amount_currency = values.get('amount_currency', False)
	# 						if amount_currency and amount_currency < 0:
	# 							new_amount = purchase_order.currency_id\
	# 								._convert(abs(amount_currency), purchase_order.company_id.currency_id, purchase_order.company_id, purchase_order.date_approve)
	# 							values['credit'] = new_amount
	# 						elif amount_currency and amount_currency > 0:
	# 							new_amount = purchase_order.currency_id\
	# 								._convert(abs(amount_currency), purchase_order.company_id.currency_id, purchase_order.company_id, purchase_order.date_approve)
	# 							values['debit'] = new_amount
	# 	return vals

