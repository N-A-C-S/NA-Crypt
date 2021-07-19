from tkinter import *  
from tkinter.ttk import *
from tkinter.filedialog import askopenfile,asksaveasfile
from PIL import ImageTk,Image
from cryptography.fernet import Fernet
from PyPDF2 import PdfFileWriter, PdfFileReader
import time
import random
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import name
import smtplib
from twilio.rest import Client

fromaddr = "tekops18bce@gmail.com"
password = "2HmwTLDG"

account_sid = "AC614c65332cef15b5716835bbf9159356"
auth_token = "b1cd5a1dd9375422bbdc91dd8e6f2be3"

#----------------------------------Send Msg---------------------------------------#
def send_sms(phone_no,key):
   client = Client(account_sid, auth_token)
   message = client.messages.create(body="Key : "+key, from_=+19126423635, to=int(phone_no))
#----------------------------------Send Msg---------------------------------------#

#--------------------------------Send Email-------------------------------------#
def send_email(filename,attatchment,toaddr,subject):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = subject
    msg.attach(MIMEText(body,'plain'))

    attatchment = open(attatchment,'rb')

    P = MIMEBase('application','octet-stream')
    P.set_payload((attatchment).read())
    encoders.encode_base64(P)

    P.add_header('Content-Disposition','attatchment : filename = %s ' % filename)
    msg.attach(P)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    s.quit()
#--------------------------------Send Email-------------------------------------#

#Encryption
f = None
#-----------------------------CSV----------------------------------------------#
def file_encryption_csv(filename):
   key = Fernet.generate_key()
   fernet = Fernet(key)
   with open(filename, 'rb') as file:
      original = file.read()
   encrypted = fernet.encrypt(original)
   p = filename.split("/")
   p[-1] = "encrypted.csv"
   p = "/".join(p)
   with open(p, 'wb') as encrypted_file:
      encrypted_file.write(encrypted)
   key = key.decode('utf-8')
   Label(root, text='Key : '+str(key), foreground='blue').pack(side = TOP, pady=10)
   return key,p
   
def file_decryption_csv(key,p):
   key = key.encode('utf-8')
   fernet = Fernet(key)
   with open(p, 'rb') as enc_file:
      encrypted = enc_file.read()

   decrypted = fernet.decrypt(encrypted)
   p = p.split("/")
   p[-1] = "decrypted.csv"
   p = "/".join(p)
   with open(p, 'wb') as dec_file:
      dec_file.write(decrypted)
   
#-----------------------------CSV----------------------------------------------#

#-----------------------------png----------------------------------------------#

def file_encryption_png(filename):
   key = random.randint(0,255)
   fin = open(filename,'rb')
   image = fin.read()
   fin.close()
   image = bytearray(image)
   for index, values in enumerate(image):
        image[index] = values ^ key
   fin = open(filename, 'wb')
   fin.write(image)
   fin.close()
   return key,filename

def file_decryption_png(key,p):
   key = int(key)
   fin = open(p,'rb')
   image = fin.read()
   fin.close()
   image = bytearray(image)
   for index, values in enumerate(image):
      image[index] = values ^ key
   fin = open(p, 'wb')
   fin.write(image)
   fin.close()
   
    
#-----------------------------png----------------------------------------------#

