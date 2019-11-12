
def boolean_retrieval(inverted_index):
    queries_results = []

    # (hubble AND ( telescope NOT space) )
    hubble_pl = inverted_index.get_postlist('hubble').get_docno_set()
    telescope_pl = inverted_index.get_postlist('telescope').get_docno_set()
    space_pl = inverted_index.get_postlist('space').get_docno_set()
    queries_results.append(hubble_pl.intersection(telescope_pl.difference(space_pl)))

    # ((iran OR africa) NOT ( sanctions OR support) )
    iran_pl = inverted_index.get_postlist('iran').get_docno_set()
    africa_pl = inverted_index.get_postlist('africa').get_docno_set()
    sanctions_pl = inverted_index.get_postlist('sanctions').get_docno_set()
    support_pl = inverted_index.get_postlist('support').get_docno_set()
    queries_results.append(iran_pl.union(africa_pl).intersection(sanctions_pl.union(support_pl)))

    # (iran AND israel)
    iran_pl = inverted_index.get_postlist('iran').get_docno_set()
    israel_pl = inverted_index.get_postlist('israel').get_docno_set()
    queries_results.append(iran_pl.intersection(israel_pl))

    # ((south NOT african) NOT sanctions)
    south_pl = inverted_index.get_postlist('south').get_docno_set()
    african_pl = inverted_index.get_postlist('african').get_docno_set()
    sanctions_pl = inverted_index.get_postlist('sanctions').get_docno_set()
    queries_results.append(south_pl.difference(african_pl).difference(sanctions_pl))

    # (technion OR haifa)
    technion_pl = inverted_index.get_postlist('technion').get_docno_set()
    haifa_pl = inverted_index.get_postlist('haifa').get_docno_set()
    queries_results.append(technion_pl.union(haifa_pl))

    return [' '.join(x) for x in queries_results]
