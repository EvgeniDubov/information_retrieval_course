from os import listdir, path
import gc
import operator


class InvertedIndex(object):
    """
    InvertedIndex class represents the inverted index.
    Holds the inverted index data and provides an API to work with it

    Parameters:
        inverted_index_file: path to inverted index file
        docidmap_file: path to file containing doc_id to doc_name map
    """

    def __init__(self, inverted_index_file='', docidmap_file=''):
        self.index = {}
        self.docidmap = {}

        # build inverted index object from inverted index file
        if inverted_index_file:
            with open(inverted_index_file, 'r') as file:
                line = file.readline().strip()
                # each line in the file starts with the term and followed by sorted posting list
                # posting list consists of doc_ids (which were assigned during indexing)
                while line != '':
                    line_split = line.split(PostingList.separator)
                    term = line_split[0][1:-1]
                    entry = IndexEntry(line_split[1:])
                    self.index[term] = entry
                    line = file.readline().strip()
                    gc.collect()

        # build dictionary of doc_id to doc_name from a file
        if docidmap_file:
            with open(docidmap_file, 'r') as file:
                docidmap = file.readlines()
                for doc in docidmap:
                    docid = doc.split(' ')[0].strip()
                    docno = doc.split(' ')[1].strip()
                    self.docidmap[docid] = docno

    # get the term with the highest df in the inverted index
    def get_max_df(self):
        return max([v.df for k, v in self.index.items()])

    # get the term with the lowest df in the inverted index
    def get_min_df(self):
        return min([v.df for k, v in self.index.items()])

    # add document to the inverted index
    def add_doc(self, doc):

        # add doc_id and doc_name to the mapping dictionary
        self.docidmap[doc.id] = doc.name

        # go over all terms in the document text
        terms = doc.text.split(' ')
        for term in terms:
            term = term.strip()
            if term == '': continue

            # update the inverted index with the term
            self.update_term(term, doc.id)

    # return doc_name matching to given doc_id
    def get_doc_name(self, docid):
        return self.docidmap[docid]

    # update the inverted index with the term
    def update_term(self, term, docid):
        # in case term not in index, add new entry with doc_id as first in the posting list
        if term not in self.index:
            self.index[term] = IndexEntry([docid])

        # in case term is in index, add the doc_id to the index
        else: self.index[term].add_doc(docid)

    # return posting list of given term
    def get_postlist(self, term):
        if term not in self.index: return None
        return self.index[term].posting_list.get_docid_set()

    # merge the given posting list into existing one
    def merge(self, new_index):
        for k, v in new_index.index.items():
            if k not in self.index:
                self.index[k] = v
            else:
                self.index[k].merge(v)

    # return 'top' terms with the highest dfs in the inverted index
    def get_top_df_ids(self, top):
        return sorted({k: v.df for k, v in self.index.items()}.items(), key=operator.itemgetter(1))[(-1)*top:]

    # return 'bottom' terms with the lowest dfs in the inverted index
    def get_bottom_df_ids(self, bottom):
        return sorted({k: v.df for k, v in self.index.items()}.items(), key=operator.itemgetter(1))[:bottom]

    # write inverted index to file
    def index_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for k, v in self.index.items():
                file.write("'{}'{}{}\n".format(k, PostingList.separator, str(v)))
                file.flush()

    # write doc_id to doc_name to file
    def docidmap_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for k, v in self.docidmap.items():
                file.write("{} {}\n".format(k, v))


class IndexEntry(object):
    """
    IndexEntry class represents a single entry in the inverted index.
    Holds the df and the posting list, and provides the api to work with it.
    """

    # converts the posting list to a string
    def __str__(self):
        return str(self.posting_list)

    def __init__(self, docids):
        self.df = len(docids)
        self.posting_list = PostingList(docids)

    # add document to the entry
    def add_doc(self, docid):
        # in case document is not present in posting list
        if not self.posting_list.contains(docid):
            # increase df and add the doc_id at the end of the list
            self.df += 1
            self.posting_list.add_doc(docid)

    # merge new entry into existing entry
    def merge(self, new_entry):
        self.df += new_entry.df
        self.posting_list.merge(new_entry.posting_list)


class PostingList(object):
    """
    PostingList class represents a posting list.
    Holds ordered doc ids list
    """

    # separator string for writing index to a file and parsing existing one
    separator = '->'

    # converts the posting list to string
    def __str__(self):
        return PostingList.separator.join([str(x) for x in self.postlist])

    def __init__(self, docids):
        self.postlist = docids

    # add doc to posting list, keeping the list ordered
    def add_doc(self, docid):
        self.postlist.append(docid)

    # does the posting list contain the doc
    def contains(self, docid):
        return self.postlist[-1] == docid

    # convert the posting list to a set
    def get_docid_set(self):
        return set(self.postlist)

    # merge new posting list to the existing one, keeping the result ordered
    def merge(self, new_posting_list):
        if self.postlist[-1] < new_posting_list[0]:
            self.postlist.extend(new_posting_list)
        else:
            new_posting_list.extend(self.postlist)
            self.postlist = new_posting_list


class DocumentsFile(object):
    """
    DocumentsFile class provides static functions for parsing document files
    """

    @staticmethod
    def tokenize(text):
        # basic tokenization, assuming the doc is already went through pre-processing
        tokenized_text = text.strip()
        tokenized_text = tokenized_text.replace('\n', ' ')
        return tokenized_text

    @staticmethod
    def doc_file_to_docs(doc_file):

        # read the file
        with open(doc_file, 'r') as file:
            file_content = file.read()

        # get all documents from the file
        doc_list = []
        docs = file_content.split('<DOC>')

        # first element in list after split is empty
        del docs[0]

        # print amount of documents in the file
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
    """
    Document class represents a single document from a documents file
    """
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

        # retrieve all documents from given file
        docs = DocumentsFile.doc_file_to_docs(path.join(docs_dir, doc_file))

        # add all documents to inverted index
        for doc in docs:
            inverted_index.add_doc(doc)

    return inverted_index
