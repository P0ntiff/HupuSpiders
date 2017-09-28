import string


def postProcessing():
	with open("HupuSpiders_chi_noemptystring.xml") as input:
		lines = input.read().splitlines()
		with open("newhupuspiders2_chi.xml", "w") as output:
			for n in range(0, len(lines)):
				if ((("<dialog>" in lines[n]) and ("</dialog>" in lines[n + 1])) or
					(("</dialog>" in lines[n]) and ("<dialog>" in lines[n - 1])) or 
					(lineIsEmpty(lines[n]))):
					continue
				else:
					output.write(lines[n] + "\n")

#NOT IMPLEMENTED: 
#Example: <s><utt uid="2353"></utt><utt uid="2354"></utt></s>
#	-->Should return 'true' as "line Is Empty"
def lineIsEmpty(line):
	return False

postProcessing()