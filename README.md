# ATONTE Structure and Disambiguate
This repository contains the ATONTE (ATlantis Ontology and kNowledge graph development from Texts and Experts) structure and disambiguate files.

It allows the automated structuring of information extracted from text as a knowledge graph according to an ontology, and disambiguating entities via entity linking to a reference resource. This code constitutes a proof of concept, using off-the-shelf tools to first structure spatial entities and relations extracted from a text corpus as Resource Description Framework (RDF) triples to populate and enrich an existing ontology ([ATLANTIS Ontology](https://github.com/umrlastig/atlantis-ontology)), and then to link the spatial entities to their corresponding entries in a .geojson file of toponyms and locations extracted from the [BD TOPO®](https://geoservices.ign.fr/bdtopo).

For more information, please see https://theses.hal.science/tel-04599846, page 131 onwards.

## Tutorial
### Structuring
- install SPARQL-Generate
### Disambiguating
- install Python, Elasticsearch, PyCharm Community and GraphDB Free Edition
- (optional) install [Elasticvue](https://github.com/cars10/elasticvue) plugin for browsers
- launch Pycharm and create a new PyCharm project with a virtual environment and clone the files from this repository in the project folder
- launch GraphDB and create a new repository
- import the RDF files of the spatial entities that need to be disambiguated into this repository
- launch Elasticsearch
- launch the InitializeEverything.py script to create an Elasticsearch index that contains the entries from your dictionary (in our case, the toponyms from a .geojson file)
- if you installed the Elasticvue browser plugin, you can visualise your dictionary in your browser
- run any of the scripts in the Main folder to disambiguate your RDF entities according to the method indicated in the file name
- upload the resulting .ttl files to GraphDB
- run the MesureResultats.py script to evaluate the disambiguation results

## Acknowledgements
This work was co-financed by the Shom and the IGN and was carried out at the LASTIG, a research unit at Université Gustave Eiffel.

Contributors for the Structuring code: Léa Lamotte, Nathalie Abadie, Helen Rawsthorne

Contributors for the Disambiguation code: Mayeul de Loynes, Romain Ruiz, Nathalie Abadie, Helen Rawsthorne

## Licence
The content of this repository is licenced under the Etalab Open License Version 2.0 and the CC BY 4.0 licence.
