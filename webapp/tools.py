import os, sys, shutil
import json, yaml
from typing import Protocol
import hashlib, binascii
from flask.globals import request
import re
from OpenSSL import crypto, SSL
import string
import random
import jwt
from datetime import datetime
import tarfile

#-Tools Globals------------------------------------
curDir = os.path.dirname(os.path.realpath(__file__)) 

baseFolderPath = os.path.join(curDir, "certs")

settingsPath = os.path.join(curDir, "settings.yaml")
accessFilePath = os.path.join(curDir, "access.yaml")

flObj = open(settingsPath, "r")
objIn = yaml.safe_load(flObj)
flObj.close()

#-Configure Data Path for Cert Data---
if "customDataPath" in objIn:
  customDataPath = objIn["customDataPath"]
  if customDataPath:
    baseFolderPath = os.path.join(customDataPath, "certs")
#-------------------------------------

folders = objIn["folders"]
subjects = objIn["subjects"]
sanTypes = objIn["sanTypes"]
mandaSubjects = objIn["mandaSubjects"]
stdRootValidity = objIn["stdRootValidity"]
stdCertValidity = objIn["stdCertValidity"]
keyLen = objIn["keyLen"]
endings = objIn["endings"]


#Das Ding muss noch weg... in nen config file....
countryCodes = [
  "AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN",
  "BO","BQ","BR","BS","BT","BV","BW","BZ","CA","CC","CD","CF","CG","CH","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ",
  "DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN",
  "GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO",
  "JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF",
  "MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR",
  "NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE",
  "SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","TC","TD","TF","TG","TH","TJ","TK","TM","TN","TO","TR","TT","TV",
  "TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"
]


#----------------------------------------------------------

class helpers:
  #----------------------------------
  def __init__(self):
    inf = "helpers object created"

  #----------------------------------
  def chk_base_folder(self):
    if not os.path.isdir(baseFolderPath):
      os.makedirs(baseFolderPath, exist_ok=True)

  #----------------------------------
  def gen_rendom_sn(self, bits=64):
    ranSn = random.getrandbits(bits)
    return ranSn
  
  #----------------------------------
  def gen_rendom_key(self, le=32):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=le))
    return res

  #----------------------------------
  def create_unix_timestamp(self):
    toDay = datetime.today()
    res = toDay.strftime('%Y-%m-%d %H:%M:%S')
    return res

  #----------------------------------
  def asn1_to_datestr(self, asn, fmt='%Y-%m-%d'):
    tmpDateStr = asn.decode()[:8]
    try:
      tmpDate = datetime.strptime(tmpDateStr, '%Y%m%d')
      newDateStr = tmpDate.strftime(fmt)
      return newDateStr
    except Exception as e:
      print(e)
      return tmpDateStr

  #----------------------------------
  def check_access_file(self):
    try:
      flObj = open(accessFilePath, "r")
      objIn = yaml.safe_load(flObj)
      objIn["users"]
      objIn["tokens"]
      flObj.close()
    except Exception as e:
      #print(e)
      print("creating new access file")
      dataObj = {
        "users": [],
        "tokens": []
      }
      flObj = open(accessFilePath, "w")
      yaml.dump(dataObj, flObj, default_flow_style=False)
      flObj.close()

  #----------------------------------
  def get_fqdn_from_str(self, crtStr):
    #print(crtStr)
    reqObj = crypto.load_certificate_request(crypto.FILETYPE_PEM, crtStr)
    fqdn = reqObj.get_subject().CN
    return fqdn

  #----------------------------------
  def chk_san_validity(self, key, val):
    key = key.upper()
    tmpcrtObj = crypto.X509Req()
    tmpcrtObj.set_version(3)

    #------------------
    sanList = [
      key+": {0}".format(str(val))
    ]
    sanListStrEnc = ", ".join(sanList).encode()
    
    #------------
    sanObj = [ 
      crypto.X509Extension(type_name=b"subjectAltName", critical=False, value=sanListStrEnc)
    ]
    try:
      tmpcrtObj.add_extensions(sanObj)
      return True
    except Exception as e:
      print(e)
      return False

  #----------------------------------
  def get_req_sans_list(self, reqObj):
    extAry = reqObj.get_extensions()# UIUIUI WZF
    sansList = []
    for ext in extAry:
      extStr = str(ext)
      extStrAry = extStr.split(", ")
      for san in sanTypes:
        for extEntry in extStrAry:
          if extEntry.startswith(san):
            sanObj = {
              "key": san,
              "val": extEntry.split(":")[1]
            }
            sansList.append(sanObj)
    
    return sansList

  #----------------------------------
  def get_crt_sans_list(self, crtObj):
    sansList = []
    sanLen = crtObj.get_extension_count() # UIUIUI noch mehr WZF
    for i in range(sanLen):
      extStr = str(crtObj.get_extension(i))
      extStrAry = extStr.split(", ")
      for san in sanTypes:
        for extEntry in extStrAry:
          if extEntry.startswith(san):
            sanObj = {
              "key": san,
              "val": extEntry.split(":")[1]
            }
            sansList.append(sanObj)
    
    return sansList

  #----------------------------------
  def update_domain_access(self):
    myUser = user()
    usersObj = myUser.get_users_object()
    
    myMetaColl = meta_collector()
    domList = myMetaColl.list_cas()

    i=0
    for usrObj in usersObj:
      domObj = {}

      if usrObj["role"] == "admin":
        for dom in domList:
          domObj[dom] = True
      else:
        for dom in domList:
          try: 
            domObj[dom] = usrObj["domains"][dom]
          except:
            domObj[dom] = False
          
      usersObj[i]["domains"] = domObj
      i+=1

    myUser.write_user_object(usersObj)
    return usersObj



  #----------------------------------
  def chk_app_init(self):
    try:
      flObj = open(accessFilePath, "r")
      objIn = yaml.safe_load(flObj)
      objIn["users"]
      objIn["tokens"]
      flObj.close()
    except Exception as e:
      print(e)
      return True

    if len(objIn["users"]) > 0:
      return False
    else:
      return True
    
  #----------------------------------
  def reset_app(self, delCrts=False):
    
    if delCrts:
      shutil.rmtree(baseFolderPath)

    dataObj = {
      "users": [],
      "tokens": []
    }
    flObj = open(accessFilePath, "w")
    yaml.dump(dataObj, flObj, default_flow_style=False)
    flObj.close()

  #----------------------------------

