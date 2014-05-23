import string
import copy

K_NAME_FOR_CONSTANT = " "
K_ZERO_MONOM = {}
K_ZERO_POLY = []

def lex_common(first_monom, second_monom, variable_order):
	for variable in variable_order:
		if variable in first_monom and variable not in second_monom:
			return -1
		if variable not in first_monom and variable in second_monom:
			return 1
		if variable not in first_monom:
			continue;
		if first_monom[variable] != second_monom[variable]:
			return second_monom[variable]-first_monom[variable]
	return 0

def lex_compare(first_monom, second_monom):
	return lex_common(first_monom, second_monom, string.ascii_letters)

def inverse_lex_compare(first_monom, second_monom):
	return lex_common(first_monom, second_monom, reversed(string.ascii_letters))

def constant(monom):
	if monom == K_ZERO_MONOM:
		return 0;
	if K_NAME_FOR_CONSTANT in monom:
		return monom[K_NAME_FOR_CONSTANT]
	return 1

def multiorder(monom, all_degrees=False):
	result = []
	if all_degrees:
		variable_pool = string.ascii_letters
	else:
		variable_pool = monom
	for variable in variable_pool:
		if variable == K_NAME_FOR_CONSTANT:
			continue
		if variable in monom:
			order = monom[variable]
		else:
			order = 0
		result.append(order)
	return result

def same(first_monom, second_monom, constant_matter=True):
	return multiorder(first_monom, True) == multiorder(second_monom, True) and (not constant_matter or (constant(first_monom) == constant(second_monom)))

def grad_compare(first_monom, second_monom):
	first_order = sum(multiorder(first_monom))
	second_order = sum(multiorder(second_monom))
	if (first_order == second_order):
		return lex_compare(first_monom, second_monom)
	return second_order - first_order

def add(first_poly, second_poly):
	result = copy.deepcopy(first_poly)
	for monom_second in second_poly:
		found = False
		for monom_result in result:
			if same(monom_result, monom_second, False):
				found = True
				monom_result[K_NAME_FOR_CONSTANT] = constant(monom_result) + constant(monom_second)
				break
		if not found:
			result.append(monom_second)
	final_result = []
	for monom in result:
		if constant(monom) != 0:
			final_result.append(monom)
	return final_result

def unary_minus(poly):
	result = copy.deepcopy(poly)
	for monom in result:
		monom[K_NAME_FOR_CONSTANT] = -constant(monom)
	return result

def minus(poly_first, poly_second):
	return add(poly_first, unary_minus(poly_second))

def print_monome(monom, new_line=False, print_sorted=True):
	if K_NAME_FOR_CONSTANT in monom:
		if monom[K_NAME_FOR_CONSTANT] != 0:
			print(monom[K_NAME_FOR_CONSTANT]),
	if print_sorted:
		print_from = string.ascii_letters
	else:
		print_from = monom
	for variable in print_from:
		if variable == K_NAME_FOR_CONSTANT:
			continue
		if variable not in monom:
			continue
		if monom[variable] == 0:
			continue
		print ("%s^%d"%(variable, monom[variable])),
	if new_line:
		print

def poly_update(poly):
	updated = []
	for monom in poly:
		if constant(monom) != 0:
			if (sum(multiorder(monom)) == 0):
				updated = add(updated, [{K_NAME_FOR_CONSTANT:constant(monom)}])
			else:
				updated.append(copy.deepcopy(monom))
	return updated

def print_poly(poly, new_line=False, print_sorted=True):
	poly = poly_update(poly)
	first = True
	for monom in poly:
		if (first):
			print_monome(monom, print_sorted = print_sorted),
		else:
			print("+"),
			print_monome(monom, False, print_sorted)
		first = False
	if new_line:
		print

def order_of(monom, variable):
	if variable not in monom:
		return 0
	return monom[variable]

def leading_term(poly, order):
	if len(poly) == 0:
		return copy.deepcopy(K_ZERO_MONOM)
	tmp = copy.deepcopy(poly);
	tmp.sort(cmp=order)
	return tmp[0]

def monom_multiply(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)
	for variable in string.ascii_letters:
		to_add = order_of(monom_a, variable) + order_of(monom_b, variable)
		if to_add == 0:
			continue
		result[variable] = to_add;
	result[K_NAME_FOR_CONSTANT] = constant(monom_a) * constant(monom_b)
	return result

def poly_monom_multiply(monom, poly):
	result = copy.deepcopy(K_ZERO_POLY)
	for monom_in_poly in poly:
		result = add([monom_multiply(monom, monom_in_poly)], result)
	return result

def poly_multiply(poly_a, poly_b):
	result = copy.deepcopy(K_ZERO_POLY)
	for monom_in_a in poly_a:
		result = add(result, poly_monom_multiply(monom_in_a, poly_b))
	return result

def divides(monom_a, monom_b):
	for variable in monom_b:
		if variable == K_NAME_FOR_CONSTANT:
			continue
		if variable not in monom_a:
			return False
		if monom_a[variable] < monom_b[variable]:
			return False
	return True

def monom_divide(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)
	for variable in monom_a:
		if variable == K_NAME_FOR_CONSTANT:
			result[variable] = monom_a[variable] / constant(monom_b)
		else:
			result[variable] = monom_a[variable] - order_of(monom_b, variable)
	return result

def poly_divide(poly, poly_list, order=lex_compare):
	quotient = [copy.deepcopy(K_ZERO_POLY)] * len(poly_list)
	remainder = copy.deepcopy(K_ZERO_POLY)
	h = copy.deepcopy(poly)

	while (h != K_ZERO_POLY):
		changed = False;		
		
		h_leading_term = leading_term(h, order)
		
		for index in range(len(poly_list)):
			fi_leading_term = leading_term(poly_list[index], order)

			if divides(h_leading_term, fi_leading_term):
				changed = True
				tmp = monom_divide(h_leading_term, fi_leading_term)
				quotient[index] = add(quotient[index], [tmp])
				h = minus(h, poly_monom_multiply(tmp, poly_list[index]))
				break
		if not changed:
			remainder = add(remainder, [h_leading_term])
			h = minus(h, [h_leading_term])
	return (quotient, remainder)

monom1 = {};
monom2 = {};
monom3 = {};
monom4 = {};

monom1["x"] = 2
monom1["y"] = 1

monom2["x"] = 1
monom2["y"] = 2

monom3["y"] = 2

monom4[K_NAME_FOR_CONSTANT] = 8
monom4["x"] = 1
monom4["y"] = 2
monom4["z"] = 3

polinom_f  = [ {"x":2, "y":1}, {"x":1, "y":2},          {"y":2} ]
polinom_f1 = [ {"x":1, "y":1}, {K_NAME_FOR_CONSTANT:-1} ]
polinom_f2 = [ {"y":2},        {K_NAME_FOR_CONSTANT:-1} ]

poly1 = [monom1, monom2];
poly2 = [monom1, monom2];
#print_poly(poly1, True, True)
#print_poly(poly2, True, True)
print_poly(polinom_f, True)
print_poly(polinom_f1, True)
print_poly(polinom_f2, True)
print
(quotients, remainder) = poly_divide(polinom_f, [polinom_f1, polinom_f2], order=lex_compare)

def print_poly_simple(poly):
	print_poly(poly, True, False)

map(print_poly_simple, quotients)
print_poly(remainder, True, False)
