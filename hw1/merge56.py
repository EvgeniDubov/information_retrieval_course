from indexer import InvertedIndex
print('start load index 5')
index_5 = InvertedIndex('InvertedIndex_5')
print('loaded index 5')
print('start load index 6')
index_6 = InvertedIndex('InvertedIndex_6')
print('loaded index 6')
print('try merge index 5 and 6')
index_5.merge(index_6)
print('merged index 5 and 6')
with open('InvertedIndex_56','w') as file:
    file.write(str(index_5))
print('Success!!')