#----------------------------------------------------------
class user:
  #----------------------------------
  valList = ["username", "email", "role", "passwordhash", "domains", "firstname", "lastname", "department", "invitationHash", "ldap"]
  mandaValsList = ["username", "role"]
  roles = ["admin", "caadmin"]
  #----------------------------------
  def __init__(self, username=None):
    inf = "new user object created"
    myHelpers = helpers()
    myHelpers.check_access_file()

    self.userListId = None

    self.invitationHash = None

    self.username = None
    self.email = None
    self.role = None
    self.passwordhash = None
    self.domains = {}
    self.firstname = None
    self.lastname = None
    self.department = None
    self.ldap = False

    if username:
      self.load_user(username)

  #----------------------------------
  def get_users_object(self):
    flObj = open(accessFilePath, "r")
    objIn = yaml.safe_load(flObj)
    flObj.close()
    return objIn["users"]

  #----------------------------------
  def write_user_object(self, usersObj):
    flObj = open(accessFilePath, "r")
    objIn = yaml.safe_load(flObj)
    flObj.close()

    objIn["users"] = usersObj
    flObj = open(accessFilePath, "w")
    yaml.dump(objIn, flObj)
    flObj.close()

  #----------------------------------
  def get_users_list(self):
    usersObj = self.get_users_object()
    usersList = []
    for user in usersObj:
      try:
        usersList.append(user["username"])
      except:
        continue
    
    return usersList

  #----------------------------------
  def create_passwordhash(self, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    pwdHashRes = (salt + pwdhash).decode('ascii')
  
    self.passwordhash = pwdHashRes
    return pwdHashRes

  #----------------------------------
  def create_invitation(self):
    if self.userListId == None:
      raise Exception("no user loaded...")
    
    myHelpers = helpers()
    self.invitationHash = myHelpers.gen_rendom_key(64)
    
    return self.invitationHash

  #----------------------------------
  def load_user_by_invitation_hash(self, hash):
    usersObj = self.get_users_object()
    chk = False
    for usrObj in usersObj:
      if "invitationHash" in usrObj:
        if hash == usrObj["invitationHash"]:
          self.load_user(usrObj["username"])
          chk = True
          break

    if not chk:
      raise Exception("invalid invitation hash")
    else:
      return True

  #----------------------------------
  def verify_password(self, password):
    
    #-The LDAP Auth: Ich bin mir nicht sicher, ob das hier gut aufgehoben ist ...
    if self.ldap:
      import ldap
      ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

      try:
        ldapConfObj = objIn["ldapAuth"]
        objIn["ldapAuth"]["url"]
        objIn["ldapAuth"]["domain"]
      except:
        print("LDAP is not configured correctly in settings!!")
        return False

      ldapUrl = ldapConfObj["url"]
      ldapDom = ldapConfObj["domain"]
      ldapUsrStr = self.username + '@' + ldapDom

      ldapSrv = ldap.initialize(ldapUrl)
      try:
        ldapRes = ldapSrv.simple_bind_s(ldapUsrStr, password)
        return True
      except:
        return False
      
    #-----------------------
    else:
      salt = self.passwordhash[:64]
      self.passwordhash = self.passwordhash[64:]
      pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
      pwdhash = binascii.hexlify(pwdhash).decode('ascii')
      return pwdhash == self.passwordhash

  #----------------------------------
  def load_user(self, username):
    usersList = self.get_users_list()
    if username not in usersList:
      raise Exception("User '%s' does not exist." %username)
    else:
      usersObj = self.get_users_object()
    
    i=0
    for usrObj in usersObj:
      if username == usrObj["username"]:
        self.userListId = i
        break
      else:
        i+=1

    for val in self.valList:
      if val in usrObj:
        setattr(self, val, usrObj[val])
      else:
        setattr(self, val, None)

  #----------------------------------
  def set_role(self, role):
    if role not in self.roles:
      raise Exception("Invalid Role: '%s'." %role)
    else:
      self.role = role
  
  #----------------------------------
  def create_user(self):
    newUsrObj = {}
    missingVals = []
    for val in self.valList:
      if getattr(self, val):
        newUsrObj[val] = getattr(self, val)

    for val in self.mandaValsList:
      if not getattr(self, val):
        missingVals.append(val)
      else:
        newUsrObj[val] = getattr(self, val)
    
    if len(missingVals) > 0:
      raise Exception("failed to create user. The following values are missing: %s" %missingVals)
    
    usersList = self.get_users_list()
    if self.username in usersList:
      raise Exception("user '%s' already exist." %self.username)
    
    usersObj = self.get_users_object()
    usersObj.append(newUsrObj)
    #print(usersObj)
    self.write_user_object(usersObj)

    #myHelpers = helpers()
    #myHelpers.update_domain_access()

  #----------------------------------
  def save_user(self):
    if self.userListId == None:
      raise Exception("no user loaded...")

    savUsrObj = {}
    missingVals = []
    for val in self.valList:
      if getattr(self, val):
        savUsrObj[val] = getattr(self, val)
      
      if not getattr(self, val) and val in missingVals:
        missingVals.append(val)
    
    if len(missingVals) > 0:
      raise Exception("failed to create user. The following values are missing: %s" %missingVals)

    usersObj = self.get_users_object()
    usersObj[self.userListId] = savUsrObj

    self.write_user_object(usersObj)

  #----------------------------------
  def delete_user(self ):
    if self.userListId == None:
      raise Exception("no user loaded...")
    
    usersObj = self.get_users_object()
    del usersObj[self.userListId]

    self.write_user_object(usersObj)

  #----------------------------------
  def get_meta_data(self, passwordhash=False):
    if self.userListId == None:
      raise Exception("no user loaded...")
    
    usrObj = {}
    for val in self.valList:
      if getattr(self, val):
        usrObj[val] = getattr(self, val)
    
    if not passwordhash:
      try:
        del usrObj['passwordhash']
      except:
        inf = "never mind"

    return usrObj


  #----------------------------------
  def chk_ca_admin_access(self, caname): #??bler DAU-CODE

    if self.userListId == None:
      raise Exception("no user loaded...")

    if caname not in self.domains:
      return False
    elif self.domains[caname]:
      return True
    else:
      return False

  #----------------------------------


#----------------------------------------------------------
class token:
  #----------------------------------
  def __init__(self, ca=None, fqdn=None):
    inf = "new token object created"
    myHelpers = helpers()
    myHelpers.check_access_file()

    self.tokensArrayId = None

    self.ca = None
    self.fqdn = None
    self.token = None
    self.tokenKey = None
    self.renewal = 30

    if ca and fqdn: self.load_token(ca, fqdn)

  #----------------------------------
  def get_ca_fqdn_list(self):
    flObj = open(accessFilePath, "r")
    objIn = yaml.safe_load(flObj)
    flObj.close()
    #tokensAry = objIn["tokens"]
    tokensAry = self.get_tokens_array()
    caTokensList = []
    for token in tokensAry:
      caTokensList.append( {token["ca"]: token["fqdn"]} )

    return caTokensList
  
  #----------------------------------
  def get_tokens_array(self):
    flObj = open(accessFilePath, "r")
    objIn = yaml.safe_load(flObj)
    flObj.close()
    
    if type(objIn["tokens"]) == list:
      tokensAry = objIn["tokens"]
    else:
      tokensAry = []
    
    return tokensAry
  
  #----------------------------------
  def save_tokens_array(self, tokensAry):
    flObj = open(accessFilePath, "r")
    objIn = yaml.safe_load(flObj)
    flObj.close()

    objIn["tokens"] = tokensAry

    flObj = open(accessFilePath, "w")
    yaml.dump(objIn, flObj)
    flObj.close()
  
  #----------------------------------
  def load_token(self, ca, fqdn):
    caTokensList = self.get_ca_fqdn_list()
    if {ca: fqdn} not in caTokensList:
      raise Exception("token for '%s' does not exist." %{ca: fqdn})

    tokensAry = self.get_tokens_array()
    i = 0
    for token in tokensAry:
      if token["ca"] == ca and token["fqdn"] == fqdn:
        self.tokensArrayId = i
        self.ca = token["ca"]
        self.fqdn = token["fqdn"]
        self.token = token["token"]
        self.tokenKey = token["tokenKey"]
        self.renewal = token["renewal"]
        break
      else:
        i+=1

  #----------------------------------
  def set_ca_fqdn(self, ca, fqdn):
    myMetaColl = meta_collector()
    caList = myMetaColl.list_cas()
    if ca not in caList:
      raise Exception("Invalid root ca: '%s'."%ca)
    
    myCertFs = cert_fs(ca)
    fqdnList = myCertFs.list_certificates()
    if fqdn not in fqdnList:
      raise Exception("cert for '%s' does not exist."%fqdn)

    self.ca = ca
    self.fqdn = fqdn

  #----------------------------------
  def set_renewal(self, days):
    if type(days) == int:
      self.renewal = days
    else:
      return False
      
  #----------------------------------
  def create_token_string(self):
    if not self.ca or not self.fqdn:
      raise Exception("Please define ca and fqdn first")

    myHeleprs = helpers()
    self.tokenKey = myHeleprs.gen_rendom_key()

    payload = {
      "caname": self.ca,
      "fqdn": self.fqdn
    }
    self.token = jwt.encode(payload, self.tokenKey, algorithm="HS256").decode()

  #----------------------------------
  def save_token(self):

    neededVals = ["ca", "fqdn", "token", "tokenKey"]
    for val in neededVals:
      if not getattr(self, val):
        raise Exception("No token string to save... create one first.")

    tokenObj = {
      "fqdn": self.fqdn,
      "ca": self.ca,
      "token": self.token,
      "tokenKey": self.tokenKey,
      "renewal": self.renewal
    }
    tokensAry = self.get_tokens_array()
    if self.tokensArrayId == None:
      caTokensList = self.get_ca_fqdn_list()
      if {self.ca: self.fqdn} in caTokensList:
        raise Exception("token for '%s' already exist." %{self.ca: self.fqdn})
      tokensAry.append(tokenObj)
    else:
      tokensAry[self.tokensArrayId] = tokenObj

    self.save_tokens_array(tokensAry)
  
  #----------------------------------
  def delete_token(self):
    if self.tokensArrayId == None:
      raise Exception("No token loaded. Please load one first.")
    
    tokenAry = self.get_tokens_array()
    del tokenAry[self.tokensArrayId]
    self.save_tokens_array(tokenAry)

  #----------------------------------
  def validate_token(self, tokenStr):
    
    tokensAry = self.get_tokens_array()
    chk = False
    for tokenObj in tokensAry:
      if tokenStr == tokenObj["token"]:
        ca = tokenObj["ca"]
        fqdn = tokenObj["fqdn"]
        chk = True
        break
    if not chk:
      return False

    self.load_token(ca, fqdn)

    try:
      res = jwt.decode(tokenStr, self.tokenKey, algorithms=["HS256"])
      return res
    except Exception as e:
      print(e)
      return False
  
  #----------------------------------


#----------------------------------------------------------
class cert_fs:
  #----------------------------------
  def __init__(self, caname):
    
    self.caname = caname
    self.capath = os.path.join(baseFolderPath, caname)
    self.crtpath = os.path.join(self.capath, "root", caname+"_ca"+endings["cert"])
    self.keypath = os.path.join(self.capath, "root", caname+"_ca"+endings["key"])

    self.keysPath = os.path.join(self.capath, "key")
    self.reqsPath = os.path.join(self.capath, "req")
    self.certsPath = os.path.join(self.capath, "crt")

    self.chk_folders()

  #----------------------------------
  def chk_folders(self):
    # if not os.path.isdir(baseFolderPath):
    #   os.mkdir(baseFolderPath)
    
    if not os.path.isdir(self.capath):
      os.makedirs(self.capath)
    
    for folder in folders:
      try:
        os.mkdir(os.path.join(self.capath, folder))
      except Exception as e:
        #print(e)
        inf = "gibts schon oder darf net schreiben..."

  #----------------------------------
  def write_root_cert(self, crtStr):
    flObj = open(self.crtpath, "w")
    flObj.write(crtStr)
    flObj.close()

  #----------------------------------
  def write_root_key(self, keyStr):
    flObj = open(self.keypath, "w")
    flObj.write(keyStr)
    flObj.close()

  #----------------------------------
  def delete_root_all(self):
    shutil.rmtree(self.capath, ignore_errors=True)

  #----------------------------------
  def get_req_str(self, fqdn):
    path = os.path.join(self.reqsPath, fqdn + endings["req"])

    flObj = open(path, "r")
    reqStr = flObj.read()
    flObj.close()
    return reqStr

  #----------------------------------
  def get_cert_str(self, fqdn=None):
    if not fqdn: path = self.crtpath
    else: path = os.path.join(self.certsPath, fqdn + endings["cert"])

    flObj = open(path, "rt")
    crtStr = flObj.read()
    flObj.close()
    return crtStr

  #----------------------------------
  def get_key_str(self, fqdn=None):
    if not fqdn: path = self.keypath
    else: path = os.path.join(self.keysPath, fqdn + endings["key"])

    flObj = open(path, "rt")
    keyStr = flObj.read()
    flObj.close()
    return keyStr

  #----------------------------------
  def write_cert_pkey(self, fqdn, keyStr):
    curKeyPath = os.path.join(self.keysPath, fqdn + endings["key"])
    flObj = open(curKeyPath, "w")
    flObj.write(keyStr)
    flObj.close()

  #----------------------------------
  def write_cert_req(self, fqdn, reqStr):
    curReqPath = os.path.join(self.reqsPath, fqdn + endings["req"])
    flObj = open(curReqPath, "w")
    flObj.write(reqStr)
    flObj.close()

  #----------------------------------
  def write_cert_crt(self, fqdn, crtStr):
    curCrtPath = os.path.join(self.certsPath, fqdn + endings["cert"])
    flObj = open(curCrtPath, "w")
    flObj.write(crtStr)
    flObj.close()

  #----------------------------------
  def delete_cert_req(self, fqdn):
    curReqPath = os.path.join(self.reqsPath, fqdn + endings["req"])
    if os.path.isfile(curReqPath):
      os.remove(curReqPath)

  #----------------------------------
  def delete_cert_all(self, fqdn):
    delPathAry = [
      os.path.join(self.keysPath, fqdn + endings["key"]),
      os.path.join(self.reqsPath, fqdn + endings["req"]),
      os.path.join(self.certsPath, fqdn + endings["cert"]),
    ]
    for curPath in delPathAry:
      if os.path.isfile(curPath):
        os.remove(curPath)

  #----------------------------------
  def list_requests(self):
    resAry = []
    tmpRes = os.listdir(self.reqsPath)
    for reqFileName in tmpRes:
      tmpFilePath = os.path.join(self.reqsPath, reqFileName)
      if os.path.isfile(tmpFilePath):
        cn = reqFileName.replace(endings["req"], "")
        resAry.append(cn)

    return resAry

  #----------------------------------
  def list_certificates(self):
    resAry = []
    tmpRes = os.listdir(self.certsPath)
    for crtFileName in tmpRes:
      tmpFilePath = os.path.join(self.certsPath, crtFileName)
      if os.path.isfile(tmpFilePath):
        cn = crtFileName.replace(endings["cert"], "")
        resAry.append(cn)

    return resAry
  
  #----------------------------------
  def create_export(self):
    filename = self.caname+"_export.tar.gz"  
    tgtPath = os.path.join(baseFolderPath, filename)

    tar = tarfile.open(tgtPath, "w:gz")
    tar.add(self.capath, arcname=self.caname)
    
    myHelpers = helpers()
    expDataObj = {
      "caname": self.caname,
      "timestamp": myHelpers.create_unix_timestamp()
    }

    infTgtPath = os.path.join(self.capath, 'export.yaml')
    flObj = open(infTgtPath, 'w')
    yaml.dump(expDataObj, flObj, default_flow_style=False)
    flObj.close()

    tar.add(infTgtPath, arcname="export.yaml")
    tar.close()
    
    #return tgtPath
    return baseFolderPath, filename
  
  #----------------------------------
  def clear_export(self):
    filenames = [
      self.caname+"_export.tar.gz",
      "export.yaml"
    ]
    for filename in filenames:
      rmPath = os.path.join(self.capath, filename)
      os.remove(rmPath)

  #----------------------------------
  def import_ca(self, expPath):
    #print(expPath)
    tarObj = tarfile.open(expPath)
    # flList = tarObj.getmembers()
    # print(flList)
    infFile = tarObj.getmember("export.yaml")
    flObj = tarObj.extractfile(infFile)
    objIn = yaml.safe_load(flObj)

    if "caname" not in objIn or "timestamp" not in objIn:
      raise Exception("invalid ca export file")
    else:
      caname = objIn["caname"]
    
    if os.path.isdir(os.path.join(baseFolderPath, caname)):
      raise Exception("ca '%s' already exists" %caname)

    tarObj.extractall(path=baseFolderPath)
    tarObj.close()
    os.remove(os.path.join(baseFolderPath, "export.yaml"))
    os.remove(expPath)

#----------------------------------------------------------
class meta_collector:

  #----------------------------------
  def __init__(self):
    inf = "meta collector object created"

  #----------------------------------
  def list_cas(self):
    caAry = []
    tmpRes = os.listdir(baseFolderPath)
    for dirname in tmpRes:
      tmpPath = os.path.join(baseFolderPath, dirname)
      if os.path.isdir( tmpPath):
        caAry.append(dirname)
    
    return caAry

  #----------------------------------
  def collect_certificate_authorities(self ): # Ein Traum in Code!!!!
    
    resObj = []
    caAry = self.list_cas()

    for caname in caAry:
      try:
        tmpRootCert = cert_root(caname)
        tmpRootCert.load_cert_from_fs()
      except Exception as e:
        print(e)
        continue
      
      tmpObj = tmpRootCert.get_meta_data()
      tmpObj["name"] = caname

      resObj.append(tmpObj)

    #--------------------------
    return resObj

  #----------------------------------
  def collect_requests(self, caname):
    resObj = []
    
    myCertFs = cert_fs(caname)
    reqAry = myCertFs.list_requests()
    
    for cn in reqAry:
      try:
        tmpReq = cert_websrv(caname, cn)
        tmpReq.load_req_from_fs()
      except Exception as e:
        print(e)
        continue
      
      tmpObj = tmpReq.get_meta_data(req=True)
      tmpObj["caname"] = caname

      resObj.append(tmpObj)

    return resObj
    
  #----------------------------------
  def collect_certificates(self, caname):
    resObj = []
    
    myCertFs = cert_fs(caname)
    crtAry = myCertFs.list_certificates()
    
    for cn in crtAry:
      try:
        tmpCert = cert_websrv(caname, cn)
        tmpCert.load_cert_from_fs()
      except Exception as e:
        print(e)
        continue
      
      tmpObj = tmpCert.get_meta_data()
      tmpObj["caname"] = caname

      # for classKey, crtKey in subjects.items():
      #   if hasattr(tmpCert, classKey):
      #     if getattr(tmpCert, classKey):
      #       tmpObj[classKey] = getattr(tmpCert, classKey)

      resObj.append(tmpObj)

    return resObj

  #----------------------------------
  
  
  #----------------------------------
  
  
  #----------------------------------


#----------------------------------------------------------
class cert_root:
  #----------------------------------
  def __init__(self, caname=None):
    self.commonname = None
    if caname: self.set_common_name(caname)

    self.country = None
    self.state = None
    self.city = None
    self.organization = None
    self.unit = None
    self.email = None

    self.validity = None
    self.renewTime = stdRootValidity

    self.key = None
    self.crtObj = None

    self.crtStr = None
    self.keyStr = None

  #----------------------------------
  def set_common_name(self, cn ):
    cn = cn.lower()
    if type(cn) != str:
      raise Exception("wrong format. Use string")
    
    regEx = re.search('[a-z/.-]+[a-z]{2}$', cn)
    if not regEx:
      raise Exception("invalid ca name: %s" %cn)

    self.commonname = cn

  #----------------------------------
  def set_country_code(self, ccode ):
    try:
      ccode = ccode.upper()
    except:
      raise Exception("use string with two characters")

    if ccode not in countryCodes:
      raise Exception("Invalid country code. Use one of the following:\n %s" %countryCodes)
    else:
      self.country = ccode

  #----------------------------------
  def set_state(self, state ):
    if type(state) != str:
      raise Exception("wrong format. Use string")
    else:
      self.state = state
  
  #----------------------------------
  def set_city(self, city ):
    if type(city) != str:
      raise Exception("wrong format. Use string")
    else:
      self.city = city

  #----------------------------------
  def set_organization(self, organization ):
    if type(organization) != str:
      raise Exception("wrong format. Use string")
    else:
      self.organization = organization

  #----------------------------------
  def set_unit(self, unit ):
    if type(unit) != str:
      raise Exception("wrong format. Use string")
    else:
      self.unit = unit

  #----------------------------------
  def set_email(self, email):
    email = email.lower()
    if type(email) != str:
      raise Exception("wrong format. Use string")
    
    #regEx = re.search('[a-z1-9.\-]+[@][a-z1-9]+[.][a-z]{2,4}$', email)
    regEx = re.search('[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email)
    if not regEx:
      raise Exception("invalid email: %s" %email)

    self.email = email

  #----------------------------------
  def gen_priv_key(self):
    keyObj = crypto.PKey()
    keyObj.generate_key(crypto.TYPE_RSA, keyLen)
    self.key = keyObj

  #----------------------------------
  def create_root_cert(self):
    missingSubs = []
    for sub in mandaSubjects:
      if not getattr(self, sub):
        missingSubs.append(sub)
    
    if len(missingSubs) > 0:
      raise Exception("the following subjects are missing: %s" %missingSubs)

    if not self.key:
      raise Exception("Please generate or load a private key first")

    self.crtObj = crypto.X509()

    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        setattr(self.crtObj.get_subject(), crtKey, curVal)

    myHelpers = helpers()
    self.crtObj.set_serial_number(myHelpers.gen_rendom_sn())
    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(self.renewTime)

    self.crtObj.set_issuer(self.crtObj.get_subject())

    self.crtObj.set_pubkey(self.key)
    self.crtObj.sign(self.key, 'sha512')

  #----------------------------------
  def renew_root_cert(self, days=None):
    if not self.crtObj or not self.key:
      raise Exception("Please generate or load a certificate and private key first")
    
    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        setattr(self.crtObj.get_subject(), crtKey, curVal)

    if days:
      renewPeriod = days*24*60*60
    else:
      renewPeriod = self.renewTime

    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(renewPeriod)

    self.crtObj.set_issuer(self.crtObj.get_subject())
    self.crtObj.set_pubkey(self.key)
    self.crtObj.sign(self.key, 'sha512')

  #----------------------------------
  def convert_cert_to_string(self):
    if not self.crtObj or not self.key:
      raise Exception("Please generate or load a certificate and private key first")

    crtStr = crypto.dump_certificate(crypto.FILETYPE_PEM, self.crtObj)
    keyStr = crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key)
    self.crtStr = crtStr.decode("utf-8")
    self.keyStr = keyStr.decode("utf-8")

  #----------------------------------
  def write_cert_to_fs(self):
    self.convert_cert_to_string()
    myCertFs = cert_fs(self.commonname)
    myCertFs.write_root_cert(self.crtStr)
    myCertFs.write_root_key(self.keyStr)

  #----------------------------------
  def load_cert_from_fs(self):
    myCertFs = cert_fs(self.commonname)
    self.keyStr = myCertFs.get_key_str()
    self.crtStr = myCertFs.get_cert_str()

    self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.keyStr)
    self.crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, self.crtStr)
    
    for classKey, crtKey in subjects.items():
      if hasattr(self.crtObj.get_subject(), crtKey):
        curVal = getattr(self.crtObj.get_subject(), crtKey)
        setattr(self, classKey, curVal)
        #print(curVal)
    
    self.validity = self.crtObj.get_notAfter()

  #----------------------------------
  def get_meta_data(self):
    self.load_cert_from_fs()
    resObj = {}
    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        resObj[classKey] = curVal
    
    if self.validity:
      myHelpers = helpers()
      resObj["validity"] = myHelpers.asn1_to_datestr(self.validity)

    return resObj
  
  #----------------------------------
  

  
  #----------------------------------


