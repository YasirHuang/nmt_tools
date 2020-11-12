from __future__ import print_function
import os
import argparse
def merge_vocab(vocab_prefix, suffix0, suffix1):
    with open("%s.counted.%s" % (vocab_prefix, suffix0), 'r') as fp:
        vocab0 = [l.strip().split() for l in fp.readlines()]
    with open("%s.counted.%s" % (vocab_prefix, suffix1), 'r') as fp:
        vocab1 = [l.strip().split() for l in fp.readlines()]
        
    for v1 in vocab1:
        v_in_0 = False
        for v0 in vocab0:
            if v1[0] == v0[0]:
                v_in_0 = True
        if not v_in_0:
            vocab0.append(v1)

    vocab = sorted(vocab0, key=lambda x: int(x[1]), reverse=True)
    out_file = "%s.%s-%s" % (vocab_prefix, suffix0, suffix1)
    c_out_file = "%s.counted.%s-%s" % (vocab_prefix, suffix0, suffix1)
    with open(out_file, 'w') as fp:
        print("write vocab to:", out_file)
        for v in vocab:
            fp.write("%s\n" % v[0])
            
    with open(c_out_file, 'w') as fp:
        print("write counted vocab to:", c_out_file)
        for v in vocab:
            fp.write("%s\t%s\n" % (v[0], v[1]))
    print('done')

def add_arguments(parser):
    """Build ArgumentParser."""
    parser.register("type", "bool", lambda v: v.lower() == "true")

    parser.add_argument("--langs", type=str, default=['en', 'de'],
                        help="")
    parser.add_argument("--vocab_prefix", type=str, default='/home/xhuang/work/corpus/Multi30K/task1_fixed_by_task2/vocab.tok.lc',
                        help="")

def main(FLAGS):
    assert isinstance(FLAGS.langs, list)
    assert len(FLAGS.langs) >= 2
    resolved_pair = []
    for l0 in FLAGS.langs:
        for l1 in FLAGS.langs:
            if l0 == l1:
                continue
            if "%s-%s" % (l0, l1) in resolved_pair or "%s-%s" % (l1, l0) in resolved_pair:
                continue
            lang_pair = "%s-%s" % (l0, l1)
            resolved_pair.append(lang_pair)
            print("merge language pair:", lang_pair)
            merge_vocab(FLAGS.vocab_prefix, l0, l1)
    #l0, l1 = FLAGS.langs[0], FLAGS.langs[1]
    #merge_vocab(FLAGS.vocab_prefix, l0, l1)


if __name__ == "__main__":
    cc_parser = argparse.ArgumentParser()
    add_arguments(cc_parser)
    FLAGS, unparsed = cc_parser.parse_known_args()
    # tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
    main(FLAGS)
