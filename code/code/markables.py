#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys
import os.path
from corpus import Corpus

class Markables:
    
    _POS_PRP = r'(?:POS|PRP)'
    _NP_WHNP = r'(?:NP|WHNP)'
    _NP_regex = re.compile(r'^.*\(' + _NP_WHNP + '\*?\).*$') # ( (WH)|(NP)NP(*) )
    trim_parse_bit_regex = re.compile(r'\(' + _NP_WHNP + '\*?.*')
    _NP_start_regex = re.compile(r"""(\(""" + _NP_WHNP + """\*?)(?![)])""", re.VERBOSE) # open ended _NP_regex

    def __init__(self, file_path):
        self.corpus_ins = Corpus(file_path)
        self.sentences = self.corpus_ins.get_sent_list()

    def get_sentences(self):
        return self.sentences

    def extract_markables(self):
        # Markables from the parse bits
        current = list() # list of Tokens
        list_of_NPs = list() # list of list of Tokens
        np_start_list = list() # list of strings
        for sent in self.sentences:
            list_of_tokens = sent.get_token_list()
            for token in list_of_tokens:
                parse_bit = token.get_parse_bit()
                # Check if token's parse bit is already a complete NP.
                # 
                # 'search()' returns the span of match in a tuple
                # where the second element being exclusive.
                if re.search(self._NP_regex, parse_bit):
                    list_of_NPs.append([token])
                # If NP is of a couple of words
                elif re.search(self._NP_start_regex, parse_bit):
                    np_start_list = re.findall(self._NP_start_regex, parse_bit)
                    num_of_NPs = -1

                    for _ in range(len(np_start_list)):
                        num_of_NPs += 1
                        current = [token]
                        open_bra_list = re.findall(self.trim_parse_bit_regex, parse_bit)
                        num_of_open_bra = len(re.findall(r'\(', open_bra_list[0])) - num_of_NPs

                        for rest_of_tokens in list_of_tokens[token.get_token_index()+1:]:
                            parse_bit_of_rest = rest_of_tokens.get_parse_bit()
                            num_of_closed_bra = len(re.findall(r'\)', parse_bit_of_rest))
                            num_of_open_bra += len(re.findall(r'\(', parse_bit_of_rest)) - num_of_closed_bra
                            current.append(rest_of_tokens)
                            # No need to go further if the NP is complete.
                            if num_of_open_bra <= 0:
                                break
                        list_of_NPs.append(current)
                # Markables from the POS tag level
                pos_tag = token.get_pos_tag()
                if re.search(self._POS_PRP, pos_tag):
                    if [token] not in list_of_NPs[-len(np_start_list):]:
                        list_of_NPs.insert(-len(np_start_list), [token])
        return list_of_NPs

def main():
    file_path = str(sys.argv[1])
    filename = os.path.splitext(file_path)[0]
    mark_ins = Markables(file_path)
    mark_list = mark_ins.extract_markables() 
    # from string import punctuation as punc
    with open(filename+'.out', 'w') as out:
        for loT in mark_list:
            markable = str()
            for token_obj in loT:
                token_text = token_obj.get_token()
                # if any(_ in punc for _ in token_text):
                if any(_ in token_text for _ in ["'", ',']):
                    markable += token_text
                else:
                    markable += ' ' + token_text
            out.write(markable.lstrip() + '\n')

if __name__=='__main__':
    main()