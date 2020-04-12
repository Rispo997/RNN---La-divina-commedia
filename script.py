lines = []
with open("DC-modified.txt", 'r', encoding='utf8', errors='ignore') as fp:
	i = 0
	first = True
	for line in fp: 
		if (not line.startswith("\n")):
			if(line.find("Canto") != -1 and (line.find("Inferno") != -1 or line.find("Purgatorio") != -1 or line.find("Paradiso") != -1)):
				if (not first):
					del lines[-1]
					lines.append(" _end_ ")
				first = False
				lines.append("_start_ ")
			else:
				lines.append(line[:-1])
				lines.append(" _verse_ ")
	del lines[-1]
	lines.append(" _end_ ")
# Writing to file 
output = open('output.txt', 'w') 
output.writelines(lines) 
output.close() 