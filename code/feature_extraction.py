#!/usr/bin/python3
# -*- coding: utf-8 -*-

import token
from corpus import Corpus
from markables import Markables


PERS_SUBJ_PRON = {'I', 'you', 'he', 'she', 'it', 'we', 'they', 'one'}
PERS_OBJ_PRON = {'me', 'you', 'him', 'her', 'it', 'us', 'them', 'one'}
POSS_PRON = {'mine', 'yours', 'his', 'hers', 'its', 'ours', 'theirs', 'one\'s'}
REFL_PRON = {'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves', 'oneself'}
PRON = PERS_SUBJ_PRON.union(PERS_OBJ_PRON.union(POSS_PRON.union(REFL_PRON)))

DEMONS_PRON = {'this', 'these', 'that', 'those'}

INDEF_ART = {'a', 'an'}
DEF_ART = {'the'}
ART = INDEF_ART.union(DEF_ART)

class FeatureExtractor:

    def __init__(self, file_path):
        mark_ins = Markables(file_path)
        self.mark_dict = mark_ins.get_markables()

    def generate_mention_pairs(self, sent_list):
        result = list()
        sent_list = reduce(lambda x, y: x+y, sent_list)
        for i in range(len(sent_list)):
            full_list = sent_list[:]
            pivot = sent_list.pop(i)
            sent_list = full_list
            for j in range(i+1, len(sent_list)):
                result.append((pivot, sent_list[j]))
        return result

    def markable_string(self, markable):
        assert isinstance(markable, list)
        string_form = str()
        for elem in markable:
            string_form += elem.get_token() + ' '
        return string_form.rstrip().lower()

    def string_match(self, mention1, mention2):
        assert isinstance(mention1, str)
        assert isinstance(mention2, str)
        mention1 = [token for token in mention1.split() if token not in ART.union(DEMONS_PRON)]
        mention2 = [token for token in mention2.split() if token not in ART.union(DEMONS_PRON)]
        # mention1 = [mention1.replace(token, '').strip() for token in mention1.split() if token in ART.union(DEMONS_PRON)]
        # mention2 = [mention2.replace(token, '').strip() for token in mention2.split() if token in ART.union(DEMONS_PRON)]
        return mention1 == mention2

    def create_feature_vector(self):
        features = list()
        for doc, sent_list in iter(self.mark_dict.items()):
            current_pair = self.generate_mention_pairs(sent_list)
            for pair in current_pair:
                mention1 = pair[0] # list type
                mention2 = pair[1] # list type
                mention1_text = self.markable_string(mention1)
                mention2_text = self.markable_string(mention2)

                # Features
                _DIST = mention2[0].get_sent_id() - mention1[0].get_sent_id()
                _I_PRONOUN = mention1_text in PRON
                _J_PRONOUN = mention2_text in PRON
                _STR_MATCH = self.string_match(mention1_text, mention2_text)
                _DEF_NP = mention2_text.startswith('the')
                _DEM_NP = any(filter(lambda w: mention2_text.startswith(w), DEMONS_PRON))

                # Feature vector
                feature = [(mention1_text, mention2_text), _DIST, _I_PRONOUN, _J_PRONOUN, _STR_MATCH, _DEF_NP, _DEM_NP]
                features.append(feature)
        return features

    def store_features(self, file_name):
        features = self.create_feature_vector()
        with open(file_name+'.features', 'w') as f:
            for feature in features:
                mention_pairs = feature[0]
                _DIST = feature[1]
                _I_PRONOUN = feature[2]
                _J_PRONOUN = feature[3]
                _STR_MATCH = feature[4]
                _DEF_NP = feature[5]
                _DEM_NP = feature[6]
                f.write('Mention 1: {}\n'.format(mention_pairs[0]))
                f.write('Mention 2: {}\n'.format(mention_pairs[1]))
                f.write('Distance between: {}\n'.format(_DIST))
                f.write('Mention 1 is a pronoun: {}\n'.format(_I_PRONOUN))
                f.write('Mention 2 is a pronoun: {}\n'.format(_J_PRONOUN))
                f.write('String of Mention 1 matches that of Mention 2: {}\n'.format(_STR_MATCH))
                f.write('Mention 2 is a definite NP: {}\n'.format(_DEF_NP))
                f.write('Mention 2 is a demonstrative NP: {}\n'.format(_DEM_NP))
                f.write('\n')

def main():
    import sys, os.path
    file_path = str(sys.argv[1])
    file_name = os.path.splitext(file_path)[0]
    feat_ins = FeatureExtractor(file_path)
    feat_ins.store_features(file_name)

if __name__=='__main__':
    main()