from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS 


#from OpenSSL import SSL
#context = SSL.Context()

# import ssl

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.use_privatekey_file('./certs/app-scape/crt/caweb.app-scape.lab.crt')
# context.use_certificate_file('./certs/app-scape/key/caweb.app-scape.lab.key')   


context = ('./certs/app-scape.lab/crt/caweb.app-scape.lab.crt', './certs/app-scape.lab/key/caweb.app-scape.lab.key')

#-Build the flask app object---------------------------------------
#app = Flask(__name__ )
app = Flask(__name__, static_url_path='', static_folder='dist' )
app.secret_key = "changeit"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#-The APP Request Handler Area-------------------------------------
@app.route('/', methods=["GET"])
def htmo_home_get():
    return 'Flask is running!'

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


#-App Runner------------------------------------------------------
if __name__ == "__main__":
  #app.run(host="0.0.0.0", port=5000)
  app.run(host="0.0.0.0", port=8443, ssl_context=context)

#------------------------------------------------------------------