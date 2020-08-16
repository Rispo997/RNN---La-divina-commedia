rhymes = ['_000_ ', '_001_ ']
rhymes_counter = [1, 0]
currentRhyme = 0
next = 2
firstRhyme = True;

def initRhymeTagSystem():
	global next
	global rhymes 
	global rhymes_counter
	global currentRhyme
	global firstRhyme
	rhymes = ['_000_ ', '_001_ ']
	rhymes_counter = [1, 0]
	currentRhyme = 0
	next = 2
	firstRhyme = True;

def nextRhymeTag():
	global next
	rhymes[0] = rhymes[1]
	rhymes[1] = '_{:0>3}_ '.format(str(next))
	rhymes_counter[0] = rhymes_counter[1]
	rhymes_counter[1] = 0
	next = next + 1


lines = []
with open("../resources/DC-cleaned.txt", 'r', encoding='utf8', errors='ignore') as fp:
	i = 0
	first = True
	newTercet = False
	for line in fp: 
		if (not line.startswith("\n")):
			if(line.find("Canto") != -1 and (line.find("Inferno") != -1 or line.find("Purgatorio") != -1 or line.find("Paradiso") != -1)):
				if (not first):
					del lines[-1]
					lines.append("_sol_ _end_ _eol_\n")
				first = False
				lines.append("_sol_ _start_ _eol_\n")
				#initRhymeTagSystem()
			else:
				#insert rhyme tag
				#lines.append(rhymes[currentRhyme])
				#rhymes_counter[currentRhyme] += 1
				#if(rhymes_counter[currentRhyme] == 3):
				#	nextRhymeTag()
				#else:
				#	currentRhyme = 1 if currentRhyme == 0 else 0
				#rhymes_counter[0]
				lines.append("_sol_ ")
				lines.append(line[:-1].lower().replace("’", "'"))
				lines.append(" _verse_ _eol_\n")
				newTercet = True
		else:
			if(newTercet):
				lines.append("_sol_ _tercet_ _eol_\n")
				newTercet = False
	del lines[-1]
	lines.append(" _verse_ _eol_\n")
	lines.append("_sol_ _end_ _eol_\n")
# Writing to file 
output = open('output.txt', 'w') 
output.writelines(lines) 
output.close() 