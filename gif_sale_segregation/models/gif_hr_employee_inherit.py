from odoo import api, fields, models

class HrEmployeeSS(models.Model):
    _inherit = 'hr.employee'

    #Añadir en ventas un campo donde pueda seleccionar el tipo de producto.
    #Solo pueden tener un tipo de producto.
    #Order line debe de ser read only hasta que se seleccione el tipo de producto.    
    productos_oficina_i = fields.Selection(string='Productos Oficina', selection=[('1', 'Usuario'), ('2', 'Administrador'),])
    productos_primarios_i = fields.Selection(string='Productos Primarios', selection=[('1', 'Usuario'), ('2', 'Administrador'),])
    descuentos_y_beneficios_i = fields.Selection(string='Descuentos y Beneficios', selection=[('1', 'Usuario'), ('2', 'Administrador'),],default='1')

    def onchange_productos_oficina_i(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Ingreso Productos de Oficina')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Ingreso Productos de Oficina')])
        add_user = self.user_id
        try:
            if self.productos_oficina_i == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.productos_oficina_i == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(4, add_user.id)]
                    })
            elif self.productos_oficina_i == False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass


    def onchange_productos_primarios_i(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Ingreso Productos Primarios')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Ingreso Productos Primarios')])
        add_user = self.user_id
        try:
            if self.productos_primarios_i == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.productos_primarios_i == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(4, add_user.id)]
                    })
            elif self.productos_primarios_i == False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass

        
    def onchange_descuentos_y_beneficios_i(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Ingreso Descuentos y Beneficios')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Ingreso Descuentos y Beneficios')])
        add_user = self.user_id
        try:
            if self.descuentos_y_beneficios_i == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.descuentos_y_beneficios_i == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(4, add_user.id)]
                    })
            elif self.descuentos_y_beneficios_i == False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass

    def save_in(self):
        self.onchange_descuentos_y_beneficios_i()
        self.onchange_productos_primarios_i()
        self.onchange_productos_oficina_i()
    