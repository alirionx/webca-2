import os, sys
import json, yaml
import re
from OpenSSL import crypto, SSL
import random


#-Tools Globals------------------------------------
curDir = os.path.dirname(os.path.realpath(__file__)) 

baseFolderPath = os.path.join(curDir, "certs")
folders = ["root", "req", "crt", "key"]

subjects = {
  "commonname": "CN", 
  "country": "ST", 
  "city": "L", 
  "organization": "O", 
  "unit": "OU", 
  "email": "emailAddress"
}
mandaSubjects = ["commonname", "country", "organization", "email"]

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

stdRootValidity = 10*365*24*60*60
stdCertValidity = 3*365*24*60*60

keyLen = 2048

#----------------------------------------------------------

class helpers:
  #----------------------------------
  def __init__(self):
    inf = "helpers object created"

  #----------------------------------
  def gen_rendom_sn(self, bits=64):
    ranSn = random.getrandbits(bits)
    return ranSn
  
  #----------------------------------

#----------------------------------------------------------
class cert_fs:
  #----------------------------------
  def __init__(self, caname):
    
    self.caname = caname
    self.capath = os.path.join(baseFolderPath, caname)
    self.crtpath = os.path.join(self.capath, "root", caname+"_ca.crt")
    self.keypath = os.path.join(self.capath, "root", caname+"_ca.key")

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
  def get_cert_str(self, fqdn=None):
    if not fqdn: path = self.crtpath
    else: path = os.path.join(self.certsPath, fqdn+".crt")

    flObj = open(path, "rt")
    crtStr = flObj.read()
    flObj.close()
    return crtStr

  #----------------------------------
  def get_key_str(self, fqdn=None):
    if not fqdn: path = self.keypath
    else: path = os.path.join(self.keysPath, fqdn+".key")

    flObj = open(path, "rt")
    keyStr = flObj.read()
    flObj.close()
    return keyStr

  #----------------------------------
  def write_cert_pkey(self, fqdn, pKeyStr):
    curKeyPath = os.path.join(self.keysPath, fqdn+".key")
    flObj = open(curKeyPath, "w")
    flObj.write(pKeyStr)
    flObj.close()

  #----------------------------------
  def write_cert_req(self, fqdn, reqStr):
    curReqPath = os.path.join(self.reqsPath, fqdn+".csr")
    flObj = open(curReqPath, "w")
    flObj.write(reqStr)
    flObj.close()

  #----------------------------------
  def write_cert_crt(self, fqdn, crtStr):
    curCrtPath = os.path.join(self.certsPath, fqdn+".crt")
    flObj = open(curCrtPath, "w")
    flObj.write(crtStr)
    flObj.close()

  #----------------------------------
  def list_certificates(self):
    resAry = []
    tmpRes = os.listdir(self.certsPath)
    for crtFileName in tmpRes:
      tmpFilePath = os.path.join(self.certsPath, crtFileName)
      if os.path.isfile(tmpFilePath):
        cn = crtFileName.replace(".crt", "").replace(".pem", "")
        resAry.append(cn)

    return resAry
  
  #----------------------------------
  
  
  #----------------------------------


