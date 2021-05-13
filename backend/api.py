#-Module imports--------------------------------------------------
from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS 
import json

#-Custom Modules and mappers-------
from tools import cert_fs, meta_collector, cert_root, cert_websrv

caFuncMap = {
  "commonname": "set_common_name",
  "country": "set_country_code",
  "state": "set_state",
  "city": "set_city",
  "organization": "set_organization",
  "unit": "set_unit",
  "email": "set_email"
}
certFuncMap = {
  "fqdn": "set_fqdn",
  "country": "set_country_code",
  "state": "set_state",
  "city": "set_city",
  "organization": "set_organization",
  "unit": "set_unit",
  "email": "set_email",
  "ipv4": "set_ipv4"
}

#-Build the flask app object---------------------------------------
#app = Flask(__name__ )
app = Flask(__name__, static_url_path='', static_folder='dist' )
app.secret_key = "changeit"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#-The APP Request Handler Area-------------------------------------
@app.route('/', methods=["GET"])
def htmo_home_get():
  return 'Hello from the App root'

#------------------------------------------------------------------
@app.route('/api', methods=["GET"])
def api_root_get():
  testObj = {
    "path": "/api",
    "method": "GET",
    "status": 200,
    "message": "Hello from the API"
  }
  return jsonify(testObj), 200

#-------------------------------------------
@app.route('/api/cas', methods=["GET"])
def api_cas_get():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  myMetaColl = meta_collector()
  try:
    resObj["data"] = myMetaColl.collect_certificate_authorities() 
  except Exception as e:
    print(e)
    resObj["msg"] = " something went wrong: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/ca/<ca>', methods=["GET"])
def api_ca_get(ca):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  try:
    myRootCert = cert_root(ca)
    resObj["data"] = myRootCert.get_meta_data()
  except Exception as e:
    print(e)
    resObj["msg"] = " Failed to load ca: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/ca', methods=["POST"])
def api_ca_post():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #-----------------------
  postIn = request.json
  if not postIn or "commonname" not in postIn:
    resObj["msg"] = "JSON Input is missing! Please try again..."
    resObj["status"] = 400
    return jsonify(resObj), 400

  #-----------------------
  cnAry = []
  myMetaColl = meta_collector()
  caAry = myMetaColl.collect_certificate_authorities()
  for ca in caAry:
    cnAry.append(ca["commonname"])
  if postIn["commonname"] in cnAry:
    resObj["msg"] = "ca already exists: '%s'" %postIn["commonname"]
    resObj["status"] = 400
    return jsonify(resObj), 400

  #-----------------------
  myRootCert = cert_root()
  for key, funcStr in caFuncMap.items():
    if key in postIn:
      try:
        curFunc = getattr(myRootCert, funcStr)
        curFunc(postIn[key])
      except Exception as e:
        print(e)
        continue
  
  #-----------------------
  try:
    myRootCert.gen_priv_key()
    myRootCert.create_root_cert()
    myRootCert.convert_cert_to_string()
    myRootCert.write_cert_to_fs()
  except Exception as e:
    print(e)
    resObj["msg"] = "Failed to create new ca: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  #-----------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/ca/<ca>', methods=["PUT"]) # Renew Only!!!
def api_ca_put(ca):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #-----------------------
  putIn = request.json
  try:
    myRootCert = cert_root(ca)
    myRootCert.load_cert_from_fs()
  except Exception as e:
    print(e)
    resObj["msg"] = " Failed to load ca: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #-----------------------
  for key, funcStr in caFuncMap.items():
    if key in putIn and key != "commonname": # Schrott, aber hier sei es dir verziehen...
      try:
        curFunc = getattr(myRootCert, funcStr)
        curFunc(putIn[key])
      except Exception as e:
        print(e)
        continue
  
  days = None
  if "days" in putIn:
    if type(putIn["days"]) == int:
      days = putIn["days"]
  myRootCert.renew_root_cert(days)

  #-----------------------
  try:
    myRootCert.convert_cert_to_string()
    myRootCert.write_cert_to_fs()
  except Exception as e:
    print(e)
    resObj["msg"] = "Failed to renew ca: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  #-----------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/certs/<ca>', methods=["GET"])
