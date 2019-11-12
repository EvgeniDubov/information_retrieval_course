from os import listdir, path


class InvertedIndex(object):

    def __str__(self):
        return '\n'.join(["'{}'{}".format(k, str(v)) for k, v in self.index.items()])

    def __init__(self, inverted_index_file=''):
        self.index = {}
        self.docidmap = {}

        if inverted_index_file:
            with open(inverted_index_file, 'r') as file:
                inverted_index_entries = file.readlines()

            for entry in inverted_index_entries:
                post_list = entry.split(' -> ')
                term = post_list[0][1:-1]
                for post in post_list[1:]:
                    post_details = post.split(' ')
                    docid = int(post_details[0])
                    docno = post_details[1][1:-1]
                    self.docidmap[docid] = docno
                    self.update_term(term, docid, docno)

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
            self.update_term(term, doc.id, doc.name)

    def get_doc_name(self, docid):
        return self.docidmap[docid]

    def update_term(self, term, docid, docno):
        if term not in self.index:
            self.index[term] = IndexEntry()
        self.index[term].add_doc(docid, docno)

    def get_postlist(self, term):
        if term not in self.index: return None
        return self.index[term].posting_list


class IndexEntry(object):

    def __str__(self):
        return str(self.posting_list)

    def __init__(self):
        self.df = 0
        self.posting_list = PostingList()

    def add_doc(self, docid, docno):
        if not self.posting_list.contains(docid):
            self.df += 1
            self.posting_list.add_doc(docid, docno)


class PostingList(object):

    def __str__(self):
        post_list_str = ''

        iterator = self.head
        while iterator is not None:
            post_list_str += ' -> {} ({})'.format(iterator.docid,
                                                  iterator.docno)
            iterator = iterator.next_post

        return post_list_str

    def __init__(self):
        self.head = None
        self.last = None

    def add_doc(self, docid, docno):
        post = Post(docid, docno, None)

        # TODO: fix this ugly code part
        if self.head is None:
            self.head = self.last = post
        else:
            self.last.next_post = post
            self.last = post

    def contains(self, docid):
        contains = False
        iterator = self.head
        while iterator is not None:
            if iterator.docid == docid:
                contains = True
                break
            iterator = iterator.next_post

        return contains

    def get_docno_set(self):
        docno_set = set()
        iterator = self.head
        while iterator is not None:
            docno_set.add(iterator.docno)
            iterator = iterator.next_post

        return docno_set


class Post(object):

    def __init__(self, docid, docno, next_post):
        self.docid = docid
        self.docno = docno
        self.next_post = next_post


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
