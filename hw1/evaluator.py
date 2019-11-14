
def boolean_retrieval(inverted_index):
    queries_results = []

    # (hubble AND ( telescope NOT space) )
    hubble_pl = inverted_index.get_postlist('hubble')
    telescope_pl = inverted_index.get_postlist('telescope')
    space_pl = inverted_index.get_postlist('space')
    if hubble_pl and telescope_pl and space_pl:
        queries_results.append(hubble_pl.intersection(telescope_pl.difference(space_pl)))
    else:
        queries_results.append(set())

    # ((iran OR africa) NOT ( sanctions OR support) )
    iran_pl = inverted_index.get_postlist('iran')
    africa_pl = inverted_index.get_postlist('africa')
    sanctions_pl = inverted_index.get_postlist('sanctions')
    support_pl = inverted_index.get_postlist('support')
    if iran_pl and africa_pl and sanctions_pl and support_pl:
        queries_results.append(iran_pl.union(africa_pl).intersection(sanctions_pl.union(support_pl)))
    else:
        queries_results.append(set())

    # (iran AND israel)
    iran_pl = inverted_index.get_postlist('iran')
    israel_pl = inverted_index.get_postlist('israel')
    if iran_pl and israel_pl:
        queries_results.append(iran_pl.intersection(israel_pl))
    else:
        queries_results.append(set())

    # ((south NOT african) NOT sanctions)
    south_pl = inverted_index.get_postlist('south')
    african_pl = inverted_index.get_postlist('african')
    sanctions_pl = inverted_index.get_postlist('sanctions')
    if south_pl and african_pl and sanctions_pl:
        queries_results.append(south_pl.difference(african_pl).difference(sanctions_pl))
    else:
        queries_results.append(set())

    # (technion OR haifa)
    technion_pl = inverted_index.get_postlist('technion')
    haifa_pl = inverted_index.get_postlist('haifa')
    if technion_pl and haifa_pl:
        queries_results.append(technion_pl.union(haifa_pl))
    else:
        queries_results.append(set())

    return [' '.join([inverted_index.docidmap[i].strip() for i in x]) for x in queries_results]