def api_certs_get(ca):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  try:
    resObj["data"] = myMetaColl.collect_certificates(ca)
  except Exception as e:
    print(e)
    resObj["msg"] = "something went wrong: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/cert/<ca>/<fqdn>', methods=["GET"])
def api_cert_get(ca, fqdn):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  myCertsFs = cert_fs(ca)
  crtAry = myCertsFs.list_certificates()
  if fqdn not in crtAry:
    resObj["msg"] = "Certificate not exist: '%s'" %fqdn
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  myCert = cert_websrv(ca, fqdn)
  try:
    myCert.load_cert_from_fs()
    resObj["data"] = myCert.get_meta_data()
  except:
    resObj["msg"] = "Failes to load Certificate: '%s'" %fqdn
    resObj["status"] = 500
    return jsonify(resObj), 500

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/cert/<ca>/<fqdn>', methods=["PUT"])
def api_cert_put(ca, fqdn):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------



  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/reqs/<ca>', methods=["GET"])
def api_reqs_get(ca):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  try:
    resObj["data"] = myMetaColl.collect_requests(ca)
  except Exception as e:
    print(e)
    resObj["msg"] = "something went wrong: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/req/<ca>/<fqdn>', methods=["GET"])
def api_req_get(ca, fqdn):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  myCertsFs = cert_fs(ca)
  crtAry = myCertsFs.list_requests()
  if fqdn not in crtAry:
    resObj["msg"] = "Cert Request not exist: '%s'" %fqdn
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  myReq = cert_websrv(ca, fqdn)
  try:
    myReq.load_req_from_fs()
    resObj["data"] = myReq.get_meta_data(req=True)
  except:
    resObj["msg"] = "Failes to load Certificate: '%s'" %fqdn
    resObj["status"] = 500
    return jsonify(resObj), 500


  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/req/<ca>', methods=["POST"]) # Create Cert Request
def api_req_post(ca):
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "msg": ""
  }

  #---------------------
  postData = request.json
  if "fqdn" not in postData:
    resObj["msg"] = "FQDN required for new Cert"
    resObj["status"] = 400
    return jsonify(resObj), 400
  else:
    fqdn = postData["fqdn"]

  #---------------------
  myMetaColl = meta_collector()
  caAry = myMetaColl.list_cas()
  if ca not in caAry:
    resObj["msg"] = "CA does not exist: '%s'" %ca
    resObj["status"] = 404
    return jsonify(resObj), 404

  #---------------------
  myCertFs = cert_fs(ca)
  reqAry = myCertFs.list_requests()
  if fqdn in reqAry:
    resObj["msg"] = "A cert request for '%s' already exist" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400

  #---------------------
  myCert = cert_websrv(ca, fqdn)
  for key, funcStr in certFuncMap.items():
    if key in postData:
      try:
        curFunc = getattr(myCert, funcStr)
        curFunc(postData[key])
      except Exception as e:
        print(e)
        continue
  
  #-----------------------
  try:
    myCert.gen_priv_key()
    myCert.create_cert_request()
    myCert.convert_cert_objects_to_string()
    myCert.write_cert_objects_to_fs()
  except Exception as e:
    print(e)
    resObj["msg"] = "Failed to create cert: %s" %e
    resObj["status"] = 500
    return jsonify(resObj), 500

  #---------------------
  return jsonify(resObj), 200




#-------------------------------------------

#-------------------------------------------

#-App Runner------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

  context = ('./certs/app-scape.lab/crt/caweb.app-scape.lab.crt', './certs/app-scape.lab/key/caweb.app-scape.lab.key')
  # app.run(host="0.0.0.0", port=8443, ssl_context=context)

#------------------------------------------------------------------