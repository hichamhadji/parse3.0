# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:26:06 2020

@author: vibhanshuv
"""
import pytesseract
import docx2txt
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string
import glob2
import json
import os
import shutil

def pdf_doc_to_text(full_file_path):
    files = []
    file_path = full_file_path.rsplit('.',1)[0]
    for filename in os.listdir(file_path):
        path = os.path.join(file_path, filename)
        if os.path.isfile(path):
            file_format = filename.rsplit('.',1)[1]
            if file_format=='pdf' or file_format=='doc':
                files.append(filename)
    for file in files:
        file_format = str(file).rsplit('.', 1)[1]
        if file_format == "pdf":
            pages = convert_from_path(os.path.join(file_path,file), 300)
            text_out=[]
            for j in range(0,len(pages)):
                pages[j].save(file_path+'/out'+str(j)+'.png')          
            
            path = file_path+"/*.png"
            
            img_files = glob2.glob(path)
            for file in img_files:
                file_str = str(file)   
                image=Image.open(file_str)
                text_out.append(image_to_string(image,lang='eng'))
                lstr = ' '.join([str(elem) for elem in text_out]) 
                with open("./margin_call/UPLOAD_FOLDER"+"/out1.txt", 'w') as file:
                    file.write(lstr)
        elif file_format == "doc":
            doc_to_text=docx2txt.process(os.path.join(file_path,file))
            doctext_reader = open(doc_to_text,'r')
            text_file='out2.txt'
            doc_text = open(os.path.join('./margin_call/UPLOAD_FOLDER',text_file),'w')
            doc_text.write(doctext_reader.read())
            doc_text.close()
        else:
            pass
        with open('./margin_call/output_file.txt','wb') as wfd:
            for f in [os.path.join('./margin_call/UPLOAD_FOLDER','out1.txt'),os.path.join('./margin_call/UPLOAD_FOLDER','out2.txt')]:
                if os.path.exists(f):
                    with open(f,'rb') as fd:
                        shutil.copyfileobj(fd, wfd)
    return os.path.join('./margin_call','output_file.txt')
