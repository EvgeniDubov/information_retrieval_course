import argparse
from indexer import build_inverted_index
from indexer import InvertedIndex
from evaluator import boolean_retrieval


def main():
    # define parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--documents_folder', action='store')
    parser.add_argument('-o', '--index_output_file', action='store')
    parser.add_argument('-i', '--index_input_file', action='store')
    parser.add_argument('-q', '--queries_file', action='store')
    parser.add_argument('-a', '--queries_result_file', action='store')
    parser.add_argument('-p', '--part_three_answers', action='store')

    # parse parameters
    args = parser.parse_args()
    print('received the following arguments')
    for k, v in vars(args).items():
        print(k, v)

    inverted_index = None

    # build index if requested
    if args.documents_folder is not None:
        inverted_index = build_inverted_index(args.documents_folder)

        # export inverted index to a file if request
        if args.index_output_file is not None:
            with open(args.index_output_file, 'w') as file:
                file.write(str(inverted_index))

    # load inverted index from file
    if args.index_input_file is not None:
        inverted_index = InvertedIndex(args.index_input_file)

    # run queries
    if args.queries_file and inverted_index and args.queries_result_file:
        queries_results = boolean_retrieval(inverted_index, args.queries_file)
        with open(args.queries_result_file, 'w') as file:
            file.write(queries_results)

    # print hw part 3 answers
    if args.part_three_answers and inverted_index:
        print('max df: {}'.format(inverted_index.get_max_df()))
        print('min df: {}'.format(inverted_index.get_min_df()))
        # TODO: Explain the different characteristics of the above two sets of terms
        print('The different characteristics of the above two sets of terms:')
        print('maxdf is the most common term in the collection, located in large number of documents')
        print('mindf is the rarest term in the collection, located only in few documents')


if __name__ == '__main__':
    main()
