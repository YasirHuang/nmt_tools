from __future__ import print_function
import os
import argparse

def add_arguments(parser):
    """Build ArgumentParser."""
    parser.register("type", "bool", lambda v: v.lower() == "true")

    parser.add_argument("--lang", type=str, default='en',
                        help="")
    parser.add_argument("--in_dir", type=str, default='/home/xhuang/work/corpus/Multi30K/task1_fixed_by_task2',
                        help="")
    parser.add_argument("--out_dir", type=str, default='/home/xhuang/work/corpus/Multi30K/task1_fixed_by_task2',
                        help="")
    parser.add_argument("--in_file_name", type=str, default='train.fixed.tok.lc', help="")
    parser.add_argument("--out_file_name", type=str, default='vocab.tok.lc', help="")
    parser.add_argument("--out_counted_file_name", type=str, default='vocab.tok.lc.counted', help="")
    parser.add_argument("--max_vocab_length", type=int, default=20000, help="")
    parser.add_argument("--min_show_time", type=int, default=0, help="")


def main(FLAGS):
    max_vocab_length = FLAGS.max_vocab_length
    min_show_time = FLAGS.min_show_time
    IN_PATH = os.path.join(FLAGS.in_dir, '%s.%s' % (FLAGS.in_file_name, FLAGS.lang))
    OUT_PATH = os.path.join(FLAGS.out_dir, '%s.%s' % (FLAGS.out_file_name, FLAGS.lang))
    OUT_PATH2 = os.path.join(FLAGS.out_dir, '%s.%s' % (FLAGS.out_counted_file_name, FLAGS.lang))

    fr = open(IN_PATH, 'r')
    fw = open(OUT_PATH, 'w')
    fw2 = open(OUT_PATH2, 'w')

    vocab = {}
    sentence = fr.readline()
    while (sentence):
        words = sentence.split()
        for word in words:
            if word in vocab:
                vocab[word] = vocab[word] + 1
            else:
                vocab[word] = 1
        sentence = fr.readline()

    vocab_dict = sorted(vocab.items(), key=lambda d: d[1], reverse=True)
    count = 0
    for item in vocab_dict:
        if item[1] < min_show_time:
            continue
        count = count + 1
        fw.write('%s\n' % item[0])
        fw2.write('%s\t%d\n' % (item[0], item[1]))
        if count >= max_vocab_length:
            break
    fr.close()
    fw.close()
    fw2.close()

if __name__ == "__main__":
    cc_parser = argparse.ArgumentParser()
    add_arguments(cc_parser)
    FLAGS, unparsed = cc_parser.parse_known_args()
    # tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

    main(FLAGS)
