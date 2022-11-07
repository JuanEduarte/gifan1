from odoo import api, fields, models


class GifDefaultCustomers(models.Model):
    _name = 'default.customers'
    _description = 'Clientes a los que se realizará la orden de venta masiva.'

    def default_sor(self):
        wizard = self.env['default.customers'].search([])
        sor = wizard[-1].gif_partner_soriana if wizard and wizard[-1] else False
        wizard[0].unlink() if len(wizard) > 1 else False
        return sor

    def default_frk(self):
        wizard = self.env['default.customers'].search([])
        fsk = wizard[-1].gif_partner_cityfresko if wizard and wizard[-1] else False
        return fsk

    def default_che(self):
        wizard = self.env['default.customers'].search([])
        che = wizard[-1].gif_partner_chedraui if wizard and wizard[-1] else False
        return che

    def default_liv(self):
        wizard = self.env['default.customers'].search([])
        liv = wizard[-1].gif_partner_liverpool if wizard and wizard[-1] else False
        return liv

    def default_heb(self):
        wizard = self.env['default.customers'].search([])
        heb = wizard[-1].gif_partner_heb if wizard and wizard[-1] else False
        return heb
    
    gif_partner_soriana = fields.Many2one('res.partner',string='Soriana', default=default_sor, required="True")
    gif_partner_cityfresko = fields.Many2one('res.partner',string='City Fresko',default=default_frk, required="True")
    gif_partner_chedraui = fields.Many2one('res.partner',string='Chedraui',default=default_che, required="True")
    gif_partner_liverpool = fields.Many2one('res.partner',string='Liverpool', default=default_liv, required="True")
    gif_partner_heb = fields.Many2one('res.partner',string='HEB', default=default_heb, required="True")

    
    def write_vals(self):
        self.write({
            'gif_partner_soriana':self.gif_partner_soriana,
            'gif_partner_cityfresko':self.gif_partner_cityfresko,
            'gif_partner_chedraui':self.gif_partner_chedraui,
            'gif_partner_liverpool':self.gif_partner_liverpool,
            'gif_partner_heb':self.gif_partner_heb,
        })
        return True

