from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class GroupContacts(models.Model):
    _name = 'gif.groups'
    _description = 'Modelo de Grupos'

    name = fields.Char(string='Nombre',required=True)
    sales_count = fields.Integer(compute='_sales_count', string="Ventas")
    purchases_count = fields.Integer(compute='_purchase_count',string="Compras")
    total_invo_out = fields.Integer(compute='_invoice_count_out', string="Facturas Cliente")
    total_invo_in = fields.Integer(compute='_invoice_count_in', string="Facturas Proveedor")
    
    ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    display_name = fields.Char(compute='_compute_display_name', recursive=True, store=True, index=True)
    date = fields.Date(index=True)
    title = fields.Many2one('res.partner.title')
    companys_ids = fields.One2many('res.partner', 'parent_id', string='Contact', domain=[('active', '=', True)])
    ref = fields.Char(string='Reference', index=True)
    lang = fields.Many2one('res.lang', string='Language')

    vat = fields.Char(string='RFC', index=True, help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    same_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID', compute='_compute_same_vat_partner_id', store=False)
    bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Banks')
    website = fields.Char('Website Link')
    comment = fields.Html(string='Notes')
    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='category_id', string='Tags', default=_default_category)
    credit_limit = fields.Float(string='Credit Limit')
    active = fields.Boolean(default=True)
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
         ("private", "Private Address"),
        ], string='Address Type',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char(string="E-mail")
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char("Telefono")
    mobile = fields.Char("Celular")
    is_group = fields.Boolean(string='Es un grupo', default=True)
    industry_id = fields.Many2one('res.partner.industry', 'Industry')
    color = fields.Integer(string='Color Index')
    user_ids = fields.One2many('res.users', 'partner_id', string='Users', auto_join=True)
    partner_share = fields.Boolean(
        'Share Partner', compute='_compute_partner_share', store=True,
        help="Either customer (not a user), either shared user. Indicated the current partner is a customer without "
             "access or with a limited access created for sharing data.")
    contact_address = fields.Char(compute='_compute_contact_address', string='Complete Address')

    partners_ids = fields.One2many('res.partner', 'group_id', string='Socios')

    # technical field used for managing commercial fields
    commercial_partner_id = fields.Many2one('res.partner', string='Commercial Entity',
                                            compute='_compute_commercial_partner', recursive=True,
                                            store=True, index=True)
    commercial_company_name = fields.Char('Company Name Entity', compute='_compute_commercial_company_name',
                                          store=True)
    company_name = fields.Char('Company Name')
    barcode = fields.Char(help="Use a barcode to identify this contact.", copy=False, company_dependent=True)

    l10n_mx_edi_curp = fields.Char(
        string="CURP", size=18,
        help="In Mexico, the Single Code of Population Registration (CURP) is a unique alphanumeric code of 18 characters used to officially identify both residents and Mexican citizens throughout the country.")
    l10n_mx_edi_operator_licence = fields.Char('Licencia del operador')
    l10n_it_pec_email = fields.Char(string="PEC e-mail")
    l10n_it_codice_fiscale = fields.Char(string="Codigo Fiscal", size=16)
    l10n_it_pa_index = fields.Char(string="PA index",
        size=7,
        help="Must contain the 6-character (or 7) code, present in the PA\
              Index in the information relative to the electronic invoicing service,\
              associated with the office which, within the addressee administration, deals\
              with receiving (and processing) the invoice.")
   
    def _sales_count(self):
        for record in self: 
            partners_s = self.env['res.partner'].search([('group_id', '=', record.id)])
            count_s = 0
            for partner_s in partners_s:
                count_s = count_s + partner_s.sale_order_count
            record.sales_count = count_s

    def _purchase_count(self):
        for record in self:
            partners_p = self.env['res.partner'].search([('group_id', '=', record.id)])
            count_p = 0
            for partner_p in partners_p: 
                count_p = count_p + partner_p.purchase_order_count
            record.purchases_count = count_p

    def _invoice_count_in(self):
        for record in self:
            partners_in = self.env['res.partner'].search([('group_id','=', record.id)])
            count_in = 0
            print(partners_in)
            for partner_in in partners_in:
                count_in = count_in + partner_in.supplier_invoice_count
            record.total_invo_in = count_in


    def action_show_sales(self):
        if (self.sales_count) == 0:
            raise ValidationError(_('Debe de haber al menos una empresa con ventas realizadas'))
        action_s = self.env["ir.actions.actions"]._for_xml_id("sale.act_res_partner_2_sale_order")
        action_s['context'] = {}
        action_s['domain'] = [('partner_id.group_id', '=', self.id)]
        return action_s

    def action_show_purchases(self):
        if(self.purchases_count) == 0:
            raise ValidationError(_('Debe de haber al menos una empresa con compras realizadas'))
        action_p = self.env["ir.actions.actions"]._for_xml_id("purchase.act_res_partner_2_purchase_order")
        action_p['context'] = {}
        action_p['domain'] = [('partner_id.group_id', '=', self.id)]
        return action_p

    def action_show_invoices_out(self):
        if(self.total_invo_out) == 0:
            raise ValidationError(_('Debe de haber al menos una empresa con facturas'))
        action_in_out = self.env['ir.actions.actions']._for_xml_id("sale.action_invoice_salesteams")
        action_in_out['context'] = {}
        action_in_out['domain'] = ['&',('partner_id.group_id','=',self.id),'|',('move_type','=','out_invoice'),('move_type','=','out_refund')]
        return action_in_out
    
    def action_show_invoices_in(self):
        if(self.total_invo_in) == 0:
            raise ValidationError(_('Debe de haber al menos una empresa con facturas'))
        action_in_in = self.env['ir.actions.actions']._for_xml_id("sale.action_invoice_salesteams")
        action_in_in['context'] = {}
        action_in_in['domain'] = ['&',('partner_id.group_id','=',self.id),'|',('move_type','=','in_invoice'),('move_type','=','in_refund')]
        return action_in_in

    def _invoice_count_out(self):
        for record in self:
            partners_out = self.env['res.partner'].search([('group_id','=', record.id)])
            count_out = 0
            print(partners_out)
            for partner_out in partners_out:
                count_out = count_out + partner_out.customer_invoice_count
            record.total_invo_out = count_out


class ContactsInherit(models.Model):
    _inherit = 'res.partner'

    group_id= fields.Many2one(comodel_name='gif.groups', string='Grupo')
    customer_invoice_count = fields.Integer(compute='_compute_customer_invoice_count')
    def _compute_customer_invoice_count(self):
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        client_invoice_groups = self.env['account.move'].read_group(
            domain=[('partner_id', 'in', all_partners.ids),
                    ('move_type', 'in', ('out_invoice', 'out_refund'))],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in client_invoice_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.customer_invoice_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).customer_invoice_count = 0


            
            
    
    
