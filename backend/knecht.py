import json

import sys
sys.path.append(".")
from tools import helpers, user, token, cert_fs, meta_collector, cert_root, cert_websrv


# myRootCert = cert_root()
# myRootCert.set_common_name("iaas-demo.de")
# myRootCert.set_country_code("DE")
# myRootCert.set_state("BW")
# myRootCert.set_city("STG")
# myRootCert.set_organization("IaaS")
# myRootCert.set_unit("LAB")
# myRootCert.set_email("dquilitzsch@outlook.de")

# myRootCert.gen_priv_key()
# myRootCert.create_root_cert()
# myRootCert.convert_cert_to_string()

# myRootCert.write_cert_to_fs()

# myRootCert = cert_root("app-scape")
# myRootCert.load_cert_from_fs()
# print(myRootCert.crtStr)
# print(myRootCert.keyStr)
# print(myRootCert.country, myRootCert.organization, myRootCert.commonname)

# myRootCert.renew_root_cert(days=1825)
# myRootCert.write_cert_to_fs()


# myCert = cert_websrv(caname='app-scape.lab', fqdn='san1.app-scape.lab')
# myCert.set_country_code ("DE")
# myCert.set_state("BW")
# myCert.set_city("STG")
# myCert.set_organization("AppScape")
# myCert.set_unit("LAB")
# myCert.set_email("dquilitzsch@app-scape.lab")
# myCert.add_san("dns", "palim.appscape.com")
# myCert.add_san("ip", "192.168.10.66")
# myCert.add_san("ip", "192.168.10.67")
# myCert.gen_priv_key()
# myCert.create_cert_request()
# myCert.convert_cert_objects_to_string()
# myCert.write_cert_objects_to_fs()

#   "commonname": "set_common_name",
#   "country": "set_country_code",
#   "state": "set_state",
#   "city": "set_city",
#   "organization": "set_organization",
#   "unit": "set_unit",
#   "email": "set_email"

#myCert.ipv4 = "192.168.10.23"
#print(myCert.commonname)
#print(myCert.caCrtObj.get_subject().CN)

# myCert.gen_priv_key()
# myCert.create_cert_request()
# myCert.sign_cert()
# res = myCert.convert_cert_objects_to_string()
# res = myCert.write_cert_objects_to_fs()

# myCert.load_cert_from_fs()
# myCert.renew_cert(days=10*365)
# myCert.write_cert_objects_to_fs()
# myCert.print_cert_subs()


# myMetaColl = meta_collector()
# res = myMetaColl.collect_certificate_authorities()
#print(json.dumps(res, indent=2))

# res = myMetaColl.collect_certificates("app-scape.lab")
# print(json.dumps(res, indent=2))


# myCert = cert_websrv(caname='app-scape.lab', fqdn='smtp.app-scape.lab')
# myCert.load_req_from_fs()


# myUser = user("mrrobot")
# myUser.create_passwordhash("Oviss1234!")
# res = myUser.verify_password("Oviss1234!")
# print( res )
# myUser.save_user()
# myUser.set_role("admin")

# print(myUser.userListId)

# print(myUser.get_meta_data(True))


# myUser = user("penner")
# myUser.username = "penner"
# myUser.email = "penner@bcl.com"
# myUser.set_role("caadmin")
# myUser.create_passwordhash("Penner12434!")
# print(myUser.passwordhash)
# myUser.create_user()

#myUser.delete_user()

# myToken = token("app-scape.lab", "smtp.app-scape.lab")
# myToken = token()
# myToken.set_ca_fqdn("app-scape.lab", "www.app-scape.lab")
# myToken.load_token("app-scape.lab", "smtp.app-scape.lab")
# myToken.create_token_string()
# print(myToken.token)
# myToken.save_token()

# myToken = token("app-scape.lab", "www.app-scape.lab")
# myToken.delete_token()

# tokenStr = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjYSI6ImFwcC1zY2FwZS5sYWIiLCJmcWRuIjoic210cC5hcHAtc2NhcGUubGFiIn0.G2ICMitYSP0aSVjKyg-4vTttYMGUBhzE051EBkFu_SI"
# myToken.validate_token(tokenStr, "smtp.app-scape.lab")


# myUser = user("dquilitzsch")
# myUser.create_passwordhash("Dodger08398!")
# print(myUser.passwordhash)
# myUser.save_user()


myHelpers = helpers()
# myHelpers.chk_san_validity("dns", "mycert.com")
myHelpers.chk_san_validity("ip", "192.168.10.1233")