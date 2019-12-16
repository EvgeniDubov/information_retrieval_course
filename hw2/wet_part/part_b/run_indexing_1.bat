echo off

echo start Index1: Without stopwords removal and without stemming
echo %TIME%
indribuildindex IndriBuildIndex.xml -index=index_1 -corpus.path=AP_Coll > indexing_log_1.txt 2>&1
echo %TIME%
echo finish Index1

