# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:34:23 2020

@author: vibhanshuv
"""
import margin_call.email_read as email_read
from nltk.corpus import stopwords
import json
import glob2
import re
import os



def email_reading(full_file_path):
    #Folder_name = os.path.join(app.config['UPLOAD_FOLDER'],full_file_path.rsplit('.', 1)[0])
    Folder_name = full_file_path.rsplit('/', 1)[0]
    cmd = "python ./margin_call/email_read.py --use-file-name "+ full_file_path
    os.system(cmd)
    class KaggleWord2VecUtility(object):
        @staticmethod
        def Docs_Match_to_wordlist( Docs_Match, remove_stopwords=True ):
#        Docs_Match_text = BeautifulSoup(Docs_Match).get_text()
        # 2. Remove non-letters
            Docs_Match_text = re.sub("[^a-zA-Z]"," ", Docs_Match)
        #
        # 3. Convert words to lower case and split them
            words = Docs_Match_text.lower().split()
#        for w in words:
#            ps.stem(w)
        #
        # 4. Optionally remove stop words (false by default)
            if remove_stopwords:
                stops = set(stopwords.words('english'))
                words = [w for w in words if not w in stops]
        #
        # 5. Return a list of words
            return(words)

    # Define a function to split a Docs_Match into parsed sentences
        @staticmethod
        def Docs_Match_to_sentences( Docs_Match, tokenizer, remove_stopwords=True ):
        # Function to split a Docs_Match into parsed sentences. Returns a
        # list of sentences, where each sentence is a list of words
        #
        # 1. Use the NLTK tokenizer to split the paragraph into sentences
            raw_sentences = tokenizer.tokenize(Docs_Match.decode('utf8').strip())
        #
        # 2. Loop over each sentence
            sentences = []
            for raw_sentence in raw_sentences:
#            ps.stem(raw_sentence)
            # If a sentence is empty, skip it
                if len(raw_sentence) > 0:
                    # Otherwise, call Docs_Match_to_wordlist to get a list of words
                    sentences.append( KaggleWord2VecUtility.Docs_Match_to_wordlist( raw_sentence, \
                  remove_stopwords ))
        #
        # Return the list of sentences (each sentence is a list of words,
        # so this returns a list of lists
            return sentences
    test = glob2.glob(full_file_path)
    clean_test_Docs_Match = []
    test_labels = []
    file_name=[]    
    for file in test:
        msg = email_read.Message(file)
        clean_test_Docs_Match.append(" ".join(KaggleWord2VecUtility.Docs_Match_to_wordlist(msg.body, True))) 
        test_labels.append("Callin")
        file_name.append(file)
    comp = os.path.join(Folder_name, "Margin_data.test")
    wfile=open(comp,'w')
    for page in clean_test_Docs_Match:
#    print(page)
        wfile.write("Callin")
        wfile.write("\t")
        wfile.write(page)
        wfile.write("\n")
    wfile.close()
    completeName = os.path.join(Folder_name, "BAT.txt")         
    full_text_writer = open(completeName,'w')
    msg = email_read.Message(full_file_path)
    body_text = msg.body
    subject_text = msg.subject
    full_text_writer.write("SUB:")
    full_text_writer.write(subject_text.encode('ascii', 'ignore').decode('ascii'))
    full_text_writer.write(body_text.encode('ascii', 'ignore').decode('ascii'))
    return Folder_name
