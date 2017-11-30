#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Sentence:

    def __init__(self):
        self.token_list = list()

    def add_token(self, token_obj):
        self.token_list.append(token_obj)

    def get_token_list(self):
        return self.token_list

    def print_sentence(self):
        sent = str()
        for token_obj in self.token_list:
            token_text = token_obj.get_token()
            if "'" in token_text:
                sent += token_text
            else:
                sent += ' ' + token_text
        print(sent.lstrip())