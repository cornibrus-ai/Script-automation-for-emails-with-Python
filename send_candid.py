
#Python prend déjà en charge tous les modules présents ici dans sa bibliothèque  -- pas besoin de les installer via le cmd.exe ;)

import smtplib
import sys
from email.message import EmailMessage
import ssl

#Import des modules pour personnaliser les délais d'envoie
import time
import random

#Import des modules pour créer une pièce jointe MIME
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText #inclure du contenu HTML dans le corps de l'email.
from email.mime.multipart import MIMEMultipart
from email import encoders

#Configuration de la console pour utiliser UTF-8 # -*- coding: utf-8 -*-
import os
if os.name == 'nt':
  os.system('chcp 65001')

  '''
  #Gestion robuste de l'encodage UTF-8 avec le cmd et PowerShell
  if platform.system() == 'Windows':
    import subprocess
    subprocess.call(['powershell', '-Command', '$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = New-Object System.Text.UTF8Encoding'])
  '''

from dotenv import load_dotenv, dotenv_values #import des paires clé-valeur pour charger les variables d'environnement depuis le fichier .env

#Import du module json
import json

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

#coordonnées de l'email
email_sender = "ve31600@gmail.com"
email_receiver = "maxime.ravaux@viacesi.fr"
app_password = os.getenv("GOOGLE_API_KEY") #mot de passe d'applications Google

# Vérifie que le mot de passe de l'application est défini avant de passer à la suite
if app_password is None:
  raise ValueError(f"La variable d'environnement {app_password} n'est pas definie.")
else :
  app_password_verified = print((f"Le mot de passe de l'application est : {app_password}").encode(encoding='utf-8',errors='ignore'))

# Charger les adresses email et informations depuis le fichier emails.json
with open('emails.json', 'r', encoding='utf-8') as file:
  email_data = json.load(file)

#Sécurité lors de l'envoie de l'email
context = ssl.create_default_context()

#Envoie de l'email à chaque adresse email dans le fichier emails.sjon
for data in email_data:
  fullname_receiver = data['nom_prenom']
  company_receiver = data['entreprise']
  position_receiver = data['poste']
  email_receiver = data['adresse_mail']

  #Corps de l'email (em.as_string())
  subject = "Candidature stage [R&D IA]"
  fullname_sender = "Maxime RAVAUX" 
  phone_sender = "+33 601686536"
  message = f"""
  <html>
    <meta charset="utf-8">
    <body>
      <p>Bonjour {fullname_receiver},</p>
      <p>Je suis étudiant en Bachelor B1 d'IA à CESI. Je recherche un stage [Avril-Août 2025] en R&D pôle IA dans une entreprise innovante comme la vôtre.</p>
      <p>Je vous envoie ma candidature avec mon CV ci-joint pour un stage en IA.</p>
      <p>N'hésitez pas à me contacter au {phone_sender} ! </p>
      <p>Vous pouvez également visiter mon <a href="https://www.linkedin.com/in/maxime-ravaux-6a389325b/">profil LinkedIn</a>.</p>
      <p>Cordialement,<br><br>
      {fullname_sender}</p>
    </body>
  </html>
  """

  # Création de l'email
  em = MIMEMultipart()
  em["From"] = email_sender
  em["To"] = email_receiver
  em["Subject"] = subject
  em.attach(MIMEText(message,"html"))

  #Ajout du fichier PDF en pièce jointe
  pdf_file_path = r"C:\\Users\\Jeff31\\Desktop\\CV - RAVAUX Maxime.pdf" #chemin d'accès vers le fichier PDF

  with open(pdf_file_path, "rb") as pdf_file:
    attach = MIMEApplication(pdf_file.read(), _subtype="pdf")
    attach.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_file_path))
    em.attach(attach)

  #Personnalisation de l'envoie
  emails_per_batch = 70 #nombre d'emails à envoyer par lot
  batch_delay_min = 181 #délais max entre les lots (en s)
  batch_delay_max = 230 #délais max entre les lots (en s)

  # Délai aléatoire entre les emails pour éviter d'être marqué comme spam
  email_delay_min = 3 #délais min entre les emails (en s)
  email_delay_max = 5 #délais max entre les emails (en s)

  time.sleep(random.uniform(email_delay_min, email_delay_max))

  #Envoie de l'email
  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as server :#self, host, port, local_hostname, timeout, source_adress
  #server.starttls()
  #server.ehlo()
    server.login(email_sender, app_password) #adresse d'envoie
    server.sendmail (email_sender, email_receiver, em.as_string()) #envoie de l'email : email_sender -> email_receiver

  print((f"Votre email a bien été envoyé à {email_receiver}").encode(encoding='utf-8',errors='ignore'))

print(("Tous les emails ont été envoyés avec succès !").encode(encoding='utf-8',errors='ignore'))