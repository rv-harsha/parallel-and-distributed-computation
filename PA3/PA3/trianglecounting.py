import sys
import time
from pyspark import SparkContext


def mapForEdgeReverse(edge):
    """Reverses the tuple elements"""
    return (edge[1], edge[0])


def mapEdgeToCluster(row):
    """Creates the edge tuple by reading the row elements"""
    columns = row.split()
    return (int(columns[0]), int(columns[1]))


def mapForNodeReduce(row):
    """Function returns single edge tuple list"""
    columns = row.split()
    return [int(columns[0]), int(columns[1])]


def mapToCluster(data, edgesList):
    """
    Inputs: 
        - data: tuple (to, from[])
        - edgesList: edgelist [(from, to)]

    Output:
        - output: list of tuples (to, from)"""
    output = []

    # If * is present in data[0], it means no hop neighbours are present
    # in one the map reduce iterations so do not perform any action,
    # return (*, from) for all from[] nodes of data
    if data[0] == "*":
        for node in data[1]:
            output.append(("*", node))
        return output

    # Check if n-hop neighbour exists, if neighbour exits,
    # create n-hop neighbour edges from each of data(from[]) nodes to
    # the "to" node in edge of edgeList
    for edge in edgesList:
        if data[0] == edge[0]:
            for node in data[1]:
                output.append((edge[1], node))

    # If output is still empty, then no n-hop neighbours exist,
    # so all the nodes can be assigned arbitrary character (* - no node)
    # to be ignored in further Map Reduce iterations and for counting as well
    if not output:
        output.append(("*", data[0]))
        for node in data[1]:
            output.append(("*", node))

    return output


def countOnCluster(data):
    """
    Inputs:
        - data: tuple (to, from[]) 

    Output:
        - count: list [(node, counter)]
    """
    count = []

    # If "*" exists in data[0], then all nodes in from[]
    # can be assigned 0 count
    if data[0] == "*":
        for node in data[1]:
            count.append((node, 0))
    else:
        # If "to" node is non-empty, assign 0 count
        # to prevent loss of nodes in final list.
        count.append((data[0], 0))

        # If the "to" node is same as "from" node,
        # increment count, otherwise set node count as 0
        for node in data[1]:
            if node == data[0]:
                count.append((node, 1))
            else:
                count.append((node, 0))
    return count


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(str(len(sys.argv))+"Usage: trianglecounting.py <datafile>")
        exit(-1)

    sc = SparkContext(appName="trainglecounting")

    # Read data file and parallelize rows to create edges
    with open(sys.argv[1]) as f:
        rows = f.readlines()[4:]
        rowsParallel = sc.parallelize(rows)
        edges = rowsParallel.map(lambda row: mapEdgeToCluster(row))

    # Map-Reduce: Round 1
    mapReduce = edges.map(lambda edge: mapForEdgeReverse(edge)).groupByKey()
    edgesList = edges.collect()

    # Map-Reduce: Round 2 & 3 to find 2 and 3-hop neighbours of each node
    for i in range(2):
        tempMapReduce = mapReduce.flatMap(
            lambda tuple: mapToCluster(tuple, edgesList)).groupByKey()
        mapReduce = tempMapReduce

    # Final Map-Reduce to count the traingles for each node
    finalclustermap = mapReduce.flatMap(
        lambda tuple: countOnCluster(tuple)).reduceByKey(lambda a, b: a + b).sortByKey()

    finalclustermap.saveAsTextFile("traingle_output")
