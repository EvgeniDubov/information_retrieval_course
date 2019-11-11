
def evaluate(inverted_index, query_elements):
    # TODO: verify assumption that 'A NOT B' means 'A AND NOT B'

    element = query_elements[0]

    if element == '(':
        return evaluate(inverted_index, query_elements[1:])

    if element not in ['(', ')']:
        # get left postlist        
        postlist_l = inverted_index.get_postlist(element)
        if postlist_l is None: return None
        postlist_l = postlist_l.get_docno_set()

        # get operator
        operator = query_elements[1]
        if operator not in ['AND', 'OR', 'NOT']: return None

        # get right postlist
        right_element = query_elements[2]
        if right_element == '(':
            postlist_r = evaluate(inverted_index, query_elements[2:])
        else:
            postlist_r = inverted_index.get_postlist(right_element)
            if postlist_r is None: return None
            postlist_r = postlist_r.get_docno_set()

        if operator == 'AND':
            return postlist_l.intersection(postlist_r)
        if operator == 'OR':
            return postlist_l.union(postlist_r)
        if operator == 'NOT':
            return postlist_l.difference(postlist_r)


def boolean_retrieval(inverted_index, queries_file):
    queries_results = ''

    with open(queries_file, 'r') as file:
        queries = file.readlines()

    ######################################
    # DEBUG - work on few files
    # if DEBUG: del queries[1:]
    # queries = ['( than AND ( years NOT report ) )']
    ######################################

    for query in queries:
        results = evaluate(inverted_index, query.strip().split(' '))
        if results:
            results = ' '.join(results)
        else:
            results = 'NA'
        queries_results += '{}\n'.format(results)
