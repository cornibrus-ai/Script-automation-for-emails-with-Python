import smtplib
import os
from email.message import EmailMessage
import ssl

#Configuration de la console pour utiliser UTF-8
import sys
if os.name == 'nt':
  os.system('chcp 65001')

from dotenv import load_dotenv, dotenv_values #import des paires clé-valeur dans l'environnement de travail

#Python prend déjà en charge tous les modules présents ici dans sa bibliothèque  -- pas besoin de les installer via le cmd.exe ;)

'''import time
import random'''

#coordonnées de l'email
email_sender = "ve31600@gmail.com"
email_receiver = "maxime.ravaux@viacesi.fr"
app_password = os.environ.get("yupb nptt qgfp vjco") #mot de passe d'applications Google

# Vérifie que le mot de passe de l'application est défini avant de passer à la suite
if app_password is None:
  raise ValueError(f"La variable d'environnement {app_password} n'est pas definie.")
else :
  print(f"Le mot de passe de l'application est : {app_password}")

#Corps de l'email (em.as_string())
subject = "Demande de stage en IA"

pdf_file_path = r"C:\\Users\\Jeff31\\Downloads\\CV - RAVAUX Maxime.pdf" #chemin d'accès vers le cv (en format pdf)
fullname_sender = "Maxime RAVAUX" 
phone_sender = "+33 601686536"

message = f"Bonjour, \n\n Je suis {fullname_sender}, étudiant en Bachelor B1 d'IA à CESI. \n\n Je vous envoie ma candidature avec mon CV ci-joint : {pdf_file_path} \n\n Contactez-moi au {phone_sender} !"

em = EmailMessage()
em["From"] = email_sender
em["To"] = email_receiver
em["Subject"] = subject
em.set_content(message)

#Sécurité lors de l'envoie de l'email
context = ssl.create_default_context()

#Envoie de l'email
server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) #self, host, port, local_hostname, timeout, source_adress
#server.starttls()
server.ehlo()
server.login(email_sender, app_password) #adresse d'envoie
server.sendmail (email_sender, email_receiver, em.as_string()) #envoie de l'email : email_sender -> email_receiver

print(f"Votre email a bien été envoyé à {email_receiver}")

#Personnalisation de l'envoie
emails_per_batch = 70 #nombre d'emails à envoyer par lot
batch_delay_min = 181 #délais max entre les lots (en s)
batch_delay_max = 230 #délais max entre les lots (en s)
email_delay_min = 3 #délais min entre les emails indiv (en s)
email_delay_max = 5 #délais max entre les emails indiv (en s)