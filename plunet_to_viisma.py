from zeep import Client
import requests
import datetime
import sys
#import config
from config import *
print(datetime.datetime.now())
#import config


class PlunetVismaIntegrationReceivables():
	def __init__(self):
		pass
		
	"""
	Purpose : To update receivables invoice details to Visma intermediate DB
	Params : self
	 """
	def plunet_to_visma_update(self):
		print("Inside plunet to visma receivables function outer")
		try:
			print("Inside plunet to visma receivables function")

			#to get initial list of orders associated with recievable invoices.
			plunet_receivable = cursor_syn_db.execute(''' select distinct K.KundeID "CustomerID",CC.Bez as "Company Code",CC.MandantID,I.AuftragID,I.StatusArchivierung,I.IDAnsprechpartner from PLUNET.auftrag I Left join PLUNET.kunde K on I.IDKunde = K.KundeID LEFT JOIN PLUNET.x_Mandant CC on K.MandantID = CC.MandantID where I.StatusArchivierung = 6 and ( CC.Bez like '%SLT-SE%' or  CC.Bez like '%SLT-NO%' or  CC.Bez like '%SLT-DK%'  or CC.Bez like '%SLT-Nordics%' ) ''')
			plunet_rec_invoices = plunet_receivable.fetchall()
			print(plunet_rec_invoices)
			if plunet_rec_invoices:
				#Hard coded type of invoice to F
				type_of_invoice ="F"
				
				for plunet_rec_invoice in plunet_rec_invoices:
					plunet_order_id=''
					visma_customer_no=''
					customer_reference_name=''
					our_reference_name=''
					local_remark=''
					delivery_date=''
					visma_header_id=''
					company_code_int=0
					
					plunet_order_id  =plunet_rec_invoice.AuftragID 
					company_code_int = plunet_rec_invoice.MandantID
					

					##Getting order details 
					order_details = cursor_syn_db.execute('''select auftrag.LieferDatum,auftrag.MemoProjektleitung from PLUNET.auftrag where AuftragID = ? ''',plunet_rec_invoice.AuftragID)
					order_details_data = order_details.fetchall()
					for order_details_each in order_details_data:
						delivery_date =order_details_each.LieferDatum 
						local_remark = order_details_each.MemoProjektleitung
						
						#Getting the visma customer external id from text module
						kunde_details = cursor_syn_db.execute('''select * FROM PLUNET.kunde_textmodul where IDTextModul=? and IDMain =  ?''',(visma_text_module_customer_id,plunet_rec_invoice.CustomerID))
						kunde_details_data = kunde_details.fetchall()
						for kunde_details_each in kunde_details_data:
							visma_customer_no = kunde_details_each.Inhalt


						##Getting the customer contact name.
						ansprechpartner_details = cursor_syn_db.execute('''select concat(m2.vorname,' ',m2.nachname) as "customer_reference_Name" from  PLUNET.ansprechpartner m2 where AnsprechpartnerID= ? ''',plunet_rec_invoice.IDAnsprechpartner)
						ansprechpartner_details_data = ansprechpartner_details.fetchone()
						if(ansprechpartner_details_data):
							customer_reference_name = ansprechpartner_details_data.customer_reference_Name
						else:
							customer_reference_name =''
						
						#getting the Project manager details.
						order_assitant_details = cursor_syn_db.execute('''select IDMitarbeiter from PLUNET.auftragassistent where ProjektRolleID = 2 and  IDMain = ?''',plunet_rec_invoice.AuftragID)
						order_assitant_details_data = order_assitant_details.fetchall()
						for order_assitant_details_data_each in order_assitant_details_data:
							print(order_assitant_details_data_each.IDMitarbeiter) 
							project_manager_details = cursor_syn_db.execute(''' select concat(m2.vorname,' ',m2.nachname) as "Project_Manager_Name" from PLUNET.mitarbeiter m2 where mitarbeiterid = ?''', order_assitant_details_data_each.IDMitarbeiter)
							project_manager_details_data=project_manager_details.fetchall()
							for project_manager_details_data_each in project_manager_details_data:
								our_reference_name = project_manager_details_data_each.Project_Manager_Name
								#print("project manager name:",our_reference_name)
												
						#Add to visma intermediate db table invoice header
						print(plunet_order_id,visma_customer_no,customer_reference_name, our_reference_name ,local_remark,delivery_date,type_of_invoice,company_code_int)

						#Check whether plunet order exists for restricting duplicate entry.
						visma_header_details = cursor_syn_db_visma.execute('''select  * from dbo.DevInvoiceHeader where  PlunetOrderId = ?''',plunet_rec_invoice.AuftragID)
						visma_header_details_data = visma_header_details.fetchall()

						if(visma_header_details_data):
							for visma_header_details_each in visma_header_details_data:
								print("data already present in Visma")
								print(visma_header_details_each.InvoiceHeaderId)
						else:
							print("no data for the plunet order in visma.New entry")
						
							#Setting order details to visma.
							cursor_syn_db_visma.execute('''
			                INSERT INTO dbo.DevInvoiceHeader(PlunetOrderId, VismaCustomerNo, TypeOfInvoice,CustomerReferenceName,OurReferenceName,LocalRemark,DeliveryDate,SentToVisma,Paid,CompanyCode)
			                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',(plunet_order_id,visma_customer_no,type_of_invoice,customer_reference_name,our_reference_name ,local_remark,delivery_date,0,0,company_code_int))
							cnxn_syn_db_visma.commit()

							#Fetching header id of added order.
							visma_header_details = cursor_syn_db_visma.execute('''select  * from dbo.DevInvoiceHeader where  PlunetOrderId = ?''',plunet_rec_invoice.AuftragID)
							visma_header_details_data = visma_header_details.fetchall()
							for visma_header_details_each in visma_header_details_data:
								visma_header_id =visma_header_details_each.InvoiceHeaderId


							#writing  order item details to row table:
							order_item_details = cursor_syn_db.execute('''select * from PLUNET.auftragposition where auftragposition.IDMain =?''',plunet_rec_invoice.AuftragID)
							order_item_details_data =order_item_details.fetchall()
							for order_item_details_data_each in order_item_details_data:
								article_number =''
								delivered_quantity=0.0
								unit_price=0.0
								row_text=''
								print(order_item_details_data_each.PositionID)

								#Getting price details for order items.
								item_price_details= cursor_syn_db.execute('''select IDPreiseinheit,auftragposzeilenpreis.PreisProEinheit,auftragposzeilenpreis.Umfang from PLUNET.auftragposzeilenpreis where auftragposzeilenpreis.IDPosition =?''',order_item_details_data_each.PositionID)	
								item_price_details_data = item_price_details.fetchall()
								for item_price_details_data_each in item_price_details_data:
									unit_price =item_price_details_data_each.PreisProEinheit
									delivered_quantity = item_price_details_data_each.Umfang
									print(delivered_quantity,unit_price)
									price_unit_details = cursor_syn_db.execute(''' select English from PLUNET.preiseinheit where PreisEinheitID =?''',item_price_details_data_each.IDPreiseinheit)
									price_unit_details_data = price_unit_details.fetchall()
									for price_unit_details_data_each in price_unit_details_data:
										article_number = price_unit_details_data_each.English

								#Description for order item.
								row_text = order_item_details_data_each.Beschreibung
								print("row_text",row_text)
								
								#Adding order item details to Invoice Row table.							
								cursor_syn_db_visma.execute('''
				                INSERT INTO dbo.DevInvoiceRow (InvoiceHeaderId, ArticleNumber, DeliveredQuantity,UnitPrice,RowText)
				                VALUES (?, ?, ?, ?, ?) ''',(visma_header_id,article_number,delivered_quantity,unit_price,row_text))
								cnxn_syn_db_visma.commit()

								visma_row_details = cursor_syn_db_visma.execute('''select  * from dbo.DevInvoiceRow where InvoiceHeaderId = ?''',visma_header_id)
								visma_row_details_data = visma_row_details.fetchall()

								if(visma_row_details_data):
									for visma_row_details_each in visma_row_details_data:
										print(visma_row_details_each.RowId)
			
		except:
				print("Error:: ", sys.exc_info()[0], "occurred.")	

class PlunetVismaIntegrationPayables():
	def __init__(self):
		pass

	""" 
	Purpose: Function to write payables invoice data and jobs to visma.
	Params:self
	"""		
	def plunet_to_visma_update(self):
		print("in plunet function payables")
		
		# try:
			#plunet_receivable = cursor_syn_db.execute(''' select distinct K.KundeID "CustomerID",CC.Bez as "Company Code",I.AuftragID,I.StatusArchivierung from PLUNET.auftrag I Left join PLUNET.kunde K on I.IDKunde = K.KundeID LEFT JOIN PLUNET.x_Mandant CC on K.MandantID = CC.MandantID where I.StatusArchivierung = 2 and CC.Bez like '%PL%' ''')
		plunet_payables = cursor_syn_db.execute(''' select distinct M.MitarbeiterID as "Resource_ID",M.MWSTArt as Tax_type,J.status,CC.bez "Company Code" from (select * from PLUNET.Mitarbeiter where arbeitsverhaeltnis=2 ) M left join PLUNET.x_mandant CC on M.MandantID = CC.MandantID left join PLUNET.Job J on J.IDMitarbeiter = M.MitarbeiterID where  J.status = 5  and CC.Bez like'%SLT-Nordics%' ''')
		plunet_payables_jobs = plunet_payables.fetchall()
		print(plunet_payables_jobs)
		plunet_jobs=[]
		if plunet_payables_jobs:
			
			VismaSupplierNo=''
			header_id=''
			
			for plunet_payables_job in plunet_payables_jobs:
				if(plunet_payables_job.Resource_ID not in plunet_jobs):

					#To check if resource id is duplicated or not in the list.
					plunet_jobs.append(plunet_payables_job.Resource_ID)

					#Getting the supplier visma external id.
					textmodule_externalid_details = cursor_syn_db.execute('''select * from PLUNET.mitarbeiter_textmodul where IDTextModul=? and IDMain=?''',(visma_text_module_supplier_id,plunet_payables_job.Resource_ID))
					textmodule_externalid_each = textmodule_externalid_details.fetchone()
					if(textmodule_externalid_each):
						VismaSupplierNo = textmodule_externalid_each.Inhalt
						print(VismaSupplierNo)
						if(VismaSupplierNo):
							
							#Infering the tax type to find the company code for payables.
							tax_type_dict = {'0':'Tax_1','1':'Tax_2','7':'Tax_3'}
							company_code_dict = {'Tax_1':{"text" :"SLT-SE","value":12},'Tax_2':{"text" :"SLT-NO","value":14},'Tax_3':{"text" :"SLT-DK","value":16}}
							

							print(plunet_payables_job.Tax_type)
							tax_type_valid = tax_type_dict.get(str(plunet_payables_job.Tax_type),"Not found")
							print(tax_type_valid)
							if(tax_type_valid !="Not found"):
								company_code_visma = company_code_dict[tax_type_dict[str(plunet_payables_job.Tax_type)]]["value"]
							else:
								company_code_visma =0
							print("company_code_visma",company_code_visma)

							#getiing payable invoices associated with resources
							supplier_invoices = cursor_syn_db.execute('''select * from Plunet.rechnungmitarbeiter where IDMitarbeiter = ? and Preis != 0''',plunet_payables_job.Resource_ID)
							supplier_invoices_data = supplier_invoices.fetchall()
							print(supplier_invoices_data)
							for supplier_invoices_data_each in supplier_invoices_data:
								print("internal invoice id",supplier_invoices_data_each.RechnungMitarbeiterID)
								print("Extern invoice number",supplier_invoices_data_each.RechNrExtern)

								#The supplier invoice number is necessary to put data to db.
								if(supplier_invoices_data_each.RechNrExtern):

									#Checking whether invoice details already present in DB.
									invoice_details_visma = cursor_syn_db_visma.execute('''select * from dbo.DevSupplierInvoiceHeader  where SupplierInvoiceNumber = ?''',supplier_invoices_data_each.RechNrExtern)
									invoice_details_visma_each = invoice_details_visma.fetchone()
									if(invoice_details_visma_each):
										print("invoice already present in DB:", invoice_details_visma_each.SupplierInvoiceHeaderId)
										
									else:
										print("add items")

										#Add header details
										cursor_syn_db_visma.execute('''INSERT INTO dbo.DevSupplierInvoiceHeader(VismaSupplierNo,Paid,CompanyCode,SupplierInvoiceNumber) VALUES (?,?,?,?) ''',(VismaSupplierNo,0,company_code_visma, supplier_invoices_data_each.RechNrExtern))
										cnxn_syn_db_visma.commit()

										#To get header id for 
										visma_header_details = cursor_syn_db_visma.execute('''select  SupplierInvoiceHeaderId from DevSupplierInvoiceHeader where  SupplierInvoiceNumber = ?''',supplier_invoices_data_each.RechNrExtern)
										visma_header_details_id = visma_header_details.fetchone()
										header_id = visma_header_details_id.SupplierInvoiceHeaderId
										print("New header id :",header_id)
														
										#setting invoice position details to get job associated iwth invoice.
										invoice_position_details = cursor_syn_db.execute('''select * from Plunet.rechnungmitarbeiterposition  where RechnungMitarbeiterId = ?''',supplier_invoices_data_each.RechnungMitarbeiterID)
										invoice_position_details_data =invoice_position_details.fetchall()
										for invoice_position_details_data_each in invoice_position_details_data:
											print(invoice_position_details_data_each.JobID)

											#To add jobs to list of not added jobs in visma for an invoice.
											jobs_in_plunet =  cursor_syn_db.execute('''select * from PLUNET.Job  where JobID=? and status =5''',invoice_position_details_data_each.JobID)
											jobs_in_plunet_details = jobs_in_plunet.fetchall()
											if(jobs_in_plunet_details):
												print("jobs")
																					
												not_added_jobs =[]

												#To check whether job alerady exists in db.
												job_details_visma = cursor_syn_db_visma.execute('''select * from dbo.DevSupplierInvoiceRow where JobID = ?''',(invoice_position_details_data_each.JobID))
												job_details_visma_each = job_details_visma.fetchone()
												if(job_details_visma_each):
														
													print("job exists:" ,job_details_visma_each.JobId)
													print("invoice row id",job_details_visma_each.RowId)
													print("Header id",job_details_visma_each.SupplierInvoiceHeaderId)
													
												else:
														
											 		#New Jobs of a supplier is added to a list.
													not_added_jobs.append(invoice_position_details_data_each.JobID)
														
												print(VismaSupplierNo)
												print(plunet_payables_job.Resource_ID)
												print(not_added_jobs)


												if  not_added_jobs:
														print("There are not added jobs")
														print(not_added_jobs)

														
							     
														for not_added_jobs_each in not_added_jobs:	

															#Getting each job details.					
															job_details = cursor_syn_db.execute('''select * from PLUNET.Job  where JobID=? and status =5''',not_added_jobs_each)
															job_details_data_each=job_details.fetchone()

														
															PlunetJobNo=''
															TotalRowAmount=0.0
															RowText_description=''
															PM_NO=0
															job_id=0

															
															#Concatinating display name and job number to get PlunetJobNo:
															order_details = cursor_syn_db.execute('''select Anzeigename from PLUNET.Auftrag where AuftragID=?''',job_details_data_each.IDAuftrag)
															order_details_each = order_details.fetchone()
															Anzeige_name= order_details_each.Anzeigename
															PlunetJobNo = Anzeige_name+"-" +str(job_details_data_each.Kurzform)+"-"+ str(job_details_data_each.JobNr)
															job_id = job_details_data_each.JobID
															
															#Getting price details.
															job_price_details=cursor_syn_db.execute('''select Umfang,PreisProEinheit  from PLUNET.jobpreis where JobId = ? ''',job_details_data_each.JobID)
															job_price_details_each=job_price_details.fetchone()
															TotalRowAmount = float(job_price_details_each.Umfang) * float(job_price_details_each.PreisProEinheit)
															#print(TotalRowAmount)

															#Description for job
															RowText_description = job_details_data_each.Gegenstand
															print("job_details_data_each.IDAuftrag", job_details_data_each.IDAuftrag)

															#Getting PM details. The Resource ID of PM is added to DB.
															order_assitant_details = cursor_syn_db.execute('''select IDMitarbeiter,AuftragAssistentID from PLUNET.auftragassistent where IDMain = ? and ProjektRolleID = 2''',job_details_data_each.IDAuftrag)
															order_assitant_details_data = order_assitant_details.fetchall()
															print(order_assitant_details_data)
															
															if(order_assitant_details_data):
																for order_assitant_details_data_each in order_assitant_details_data:
																	PM_NO = order_assitant_details_data_each.IDMitarbeiter
																	#print(order_assitant_details_data_each.IDMitarbeiter)
															else:
																	PM_NO =''

															#setting data in supplier invoice header.
															cursor_syn_db_visma.execute('''
														                INSERT INTO dbo.DevSupplierInvoiceRow (SupplierInvoiceHeaderId, PlunetJobNo, TotalRowAmount,PMNo,RowText,JobId)
														                VALUES (?, ?, ?, ?, ?, ?) ''',(header_id,PlunetJobNo,TotalRowAmount,PM_NO,RowText_description,job_id))
															cnxn_syn_db_visma.commit()
											
															print(PlunetJobNo,TotalRowAmount,RowText_description,PM_NO)
											else:
												print("jobs not found for the invoice")

								else:
									print("Supplier invoice number is not present for the invoice with internal id:", supplier_invoices_data_each.RechnungMitarbeiterID)	
							
					else:
						print("Visma supplier external id not added for supplier " + str(plunet_payables_job.Resource_ID))			

			print(plunet_jobs)
		# except:
		# 	print("Error:: ", sys.exc_info()[0], "occurred.")

plunet_to_visma_receivables = PlunetVismaIntegrationReceivables()
plunet_to_visma_receivables.plunet_to_visma_update()

plunet_to_visma_payables = PlunetVismaIntegrationPayables()
plunet_to_visma_payables.plunet_to_visma_update()



