from indexer import InvertedIndex
print('start load index 1')
index_1 = InvertedIndex('InvertedIndex_1')
print('loaded index 1')
print('start load index 2')
index_2 = InvertedIndex('InvertedIndex_2')
print('loaded index 2')
print('try merge index 1 and 2')
index_1.merge(index_2)
print('merged index 1 and 2')
with open('InvertedIndex_12','w') as file:
    file.write(str(index_1))
print('Success!!')