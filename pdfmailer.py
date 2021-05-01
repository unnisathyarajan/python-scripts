#!/usr/bin/python3.8

import os
from PyPDF2 import PdfFileReader
import tempfile
from pdf2image import convert_from_path
import random
from PIL import Image
import math
import names
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header


def Send_Email(imagefile,Book_Name):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Book_Name
    msg['From'] = str(Header('Dimitrius<unnisathya88@gmail.com>'))
    msg['To'] = "unnisathya88@gmail.com"
    text = MIMEText('<img src="cid:bookpageimage001">', 'html')
    msg.attach(text)
    image = MIMEImage(open(imagefile, 'rb').read())

    # Define the image's ID as referenced in the HTML body above
    image.add_header('Content-ID', '<bookpageimage001>')
    msg.attach(image)

    port = 465
    password = 'sendgrid_password_here'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.sendgrid.net", port, context=context) as server:
        server.login("apikey", password)
        server.sendmail("unnisathya88@gmail.com", "unnisathya88@gmail.com", msg.as_string())

    print("Mail Sent")


def custom_readwise(Book,Book_Name):
    if not os.path.exists('tempstore'):
        os.makedirs('tempstore')
    
    temp_name = names.get_first_name()
    downloaded_file = "tempstore/" +temp_name+".pdf"
    command= "wget " + str(Book) + " -O " + "tempstore/" +temp_name+".pdf"
    os.system(command)    
    
    with open(downloaded_file, "rb") as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        page_count = pdf_reader.numPages
    
    n = random.randint(1,page_count)
    m = n-1
 
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(downloaded_file, output_folder=path, last_page=n, first_page=m)
    base_filename  =  os.path.splitext(os.path.basename(downloaded_file))[0] + '.jpg'     
    save_dir = 'tempstore'
 
    for page in images_from_path:
        page.save(os.path.join(save_dir, base_filename), 'JPEG')
    image_name = save_dir+"/"+base_filename
    foo = Image.open(image_name)
    x, y = foo.size
    x2, y2 = math.floor(x-50), math.floor(y-20)
    foo = foo.resize((x2,y2),Image.ANTIALIAS)
    reduced_filename = image_name[:-4]+"_reduced.jpg"
    foo.save(reduced_filename,quality=30)

    Send_Email(reduced_filename,Book_Name)

    cleanup_cmd = "rm -rf "+save_dir+"/*"
    os.system(cleanup_cmd) 

    
    
def main():
    Book1_URL="https://online-pdf-url"
    Book1_Name="book_name_here"
    custom_readwise(Book1_URL,Book1_Name)


if __name__ == '__main__':
    main()
