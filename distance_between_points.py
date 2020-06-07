#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:11:47 2020

@author: luciano
Calculates the DISTANCES between all points in a given data set. The input must
be provided via a CSV file separated by semi-colons, where the first position
has to be the name of the location, the second the x axis position and the third
the y axis position.

The output will be provided in another CSV which will contain three columns: name
of a location, name of another location and distance between them. This output
file will be created in the same folder where this script is being executed.
"""

import math
import csv
import sys
import os
import logging


def calculate_distance(pt1, pt2):
    '''
    Calculates the cartesian distance between two points.

    Parameters
    ----------
    pt1 : tuple
        x axis position in the first position and y axis position in the second.
    pt2 : tuple
        x axis position in the first position and y axis position in the second.

    Returns
    -------
    float
        The distance between pt1 and pt2.
    '''
    return math.sqrt((pt2[0] - pt1[0])**2 +  (pt2[1] - pt1[1])**2)


def validate_parms():
    '''
    Simple validation. It will stop the execution if the file name is not
    valid.
    '''
    # Let's check if the two file names were provided
    if len(sys.argv) < 2:
        logging.error('Please inform the name of the file containing the locations')
        sys.exit(24)

    # Let's check if the provided file name is valid
    if not os.path.isfile(sys.argv[1]):
        logging.error('%s is not a valid file path', sys.argv[1])
        sys.exit(25)

if __name__ == '__main__':
    validate_parms() # Wil stop the execution if validation finds errors.

    INPUT_FILE = sys.argv[1]
    qt_locations = int()
    qt_distances = int()

     # We'll store the DISTANCES in a set to eliminate duplicates such as
     # "A to B" and "B to A"
    DISTANCES = set()

    with open(INPUT_FILE) as input_csv:
        LOCATIONS = csv.reader(input_csv, delimiter=';')

        # Nested won't work with the CSV object, therefore I have to put its
        # contents in a list.
        LOCATIONS_LIST = list()
        LOCATIONS_LIST.extend(LOCATIONS)

        for loc1 in LOCATIONS_LIST:
            qt_locations += 1
            for loc2 in LOCATIONS_LIST:

                # No need to calculate a distance from a point to itself.
                if loc1[0] == loc2[0]:
                    continue

                distance = calculate_distance((float(loc1[1]), float(loc1[2])),
                                              (float(loc2[1]), float(loc2[2])))

                # We gotta sort the list to make "A to B" equals to "B to A", so
                # our set can eliminate this kind of duplicates
                result = sorted([loc1[0], loc2[0], str(distance)])

                # Since sets can not store lists, we have to store a striged
                # version of our lists of DISTANCES.
                DISTANCES.add(str(result))

    # All DISTANCES were calculated. Let's read the resulting set and save them.
    NEW_FILE = INPUT_FILE.split('.')[0] + '-distances.' + INPUT_FILE.split('.')[1]

    with open(NEW_FILE, 'w') as output_file:
        WRITER = csv.writer(output_file, lineterminator='\n')
        
        # Let's write a header in the CSV
        WRITER.writerow(['loc1', 'loc2', 'distance'])

        # And now a line for each distance
        for i in DISTANCES:
            # Let's recreate the lists from the strings stored in the set
            #print(sorted(i.strip('][').replace("'", "").split(', '), reverse=True))
            ROW = sorted(i.strip('][').replace("'", "").split(', '), reverse=True)
            WRITER.writerow(ROW)
            qt_distances += 1

    # Done!
    print(f'Locations read: {qt_locations}')
    print(f'Distances calculated: {qt_distances}')


'''
Para carregar o grafo
---------------------
LOAD CSV WITH HEADERS FROM "file:///test-distances.csv" AS row
MERGE(loc1:Localizacao{nome:row.loc1})
MERGE(loc2:Localizacao{nome:row.loc2})
MERGE(loc1)-[dist:Distancia]->(loc2)
SET dist.distancia = toInteger(row.distance)

Para criar as relações temporárias
----------------------------------
MATCH(n:Localizacao {nome:"Curitiba/PR"})
CALL algo.spanningTree.minimum("Localizacao", "Distancia", "distancia", id(n), {write:true, writeProperty:"MINST"})
YIELD loadMillis, computeMillis, writeMillis, effectiveNodeCount
RETURN loadMillis, computeMillis, writeMillis, effectiveNodeCount

Para inserir as distâncias nas relações temporárias
---------------------------------------------------
MATCH(x:Localizacao)-[mstr:MINST]-(y:Localizacao)
OPTIONAL MATCH(x:Localizacao)-[r:Distancia]-(y:Localizacao)
SET mstr.distancia = r.distancia

Para calcular o caminho
-----------------------
MATCH path = (n:Localizacao {nome:"Curitiba/PR"})-[:MINST*]-()
WITH relationships(path) AS rels
UNWIND rels AS rel
WITH DISTINCT rel AS rel
RETURN startNode(rel).nome AS source, endNode(rel).nome AS destination, rel.distancia AS cost

Para deletar as relações temporárias
------------------------------------
MATCH(x:Localizacao)-[r:MINST]-(y:Localizacao)
DELETE r
'''