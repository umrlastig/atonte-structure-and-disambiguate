# Implémentation des méthodes de recherche d'ES

# Docs : https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html
#       https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-edgengram-tokenizer.html

# Sélection des candidats pour un toponyme selon paramètre par défaut d'ES
def candidate_selection(toponym, results=1, method=None):  # Méthode d'égalité stricte de chaine de caracteres
    return {
        'query': {
            'match': {
                'properties.toponyme': toponym
            }
        }
    }

# ORIGINAL LEVENSHTEIN
# Sélection avec la méthode fuzzy (par défaut) = distance de levenshtein
def candidate_selection_match_fuzzy_old(esn, results=1, method=None):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # ORIG was 50, default is 10
        'query': {
            'match': {
                'properties.toponyme': {
                    'query': esn,
                    'fuzziness': "AUTO",
                    'max_expansions': 10,  # default is 50
                    'prefix_length': 2,  # default is 0
                    # 'fuzzy_transpositions': 'true',  # default is 'true'
                    'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                    'operator': 'AND'  # default is 'OR'
                }
            }
        }
    }


# ORIGINAL LEVENSHTEIN - IN REPORT
# This is a term-level query rather than a full-text query, which means that the search terms are not analysed
# Sélection avec la méthode fuzzy (par défaut) = distance de levenshtein
def candidate_selection_fuzzy_report(esn, results=1, method=None):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # ORIG was 50, default is 10
        'query': {
            'fuzzy': {
                'properties.toponyme': {
                    'value': esn,
                    'fuzziness': "AUTO",
                    'max_expansions': 100,  # default is 50
                    'prefix_length': 0,  # default is 0
                    'transpositions': 'true',  # default is 'true'
                    'rewrite': 'constant_score',  # default is 'top_terms_blended_freqs_${max_expansions}'
                }
            }
        }
    }


# HMR LEVENSHTEIN - IN REPORT - IMPROVED WITH FULL TEXT QUERY & ENTITY TYPE v1 and v2
def candidate_selection_toponyme_type(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            #'max_expansions': 100,  # default is 50
                            #'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # think this
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            #'max_expansions': 100,  # default is 50
                            #'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            #'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            #'max_expansions': 100,  # default is 50
                            #'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            #'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & OR OPERATOR v3
def candidate_selection_toponyme_type_or(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 100,  # default is 50
                            # 'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # think this
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 100,  # default is 50
                            # 'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 100,  # default is 50
                            # 'prefix_length': 0,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & AND OPERATOR & 0.2 BOOST ON TYPE v4
def candidate_selection_toponyme_type_20_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.2,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.2,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & OR OPERATOR & 0.2 BOOST ON TYPE v5
def candidate_selection_toponyme_type_or_20_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.2,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.2,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & OR OPERATOR & 0.4 BOOST ON TYPE v6
def candidate_selection_toponyme_type_or_40_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.4,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.4,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & AND OPERATOR & 0.4 BOOST ON TYPE v7
def candidate_selection_toponyme_type_40_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.4,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.4,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & AND OPERATOR & 0.6 BOOST ON TYPE v8
def candidate_selection_toponyme_type_60_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.6,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.6,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & OR OPERATOR & 0.6 BOOST ON TYPE v9
def candidate_selection_toponyme_type_or_60_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.6,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.6,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & OR OPERATOR & 0.8 BOOST ON TYPE v10
def candidate_selection_toponyme_type_or_80_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.8,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.8,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'OR'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR LEVENSHTEIN IMPROVED WITH ENTITY TYPE & AND OPERATOR & 0.8 BOOST ON TYPE v11
def candidate_selection_toponyme_type_80_boost(esn, geog_feat):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'size': 10,  # default is 10
        'query': {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.8,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'fuzziness': "AUTO",
                            'boost': 0.8,
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'fuzziness': "AUTO",
                            # 'max_expansions': 10,  # default is 50
                            # 'prefix_length': 2,  # default is 0
                            # 'fuzzy_transpositions': 'true',  # default is 'true'
                            # 'fuzzy_rewrite': 'scoring_boolean',  # default is 'top_terms_blended_freqs_${max_expansions}'
                            'operator': 'AND'  # default is 'OR'
                        }
                    }
                }
            }
        }
    }


# Sélection avec la méthode fuzzy (par défaut) = distance de levenshtein
def candidate_selection_fuzzy(toponym, results=1, method=None):  # Méthode de levenshtein implémenté dans ES
    return {
        # 'from':0,
        'size': 50,
        'query': {
            'fuzzy': {
                'properties.toponyme': {
                    'value': toponym,
                    'fuzziness': "AUTO",
                    'max_expansions': 100,
                    'prefix_length': 1,
                    'transpositions': 'true',
                    'rewrite': 'constant_score'
                }
            }
        }
    }


# OLD OLD OLD NGRAM
# Sélection avec le découpage n-gram sur le toponyme
def candidate_selection_ngram_new_likeev(toponym, results=10, method=None):
    return {
        "query": {
            "query_string": {
                "query": toponym,
            }
        }
        # },
        # "size": 10,  # default is 10
        # "from": 0,  # default is 0
        # "sort": []
    }


# ORIGINAL NGRAM
def candidate_selection_ngram(toponym, results=10, method=None):
    return {
        'query': {
            'match': {
                'properties.toponyme': {
                    'query': toponym,
                    'operator': 'and'
                }
            }
        }
    }


# HMR NGRAM v1 & v2
def candidate_selection_ngram_toponyme_type(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'operator': 'AND'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'operator': 'AND'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'AND'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v3
def candidate_selection_ngram_toponyme_type_or(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'operator': 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'operator': 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v4
def candidate_selection_ngram_toponyme_type_20_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.2,
                            'operator': 'AND'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.2,
                            'operator': 'AND'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'AND'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v5
def candidate_selection_ngram_toponyme_type_or_20_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.2,
                            'operator': 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.2,
                            'operator': 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v6
def candidate_selection_ngram_toponyme_type_or_40_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.4,
                            'operator': 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.4,
                            'operator': 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v7
def candidate_selection_ngram_toponyme_type_40_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.4,
                            'operator': 'AND'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.4,
                            'operator': 'AND'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'AND'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v8
def candidate_selection_ngram_toponyme_type_60_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.6,
                            'operator': 'AND'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.6,
                            'operator': 'AND'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'AND'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v9
def candidate_selection_ngram_toponyme_type_or_60_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.6,
                            'operator': 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.6,
                            'operator': 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v10
def candidate_selection_ngram_toponyme_type_or_80_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.8,
                            'operator': 'OR'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.8,
                            'operator': 'OR'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'OR'
                        }
                    }
                }
            }
        }
    }


# HMR NGRAM v11
def candidate_selection_ngram_toponyme_type_80_boost(esn, geog_feat):
    return {
        "query": {
            'bool': {
                'should': {
                    'match': {
                        'properties.nature': {
                            'query': geog_feat,
                            'boost': 0.8,
                            'operator': 'AND'
                        }
                    }
                },
                'should': {
                    'match': {
                        'properties.naturedetaillee': {
                            'query': geog_feat,
                            'boost': 0.8,
                            'operator': 'AND'
                        }
                    }
                },
                'must': {
                    'match': {
                        'properties.toponyme': {
                            'query': esn,
                            'operator': 'AND'
                        }
                    }
                }
            }
        }
    }
