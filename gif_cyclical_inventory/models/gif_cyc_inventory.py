from odoo import api, fields, models, _
from datetime import datetime


class GifCyclicalInventory(models.Model):
    _name = 'gif.cyc.inventory'
    _description = 'Realizar el inventario Ciclico'

    gif_name = fields.Char(string='Consecutivo',index=True,readonly=True,copy=False)
    state = fields.Selection(string='Status', selection=[('draft', 'Borrador'),('done', 'Confirmado'),('canceled','Cancelado')],readonly=True,copy=False,index=True,tracking=3,default='draft')
    gif_cyc_inv = fields.One2many(comodel_name='gif.inventory', inverse_name='gif_rel',string='Reporte')
    gif_resp = fields.Char(string='Responsable',default=lambda self:self.env.user.name,readonly=True,store=True)
    gif_init_date = fields.Date(string='Fecha de Conteo',default=datetime.today(),readonly=True,store=True)
    gif_end_date = fields.Date(string='Fecha de conclusión',store=True,readonly=True)
    gif_porc = fields.Char(string='Porcentaje de aciertos')
    gif_count_ubi = fields.Integer(string='Ubicaciones Escaneadas')
    gif_cons_ubi = fields.Integer(string='Ubicaciones Consistentes')
    gif_err_ubi = fields.Integer(string = 'Ubicaciones No Consistentes')
    
    

    @api.model 
    def create(self, vals): 
        vals['gif_name'] =self.env['ir.sequence'].next_by_code('gif.cyc.inventory.name')      
        return super(GifCyclicalInventory, self).create(vals)

    @api.onchange('gif_cyc_inv')
    def _onchange_gif_cyc_inv(self):
        for record in self.gif_cyc_inv:
            record.state = self.state
    

    # def set_on_progress(self):
    #     self.gif_init_date = datetime.now()
    #     self.state = 'first_c'
    #     self.gif_cyc_inv.state = self.state

    def set_on_done(self):
        n_data = len(self.gif_cyc_inv)
        ubis = []
        cons_ubis = []
        counter = 0
        for record in self.gif_cyc_inv:
            if record.gif_check == True:
                counter += 1
                if record.gif_location.id not in cons_ubis:
                    cons_ubis.append(str(record.gif_location.id))
            if record.gif_location.id not in ubis:
                ubis.append(str(record.gif_location.id))
        res = (counter/n_data)*100
        self.gif_porc = str(res) + '%'
        self.state = 'done'
        self.gif_end_date = datetime.now()
        self.gif_count_ubi = len(ubis)
        self.gif_cons_ubi = len(cons_ubis)
        self.gif_err_ubi = (len(ubis) - len(cons_ubis))

    def cancel(self):
        self.gif_name = 'CANCELADO'
        self.state = 'canceled'
    


    
    
    
