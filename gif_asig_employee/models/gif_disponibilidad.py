
from odoo.exceptions import UserError
from odoo import api, fields, models


class GifDisponibilidad(models.Model):
    _name = 'gif.disponibilidad'
    _description = 'Disponibilidad De Empleados'

    name = fields.Char(string='Nombre', default='Control de Empleados')
    gif_emp_total=fields.Float(string="Empleados Registrados")
    gif_emp_linea=fields.Float(string="Empleados en Linea")
    # gif_emp_linea_phantom=fields.Float(string="phantom")
    gif_emp_dps=fields.Float(string="Empledos Disponibles")
    # gif_emp_miss=fields.Float(string="Empleados Faltantes")
    gif_emp_alta=fields.Integer(string="Alta" )
    gif_emp_baja=fields.Integer(string="Baja")
    company_id = fields.Many2one('res.company', string='Compañia', required=True, default=lambda self:self.env.company.id) 
    

    def in_emp(self):
        for record in self:
            if record.gif_emp_alta <= 0:
                raise UserError(("Por Favor revisé la cantidad ingresada"))
            else:
                record.gif_emp_total += record.gif_emp_alta
                record.gif_emp_dps = record.gif_emp_total - record.gif_emp_linea

    def out_emp(self):
        for record in self:
            if record.gif_emp_total - record.gif_emp_baja < 0:
                raise UserError(("""No puede remover a los empleados solicitados. Por Favor revisé la cantidad ingresada."""))
            elif record.gif_emp_baja <= 0:
                raise UserError(("Por Favor revisé la cantidad ingresada"))
            elif record.gif_emp_total - record.gif_emp_linea < record.gif_emp_baja:
                raise UserError(("No puede dar de baja empleados que continuan en linea de producción"))
            else:
                record.gif_emp_total -= record.gif_emp_baja
                record.gif_emp_dps -= record.gif_emp_baja

    def emp_history(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("gif_asig_employee.gif_history_action")
        return action


