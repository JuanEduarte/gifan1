
#from email.policy import default
from cgi import print_arguments
from odoo import api, fields, models


#Agrega un campo en Contactos para dar la oṕcion de desglosar el IEPS o no en Sale, Purchase y Account
class GifResPartner(models.Model):
     _inherit="res.partner"

     gif_ieps_desglose = fields.Boolean(string = "Desglosar IEPS")

