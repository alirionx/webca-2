#-Module imports--------------------------------------------------
from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS 

#-Custom Modules------------
from tools import cert_fs, meta_collector, cert_root, cert_websrv




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


#-App Runner------------------------------------------------------
if __name__ == "__main__":
  #app.run(host="0.0.0.0", port=5000)

  context = ('./certs/app-scape.lab/crt/caweb.app-scape.lab.crt', './certs/app-scape.lab/key/caweb.app-scape.lab.key')
  app.run(host="0.0.0.0", port=8443, ssl_context=context)

#------------------------------------------------------------------