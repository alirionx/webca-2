import os, sys
import json, yaml
from OpenSSL import crypto, SSL
import random


#-Tools Globals------------------------------------
curDir = os.path.dirname(os.path.realpath(__file__)) 

baseFolderPath = os.path.join(curDir, "certs")
folders = ["root", "req", "crt", "key"]

subjects = ["commonname", "country", "state", "city", "organization", "unit"]
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

domChars = [
  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", 
  "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-" 
]

stdValidity = 3*365*24*60*60

keyLen = 2048

#--------------------------------------------------


#--------------------------------------------------
class cert_fs:
  #----------------------------------
  def __init__(self, caname):
    
    self.caname = caname
    self.capath = os.path.join(baseFolderPath, caname)
    self.crtpath = os.path.join(self.capath, "root", caname+"_ca.pem")
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
  def get_root_cert_str(self):
    flObj = open(self.crtpath, "rt")
    crtStr = flObj.read()
    flObj.close()
    return crtStr

  #----------------------------------
  def get_root_key_str(self):
    flObj = open(self.keypath, "rt")
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


#--------------------------------------------------
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

    self.validity = stdValidity
    
    self.key = None
    self.crtObj = None

    self.crtStr = None
    self.keyStr = None

  #----------------------------------
  def set_common_name(self, cn ):
    cn = cn.lower()
    if type(cn) != str:
      raise Exception("wrong format. Use string")
    if len(cn) < 4:
      raise Exception("common name to short. Min 4 chars required.")
    for char in cn:
      if char not in domChars:
        raise Exception("invalid character: %s" %char)
    
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
  def gen_rendom_sn(self):
    ranSn = random.getrandbits(64)
    return ranSn

  #----------------------------------
  def gen_priv_key(self):
    keyObj = crypto.PKey()
    keyObj.generate_key(crypto.TYPE_RSA, keyLen)
    self.key = keyObj

  #----------------------------------
  def create_root_cert(self):
    missingSubs = []
    for sub in subjects:
      if not getattr(self, sub):
        missingSubs.append(sub)
    
    if len(missingSubs) > 0:
      raise Exception("the following subjects are missing: %s" %missingSubs)

    if not self.key:
      raise Exception("Please generate or load a private key first")

    self.crtObj = crypto.X509()
    self.crtObj.get_subject().C = self.country
    self.crtObj.get_subject().ST = self.state
    self.crtObj.get_subject().L = self.city
    self.crtObj.get_subject().O = self.organization
    self.crtObj.get_subject().OU = self.unit
    self.crtObj.get_subject().CN = self.commonname

    self.crtObj.set_serial_number(self.gen_rendom_sn())
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
    self.keyStr = myCertFs.get_root_key_str()
    self.crtStr = myCertFs.get_root_cert_str()
    
    self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.keyStr)
    self.crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, self.crtStr)
    
    self.country = self.crtObj.get_subject().C
    self.state = self.crtObj.get_subject().ST 
    self.city = self.crtObj.get_subject().L
    self.organization = self.crtObj.get_subject().O 
    self.unit = self.crtObj.get_subject().OU
    #self.commonname = self.crtObj.get_subject().CN
    
  #----------------------------------
  
  
  #----------------------------------
  
  
  #----------------------------------


class cert_websrv:
  #----------------------------------
  def __init__(self, caname, fqdn):
    
    self.caname = None
    self.caCrtObj = None
    self.fqdn = None

    self.country = None
    self.state = None
    self.city = None
    self.organization = None
    self.unit = None

    self.load_ca(caname)
    self.set_fqdn(fqdn)

    self.validity = stdValidity

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
    elif len(fqdn) < 8:
      raise Exception("common name to short. Min 8 chars required.")
    elif "." not in fqdn or "." in fqdn[-2:] or "-" in fqdn[-2:]:
      raise Exception("invalid FQDN: %s" %fqdn)
    
    for char in fqdn:
      if char not in domChars:
        raise Exception("invalid character: %s" %char)
    
    self.fqdn = fqdn

  #----------------------------------
  def load_ca(self, caname):
    
    try:
      myCa = cert_root(caname)
      myCa.load_cert_from_fs()
    except Exception as e:
      print(e)
      raise Exception("infailed to load ca: %s" %caname)
    
    self.caname = caname
    self.caCrtObj = myCa.crtObj

    self.country = myCa.country
    self.state = myCa.state
    self.city = myCa.city
    self.organization = myCa.organization
    self.unit = myCa.unit

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

    self.reqObj.get_subject().C = self.country
    self.reqObj.get_subject().ST = self.state
    self.reqObj.get_subject().L = self.city
    self.reqObj.get_subject().O = self.organization
    self.reqObj.get_subject().OU = self.unit
    self.reqObj.get_subject().CN = self.fqdn

    self.reqObj.set_pubkey(self.pKey)
  
  #----------------------------------
  def write_cert_objects_to_fs(self, cus=None):
    if type(cus) == list:
      res = cus
    else:
      res = self.convert_cert_objects_to_string()
    
    myCertFs = cert_fs(self.caname)

    if "key" in res:
      myCertFs.write_cert_pkey(fqdn=self.fqdn, pKeyStr=self.pKeyStr)

    if "req" in res:
      myCertFs.write_cert_req(fqdn=self.fqdn, reqStr=self.reqStr)

    if "crt" in res:
      myCertFs.write_cert_crt(fqdn=self.fqdn, crtStr=self.crtStr)

    return res

    
    


  #----------------------------------
  
  
  #----------------------------------
  
  
  #----------------------------------