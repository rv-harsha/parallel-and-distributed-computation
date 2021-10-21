import sys
from pyspark import SparkContext


def mapForEdgeReverse(edge):
    return (edge[1], edge[0])


def mapForEdgeReduce(row):
    columns = row.split()
    return (int(columns[0]), int(columns[1]))


def mapForNodeReduce(row):
    columns = row.split()
    return [int(columns[0]), int(columns[1])]


def mapToCluster(data, edges):
    output = []
    for edge in edges:
        if data[0] == edge[0]:
            for node in data[1]:
                output.append((edge[1], node))
    return output


def countOnCluster(data):
    count = 0
    for node in data[1]:
        if node == data[0]:
            count = count + 1
    return (data[0], count)


def traingleCount(node, map):
    nodeFound = False
    for tuple in map:
        if tuple[0] == node:
            return tuple
    if nodeFound == False:
        return (node, 0)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(str(len(sys.argv))+"Usage: trianglecounting.py <datafile>")
        exit(-1)

    sc = SparkContext(appName="trainglecounting")

    # Read data file and Parallelize rows
    with open(sys.argv[1]) as f:
        rows = f.readlines()[4:]
        rows_parallel = sc.parallelize(rows)
        edges = rows_parallel.map(lambda row: mapForEdgeReduce(row))
        nodes = rows_parallel.flatMap(
            lambda tuple: mapForNodeReduce(tuple)).distinct()

    # Map-Reduce: Round 1
    map_reduce_1 = edges.map(lambda edge: mapForEdgeReverse(edge)).groupByKey()

    # Map-Reduce: Round 2, find 2-hop neighbours of v
    edges = edges.collect()

    map_reduce_2 = map_reduce_1.flatMap(
        lambda tuple: mapToCluster(tuple, edges)).groupByKey()

    # Map-Reduce: Round 3, find 3-hop neighbours of v
    map_reduce_3 = map_reduce_2.flatMap(
        lambda tuple: mapToCluster(tuple, edges)).groupByKey()

    # Map to count the nodes with same 3rd hop neighbour
    clustermap = map_reduce_3.map(
        lambda tuple: countOnCluster(tuple)).collect()

    # Map-Reduce to add nodes that do not have 1-hop neighbour 
    # (with 0 count) and were discarded in Map-Reduce (Round 2)
    finalclustermap = nodes.map(
        lambda node: traingleCount(node, clustermap)).sortByKey()
    finalclustermap.saveAsTextFile("traingle_output_with_nodes")