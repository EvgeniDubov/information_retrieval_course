from os import listdir, path
import gc
import operator

class InvertedIndex(object):

    def __init__(self, inverted_index_file='', docidmap_file=''):
        self.index = {}
        self.docidmap = {}

        if inverted_index_file:
            with open(inverted_index_file, 'r') as file:
                line = file.readline().strip()
                while line != '':
                    line_split = line.split(PostingList.separator)
                    term = line_split[0][1:-1]
                    entry = IndexEntry(line_split[1:])
                    self.index[term] = entry
                    line = file.readline().strip()
                    gc.collect()

        if docidmap_file:
            with open(docidmap_file, 'r') as file:
                docidmap = file.readlines()
                for doc in docidmap:
                    docid = doc.split(' ')[0].strip()
                    docno = doc.split(' ')[1].strip()
                    self.docidmap[docid] = docno


    def get_max_df(self):
        return max([v.df for k, v in self.index.items()])

    def get_min_df(self):
        return min([v.df for k, v in self.index.items()])

    def add_doc(self, doc):
        self.docidmap[doc.id] = doc.name
        terms = doc.text.split(' ')
        for term in terms:
            term = term.strip()
            if term == '': continue
            self.update_term(term, doc.id)

    def get_doc_name(self, docid):
        return self.docidmap[docid]

    def update_term(self, term, docid):
        if term not in self.index:
            self.index[term] = IndexEntry([docid])
        else: self.index[term].add_doc(docid)

    def get_postlist(self, term):
        if term not in self.index: return None
        return self.index[term].posting_list.get_docid_set()

    def merge(self, new_index):
        for k, v in new_index.index.items():
            if k not in self.index:
                self.index[k] = v
            else:
                self.index[k].merge(v)

    def get_top_df_ids(self, top):
        return sorted({k: v.df for k, v in self.index.items()}.items(), key=operator.itemgetter(1))[(-1)*top:]

    def get_bottom_df_ids(self, bottom):
        return sorted({k: v.df for k, v in self.index.items()}.items(), key=operator.itemgetter(1))[:bottom]

    def index_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for k, v in self.index.items():
                file.write("'{}'{}{}\n".format(k, PostingList.separator, str(v)))
                file.flush()

    def docidmap_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for k, v in self.docidmap.items():
                file.write("{} {}\n".format(k, v))


class IndexEntry(object):

    def __str__(self):
        return str(self.posting_list)

    def __init__(self, docids):
        self.df = len(docids)
        self.posting_list = PostingList(docids)

    def add_doc(self, docid):
        if not self.posting_list.contains(docid):
            self.df += 1
            self.posting_list.add_doc(docid)

    def merge(self, new_entry):
        self.df += new_entry.df
        self.posting_list.merge(new_entry.posting_list)


class PostingList(object):

    separator = '->'

    def __str__(self):
        return PostingList.separator.join([str(x) for x in self.postlist])

    def __init__(self, docids):
        self.postlist = docids

    def add_doc(self, docid):
        self.postlist.append(docid)

    def contains(self, docid):
        return self.postlist[-1] == docid

    def get_docid_set(self):
        return set(self.postlist)

    def merge(self, new_posting_list):
        if self.postlist[-1] < new_posting_list[0]:
            self.postlist.extend(new_posting_list)
        else:
            new_posting_list.extend(self.postlist)
            self.postlist = new_posting_list


class DocumentsFile(object):

    @staticmethod
    def tokenize(text):
        # TODO: should we do more tokenization?
        tokenized_text = text.strip()
        tokenized_text = tokenized_text.replace('\n', ' ')
        return tokenized_text

    @staticmethod
    def doc_file_to_docs(doc_file):
        with open(doc_file, 'r') as file:
            file_content = file.read()

        doc_list = []
        docs = file_content.split('<DOC>')

        # first element in list after split is empty
        del docs[0]
        print('documents in file: {}'.format(len(docs)))

        # process all documents in the file
        for doc in docs:
            # cannot process document without a name
            if '<DOCNO>' not in doc: continue

            # retrieve document name
            docno_start = doc.index('<DOCNO>') + 7
            docno_end = doc.index('</DOCNO>')
            docno = doc[docno_start:docno_end].strip()

            # nothing to process in case document does not contain <TEXT> tag
            if '<TEXT>' not in doc: continue

            # retrieve text from document
            # support multiple TEXT tags in a single document
            texts = doc.split('<TEXT>')
            del texts[0]  # first element is the everything before the text
            doc_text = ''
            # TODO: replace with ' '.join(texts)
            for text in texts:
                doc_text = '{} {}'.format(doc_text, DocumentsFile.tokenize(text.split('</TEXT>')[0].strip()))

            # trim trailing and heading spaces
            doc_text = doc_text.strip()

            # ignoring empty documents
            if doc_text == '': continue

            # create and add new document object to the list
            document = Document(docno, doc_text)
            doc_list.append(document)

        return doc_list


class Document(object):
    max_id = 0

    def __init__(self, name, text):
        Document.max_id += 1
        self.id = Document.max_id
        self.name = name
        self.text = text


def build_inverted_index(docs_dir):
    # create empty inverted index object
    inverted_index = InvertedIndex()

    # get list of all doc files in given directory
    doc_file_list = listdir(docs_dir)

    # process all files
    for doc_file in doc_file_list:
        print(doc_file)

        # retreive all documents from given file
        docs = DocumentsFile.doc_file_to_docs(path.join(docs_dir, doc_file))

        # add all documents to inverted index
        for doc in docs:
            inverted_index.add_doc(doc)

    return inverted_index
