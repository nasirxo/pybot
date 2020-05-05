from requests import *
from bs4 import *
import os
import json
from base64 import *



url = "https://free.facebook.com{}"
agent = {'user-agent':"Mozilla/5.0 (Linux; Android 5.0; ASUS_T00G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"}
s = Session()

if not os.path.exists(".cookie"):
   pass
else:
   try:
      s.cookies.update(json.loads(open('.cookie','r').read()))
   except:
      pass



def fblogin(email,password):
 try:
   s = Session()
   cred = {'email':str(email),'pass':str(password)}
   r = s.post(url.format("/login"),data = cred)
   if "m_ses" in r.url or "home.php" in r.url:
       with open(".cookie","w") as cok:
         cok.write(json.dumps(s.cookies.get_dict()))
    
       return {
       'login_status':'sucessfull',
       'email':email,
       'account_id':s.cookies.get_dict()['c_user'],
       'cookie_datr':s.cookies.get_dict()['datr'],
       }
   else:
       return {
        'login_status':'failed',
        'account':email,
        'url':r.url
       }
 except:
   return {
    'login_status':'error',
    'error':'No_Internet',
    'type':'404'
   }



def fbsend(message,account_id):
 #s = Session()
 #s.cookies.update(json.loads(open('.cookie','r').read()))
 k = url.format('/messages/thread/'+str(account_id))
 data=[]
 urlm=BeautifulSoup(s.get(k).content,"html.parser")
 for x in urlm("form"):
    if "/messages/send/" in x["action"]:
       data.append(url.format(x["action"]))
       break
       			
 for x in urlm("input"):
   try:
     if "fb_dtsg" in x["name"]:
   		  data.append(x["value"])
     if "jazoest" in x["name"]:
   		  data.append(x["value"])
     if "ids" in x["name"]:
       data.append(x["name"])
       data.append(x["value"])
     if len(data) == 7: break
   except: pass
		
 if len(data) == 7:
  f=s.post(data[0],data={
		"fb_dtsg":data[1],
		"jazoest":data[2],
		data[3]:data[4],
		data[5]:data[6],
		"body":message,
		"Send":"Kirim"}).url
  if "send_success" in f:
    return {
	    'status':'message_sent',
	    'account_id':account_id,
	    'message_length':len(message)
    }
  else:
    return {
        'status':'message_failed',
        'account_id':account_id,
        'message_length':len(message)
    }


def newmsgs():
  r=s.get(url.format("/messages"))
  html = BeautifulSoup(r.content,"html.parser")
  T = html.find_all('table')
  TB = []
  for C in T:
   try:
     if '/messages/read' in C.a['href']:
       TB.append(C)
   except:
     pass

  #print(TB)
  tclass = " ".join(TB[0]['class'])
  sclass = " ".join(TB[0].span['class'])
  print(tclass)
  msg = {}

  Z = html.find_all('table',attrs={'class':tclass})
  i=0
  for M in Z:
   try:
     xid = M.a['href']
     mid = xid.split('c.')[1].split('&')[0].split('%3A')[1]
     mtext = M.span
     msg[i]={
     M.a.get_text():mtext.get_text(),
     'ID':mid
     }
     i+=1
   except:
     pass
  return msg

  
'''

def newm():
'''  

#print(newmsgs())

old = []
while True:
 M = newmsgs()
 try:
    name = [x for x in M[0].keys()][0]
    rmsg = M[0].get(name)
    print(rmsg)
    ID = M[0].get('ID')
    if rmsg[0] != '|':
     ANS = eval(rmsg)
     #smsg = "* Name {} : \nID : {}\nANS : {}".format(name,ID,ANS)
     smsg = "| Answer : {}".format(ANS)
     #old.append(rmsg)
     print(smsg)
     #input()
     fbsend(smsg,ID)
 except: pass