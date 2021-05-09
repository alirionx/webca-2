from tools import cert_fs, cert_root, cert_websrv

# myRootCert = cert_root()
# myRootCert.set_common_name("app-scape.lab")
# myRootCert.set_country_code("DE")
# myRootCert.set_state("BW")
# myRootCert.set_city("STG")
# myRootCert.set_organization("AppScape")
# myRootCert.set_unit("LAB")

# myRootCert.gen_priv_key()
# myRootCert.create_root_cert()
# myRootCert.convert_cert_to_string()

# print(myRootCert.crtStr)
# print(myRootCert.keyStr)
# myRootCert.write_cert_to_fs()

# myRootCert = cert_root("app-scape")
# myRootCert.load_cert_from_fs()
# print(myRootCert.crtStr)
# print(myRootCert.keyStr)
# print(myRootCert.country, myRootCert.organization, myRootCert.commonname)

# myRootCert.renew_root_cert(days=1825)
# myRootCert.write_cert_to_fs()


myCert = cert_websrv(fqdn='caweb.app-scape.lab', caname='app-scape.lab')
print(myCert.fqdn)
print(myCert.caCrtObj.get_subject().CN)

myCert.gen_priv_key()
myCert.create_cert_request()
myCert.sign_cert()
res = myCert.convert_cert_objects_to_string()
res = myCert.write_cert_objects_to_fs()

myCert.print_cert_subs()