#----------------------------------------------------------
class meta_collector:

  #----------------------------------
  def __init__(self):
    inf = "meta collector object created"

  #----------------------------------
  def collect_certificate_authorities(self): # Ein Traum in Code!!!!
    
    resObj = []
    caAry = []
    tmpRes = os.listdir(baseFolderPath)
    for dirname in tmpRes:
      tmpPath = os.path.join(baseFolderPath, dirname)
      if os.path.isdir( tmpPath):
        caAry.append(dirname)

    for caname in caAry:
      try:
        tmpRootCert = cert_root(caname)
        tmpRootCert.load_cert_from_fs()
      except Exception as e:
        print(e)
        continue

      tmpObj = { "name": caname }
      for classKey, crtKey in subjects.items():
        if hasattr(tmpRootCert, classKey):
          if getattr(tmpRootCert, classKey):
            tmpObj[classKey] = getattr(tmpRootCert, classKey)

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

      tmpObj = { "name": cn }
      for classKey, crtKey in subjects.items():
        if hasattr(tmpCert, classKey):
          if getattr(tmpCert, classKey):
            tmpObj[classKey] = getattr(tmpCert, classKey)

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

    self.validity = stdRootValidity
    
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
    
    regEx = re.search('[a-z1-9.\-]+[@][a-z1-9]+[.][a-z]{2,4}$', email)
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

    # self.crtObj.get_subject().C = self.country
    # self.crtObj.get_subject().ST = self.state
    # self.crtObj.get_subject().L = self.city
    # self.crtObj.get_subject().O = self.organization
    # self.crtObj.get_subject().OU = self.unit
    # self.crtObj.get_subject().CN = self.commonname

    myHelpers = helpers()
    self.crtObj.set_serial_number(myHelpers.gen_rendom_sn())
    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(self.validity)

    self.crtObj.set_issuer(self.crtObj.get_subject())

    self.crtObj.set_pubkey(self.key)
    self.crtObj.sign(self.key, 'sha512')

  #----------------------------------
  def renew_root_cert(self, days=None):
    if not self.crtObj or not self.key:
      raise Exception("Please generate or load a certificate and private key first")
    
    if days:
      renewPeriod = days*24*60*60
    else:
      renewPeriod = self.validity

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
      
    # self.country = self.crtObj.get_subject().C
    # self.state = self.crtObj.get_subject().ST 
    # self.city = self.crtObj.get_subject().L
    # self.organization = self.crtObj.get_subject().O 
    # self.unit = self.crtObj.get_subject().OU
    # self.commonname = self.crtObj.get_subject().CN
    
  #----------------------------------
  
  
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

    self.country = None
    self.state = None
    self.city = None
    self.organization = None
    self.unit = None
    self.email = None

    self.load_ca(caname)
    self.set_fqdn(fqdn)

    self.validity = stdCertValidity

    self.pKey = None

    self.reqObj = None
    self.crtObj = None

    self.pKeyStr = None
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
    
    regEx = re.search('[a-z1-9.\-]+[@][a-z1-9\-]+[.][a-z]{2,4}$', email)
    if not regEx:
      raise Exception("invalid email: %s" %email)

    self.email = email
  
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
      self.pKeyStr = keyStr.decode("utf-8")
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
  def create_cert_request(self):
    self.reqObj = crypto.X509Req()
    self.reqObj.set_version(3)


    for classKey, crtKey in subjects.items():
      curVal = getattr(self, classKey)
      if curVal:
        setattr(self.reqObj.get_subject(), crtKey, curVal)

    # self.reqObj.get_subject().C = self.country
    # self.reqObj.get_subject().ST = self.state
    # self.reqObj.get_subject().L = self.city
    # self.reqObj.get_subject().O = self.organization
    # self.reqObj.get_subject().OU = self.unit
    # self.reqObj.get_subject().CN = self.commonname
    # self.reqObj.get_subject().emailAddress = self.email
    # test = self.reqObj.get_subject()
    # res = setattr(self.reqObj.get_subject(), "OU", "Palim")

    sanList = [
      "DNS: {0}".format(self.commonname),
    ]
    if self.ipv4: 
      sanList.append( "IP: {0}".format(self.ipv4) )
    if self.ipv6: 
      sanList.append( "IP: {0}".format(self.ipv6) )


    sanListStrEnc = ", ".join(sanList).encode()

    sanObj = [ 
      crypto.X509Extension(type_name=b"basicConstraints", critical=False, value=b"CA:FALSE" ),
      crypto.X509Extension(type_name=b"keyUsage", critical=False, value=b"digitalSignature" ),
      crypto.X509Extension(type_name=b"extendedKeyUsage", critical=False, value=b"serverAuth" ),
      crypto.X509Extension(type_name=b"subjectAltName", critical=False, value=", ".join(sanList).encode())
    ]
    self.reqObj.add_extensions(sanObj)

    self.reqObj.set_pubkey(self.pKey)
  
  #----------------------------------
  def sign_cert(self):
    if not self.pKey or not self.reqObj:
      raise Exception("Please create/load key and req first")
    
    self.crtObj = crypto.X509()
    self.crtObj.set_version(2) # Drecksack!!!!!!!!!!!!

    myHelpers = helpers()
    self.crtObj.set_serial_number(myHelpers.gen_rendom_sn())
    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(self.validity)

    self.crtObj.set_issuer(self.caCrtObj.get_subject())
    self.crtObj.set_subject(self.reqObj.get_subject())
    self.crtObj.add_extensions(self.reqObj.get_extensions())
    self.crtObj.set_pubkey(self.pKey)

    self.crtObj.sign(self.caKeyObj, 'sha512')

  #----------------------------------
  def write_cert_objects_to_fs(self, cus=None):
    if type(cus) == list:
      res = cus
    else:
      res = self.convert_cert_objects_to_string()
    
    myCertFs = cert_fs(self.caname)

    if "key" in res:
      myCertFs.write_cert_pkey(fqdn=self.commonname, pKeyStr=self.pKeyStr)

    if "req" in res:
      myCertFs.write_cert_req(fqdn=self.commonname, reqStr=self.reqStr)

    if "crt" in res:
      myCertFs.write_cert_crt(fqdn=self.commonname, crtStr=self.crtStr)

    return res

  #----------------------------------
  def load_cert_from_fs(self):
    myCertFs = cert_fs(self.caname)
    self.keyStr = myCertFs.get_key_str(fqdn=self.commonname)
    self.crtStr = myCertFs.get_cert_str(fqdn=self.commonname)

    self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.keyStr)
    self.crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, self.crtStr)
    
    for classKey, crtKey in subjects.items():
      if hasattr(self.crtObj.get_subject(), crtKey):
        curVal = getattr(self.crtObj.get_subject(), crtKey)
        setattr(self, classKey, curVal)

  #----------------------------------
  def renew_cert(self, days=None):
    if not self.crtObj or not self.key:
      raise Exception("Please generate or load a certificate and private key first")
    
    if days:
      renewPeriod = days*24*60*60
    else:
      renewPeriod = self.validity

    self.crtObj.gmtime_adj_notBefore(0)
    self.crtObj.gmtime_adj_notAfter(renewPeriod)

    self.crtObj.set_issuer(self.crtObj.get_subject())
    self.crtObj.set_pubkey(self.key)
    self.crtObj.sign(self.key, 'sha512')
    

  #----------------------------------
  def print_cert_subs(self):
    common_name = self.crtObj.get_subject().CN
    print(common_name)

  #----------------------------------
  
  
  #----------------------------------
  
  
  #----------------------------------