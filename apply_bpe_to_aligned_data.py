import argparse
class Sentence:
    def __init__(self, words=None, phrases=None, sentence=None):
        self.words = words if words is not None else []
        self.phrases = phrases if phrases is not None else []
        self.sentence = sentence
        
    def __dict__(self):
        return {'sentence':self.__str__(),
               'phrases':[p.__dict__() for p in self.phrases],
               'all_tag':[w.all_tag for w in self.words],
               'key_tag':[w.key_tag for w in self.words]}
        
    def __str__(self):
        s = []
        for w in self.words:
            s.append(str(w))
        return ' '.join(s)
        
class Phrase:
    def __init__(self, phrase=None, words=None, sentence=None):
        self.phrase = phrase['phrase'].lower()
        self.first_word_index = phrase['first_word_index']
        self.phrase_id = phrase['phrase_id']
        self.phrase_type = phrase['phrase_type']
        
        self.words = words if words is not None else []
        self.sentence = sentence
        
    def __dict__(self):
        return {'first_word_index':self.words[0].index_in_sentence, 
               'phrase_id':self.phrase_id,
               'phrase_type':self.phrase_type,
               'phrase':' '.join([str(w) for w in self.words])}
    def __str__(self):
        return str(self.__dict__())
        
class Word:
    def __init__(self, word=None, phrase=None, sentence=None):
        self.word=word
        self.phrase=phrase
        self.sentence=sentence
        
        self.all_tag = None
        self.key_tag = None
        
    def copy_from_word(self, word):
        self.word = word.word
        self.phrase = word.phrase
        self.sentence = word.sentence
        self.all_tag = word.all_tag
        self.key_tag = word.key_tag
        
    @property
    def index_in_sentence(self):
        return self.sentence.words.index(self)
    @property
    def index_in_phrase(self):
        return self.phrase.words.index(self)
    
    def __str__(self):
        return self.word
#         return "word:%s\nNUM:%d in sentence: %s\nNUM:%d in phrase: %s" % (self.word,
#                                                                        self.index_in_sentence,
#                                                                        self.sentence.sentence,
#                                                                        self.index_in_phrase,
#                                                                        self.phrase.phrase)

def parse_aligned_sentence(aligned_sentence):
    the_sentence = Sentence(sentence=aligned_sentence['sentence'].lower())
    all_tag = aligned_sentence['all_tag']
    key_tag = aligned_sentence['key_tag']
    for i, (w, at, kt) in enumerate(zip(the_sentence.sentence.strip().split(), all_tag, key_tag)):
        the_word = Word(word=w, sentence=the_sentence)
#         the_word.index_in_sentence = i
        the_word.all_tag = at
        the_word.key_tag = kt
        the_sentence.words.append(the_word)
    for p in aligned_sentence['phrases']:
        the_phrase = Phrase(phrase=p, words=[], sentence=the_sentence)
        the_sentence.phrases.append(the_phrase)
        for i, w in enumerate(the_phrase.phrase.strip().split()):
            the_word = the_sentence.words[i+the_phrase.first_word_index]
            assert w == the_word.word, \
                    "%s,%s" %(w, the_word.word)
            the_word.phrase = the_phrase
#             the_word.index_in_phrase = i
            the_phrase.words.append(the_word)
            assert the_phrase.words[i] is the_sentence.words[i+the_phrase.first_word_index], \
                "%s\n%s\n%s" %(the_phrase.words[i], 
                               the_sentence.words[i+the_phrase.first_word_index],
                              the_phrase)
    return the_sentence

import copy
def align_sentence(bpe_sentence, aligned_sentence):
    parsed_sentence = parse_aligned_sentence(aligned_sentence)
    bpe_sentence_splits = bpe_sentence.lower().strip().split()
    for i, bpe_word in enumerate(bpe_sentence_splits):
        if bpe_word == parsed_sentence.words[i].word:
            continue
#         print("current word:%s %s" % (bpe_word, parsed_sentence.words[i].word))
        assert bpe_word.endswith("@@"), "%s"%bpe_word
        assert i < len(bpe_sentence_splits)-1
        w = parsed_sentence.words[i]
        w.word = bpe_word
        for j, bpe_word_suffix in enumerate(bpe_sentence_splits[i+1:]):
            w_suffix = Word()
            w_suffix.copy_from_word(w)
            w_suffix.word = bpe_word_suffix
            parsed_sentence.words.insert(w.index_in_sentence+1+j, w_suffix)
            if w_suffix.phrase:
                w_suffix.phrase.words.insert(w.index_in_phrase+1+j, w_suffix)
            if not bpe_word_suffix.endswith("@@"):
                break
#         print(parsed_sentence.__dict__())
    return parsed_sentence

import json
def align_corpus(bpe_sentence_file, splits_file, json_file, out_json_file):
    with open(bpe_sentence_file, 'r') as fp:
        bpe_sentences = [l.strip() for l in fp.readlines()]
    with open(splits_file, 'r') as fp:
        splits = [l.strip().split('.')[0] for l in fp.readlines()]
    with open(json_file, 'r') as fp:
        aligned_sentences = json.load(fp)
    
    for bpe_sentence, split in zip(bpe_sentences, splits):
        parsed_aligned_sentence = align_sentence(bpe_sentence, aligned_sentences[split])
        aligned_sentences[split] = parsed_aligned_sentence.__dict__()
    
    with open(out_json_file, 'w') as fp:
        json.dump(aligned_sentences, fp, indent=4)
        
# align_corpus("./train.fixed.tok.lc.sharevocab.bpe.en", 
#              "../original/splits/train_images.txt",
#              "./train.fixed.tok.en.tagged.json",
#              "./train.fixed.tok.lc.bpe.en.tagged.json")
# align_corpus("./val.tok.lc.sharevocab.bpe.en", 
#              "../original/splits/val_images.txt",
#              "./val.tok.en.tagged.json",
#              "./val.tok.lc.bpe.en.tagged.json")
# align_corpus("./test2016.tok.lc.sharevocab.bpe.en", 
#              "../original/splits/test_images.txt",
#              "./test2016.tok.en.tagged.json",
#              "./test2016.tok.lc.bpe.en.tagged.json")


def add_arguments(parser):
    """Build ArgumentParser."""
    parser.register("type", "bool", lambda v: v.lower() == "true")

    parser.add_argument("--bpe_sentence_file", type=str, default="./train.fixed.tok.lc.bpe.en",
                        help="")
    parser.add_argument("--split_file", type=str, default='/home/xhuang/work/corpus/Multi30K/original/splits/train_images.txt',
                        help="")
    parser.add_argument("--json_file", type=str, default='./train.fixed.tok.en.tagged.json',
                        help="")
    parser.add_argument("--out_json_file", type=str, default="./train.fixed.tok.lc.bpe.en.tagged.json",
                        help="")

def main(FLAGS):
    align_corpus(
        FLAGS.bpe_sentence_file,
        FLAGS.split_file,
        FLAGS.json_file,
        FLAGS.out_json_file)


if __name__ == "__main__":
    cc_parser = argparse.ArgumentParser()
    add_arguments(cc_parser)
    FLAGS, unparsed = cc_parser.parse_known_args()
    # tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
    main(FLAGS)
