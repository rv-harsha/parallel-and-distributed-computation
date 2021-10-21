
nodes=[]
edges=[]

def checkedge(edge):
	if edge in edges:
		return True;
	return False

def readgraph(filename):
	with open(filename) as f:
		rows = f.readlines()
		rows = rows[4:]
		for row in rows:
			columns = row.split()
			#print(columns[0])
			#print(columns[1])
			edges.append((int(columns[0]), int(columns[1])))
			if int(columns[0]) not in nodes:
				nodes.append(int(columns[0]))
			if int(columns[1]) not in nodes:
				nodes.append(int(columns[1]))
				


if __name__ == "__main__":
	filename = "p2p-Gnutella06.txt"
	readgraph(filename)
	print(nodes)
	print(edges)
	print("0 - 2: " + str(checkedge((0,2))))
	print("0 - 3: " + str(checkedge((0,3))))
	print("1 - 2: " + str(checkedge((1,2))))

