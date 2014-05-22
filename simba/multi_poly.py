K_NAME_FOR_CONSTANT = " "

def print_monome(monom):
	print(monom[K_NAME_FOR_CONSTANT])
	for (variable, order) in monom:
		if (variable == K_NAME_FOR_CONSTANT):
			continue
		print (" %d^%d"%(variable, order))

moj_monom = {}
moj_monom[K_NAME_FOR_CONSTANT] = 4
print_monome(monom)
print("\n")
moj_monom["x"] = 10;

print_monome(monom)
print("\n")
moj_monom["y"] = 2;
print_monome(monom)
print("\n")
moj_monom["x"] = 5;
