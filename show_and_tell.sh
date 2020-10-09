make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=train
make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=val
#make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=test
make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=train LANG=de
make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=val LANG=de
#make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task1/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task1/ FILE_PREFIX=test LANG=de

for l in en de ;
do
	for s in {1..5}
	do
		for tv in train val;
		do
			if [ "${l}" = "de" ]; then
				fp=de_${tv}
			else
				fp=${tv}
			fi
			make all IN_DIR=/home/xhuang/work/corpus/Multi30K/original/mmt_task2/${l}/${tv}/ OUT_DIR=/home/xhuang/work/corpus/Multi30K/task2/SAT_NMT/${l}/${tv}/ FILE_PREFIX=${fp} LANG=${l} SUFFIX=${s}
		done
	done
done
