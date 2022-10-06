# from odoo import api, fields, models


# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     gif_obl_emp=fields.Boolean(string="Obligatorio")

#     def set_values(self):
#         res=super(ResConfigSettings,self).set_values()
#         self.env['ir.config_parameter'].set_param('gif_asig_employee.gif_obl_emp', self.gif_obl_emp)
#         return res

#     @api.model
#     def get_values(self):
#         res=super(ResConfigSettings,self).get_values()
#         ICPSudo = self.env['ir.config_parameter'].sudo()
#         gif_obl_emp = ICPSudo.get_param('gif_asig_employee.gif_obl_emp')
        
#         res.update(
#             gif_obl_emp = gif_obl_emp
#         )
#         return res