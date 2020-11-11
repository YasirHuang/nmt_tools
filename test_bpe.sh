# suggest 10000
bpe_ops=$1
OUT_DIR=./tmp
python ./learn_bpe.py -s $bpe_ops < ${OUT_DIR}/train.fixed.tok.lc.en > ${OUT_DIR}/bpemodel.en
python ./learn_bpe.py -s $bpe_ops < ${OUT_DIR}/train.fixed.tok.lc.de > ${OUT_DIR}/bpemodel.de

python ./apply_bpe.py -c ${OUT_DIR}/bpemodel.en < ${OUT_DIR}/train.fixed.tok.lc.en > ${OUT_DIR}/train.fixed.tok.lc.bpe.en
python ./apply_bpe.py -c ${OUT_DIR}/bpemodel.de < ${OUT_DIR}/train.fixed.tok.lc.de > ${OUT_DIR}/train.fixed.tok.lc.bpe.de

python vocab.py --in_dir=${OUT_DIR} --out_dir=${OUT_DIR} --in_file_name=train.fixed.tok.lc.bpe --out_file_name=vocab.tok.lc.bpe --out_counted_file_name=vocab.tok.lc.bpe.counted --lang=en
python vocab.py --in_dir=${OUT_DIR} --out_dir=${OUT_DIR} --in_file_name=train.fixed.tok.lc.bpe --out_file_name=vocab.tok.lc.bpe --out_counted_file_name=vocab.tok.lc.bpe.counted --lang=de

python merge_vocab.py --vocab_prefix=${OUT_DIR}/vocab.tok.lc.bpe -langs en de

# Deprecated method to get shared vocabulary
# shared vocab
# sbpe_ops=$2
#python ./learn_bpe.py -s $sbpe_ops < ${OUT_DIR}/train.fixed.tok.lc.en-de > ${OUT_DIR}/bpemodel.en-de

#python ./apply_bpe.py -c ${OUT_DIR}/bpemodel.en-de < ${OUT_DIR}/train.fixed.tok.lc.en-de > ${OUT_DIR}/train.fixed.tok.lc.sbpe.en-de
#python ./apply_bpe.py -c ${OUT_DIR}/bpemodel.en-de < ${OUT_DIR}/train.fixed.tok.lc.en > ${OUT_DIR}/train.fixed.tok.lc.sbpe.en
#python ./apply_bpe.py -c ${OUT_DIR}/bpemodel.en-de < ${OUT_DIR}/train.fixed.tok.lc.de > ${OUT_DIR}/train.fixed.tok.lc.sbpe.de
#python vocab.py --in_dir=${OUT_DIR} --out_dir=${OUT_DIR} --in_file_name=train.fixed.tok.lc.sbpe --out_file_name=vocab.tok.lc.sbpe --out_counted_file_name=vocab.tok.lc.sbpe.counted --lang=en-de
#python vocab.py --in_dir=${OUT_DIR} --out_dir=${OUT_DIR} --in_file_name=train.fixed.tok.lc.sbpe --out_file_name=vocab.tok.lc.sbpe --out_counted_file_name=vocab.tok.lc.sbpe.counted --lang=de
#python vocab.py --in_dir=${OUT_DIR} --out_dir=${OUT_DIR} --in_file_name=train.fixed.tok.lc.sbpe --out_file_name=vocab.tok.lc.sbpe --out_counted_file_name=vocab.tok.lc.sbpe.counted --lang=en




