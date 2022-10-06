from odoo import api, fields, models


class GIFGroupRoutes(models.Model):
    _name = 'gif.group.route'
    _description = 'Agrupamiento de rutas'

    name = fields.Char(string='Nombre del grupo')
    gif_description = fields.Char(string='Descripción')
    gif_rel_to_part = fields.Many2many(comodel_name='res.partner', string='Cliente')
    
    # gif_partner_rel = fields.One2many(comodel_name='res.partner',inverse_name='gif_ro_gr',string='Direcciones')
    # gif_child_rel = fields.One2many(related='gif_partner_rel.child_ids',string='Ubicaciones',)#compute='_get_all_routs_group'

    # @api.onchange('gif_partner_rel')
    # def _onchange_name(self):
    #     print('Grupo: ')
    #     grupos = self.env['res.partner'].search([('gif_ro_gr','=','Prueba 1')])
    #     print(grupos)
    #     for record in grupos:
    #         if record.name:
    #             print(record.name)
    #             self.gif_partner_rel = record

class GIFResPartnerGR(models.Model):
    _inherit = 'res.partner'

    # gif_ro_gr = fields.One2many(comodel_name='gif.group.route', inverse_name='gif_rel_to_part' ,string='Grupo')
    gif_ro_gr = fields.Many2many(comodel_name='gif.group.route', string='Grupos')
    

    # @api.onchange('gif_ro_gr')
    # def _onchange_gif_ro_gr_gif(self):
    #     for record in self:
    #         record.write({'gif_ro_gr': record.gif_ro_gr.id})
    #         print('Id general: ',record.id)
    #         print('El del child: ',record.child_ids.id)

    @api.onchange('category_id')
    def _onchange_category_id_gif_gr_ro(self):
        for record in self:
            for r in record.child_ids:
                print('Child: ',r.id)
                print('Grupo: ',r.gif_ro_gr.name)
    
    
    

    
