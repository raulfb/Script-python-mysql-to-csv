#!/usr/bin/env python
#-*- coding: UTF-8 -*
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import pymysql
## Mysql
conn = pymysql.connect(host='127.0.0.1', user='Usuariobd', passwd="Contraseñabd", db='nombrebd')
cur = conn.cursor()
cur.execute("(SELECT 'nombre','apellido','ciudad')UNION(SELECT nombre 'nmbre',apellido 'Apellido',ciudad 'Ciudad' FROM datos WHERE (date between date_sub(now(),INTERVAL 1 WEEK) AND now())GROUP BY uniqueid INTO OUTFILE '/tmp/datos.csv'FIELDS TERMINATED BY ';'OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\r\n')")
cur.close()
conn.close()

##Envio del email
#Para las cabeceras del email
password = "Contraseñacorreo"
remitente = "remitentecorreo"
destinatario = ["correodestinatario1", "correodestinatario2"]
asunto = "Asunto del email"
mensaje = """
Contenido del email.
"""
archivo= "/tmp/datos.csv"

#Host y puerto SMTP
mail = smtplib.SMTP('servidorsmtp', 587)

#protocolo de cifrado
mail.starttls()

#Credenciales
mail.login(remitente, password)

#Cabeceras
header = MIMEMultipart()
header['Subject'] = asunto
header['From'] = remitente
header['To'] = ", ".join(destinatario)
mensaje = MIMEText(mensaje, 'html') #Content-type:text/html
header.attach(mensaje)

#Comprueba si existe el archivo
if (os.path.isfile(archivo)):
 adjunto = MIMEBase('application', 'octet-stream')
 adjunto.set_payload(open(archivo, "rb").read())
 encode_base64(adjunto)
 adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(archivo))
 header.attach(adjunto)

#Enviar email
mail.sendmail(remitente, destinatario, header.as_string())

#Cerrar la conexión SMTP
mail.quit()

# Borrar fichero del servidor
os.remove('/tmp/datos.csv')