#---------------------------password-generator---------------------------------#
def generate_password():
   alphabets = ['a','b','c','d','e','f','g','h','i','j'
   'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
   chars = ['.','/',',','!','@','#','$','%','^','&','*',]
   nums  = ['0','1','2','3','4','5','6','7','8','9']
   random.shuffle(alphabets)
   random.shuffle(chars)
   random.shuffle(nums)
   l = alphabets[:8]+chars[:3]+nums[:3]
   l = list(l)
   random.shuffle(l)
   l = "".join(l)
   return l

#---------------------------password-generator---------------------------------#

#---------------------------------pdf------------------------------------------#
def file_encryption_pdf(filename):
   out = PdfFileWriter()
   file = PdfFileReader(filename)
   num = file.numPages

   for idx in range(num):
      page = file.getPage(idx)
      out.addPage(page)

   password = generate_password()
   out.encrypt(password)

   p = filename.split("/")
   p[-1] = "encrypted.pdf"
   p = "/".join(p)
   
   with open(p,'wb') as f:
      out.write(f)
   
   return password,p

def file_decryption_pdf(key,p):
   key = str(key)
   out = PdfFileWriter()
   file = PdfFileReader(p)
   password = key

   if file.isEncrypted:
      file.decrypt(password)
      for idx in range(file.numPages):
         page = file.getPage(idx)
         out.addPage(page)
      
      p = p.split("/")
      p[-1] = "decrypted.pdf"
      p = "/".join(p)

      with open(p, "wb") as f:
         out.write(f)

#---------------------------------pdf------------------------------------------#
root = Tk()  
root.geometry("400x600")

canvas = Canvas(root, width = 300, height = 150)  
canvas.pack()  
img1 = Image.open("logo1.png")
image1 = img1.resize((300,150), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image1)  
canvas.create_image(0,0, anchor=NW, image=img) 

def open_file():
    file = askopenfile(mode ='r', filetypes =[('CSV Files', '*.csv'),('Image Files', '*.png'),('PDF Files', '*.pdf')])
    if file is not None:
       global f 
       f = str(file.name)
       pass

def Encrypt():
   if f is None:
      Label(root, text='Not uploaded a file yet!!', foreground='red').pack(side = TOP, pady=10)
   else:
      if(f[-3:]=="csv"):
         t,q = file_encryption_csv(f)
      elif(f[-3:]=="png"):
         t,q = file_encryption_png(f)
      elif(f[-3:]=='pdf'):
         t,q = file_encryption_pdf(f)
      else:
         print(f[-3:])
      bar = Progressbar(root,orient=HORIZONTAL,length=200,mode='determinate')
      bar.pack(side = TOP, pady=20)
      for i in range(5):
         root.update_idletasks()
         bar['value'] += 20
         time.sleep(1)
      bar.destroy()
      Label(root, text='File Encrypted Successfully!', foreground='green').pack(side = TOP, pady=10)
      
      Label(root, text='Enter the Email Address you want to send the file', foreground='red').pack(side = TOP)
      emaddr = Entry(root)
      emaddr.pack(side=TOP,pady=5)

      Label(root, text='Enter the Phone Number you want to send the key', foreground='red').pack(side = TOP)
      phnno = Entry(root)
      phnno.pack(side=TOP,pady=5)

      def send_info():
         send_email("File",q,str(emaddr.get()),"Encrypted File")
         time.sleep(5)
         send_sms("+91"+str(phnno.get()),t)

      btn = Button(root, text ='SendInfo', command = lambda:send_info())
      btn.pack(side = TOP, pady = 5)
      print(t)
      print(q)

def Decrypt(key):
   key = key.get()
   if(f[-3:]=='csv'):
      try:
         file_decryption_csv(key,f)
         bar = Progressbar(root,orient=HORIZONTAL,length=200,mode='determinate')
         bar.pack(side = TOP, pady=20)
         for i in range(5):
            root.update_idletasks()
            bar['value'] += 20
            time.sleep(1)
         bar.destroy()
         Label(root, text='File Decrypted Successfully!', foreground='red').pack(side = TOP, pady=10)

      except:
         Label(root, text='Error', foreground='blue').pack(side = TOP, pady=10)
   elif(f[-3:]=='png'):
      try:
         file_decryption_png(key,f)
         bar = Progressbar(root,orient=HORIZONTAL,length=200,mode='determinate')
         bar.pack(side = TOP, pady=20)
         for i in range(5):
            root.update_idletasks()
            bar['value'] += 20
            time.sleep(1)
         bar.destroy()
         Label(root, text='File Decrypted Successfully!', foreground='red').pack(side = TOP, pady=10)

      except:
         Label(root, text='Error', foreground='blue').pack(side = TOP, pady=10)
   elif(f[-3:]=='pdf'):
      try:
         file_decryption_pdf(key,f)
         bar = Progressbar(root,orient=HORIZONTAL,length=200,mode='determinate')
         bar.pack(side = TOP, pady=20)
         for i in range(5):
            root.update_idletasks()
            bar['value'] += 20
            time.sleep(1)
         bar.destroy()
         Label(root, text='File Decrypted Successfully!', foreground='red').pack(side = TOP, pady=10)

      except:
         Label(root, text='Error', foreground='blue').pack(side = TOP, pady=10)
   else:
      print(f[-3:])


      
btn = Button(root, text ='Browse Files', command = lambda:open_file())
btn.pack(side = TOP, pady = 5)

upld = Button(root, text='Encrypt', command=Encrypt)
upld.pack(side = TOP, pady=5)

Label(root, text='Enter the Decryption Key', foreground='crimson').pack(side = TOP, pady=10)
inputtxt = Entry(root)
inputtxt.pack(side=TOP,pady=5)

dec = Button(root,text='Decrypt',command = lambda:Decrypt(inputtxt))
dec.pack(side = TOP,pady = 5)

root.mainloop() 
