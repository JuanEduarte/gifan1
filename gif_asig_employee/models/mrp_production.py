from odoo.exceptions import UserError
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit="mrp.production"

    gif_checker_employer=fields.Boolean(string="Empleados", default=False)
    gif_asg_emp=fields.Integer(string="Asignar Empleados")
    gif_close_emp=fields.Boolean(string="Cerrar", default=False)
    gif_values_emp = fields.Boolean(string="Values", default=False)
    gif_traslate_emp = fields.Integer(string="Trasladar Empleados") 
    gif_traslate_des = fields.Many2one('mrp.production',string="Destino De Traslado",  domain=[('state', '=', 'progress')]) 
    gif_has_emp = fields.Boolean(default=False,compute='_has_emp')
    

    ################################################################
    #TRASLADO DE EMPLEADOS

    @api.onchange('gif_traslate_emp')
    def _has_emp(self):
        for record in self:
            if record.gif_traslate_emp > 0:
                record.gif_has_emp = True
            else:
                record.gif_has_emp = False

    def change_emp(self):
        for record in self:
            historico = self.env['gif.history'].search([('name','=',record.name)])
            values ={
                    'gif_traslate_emp': record.gif_traslate_emp,
                    'gif_traslate_des':record.gif_traslate_des.name
                } 
            if record.name != record.gif_traslate_des.name:
                if record.gif_traslate_emp >=1:
                    if record.gif_asg_emp - record.gif_traslate_emp >0:
                        record.gif_traslate_des.gif_asg_emp += record.gif_traslate_emp
                        record.gif_asg_emp -= record.gif_traslate_emp
                    else:
                        raise UserError(("No puede dejar una Orden que esta en Proceso sin empleados."))
                else:
                    raise UserError(("Agregue cuantos empleados desea transferir."))
            else:
                raise UserError(("No puede transferir empleados a la misma orden de fabricación."))
            
            if record.state != 'draft':
                if historico.id:
                    historico.update(values)
                else:
                    historico.create(values)

    ################################################################
    #ASIGNACION DE EMPLEADOS
    def _compute_employee(self):
        for record in self:
            disponibilidad = self.env['gif.disponibilidad'].search([('company_id', '=', self.env.user.company_id.id)])
            historico = self.env['gif.history'].search([('name','=',record.name)])
            opera = False
            for move in record.move_raw_ids:
                if type(move.id) == int:
                    opera = True
            print(disponibilidad)
            
            for contador in disponibilidad:
                values ={
                    'name':record.name,
                    'gif_date_planned_start':record.date_planned_start,
                    'gif_product_id':record.product_id.id,
                    'gif_duration_expected': record.production_duration_expected,
                    'gif_duration':record.production_real_duration,
                    'gif_state':record.state,
                    'gif_total_before': contador.gif_emp_total + contador.gif_emp_alta - contador.gif_emp_alta,
                    'gif_linea_before': contador.gif_emp_linea,
                    'gif_dps_before': contador.gif_emp_dps,
                }

                print('~~~~~~~~~~~~ANTES~~~~~~~~~~~~')
                print(record.state)
                print(values)

                # if record.state != 'draft':
                #     print("~~~~~~~~~~~~~~Despues~~~~~~~~~~~~~~~")
                #     print(record.state)
                #     print(values)
                #     if historico.id:
                #         historico.update(values)
                #     else:
                #         historico.create(values)   
                if record.state == 'progress' and opera == True :
                    if record.gif_values_emp == False:    
                        if record.gif_asg_emp >= 1:
                        #############################################################            
                                            #Entrada De Empleados  
                            if contador.gif_emp_linea + record.gif_asg_emp > contador.gif_emp_total:
                                raise UserError(("No tiene empleados disponibles para la Orden de Fabricacón"))
                            else:    
                                if record.gif_checker_employer == False:
                                    if contador.gif_emp_linea + record.gif_asg_emp <= contador.gif_emp_total:
                                        contador.gif_emp_linea += (record.gif_asg_emp) 
                                        contador.gif_emp_dps = contador.gif_emp_total - contador.gif_emp_linea
                                        print("ENTROENTROENTROENTROENTROENTROENTROENTRO")
                                        print(record.move_raw_ids)
                                        record.gif_checker_employer = True

                                        values.update({
                                            'name':record.name,
                                            'gif_date_planned_start':record.date_planned_start,
                                            'gif_product_id':record.product_id.id,
                                            'gif_duration_expected': record.production_duration_expected,
                                            'gif_duration':record.production_real_duration,
                                            'gif_state':record.state,
                                            'gif_linea_after':contador.gif_emp_linea,
                                            'gif_dps_after':contador.gif_emp_dps,
                                        })
                                        opera =False

                                        print("~~~~~~~~~~~~~~Despues~~~~~~~~~~~~~~~")
                                        record.gif_values_emp = True 
                                        print(record.state)
                                        print(values)
                                        if historico.id:
                                            historico.update(values)
                                        else:
                                            historico.create(values)
                                else:
                                    print("++++++++++++++++++++++++++++++++++")
                        else:
                            raise UserError(("No puede crear una Orden de Fabricación con 0 empleados"))
                    else:
                        print("VALUETRUEVALUETRUEVALUETRUEVALUETRUE")
                        
                        #############################################################            
                                            #Salida De Empleados  
                elif record.state == 'to_close':
                    print(record.state)
                    if record.gif_values_emp == True:   
                        if record.gif_checker_employer == True and record.gif_close_emp == False:
                            contador.gif_emp_linea -= record.gif_asg_emp
                            contador.gif_emp_dps = contador.gif_emp_total - contador.gif_emp_linea

                            record.gif_checker_employer = False
                            record.gif_close_emp = True

                            values.update({
                                'name':record.name,
                                'gif_date_planned_start':record.date_planned_start,
                                'gif_product_id':record.product_id.id,
                                'gif_duration_expected': record.production_duration_expected,
                                'gif_duration':record.production_real_duration,
                                'gif_state':record.state,
                                'gif_linea_after':contador.gif_emp_linea,
                                'gif_dps_after':contador.gif_emp_dps,
                            })
                            
                            print("~~~~~~~~~~~~~~Despues~~~~~~~~~~~~~~~")
                            record.gif_values_emp = False 
                            print(record.state)
                            print(values)
                            if historico.id:
                                historico.update(values)
                            else:
                                historico.create(values)
                
                elif record.state == 'cancel':
                    print(record.state)
                    if record.gif_values_emp == True:   
                        if record.gif_checker_employer == True and record.gif_close_emp == False:
                            contador.gif_emp_linea -= record.gif_asg_emp
                            contador.gif_emp_dps = contador.gif_emp_total - contador.gif_emp_linea

                            record.gif_checker_employer = False
                            record.gif_close_emp = True

                            values.update({
                                'name':record.name,
                                'gif_date_planned_start':record.date_planned_start,
                                'gif_product_id':record.product_id.id,
                                'gif_duration_expected': record.production_duration_expected,
                                'gif_duration':record.production_real_duration,
                                'gif_state':record.state,
                                'gif_linea_after':contador.gif_emp_linea,
                                'gif_dps_after':contador.gif_emp_dps,
                            })
                            
                            print("~~~~~~~~~~~~~~Despues~~~~~~~~~~~~~~~")
                            record.gif_values_emp = False 
                            print(record.state)
                            print(values)
                            if historico.id:
                                historico.update(values)
                            else:
                                historico.create(values)
                    
                    if  record.gif_checker_employer == False:
                        values.update({
                            'gif_state':record.state,
                        })
                        if historico.id:
                            historico.update(values)
                        else:
                            historico.create(values)

                elif record.state != 'draft':
                    print("~~~~~~~~~~~~~~Despues~~~~~~~~~~~~~~~")
                    print(record.state)
                    print(values)
                    if historico.id:
                        historico.update(values)
                    else:
                        historico.create(values) 

    @api.depends(
        'move_raw_ids.state', 'move_raw_ids.quantity_done', 'move_finished_ids.state',
        'workorder_ids.state', 'product_qty', 'qty_producing')
    def _compute_state(self):            
        for record in self:
            res = super(MrpProduction,self)._compute_state()
            record._compute_employee()
            print('Terminado')
            return res

class StockMove(models.Model):
    _inherit = 'stock.move'
    gif_checker_employer=fields.Boolean(string="Empleados", default=False)