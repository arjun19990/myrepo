import pyodbc

wsdl_url = 'https://mf-sul-test.plunet.com/PlunetAPI?wsdl'
login_arg_1 = 'Hitarth D'
login_arg_2 = 'Slt@2021'


#Xero credentials
xero_api_url = 'https://api.xero.com/api.xro/2.0/Invoices?unitdp=4'
refresh_token_url = 'https://identity.xero.com/connect/token'

xero_api_credentails = {
    "xero-tenant-id":"65406f71-55f1-4e47-91cb-7ff84187264d",
    "client_id":"12D78A766F4742F687EDF7BA2A5E9858",
    "client_secret":"t6tAGT4tIw38RFjDWHKTO0SSvnRmp2wV5E-fAmaAZvPsfy4d",
    "refresh_token":"9b44be7659d70602efae35651697630d0cb936a24abcb809858283fce0eb58c1",
    "access_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE2MTI4NTMwNzYsImV4cCI6MTYxMjg1NDg3NiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHkueGVyby5jb20vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiMDQwMDVDOEExMjRFNEMzNjlENUZENjlCMzc4RjlEQ0UiLCJzdWIiOiJhZjBkODdiMDE5YzA1NTQ5YTQ2YTkxMzM1NjhjOTAwOSIsImF1dGhfdGltZSI6MTYxMjg0OTE0NywieGVyb191c2VyaWQiOiJjMjRhZDQ0ZC04OTIxLTQ0NDUtOWM5NC0wMTIxZjkwZjkwZTIiLCJnbG9iYWxfc2Vzc2lvbl9pZCI6IjU2MTQ3ZTQ3MmE2ZTQ4Y2M5Mjg2ODU3ZWEyNzU2NmEzIiwianRpIjoiMDAyMTM4ODYzNjNhNDMzMjY2ZDM2NzVhODI4NTk5MDIiLCJhdXRoZW50aWNhdGlvbl9ldmVudF9pZCI6IjEwMTYyMTRhLWY4YzEtNDEyYS1hODUwLWM3MzYzNzk3NDUyMCIsInNjb3BlIjpbImVtYWlsIiwicHJvZmlsZSIsIm9wZW5pZCIsImFjY291bnRpbmcuc2V0dGluZ3MiLCJhY2NvdW50aW5nLnRyYW5zYWN0aW9ucyIsImFjY291bnRpbmcuY29udGFjdHMiLCJvZmZsaW5lX2FjY2VzcyJdfQ.CDkCtCnq_7E5L4H5wGE91pLAhvygMQ6bKGi3jIGKf2Uq4eBkp-9wPm5BUEwpIEvy464bG0H0RMDAlOaBm8GG5UG82FUm7eAaYXkRv9Hz4GUr2l15A7XxZNKOH4FjBSbdNmTcHESiUj3R1xqMgbBYnXAEEvlJwTE7Eo45BZEP2NR7srz69SkTKArfDnYmhuPLgv2qkHxj6_Hx0E7Vy3GINmtdmt4DezPg-Hr_xleCXyqI1AGuIHhWXfDizIARvWKV7MHcFHvgTW1vNsExHx62vpZkyO35n7KQQRubPpWXKL056AhluHqJvnSrwM1bK9xFMnJgV_-qP4bYmCdlYQmBKg",
    "re_directURI":"https://developer.xero.com",
    "scopes":"offline_access accounting.transactions openid profile email accounting.contacts accounting.settings"
}

xero_receivable_system_tax = {
    "NONE":2,
    "TAX010":1,
    "TAX011":7
}

xero_payable_system_tax = {
    "NONE":2,
    "TAX002":1,
}

#Visma text module
visma_text_module_customer_id = 30
visma_text_module_supplier_id =31

crm_refresh_token_url = "https://login.microsoftonline.com/4b54996c-2940-4ade-a008-43a735704bb5/oauth2/token"
crm_oppurtunity_api_url = 'https://sltdev.crm4.dynamics.com/api/data/v9.2/opportunities'

crm_won_opportunity_api_url = 'https://sltdev.crm4.dynamics.com/api/data/v9.2/WinOpportunity'

crm_lose_opportunity_api_url = 'https://sltdev.crm4.dynamics.com/api/data/v9.2/LoseOpportunity'

#Plunet API's
plunet_receive_api_url = 'http://mf-sul-test.plunet.com/DataOutgoingInvoice30?wsdl'

plunet_payable_api_url = 'http://mf-sul-test.plunet.com/DataPayable30?wsdl'

plunet_receive_api_visma_url ='https://mf-sul-test.plunet.com/DataItem30?wsdl'

plunet_payables_api_visma_url='https://mf-sul-test.plunet.com/DataJob30?wsdl'

plunet_data_30_api_url = 'http://mf-sul-test.plunet.com/DataCustomer30?wsdl'

plunet_data_custom_field_api_url = 'http://mf-sul-test.plunet.com/DataCustomFields30?wsdl'

plunet_data_customer_address = 'http://mf-sul-test.plunet.com/DataCustomerAddress30?wsdl'

plunet_data_quote = 'https://mf-sul-test.plunet.com/DataQuote30?wsdl'

plunet_data_customer_contact = 'https://mf-sul-test.plunet.com/DataCustomerContact30?wsdl'


##### crm app credentials

crm_app_credentials = {
    "client_id":"3ae8c22f-d10a-4523-abdb-f591fbe5285a",
    "client_secret":".K_H2Vo5Mf6o.PQD7wi3w7CIQ_82s0eZ4-",
    "resource":"https://sltdev.crm4.dynamics.com/",
    "grant_type":"refresh_token"
}

reason_rejection_dict ={"1" :100000000,"2":100000001,"3":100000002,"4":100000004, "6":100000003,"8":100000007,"11":100000009,"12":100000006,"14":100000005,"15":100000008}

#### QB storage contained string
connect_str="DefaultEndpointsProtocol=https;AccountName=stsltdev1;AccountKey=AczZwXcBAAN5T8UmPDsLyhzTS6Df7/wJbc2j+/oYhJw+sCJY+Fif/Rt+sKA8V+OvWtay90rpnO8oxKz0c/aWrg==;EndpointSuffix=core.windows.net"

###### db credentials

# server = 'tcp:sltsqlserverdev.database.windows.net' 
# database = 'sltdevsynap' 
# username = 'sltadmindev' 
# password = 'Powerupcloud@123'

server = 'tcp:sltsqldevserver.database.windows.net' 
database = 'sltdevsynap' 
username = 'sltadmindev' 
password = 'Powerupcloud@123'


db_schema = "slt_test"

server_visma_intermediate = 'tcp:ebissqlserver.database.windows.net' 
database_visma_intermediate = 'ebisVisma' 
username_visma_intermediate = 'powerup' 
password_visma_intermediate = 'zMeT2>!y'

try:
    cnxn_syn_db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor_syn_db = cnxn_syn_db.cursor()
except Exception as err:
    print("Exception Occured while trying to create a DB connction.", err)


try:
    cnxn_syn_db_visma = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server_visma_intermediate+';DATABASE='+database_visma_intermediate+';UID='+username_visma_intermediate+';PWD='+ password_visma_intermediate)
    cursor_syn_db_visma = cnxn_syn_db_visma.cursor()
except Exception as err:
    print("Exception Occured while trying to create a DB connction to visma intermediate db.", err)
