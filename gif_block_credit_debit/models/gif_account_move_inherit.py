from odoo import api,fields,models
from odoo.tools.misc import formatLang, format_date, get_lang


class AccounMove(models.Model):
    _inherit = 'account.move.line'

    price_unit = fields.Float(string='Unit Price', digits='Product Price')
    tax_ids = fields.Many2many(comodel_name='account.tax', string="Taxes",context={'active_test': False},check_company=True)
    tax_line_id = fields.Many2one('account.tax', string='Originator Tax', ondelete='restrict', store=True,
        compute='_compute_tax_line_id')
    tax_group_id = fields.Many2one(related='tax_line_id.tax_group_id', string='Originator tax group',
        readonly=True, store=True)
    tax_base_amount = fields.Monetary(string="Base Amount", store=True, readonly=True,
        currency_field='company_currency_id')
    tax_repartition_line_id = fields.Many2one(comodel_name='account.tax.repartition.line',
        string="Originator Tax Distribution Line", ondelete='restrict', readonly=True,
        check_company=True)
    tax_tag_ids = fields.Many2many(string="Tags", comodel_name='account.account.tag', ondelete='restrict',
        help="Tags assigned to this line by the tax creating it, if any. It determines its impact on financial reports.", tracking=True)
    tax_audit = fields.Char(string="Tax Audit String", compute="_compute_tax_audit", store=True,
        help="Computed field, listing the tax grids impacted by this line, and the amount it applies to each of them.")
    tax_tag_invert = fields.Boolean(string="Invert Tags", compute='_compute_tax_tag_invert', store=True, readonly=False,
        help="Technical field. True if the balance of this move line needs to be "
             "inverted when computing its total for each tag (for sales invoices, for example).")

    @api.depends('tax_repartition_line_id.invoice_tax_id', 'tax_repartition_line_id.refund_tax_id')
    def _compute_tax_line_id(self):
        """ tax_line_id is computed as the tax linked to the repartition line creating
        the move.
        """
        for record in self:
            rep_line = record.tax_repartition_line_id
            # A constraint on account.tax.repartition.line ensures both those fields are mutually exclusive
            record.tax_line_id = rep_line.invoice_tax_id or rep_line.refund_tax_id
    

    @api.depends('move_id.move_type', 'tax_ids', 'tax_repartition_line_id', 'debit', 'credit', 'tax_tag_ids')
    def _compute_tax_tag_invert(self):
        for record in self:
            if not record.tax_repartition_line_id and not record.tax_ids :
                # Invoices imported from other softwares might only have kept the tags, not the taxes.
                record.tax_tag_invert = record.tax_tag_ids and record.move_id.is_inbound()

            elif record.move_id.move_type == 'entry':
                # For misc operations, cash basis entries and write-offs from the bank reconciliation widget
                rep_line = record.tax_repartition_line_id
                if rep_line:
                    tax_type = (rep_line.refund_tax_id or rep_line.invoice_tax_id).type_tax_use
                    is_refund = bool(rep_line.refund_tax_id)
                elif record.tax_ids:
                    tax_type = record.tax_ids[0].type_tax_use
                    is_refund = (tax_type == 'sale' and record.debit) or (tax_type == 'purchase' and record.credit)

                record.tax_tag_invert = (tax_type == 'purchase' and is_refund) or (tax_type == 'sale' and not is_refund)

            else:
                # For invoices with taxes
                record.tax_tag_invert = record.move_id.is_inbound()
    
    @api.depends('tax_tag_ids', 'debit', 'credit', 'journal_id', 'tax_tag_invert')
    def _compute_tax_audit(self):
        separator = '        '

        for record in self:
            currency = record.company_id.currency_id
            audit_str = ''
            for tag in record.tax_tag_ids:
                tag_amount = (record.tax_tag_invert and -1 or 1) * (tag.tax_negate and -1 or 1) * record.balance

                if tag.tax_report_line_ids:
                    #Then, the tag comes from a report line, and hence has a + or - sign (also in its name)
                    for report_line in tag.tax_report_line_ids:
                        audit_str += separator if audit_str else ''
                        audit_str += report_line.tag_name + ': ' + formatLang(self.env, tag_amount, currency_obj=currency)
                else:
                    # Then, it's a financial tag (sign is always +, and never shown in tag name)
                    audit_str += separator if audit_str else ''
                    audit_str += tag.name + ': ' + formatLang(self.env, tag_amount, currency_obj=currency)

            record.tax_audit = audit_str

    

    

    
    
