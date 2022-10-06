
from datetime import datetime, date, time, timedelta
from odoo.exceptions import UserError
from odoo import models, fields, _, api


class WizardAttachmentReport(models.TransientModel):
    _name = 'wizard.attachment.report'
    _description = 'Wizard Reporte de adjuntos'

    gif_date_init = fields.Date(string='Fecha de inicio', required=True)
    gif_date_end = fields.Date(string='Fecha de termino',required=True)
    gif_purchase_draft = fields.Boolean(string='Cotización de Compra')
    gif_purchase_purchase = fields.Boolean(string='Pedido de Compra')
    gif_purchase_invoice = fields.Boolean(string='Factura de Compra')
    gif_purchase_invoice_payment = fields.Boolean(string='Pago de Compra')
    gif_purchase_invoice_retificated = fields.Boolean(string='Nota de credito sobre Compra')

    gif_sales_draft = fields.Boolean(string='Cotización de Venta')
    gif_sales_sale = fields.Boolean(string='Pedido de Venta')
    gif_sales_invoice = fields.Boolean(string='Factura de Venta')
    gif_sales_invoice_payment = fields.Boolean(string='Pago de Venta')
    gif_sales_invoice_retificated = fields.Boolean(string='Nota de credito sobre Venta')

    gif_reception = fields.Boolean(string="Recepción De Productos")
    gif_traslate = fields.Boolean(string="Traslados Internos")
    gif_pick = fields.Boolean(string="Recolección")
    gif_orden = fields.Boolean(string="Ordenes De Entrega")
    gif_election = fields.Boolean(string="Elección De Componentes")
    gif_almacen = fields.Boolean(string="Almacenamiento De Productos Terminados")

    adjuntos= fields.Many2one ('mail.thread' ,string="adjuntos")

    def gif_set_reports(self):
        for record in self:
            aux=0
            
            ##############################################
            # Búsqueda en el modulo de compras
            ##############################################
            self.env['gif.attachment.reports'].search([]).unlink()
            reports = self.env['gif.attachment.reports'].search([])
            purchaseModule = self.env['purchase.order'].search([
                    ('date_order' , '>=' , record.gif_date_init),
                    ('date_order' , '<=' , record.gif_date_end),
                    ])

            #----------------------------------------------------
            if record.gif_purchase_draft:
                aux +=1
                for compras in purchaseModule:
                    values = {
                    'name': compras.name,
                    'gif_type_document': "Cotización De Compra",
                    'gif_doc_state':compras.state ,
                    'gif_origin_reference': compras.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :'',
                    'gif_date_documents': compras.create_date ,
                    'user_id': compras.user_id.id,
                    
                }   
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', compras.id)])
                    if compras.state == 'draft':               
                        for adjunto in adjuntos:
                            if compras.message_attachment_count >0:
                                if adjunto.res_id == compras.id and adjunto.res_name == compras.name:    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if compras.message_attachment_count ==0:                            
                            reports.create(values)

            #----------------------------------------------------
            if record.gif_purchase_purchase:
                aux +=1
                for compras in purchaseModule:
                    values = {
                    'name': compras.name,
                    'gif_type_document': "Pedido De Compra",
                    'gif_doc_state':compras.state ,
                    'gif_origin_reference':  compras.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  compras.message_main_attachment_id.name,
                    'gif_date_documents': compras.create_date ,
                    'user_id': compras.user_id.id,
                }   
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', compras.id)])
                    if compras.state == 'purchase':
                        for adjunto in adjuntos:
                            if compras.message_attachment_count >0:
                                if adjunto.res_id == compras.id and adjunto.res_name == compras.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if compras.message_attachment_count ==0:                            
                            reports.create(values)
            
            #Modelo de Facturación Compras
            purchaseModule=self.env['account.move'].search([
                ('invoice_date' , '>=' , record.gif_date_init),
                ('invoice_date' , '<=' , record.gif_date_end),
                ])
            
            #----------------------------------------------------
            if record.gif_purchase_invoice:
                aux +=1 
                for compras in purchaseModule:
                    values = {
                    'name': compras.name,
                    'gif_type_document': "Factura De Compra",
                    'gif_doc_state':compras.state ,
                    'gif_origin_reference': compras.invoice_origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  compras.message_main_attachment_id.name,
                    'gif_date_documents': compras.create_date ,
                    'user_id': compras.invoice_user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', compras.id)])
                    if compras.move_type== 'in_invoice':       
                        for adjunto in adjuntos:
                            if compras.message_attachment_count >0:
                                if adjunto.res_id == compras.id and adjunto.res_name == compras.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if compras.message_attachment_count ==0:                            
                            reports.create(values)
            
            #----------------------------------------------------
            if record.gif_purchase_invoice_retificated:
                aux +=1 
                for compras in purchaseModule:
                    values = {
                    'name': compras.name,
                    'gif_type_document': "Nota De Crédito Sobre Compra",
                    'gif_doc_state':compras.state ,
                    'gif_origin_reference': compras.ref ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  compras.message_main_attachment_id.name,
                    'gif_date_documents': compras.create_date ,
                    'user_id': compras.invoice_user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', compras.id)])
                    if compras.move_type== 'in_refund':
                        for adjunto in adjuntos:
                            if compras.message_attachment_count >0:
                                if adjunto.res_id == compras.id and adjunto.res_name == compras.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if compras.message_attachment_count ==0:                            
                            reports.create(values)
            
            #----------------------------------------------------
            if record.gif_purchase_invoice_payment:
                aux +=1 
                
                purchaseModule=self.env['account.payment'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                ])
                for compras in purchaseModule:
                    values = {
                    'name': compras.name,
                    'gif_type_document': "Pago de Compra",
                    'gif_doc_state':compras.state ,
                    'gif_origin_reference': compras.ref ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  compras.message_main_attachment_id.name,
                    'gif_date_documents': compras.create_date ,
                    'user_id': compras.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', compras.id)])
                    if compras.payment_type == 'outbound':
                        for adjunto in adjuntos:
                            if compras.message_attachment_count >0:
                                if adjunto.res_id == compras.id and adjunto.res_name == compras.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if compras.message_attachment_count ==0:                            
                            reports.create(values)

                        
            ##############################################
            # Búsqueda en el modulo de ventas    
            ##############################################
            
            saleModule = self.env['sale.order'].search([
                    ('date_order' , '>=' , record.gif_date_init),
                    ('date_order' , '<=' , record.gif_date_end),
                    ])

            #----------------------------------------------------
            if record.gif_sales_draft:
                aux +=1
                for ventas in saleModule:
                    values = {
                    'name': ventas.name,
                    'gif_type_document': "Cotización De Venta",
                    'gif_doc_state':ventas.state ,
                    'gif_origin_reference':  ventas.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  ventas.message_main_attachment_id.name,
                    'gif_date_documents': ventas.create_date ,
                    'user_id': ventas.user_id.id,
                }                
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', ventas.id)])
                    if ventas.state == 'draft':
                        for adjunto in adjuntos:
                            if ventas.message_attachment_count >0:
                                if adjunto.res_id == ventas.id and adjunto.res_name == ventas.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if ventas.message_attachment_count ==0:                            
                            reports.create(values)

            #----------------------------------------------------
            if record.gif_sales_sale:
                aux +=1
                for ventas in saleModule:
                    values = {
                    'name': ventas.name,
                    'gif_type_document': "Pedido De Venta",
                    'gif_doc_state':ventas.state,
                    'gif_origin_reference': ventas.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  '',
                    'gif_date_documents': ventas.create_date ,
                    'user_id': ventas.user_id.id,
                }                
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', ventas.id)])
                    if ventas.state == 'sale':
                        for adjunto in adjuntos:
                            if ventas.message_attachment_count >0:
                                if adjunto.res_id == ventas.id and adjunto.res_name == ventas.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if ventas.message_attachment_count ==0:                            
                            reports.create(values)
    
            
            #Modelo de Facturación ventas
            saleModule=self.env['account.move'].search([
                ('invoice_date' , '>=' , record.gif_date_init),
                ('invoice_date' , '<=' , record.gif_date_end),
                ])
            
            #----------------------------------------------------
            if record.gif_sales_invoice:
                aux +=1 
                for ventas in saleModule:
                    values = {
                    'name': ventas.name,
                    'gif_type_document': "Factura De Venta",
                    'gif_doc_state':ventas.state ,
                    'gif_origin_reference': ventas.invoice_origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  ventas.message_main_attachment_id.name,
                    'gif_date_documents': ventas.create_date ,
                    'user_id': ventas.invoice_user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', ventas.id)])
                    if ventas.move_type=='out_invoice':       
                        for adjunto in adjuntos:
                            if ventas.message_attachment_count >0:
                                if adjunto.res_id == ventas.id and adjunto.res_name == ventas.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if ventas.message_attachment_count ==0:                            
                            reports.create(values)

            
            #----------------------------------------------------
            if record.gif_sales_invoice_retificated:
                aux +=1 
                for ventas in saleModule:
                    values = {
                    'name': ventas.name,
                    'gif_type_document': "Nota De Crédito Sobre Venta",
                    'gif_doc_state':ventas.state ,
                    'gif_origin_reference': ventas.ref ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  ventas.message_main_attachment_id.name,
                    'gif_date_documents': ventas.create_date ,
                    'user_id': ventas.invoice_user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', ventas.id)])
                    if ventas.move_type=='out_refund':
                        for adjunto in adjuntos:
                            if ventas.message_attachment_count >0:
                                if adjunto.res_id == ventas.id and adjunto.res_name == ventas.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if ventas.message_attachment_count ==0:                            
                            reports.create(values)

            
            #----------------------------------------------------
            if record.gif_sales_invoice_payment:
                aux +=1 
                
                saleModule=self.env['account.payment'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                ])
                for ventas in saleModule:
                    values = {
                    'name': ventas.name,
                    'gif_type_document': "Pago de Venta",
                    'gif_doc_state':ventas.state ,
                    'gif_origin_reference': ventas.ref ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  ventas.message_main_attachment_id.name,
                    'gif_date_documents': ventas.create_date ,
                    'user_id': ventas.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', ventas.id)])
                    if ventas.payment_type == 'inbound':
                        for adjunto in adjuntos:
                            if ventas.message_attachment_count >0:
                                if adjunto.res_id == ventas.id and adjunto.res_name == ventas.name :    
                                    values['gif_attachments'] = True
                                    values['gif_attachments_ids'] = adjunto.name
                                    values['gif_adj_selection']= 'yes'                                
                                    reports.create(values)
                        if ventas.message_attachment_count ==0:                            
                            reports.create(values)


            ##############################################
            # Búsqueda en el modulo de Inventarios  
            ##############################################

            if record.gif_reception:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Recepciones')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Recepción",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Recepciones":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)
        

            #-----------------------------------------------------

            if record.gif_traslate:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Traslados internos')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Traslados internos",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Traslados internos":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)

            #-----------------------------------------------------

            if record.gif_pick:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Recolección')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Recolección",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Recolección":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)

            #-----------------------------------------------------

            if record.gif_orden:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Órdenes de entrega')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Órdenes de entrega",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Órdenes de entrega":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)

            #-------------------------------------------------------

            if record.gif_election:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Elegir componentes')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Elegir componentes",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Elegir componentes":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)

            #-------------------------------------------------------

            if record.gif_almacen:
                aux +=1 
                
                pickingModule=self.env['stock.picking'].search([
                    ('date' , '>=' , record.gif_date_init),
                    ('date' , '<=' , record.gif_date_end),
                    ('picking_type_id' , '=' , 'Almacenar producto terminado')
                ])
                for pick in pickingModule:
                    values = {
                    'name': pick.name,
                    'gif_type_document': "Almacenar producto terminado",
                    'gif_doc_state':pick.state ,
                    'gif_origin_reference': pick.origin ,
                    'gif_adj_selection': 'no' ,
                    'gif_attachments_ids' :  pick.message_main_attachment_id.name,
                    'gif_date_documents': pick.create_date ,
                    'user_id': pick.user_id.id,
                } 
                    adjuntos = self.env['ir.attachment'].search([('res_id', '=', pick.id)])
                    for recepciones in pick.picking_type_id:
                        if recepciones.name == "Almacenar producto terminado":
                            for adjunto in adjuntos:
                                if pick.message_attachment_count >0:
                                    if adjunto.res_id == pick.id and adjunto.res_name == pick.name :    
                                        values['gif_attachments'] = True
                                        values['gif_attachments_ids'] = adjunto.name
                                        values['gif_adj_selection']= 'yes'                                
                                        reports.create(values)
                            if pick.message_attachment_count ==0:                            
                                reports.create(values)

            ###############################################
            #  Mensaje de error    
            ##############################################

            if aux == 0:

                raise UserError(("Necesita seleccionar al menos un campo."))
            
            return {'type': 'ir.actions.client', 'tag': 'reload'}


