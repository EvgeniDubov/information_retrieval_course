import argparse
from indexer import build_inverted_index
from indexer import InvertedIndex
from evaluator import BooleanRetrieval


def main():
    # define command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--documents_folder', action='store')
    parser.add_argument('-o', '--index_output_file', action='store')
    parser.add_argument('-c', '--docid_map_output_file', action='store')
    parser.add_argument('-i', '--index_file', action='store')
    parser.add_argument('-b', '--docid_map_file', action='store')
    parser.add_argument('-q', '--evaluate_queries', action='store_true')
    parser.add_argument('-a', '--queries_result_file', action='store')
    parser.add_argument('-p', '--part_three_file', action='store')

    # parse command line parameters
    args = parser.parse_args()
    print('received the following arguments')
    for k, v in vars(args).items():
        print(k, v)

    inverted_index = None

    # build index if requested
    if args.documents_folder is not None:
        inverted_index = build_inverted_index(args.documents_folder)

        # export inverted index to a file if requested
        if args.index_output_file is not None and args.docid_map_output_file is not None:
            inverted_index.index_to_file(args.index_output_file)
            inverted_index.docidmap_to_file(args.docid_map_output_file)

    # load inverted index from file
    if args.index_file is not None and args.docid_map_file:
        inverted_index = InvertedIndex(args.index_file, args.docid_map_file)

    # write queries results to a file
    if args.evaluate_queries and inverted_index and args.queries_result_file:
        queries_results = BooleanRetrieval(inverted_index)
        with open(args.queries_result_file, 'w') as file:
            file.write('\n'.join(queries_results))

    # write hw part 3 answers to a file
    if args.part_three_file and inverted_index:
        answer = ''
        top = 10
        bottom = 10

        # Write the top 10 terms with the highest document frequency
        top_df = inverted_index.get_top_df_ids(top)
        answer += '--------------------------------------\n'
        answer += 'Top {} df terms:\n'.format(top)
        answer += '\n'.join(['{}: {}'.format(term, df) for term, df in top_df])

        # Write the top 10 terms with the lowest document frequency
        bottom_df = inverted_index.get_bottom_df_ids(bottom)
        answer += '\n--------------------------------------\n'
        answer += 'Bottom {} df terms:\n'.format(bottom)
        answer += '\n'.join(['{}: {}'.format(term, df) for term, df in bottom_df])

        # Explain the different characteristics of the above two sets of terms
        answer += '\n--------------------------------------\n'
        answer += 'The different characteristics of the above two sets of terms:\n'
        answer += '   Top dfs terms are the most common terms in the collection, located in large number of documents\n'
        answer += '   Bottom dfs terms are the rarest terms in the collection, located only in few documents\n'
        answer += '   * in our inverted index we don\'t keep track of terms frequency inside a document, ' \
                  'meaning df of a term signifies the number of documents in which this term was present' \
                  ' at least one time\n'

        with open(args.part_three_file, 'w') as file:
            file.write(answer)


if __name__ == '__main__':
    main()
