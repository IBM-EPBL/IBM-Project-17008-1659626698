import ibm_db

try:
    ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hcq89801;PWD=usAygURNqa4m1FSR", '', '')
    print("Not Connected") 
except:
    print("Connected")         
