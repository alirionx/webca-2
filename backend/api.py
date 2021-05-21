#-Module imports--------------------------------------------------
from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS 
from flask_httpauth import HTTPBasicAuth
import json
import re

#-Custom Modules and mappers-------
from tools import cert_fs, meta_collector, cert_root, cert_websrv, token, user


#-API Globals and contructors-------------------------------------
sessVars = ["username", "role"]

roleAccessMap = {
  "^\/api\/cas": { 
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "roles": ["admin"]
  },
  "^\/api\/ca\/.*": { 
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "roles": ["admin", "caadmin"]
  },
}

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
app.secret_key = "changeitxx"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
auth = HTTPBasicAuth()

#-Access Management Section----------------------------------------
@app.before_first_request
def before_everything():
  inf = "Do something here???"
  session["username"] = None
  session["role"] = None
  
#--------------------------------
@app.before_request
def check_before_every_request():
  
  #print(str(session))
  
  for var in sessVars:
    if var not in session:
      session[var] = None

  for reStr, paras in roleAccessMap.items():
    reChk = re.search(reStr, request.path)
    if reChk and request.method in paras["methods"] and session["role"] not in paras["roles"]:
      resObj = {
        "path": request.path,
        "method": request.method,
        "status": 401,
        "msg": "Access Denied"
      }
      return jsonify(resObj), 401

#--------------------------------
@auth.verify_password
def base_auth_login(username, password):

  if username == "" or password == "":
    return False

  try:
    myUser = user(username)
  except Exception as e:
    print(e)
    return False
  
  res = myUser.verify_password(password)
  if not res:
    return False
  
  session["username"] = username
  session["role"] = myUser.role
  return username

#--------------------------------
  

#-The APP Request Handler Area-------------------------------------
@app.route('/', methods=["GET"])
def html_home_get():
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
@app.route('/api/userstate', methods=["GET"])
def api_userstate_get():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "username": session["username"],
    "role": session["role"]
  }

  return resObj, 200

#-------------------------------------------
@app.route('/api/login', methods=["POST"])
@auth.login_required
def api_login_post():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "username": session["username"],
    "role": session["role"]
  }

  return resObj, 200

#-------------------------------------------
@app.route('/api/login/json', methods=["POST"])
def api_login_post_json():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200
  }
  #-----------------------
  postIn = request.json
  res = base_auth_login(postIn["username"], postIn["password"])
  if not res:
    resObj["msg"] = "Login failed"
    resObj["status"] = 401
    return jsonify(resObj), 401
  
  #-----------------------
  resObj["username"] = session["username"],
  resObj["role"] = session["role"]

  return resObj, 200

#-------------------------------------------
@app.route('/api/logout', methods=["POST"])
def api_logout_post():
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
  }

  #-----------------------
  session["username"] = None
  session["role"] = None

  return resObj, 200

#-------------------------------------------

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
@app.route('/api/ca/<ca>', methods=["DELETE"])
def api_ca_delete(ca):
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
  myCertFs = cert_fs(ca)
  myCertFs.delete_root_all()

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/rootcert/<ca>', methods=["GET"])
def api_rootcert_get(ca):
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
  myRootCert = cert_root(ca)
  myRootCert.load_cert_from_fs()

  resObj["data"] = {
    "crt": myRootCert.crtStr,
    "key": myRootCert.keyStr
  }

  #---------------------
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
  resObj["data"] = myMetaColl.collect_certificates(ca)
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
@app.route('/api/cert/<ca>/<fqdn>', methods=["POST"])
def api_cert_post(ca, fqdn):
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
  myCertFs = cert_fs(ca)
  reqAry = myCertFs.list_requests()
  if fqdn not in reqAry:
    resObj["msg"] = "A cert request for '%s' does not exist" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400
  
  #---------------------
  try:
    myCert = cert_websrv(ca, fqdn)
    myCert.load_req_from_fs()
    myCert.sign_cert()
    myCert.convert_cert_objects_to_string()
    myCert.write_cert_objects_to_fs()
  except Exception as e:
    print(e)
    resObj["msg"] = "Failed to sign cert request for '%s'" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400

  myCertFs.delete_cert_req(fqdn)

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
  myCertFs = cert_fs(ca)
  crtAry = myCertFs.list_certificates()
  if fqdn not in crtAry:
    resObj["msg"] = "A certificate for '%s' does not exist" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------
@app.route('/api/cert/<ca>/<fqdn>', methods=["DELETE"])
def api_cert_delete(ca, fqdn):
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
  myCertFs = cert_fs(ca)
  reqAry = myCertFs.list_certificates()
  if fqdn not in reqAry:
    resObj["msg"] = "A certificate for '%s' does not exist" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400
  else:
    myCertFs.delete_cert_all(fqdn)

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
@app.route('/api/req/<ca>/<fqdn>', methods=["DELETE"])
def api_req_delete(ca, fqdn):
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
  myCertFs = cert_fs(ca)
  reqAry = myCertFs.list_requests()
  if fqdn not in reqAry:
    resObj["msg"] = "A cert request for '%s' does not exist" %fqdn
    resObj["status"] = 400
    return jsonify(resObj), 400
  else:
    myCertFs.delete_cert_req(fqdn)

  #---------------------
  return jsonify(resObj), 200

#-------------------------------------------

#-------------------------------------------

#-The Token Section-----------------------------------------------
@app.route('/api/token/<ca>/<fqdn>', methods=["GET"])
@auth.login_required
def api_token_get(ca, fqdn):
  try:
    myToken = token(ca, fqdn)
    return myToken.token
  except Exception as e:
    #print(e)
    errStr = str(e)
    return errStr, 404
  

#-------------------------------------------
@app.route('/api/token/renew', methods=["POST"])
def api_token_cert_renew():
  try:
    jwt = request.headers["jwt"]
  except:
    return "'jwt' Token missing in Headers", 400

  jwt = jwt.replace(" ", "")
  splt = jwt.split(":")
  fqdn = splt[0]
  tokenStr = splt[1]
  
  myToken = token()
  res = myToken.validate_token(tokenStr, fqdn)
  if not res:
    return "Invalid token or FQDN", 401
  
  try:
    caname = res["caname"]
    fqdn = res["fqdn"]
  except:
    return "Invalid payload", 400

  myCert = cert_websrv(caname=caname, fqdn=fqdn)
  myCert.load_cert_from_fs()
  myCert.renew_cert(days=30)
  myCert.write_cert_objects_to_fs()

  return str(res), 200

#-------------------------------------------



#-------------------------------------------


#-App Runner------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

  context = ('./certs/app-scape.lab/crt/caweb.app-scape.lab.crt', './certs/app-scape.lab/key/caweb.app-scape.lab.key')
  # app.run(host="0.0.0.0", port=8443, ssl_context=context)

#------------------------------------------------------------------