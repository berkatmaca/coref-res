#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from token import Token
from sentence import Sentence

class Corpus:

    def __init__(self, file_path):
        self.file_path = file_path
        self.sent_list = list()
        self.corpus_dict = dict()
        self.render_corpus()

    def get_sent_list(self):
    	return self.sent_list

    def get_corpus_dict(self):
        return self.corpus_dict

    def get_doc_names(self):
        return [self.corpus_dict.keys()]

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
                    begin_line = line.split()
                    doc_name = begin_line[2][1:-2] + '/' + begin_line[-1]
                    self.corpus_dict[doc_name] = list()
                # Doc end
                elif re.match(r'\#e', line):
                    num_of_sents += sent_id
                # Empty line
                elif line.strip() == '':
                    sent_id += 1
                    self.sent_list.append(sent_obj)
                    self.corpus_dict[doc_name].append(sent_obj)
                    sent_obj = Sentence()
                else:
                    splitted = line.split()
                    token_obj = Token(splitted)
                    sent_obj.add_token(token_obj)