LANG=en

IN_DIR=
OUT_DIR=${IN_DIR}
MODEL_DIR=${IN_DIR}
SUFFIX=${LANG}
FILE_PREFIX=train.caption
FILE_TOK_PRE=${FILE_PREFIX}.tok
FILE_CASE_PRE=${FILE_TOK_PRE}.truecase
FILE_LOWERCASE_PRE=${FILE_TOK_PRE}.lc
FILE_BPE_PRE=${FILE_CASE_PRE}.bpe

TRUECASE_MODEL=${MODEL_DIR}${FILE_PREFIX}.truecase-model.${LANG}
BPE_MODEL=${MODEL_DIR}${FILE_PREFIX}.bpe-model.${LANG}

FILE=${IN_DIR}${FILE_PREFIX}.${SUFFIX}
FILE_TOK=${OUT_DIR}${FILE_TOK_PRE}.${SUFFIX}
FILE_CASE=${OUT_DIR}${FILE_CASE_PRE}.${SUFFIX}
FILE_LOWERCASE=${OUT_DIR}${FILE_LOWERCASE_PRE}.${SUFFIX}
FILE_BPE=${OUT_DIR}${FILE_BPE_PRE}.${SUFFIX}

all:tok lowercase
# tokenize data
tok:
	perl tokenizer.perl -l ${LANG} -no-escape < ${FILE} > ${FILE_TOK}
# lower case
lowercase:
	perl lowercase.perl < ${FILE_TOK} > ${FILE_LOWERCASE}
# truecase data
case:
	perl train-truecaser.perl \
		--model ${TRUECASE_MODEL} \
		--corpus ${FILE_TOK}
	perl truecase.perl \
		--model ${TRUECASE_MODEL} \
		< ${FILE_TOK} \
		> ${FILE_CASE}

# bpe dat
BPE_OPS=10000
BPE_SRC=${FILE_CASE}
BPE_OUT=${FILE_BPE}
learn_bpe:
	python learn_bpe.py -s ${BPE_OPS} < ${BPE_SRC} > ${BPE_MODEL}
apply_bpe:
	python apply_bpe.py -c ${BPE_MODEL} < ${BPE_SRC} > ${BPE_OUT}
bpe:learn_bpe apply_bpe

# make vocabulary
vocab:
	python vocab.py

# clean all data
clean:
	rm *.bpe* *.tok* *.truecase* *-model*
