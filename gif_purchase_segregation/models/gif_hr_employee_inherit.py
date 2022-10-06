from odoo import api, fields, models

class HrEmployeePS(models.Model):
    _inherit = 'hr.employee'

    #Añadir en compras un campo donde pueda seleccionar el tipo de producto.
    #Solo pueden tener un tipo de producto.
    #Order line debe de ser read only hasta que se seleccione el tipo de producto.    
    productos_oficina_e = fields.Selection(string='Productos Oficina', selection=[('1', 'Usuario'), ('2', 'Administrador')])
    gastos_asociados_e = fields.Selection(string='Gastos Asociados', selection=[('1', 'Usuario'), ('2', 'Administrador')])
    productos_insumos_e = fields.Selection(string='Productos Insumos', selection=[('1', 'Usuario'), ('2', 'Administrador')])
    productos_primarios_e = fields.Selection(string='Productos Primarios', selection=[('1', 'Usuario'), ('2', 'Administrador')])
    descuentos_y_beneficios_e = fields.Selection(string='Descuentos y Beneficios', selection=[('1', 'Usuario'), ('2', 'Administrador')],default='1')

    def onchange_productos_oficina_e(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Egreso Productos de Oficina')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Egreso Productos de Oficina')])
        add_user = self.user_id
        if self.productos_oficina_e == '1':
            grupo.write({
                'users': [(4, add_user.id)]
            })
        elif self.productos_oficina_e == '2':
            grupo.write({
                'users': [(4, add_user.id)]
            })
            grupo_admin.write({
                    'users': [(4, add_user.id)]
                })
        elif self.productos_oficina_e == False:
            grupo.write({
                'users': [(3, add_user.id)]
            })
            grupo_admin.write({
                'users': [(3, add_user.id)]
            })

    
    def onchange_productos_asociados_e(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Egreso Gastos Asociados')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Egreso Gastos Asociados')])
        add_user = self.user_id
        try:
            if self.gastos_asociados_e == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.gastos_asociados_e == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                grupo_admin.write({
                        'users': [(4, add_user.id)]
                    })
            elif self.gastos_asociados_e == False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass

    def onchange_productos_insumos_e(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Egreso Productos Insumos')])
        admin_grupo = self.env['res.groups'].search([('name','=','Validador Transacciones Egreso Productos Insumos')])
        add_user = self.user_id
        try:
            if self.productos_insumos_e == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.productos_insumos_e == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                admin_grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.productos_insumos_e ==  False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                admin_grupo.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass

    def onchange_productos_primarios_e(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Egreso Productos Primarios')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Egreso Productos Primarios')])
        add_user = self.user_id
        if self.productos_primarios_e == '1':
            grupo.write({
                'users': [(4, add_user.id)]
            })
        elif self.productos_primarios_e == '2':
            grupo.write({
                    'users': [(4, add_user.id)]
                })
            grupo_admin.write({
                    'users': [(4, add_user.id)]
                })
        elif self.productos_primarios_e == False:
            grupo.write({
                'users': [(3, add_user.id)]
            })
            grupo_admin.write({
                'users': [(3, add_user.id)]
            })
            
    def onchange_descuentos_y_beneficios_e(self):
        grupo = self.env['res.groups'].search([('name','=','Transacciones Egreso Descuentos y Beneficios')])
        grupo_admin = self.env['res.groups'].search([('name','=','Validador Transacciones Egreso Descuentos y Beneficios')])
        add_user = self.user_id
        try:
            if self.descuentos_y_beneficios_e == '1':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
            elif self.descuentos_y_beneficios_e == '2':
                grupo.write({
                    'users': [(4, add_user.id)]
                })
                grupo_admin.write({
                        'users': [(4, add_user.id)]
                    })
            elif self.descuentos_y_beneficios_e == False:
                grupo.write({
                    'users': [(3, add_user.id)]
                })
                grupo_admin.write({
                    'users': [(3, add_user.id)]
                })
        except:
            pass

    def save_eg(self):
        self.onchange_productos_oficina_e()
        self.onchange_productos_asociados_e()
        self.onchange_productos_insumos_e()
        self.onchange_productos_primarios_e()
        self.onchange_descuentos_y_beneficios_e()