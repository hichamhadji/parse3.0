# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:15:11 2020

@author: vibhanshuv
"""
import json
import glob2
import re
import os
import pandas as pd
import subprocess

jar_path=''
def run_command(command):
    p = subprocess.Popen(command,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, shell=True)
    return iter(p.stdout.readline, b'')

def margin_classification(file_path):
    Output_file = './margin_call/Output.tsv'
    output_writer = open(Output_file,'w')
    for output_line in run_command('java -cp ./margin_call/stanford-classifier.jar edu.stanford.nlp.classify.ColumnDataClassifier -loadClassifier ./margin_call/MarginClassModel.ser.gz -testFile {}/Margin_data.test'.format(file_path)):
        try:
            out_data = str(output_line.decode())
        except:
            out_data = str(output_line)
            pass
        out_data = out_data.strip()
        output_writer.write(out_data)
        output_writer.write("\n")
    
    output_writer.close()

    Outputc=pd.read_csv("./margin_call/Output.tsv",header=6, delimiter="\t", quoting=3)

    #result=Outputc["classifierAnswer"][0:num1]
    result=Outputc["classifierAnswer"][0]
    
    return result
