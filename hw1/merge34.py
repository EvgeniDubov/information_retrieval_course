from indexer import InvertedIndex
print('start load index 3')
index_3 = InvertedIndex('InvertedIndex_3')
print('loaded index 3')
print('start load index 4')
index_4 = InvertedIndex('InvertedIndex_4')
print('loaded index 4')
print('try merge index 3 and 4')
index_3.merge(index_4)
print('merged index 3 and 4')
with open('InvertedIndex_34','w') as file:
    file.write(str(index_3))
print('Success!!')