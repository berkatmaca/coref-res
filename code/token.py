#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Token:

    def __init__(self, splitted):
        self.splitted = splitted
        self.doc_name = splitted[0]
        self.part_num = splitted[1]
        self.token_index = splitted[2]
        self.token = splitted[3]
        self.pos_tag = splitted[4]
        self.parse_bit = splitted[5]
        self.named_ent = splitted[10]
        self.is_entity = True if self.named_ent is not '*' else False # not very true approach!
        self.coref = splitted[-1]

    def get_token(self):
        return self.token

    def get_token_index(self):
        return int(self.token_index)

    def get_pos_tag(self):
        return self.pos_tag

    def get_parse_bit(self):
        return self.parse_bit

    def get_named_ent(self):
        return self.named_ent if self.is_entity else None

    def is_coref(self):
        return True if self.coref is not '-' else False