#------------------------------------------------------
class cert_websrv:
  #----------------------------------
  def __init__(self, caname, fqdn):
    
    self.caname = None
    self.caCrtObj = None
    self.commonname = None
    self.ipv4 = None
    self.ipv6 = None

    self.sans = []

    self.country = None
    self.state = None
    self.city = None
    self.organization = None
    self.unit = None
    self.email = None

    self.load_ca(caname)
    self.set_fqdn(fqdn)

    self.validity = None
    self.renewTime = stdCertValidity

    self.pKey = None

    self.reqObj = None
    self.crtObj = None

    self.keyStr = None
    self.reqStr = None
    self.crtStr = None
    
      
  #----------------------------------
  def set_fqdn(self, fqdn):
    fqdn = fqdn.lower()
    if type(fqdn) != str:
      raise Exception("wrong format. Use string")
    
    regEx = re.search('[a-z/.\-]+[.][a-z]{2,4}$', fqdn)
    if not regEx:
      raise Exception("invalid fqdn: %s" %fqdn)

    self.commonname = fqdn

  #----------------------------------
  def set_country_code(self, ccode ):
    try:
      ccode = ccode.upper()
    except:
      raise Exception("use string with two characters")

    if ccode not in countryCodes:
      raise Exception("Invalid country code. Use one of the following:\n %s" %countryCodes)
    else:
      self.country = ccode

  #----------------------------------
  def set_state(self, state ):
    if type(state) != str:
      raise Exception("wrong format. Use string")
    else:
      self.state = state
  
  #----------------------------------
  def set_city(self, city ):
    if type(city) != str:
      raise Exception("wrong format. Use string")
    else:
      self.city = city

  #----------------------------------
  def set_organization(self, organization ):
    if type(organization) != str:
      raise Exception("wrong format. Use string")
    else:
      self.organization = organization

  #----------------------------------
  def set_unit(self, unit ):
    if type(unit) != str:
      raise Exception("wrong format. Use string")
    else:
      self.unit = unit

  #----------------------------------
  def set_email(self, email):
    email = email.lower()
    if type(email) != str:
      raise Exception("wrong format. Use string")
    
    #regEx = re.search('[a-z1-9.\-]+[@][a-z1-9\-]+[.][a-z]{2,4}$', email)
    regEx = re.search('[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email)
    if not regEx:
      raise Exception("invalid email: %s" %email)

    self.email = email
  
  #----------------------------------
  def set_ipv4(self, ipv4Str):
    if type(ipv4Str) != str:
      raise Exception("wrong format. Use string")
    
    regEx = re.search('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ipv4Str)
    if not regEx:
      raise Exception("invalid email: %s" %ipv4Str)

    self.ipv4 = ipv4Str

  #----------------------------------
  def add_san(self, typ, sanStr):
    typ = typ.upper()
    
    #---------------
    if typ not in sanTypes:
      raise Exception("Sans type must be one of the following: %s" %sanTypes)
    
    #---------------
    myHelpers = helpers()
    res = myHelpers.chk_san_validity(typ, sanStr)
    if not res:
      raise Exception("Invalid value (string) for key: %s" %typ)

    #---------------
    sanObj = {
      "key": typ,
      "val": sanStr
    }
    self.sans.append(sanObj)

  #----------------------------------
  def load_ca(self, caname):
    try:
      myCa = cert_root(caname)
      myCa.load_cert_from_fs()
    except Exception as e:
      print(e)
      raise Exception("failed to load ca: %s" %caname)
    
    self.caname = caname
    self.caCrtObj = myCa.crtObj
    self.caKeyObj = myCa.key

    self.country = myCa.country
    #self.state = myCa.state
    #self.city = myCa.city
    self.organization = myCa.organization
    #self.unit = myCa.unit

  #----------------------------------
  def gen_priv_key(self):
    keyObj = crypto.PKey()
    keyObj.generate_key(crypto.TYPE_RSA, keyLen)
    self.pKey = keyObj 
  
  #----------------------------------
  def convert_cert_objects_to_string(self):
    chk = []
    if self.pKey:
      keyStr = crypto.dump_privatekey(crypto.FILETYPE_PEM, self.pKey)
      self.keyStr = keyStr.decode("utf-8")
      chk.append("key")

    if self.reqObj:
      reqStr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, self.reqObj)
      self.reqStr = reqStr.decode("utf-8")
      chk.append("req")

    if self.crtObj:
      crtStr = crypto.dump_certificate(crypto.FILETYPE_PEM, self.crtObj)
      self.crtStr = crtStr.decode("utf-8")
      chk.append("crt")

    return chk

  #----------------------------------
  def create_cert_request(self, update=False):
    
    missingSubs = []
    for sub in mandaSubjects:
      if not getattr(self, sub):
        missingSubs.append(sub)
    if len(missingSubs) > 0:
      raise Exception("please set the following values first: %s" %missingSubs)
    
    #------------------
    if not update:
      self.reqObj = crypto.X509Req()
    
    if self.reqObj.get_version() != 2:
      self.reqObj.set_version(2)
    
    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        setattr(self.reqObj.get_subject(), crtKey, curVal)

    #------------------
    sanList = [
      "DNS: {0}".format(self.commonname)
    ]
    #------------
    if self.ipv4: 
      sanList.append( "IP: {0}".format(self.ipv4) )
    if self.ipv6: 
      sanList.append( "IP: {0}".format(self.ipv6) )
    #------------
    for sanObj in self.sans:
      sanList.append( sanObj["key"]+": {0}".format(sanObj["val"]) )

    #------------
    sanListStrEnc = ", ".join(sanList).encode()
    #print(sanListStrEnc)
    
    sanObj = [ 
      crypto.X509Extension(type_name=b"basicConstraints", critical=False, value=b"CA:FALSE" ),
      crypto.X509Extension(type_name=b"keyUsage", critical=False, value=b"digitalSignature" ),
      crypto.X509Extension(type_name=b"extendedKeyUsage", critical=False, value=b"serverAuth" ),
      crypto.X509Extension(type_name=b"subjectAltName", critical=False, value=sanListStrEnc)
    ]

    #SANS k??nnen im Request mit pyOpenSSL nachtr??glich nicht ver??ndert werden. 
    #Zumindest habe ich nach 10h nicht rausgefunden wie...
    self.reqObj.add_extensions(sanObj)

    #------------------
    #if not update:
    self.reqObj.set_pubkey(self.pKey)
    self.reqObj.sign(self.pKey, 'sha512') # Noch mehr Drecksack!!!!!!!!!!!!!!!!!!!!!!!!

  #----------------------------------
  def sign_cert(self, days=None):
    # if not self.pKey or not self.reqObj:
    #   raise Exception("Please create/load key and req first")
    if not self.reqObj:
      raise Exception("Please create/load request first")
    
    self.crtObj = crypto.X509()
    self.crtObj.set_version(2) # Drecksack!!!!!!!!!!!!

    myHelpers = helpers()
    self.crtObj.set_serial_number(myHelpers.gen_rendom_sn())
    
    if days:
      renewPeriod = days*24*60*60
    else:
      renewPeriod = self.renewTime
    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(renewPeriod)

    self.crtObj.set_issuer(self.caCrtObj.get_subject())
    self.crtObj.set_subject(self.reqObj.get_subject())
    self.crtObj.add_extensions(self.reqObj.get_extensions())
    #self.crtObj.set_pubkey(self.pKey)
    self.crtObj.set_pubkey(self.caKeyObj)

    self.crtObj.sign(self.caKeyObj, 'sha512')

  #----------------------------------
  def write_cert_objects_to_fs(self, cus=None):
    if type(cus) == list:
      res = cus
    else:
      res = self.convert_cert_objects_to_string()
    
    myCertFs = cert_fs(self.caname)

    if "key" in res:
      myCertFs.write_cert_pkey(fqdn=self.commonname, keyStr=self.keyStr)

    if "req" in res:
      myCertFs.write_cert_req(fqdn=self.commonname, reqStr=self.reqStr)

    if "crt" in res:
      myCertFs.write_cert_crt(fqdn=self.commonname, crtStr=self.crtStr)

    return res

  #----------------------------------
  def load_req_from_fs(self):
    myCertFs = cert_fs(self.caname)
    
    self.reqStr = myCertFs.get_req_str(fqdn=self.commonname)
    self.reqObj = crypto.load_certificate_request(crypto.FILETYPE_PEM, self.reqStr) 

    try:
      self.keyStr = myCertFs.get_key_str(fqdn=self.commonname)
      self.pKey = crypto.load_privatekey(crypto.FILETYPE_PEM, self.keyStr)
    except Exception as e:
      print(e)
      self.keyStr = "Key not available. \nAsk requester ;)"

    for classKey, crtKey in subjects.items():
      if hasattr(self.reqObj.get_subject(), crtKey):
        curVal = getattr(self.reqObj.get_subject(), crtKey)
        setattr(self, classKey, curVal)

    myHelpers = helpers()
    try:
      self.sans = myHelpers.get_req_sans_list(self.reqObj)
    except Exception as e:
      print(e)

  #----------------------------------
  def load_req_from_string(self):
    self.reqObj = crypto.load_certificate_request(crypto.FILETYPE_PEM, self.reqStr) 

    for classKey, crtKey in subjects.items():
      if hasattr(self.reqObj.get_subject(), crtKey):
        curVal = getattr(self.reqObj.get_subject(), crtKey)
        setattr(self, classKey, curVal)
    
    myHelpers = helpers()
    try:
      self.sans = myHelpers.get_req_sans_list(self.reqObj)
    except Exception as e:
      print(e)
    
  #----------------------------------
  def load_cert_from_fs(self):
    myCertFs = cert_fs(self.caname)
    
    self.crtStr = myCertFs.get_cert_str(fqdn=self.commonname)
    self.crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, self.crtStr)

    try:
      self.keyStr = myCertFs.get_key_str(fqdn=self.commonname)
      self.pKey = crypto.load_privatekey(crypto.FILETYPE_PEM, self.keyStr)
    except Exception as e:
      self.keyStr = "Key not available. \nAsk requester ;)"
      print(e)
    
    for classKey, crtKey in subjects.items():
      if hasattr(self.crtObj.get_subject(), crtKey):
        curVal = getattr(self.crtObj.get_subject(), crtKey)
        setattr(self, classKey, curVal)

    self.validity = self.crtObj.get_notAfter()
    
    myHelpers = helpers()
    try:
      self.sans = myHelpers.get_crt_sans_list(self.crtObj)
    except Exception as e:
      print(e)
  
  #----------------------------------
  def renew_cert(self, days=None):
    #if not self.crtObj or not self.pKey:
    if not self.crtObj:
      raise Exception("Please generate or load a certificate")
    
    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        setattr(self.crtObj.get_subject(), crtKey, curVal)

    if days:
      renewPeriod = days*24*60*60
    else:
      renewPeriod = self.renewTime

    #UIUIUIUIUIUIUIU WZF!!!---------------------
    sanScanObj = {
      "IP": [],
      "DNS": []
    }
    x = self.crtObj.get_extension_count()
    for i in range(x):
      extStr = str( self.crtObj.get_extension(i) )
      extSplt = extStr.split(", ")
      for extStrSplt in extSplt:
        for key, tmp in sanScanObj.items():
          if extStrSplt.startswith(key):
            try: 
              extVal = extStrSplt.split(":")[1].replace(" ", "")
              sanScanObj[key].append(extVal)
            except: 
              continue 
    #print(sanScanObj)
    
    #------------
    sanList = []
    for sanObj in self.sans:
      try:
        if sanObj["val"] not in sanScanObj[sanObj["key"]]:
          sanList.append( sanObj["key"]+": {0}".format(sanObj["val"]) )
      except Exception as e:
        print(e)

    #------------
    if len(sanList) > 0:
      sanListStrEnc = ", ".join(sanList).encode()
      sanObj = [ 
        crypto.X509Extension(type_name=b"subjectAltName", critical=False, value=sanListStrEnc)
      ]
      self.crtObj.add_extensions(sanObj)

    #UIUIUIUIUIUIUIU WZF!!!---------------------

    #-------------

    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(renewPeriod)

    # Das die 4 methoden raus m??ssen is auch ganz einfach rauszufinden... WZF!
    #self.crtObj.set_issuer(self.crtObj.get_subject())  
    #self.crtObj.set_pubkey(self.pKey)
    #self.crtObj.set_pubkey(self.caKeyObj)
    #self.crtObj.sign(self.pKey, 'sha512')
    self.crtObj.sign(self.caKeyObj, 'sha512')


  #--------------------------------------------------------------
  def get_meta_data(self, req=False):
    if req: 
      self.load_req_from_fs()
    else:
      self.load_cert_from_fs()

    resObj = {}
    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        resObj[classKey] = curVal
    
    #--------------
    resObj["sans"] = self.sans

    #--------------
    if self.validity:
      myHelpers = helpers()
      resObj["validity"] = myHelpers.asn1_to_datestr(self.validity)
      
    return resObj
  
  
  #----------------------------------
  
  
  #----------------------------------