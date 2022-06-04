import os
import sys
import yaml
import bibtexparser

from datetime import datetime

def covert(yaml_dict):
    now = datetime.now()
    yaml_dict['date'] = now

    # Make a venue from fields which might exist
    for v in ['journal', 'booktitle']:
        if v in yaml_dict:
            yaml_dict['venue'] = yaml_dict[v]
            break

    # To be filled by user after
    yaml_dict['category']  = None
    yaml_dict['ispublished'] = 'arXiv' not in yaml_dict['venue']
    yaml_dict['url']       = None
    yaml_dict['poster']    = None
    yaml_dict['video']     = None
    yaml_dict['authors']   = author_str_parse(yaml_dict['author'])

    return yaml_dict['ID'], yaml_dict


def author_str_parse(author_str):
    authors = []
    for author in author_str.split(' and '):
        last, first = author.split(', ')
        authors.append(f'{first} {last}')
    return authors


if __name__ == '__main__':

    with open(f'my_bib.bib') as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_parsed = bibtexparser.loads(bibtex_str)

    for bib_dict in bib_parsed.entries:
        yaml_name, yaml_list = covert(bib_dict)
        # Skip if we already have this
        #if os.path.isfile(f'my_ymls/{yaml_name}.yml'):
        #    continue

        with open(f'my_ymls/{yaml_name}.yml', 'w') as f:
            yaml.dump(yaml_list, f, explicit_start=True, explicit_end=True)
    

#    for bib_file in os.listdir('my_bibs'):
#
#        with open(f'my_bibs/{bib_file}') as bibtex_file:
#            bibtex_str = bibtex_file.read()
#
#        yaml_name, yaml_list = covert(bibtex_str)
#
#        # Skip if we already have this
#        #if os.path.isfile(f'my_ymls/{yaml_name}.yml'):
#        #    continue
#
#        with open(f'my_ymls/{yaml_name}.yml', 'w') as f:
#            yaml.dump(yaml_list, f, explicit_start=True, explicit_end=True)
