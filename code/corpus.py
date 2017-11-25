#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from token import Token
from sentence import Sentence

class Corpus:

    def __init__(self, file_path):
        self.file_path = file_path
        self.sent_list = list()
        self.render_corpus()

    def get_sent_list(self):
    	return self.sent_list

    def render_corpus(self):
    	sent_obj = Sentence()
    	sent_id = int() # no of sents in a specific doc
    	num_of_sents = int() # no of sents in the whole
    	doc_id = -1

    	with open(self.file_path) as f:
            for line in f:
            	# Doc start
                if re.match(r'\#b', line):
                    doc_id += 1
                    sent_id = 0
                # Doc end
                elif re.match(r'\#e', line):
                    num_of_sents += sent_id
                # Empty line
                elif line.strip() == '':
                    sent_id += 1
                    self.sent_list.append(sent_obj)
                    sent_obj = Sentence()
                else:
                    splitted = line.split()
                    token_obj = Token(splitted)
                    sent_obj.add_token(token_obj)

def main():
    instance = Corpus(os.path.expanduser(str(sys.argv[1])))
    instance.get_sent_list()[-3].print_sentence()

if __name__=='__main__':
    main()
