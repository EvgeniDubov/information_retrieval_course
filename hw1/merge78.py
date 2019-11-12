from indexer import InvertedIndex
print('start load index 7')
index_7 = InvertedIndex('InvertedIndex_7')
print('loaded index 7')
print('start load index 8')
index_8 = InvertedIndex('InvertedIndex_8')
print('loaded index 8')
print('try merge index 7 and 8')
index_7.merge(index_8)
print('merged index 7 and 8')
with open('InvertedIndex_78','w') as file:
    file.write(str(index_7))
print('Success!!')