import string
import copy

K_NAME_FOR_CONSTANT = " "
K_ZERO_MONOM = {}
K_ZERO_POLY = []
VARIABLE_DOMAIN = string.ascii_letters

'''
Common code used by both lex_compare and inverse_lex_compare
'''
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

'''
Comparator function used to sort monomials in lex order
'''
def lex_compare(first_monom, second_monom):
	return lex_common(first_monom, second_monom, VARIABLE_DOMAIN)

'''
Comparator function used to sort monomials in inverse lex order.
'''
def inverse_lex_compare(first_monom, second_monom):
	return lex_common(first_monom, second_monom, reversed(VARIABLE_DOMAIN))
'''
Returns constant part of monom.

[in]		monom
	monom

[returns]	constant
	single number
'''
def constant(monom):
	if monom == K_ZERO_MONOM:
		return 0;
	if K_NAME_FOR_CONSTANT in monom:
		return monom[K_NAME_FOR_CONSTANT]
	return 1

'''
Returns multiorder of monom.

[in]		monom
	monom

[in]		all_degrees
	if True list of multiorder will contain zeroes; if not defined assumed False

[returns]	multiorder
	list representing multiorder of monom
'''
def multiorder(monom, all_degrees=False):
	result = []
	if all_degrees:
		variable_pool = VARIABLE_DOMAIN
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

'''
Checks if two monoms are same.

[in]		first_monom
	monom

[in]		second_monom
	monom

[in]		constant_matter
	if true than monoms that differ only by multiplicative constant are not considered same

[returns]	True if monoms are same and False otherwise
'''
def same(first_monom, second_monom, constant_matter=True):
	return multiorder(first_monom, True) == multiorder(second_monom, True) and (not constant_matter or (constant(first_monom) == constant(second_monom)))

'''
Comparator function that is used to sort monomials in graded lex order
'''
def grad_compare(first_monom, second_monom):
	first_order = sum(multiorder(first_monom))
	second_order = sum(multiorder(second_monom))
	if (first_order == second_order):
		return lex_compare(first_monom, second_monom)
	return second_order - first_order

'''
Calculates sum of two polynomials

[in]		first_poly
	polynomial

[in]		second_poly
	polynomial

[returns]	result
	first_poly + second_poly
'''
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

'''
Calculates polynomial opposite (addition) to given polynomial

[in]		poly
	polynomial

[returns]	result
	-poly
'''
def unary_minus(poly):
	result = copy.deepcopy(poly)
	for monom in result:
		monom[K_NAME_FOR_CONSTANT] = -constant(monom)
	return result

'''
Calculates difference between two polynomials

[in]		poly_first
	polynomial

[in]		poly_second
	polynomial

[returns]	result
	poly_first - poly_second
'''
def minus(poly_first, poly_second):
	return add(poly_first, unary_minus(poly_second))

'''
Prints monome

[in]		monom
	monom to be printed

[in]		new_line
	whether new line should be printed after monom, default false

[in]		print_sorted
	whether variables shold be sorted inside monomial
'''
def print_monome(monom, new_line=False, print_sorted=True):
	if K_NAME_FOR_CONSTANT in monom:
		if monom[K_NAME_FOR_CONSTANT] != 0:
			print(monom[K_NAME_FOR_CONSTANT]),
	if print_sorted:
		print_from = VARIABLE_DOMAIN
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

'''
Tries to remove unnecessary monoms from polynomial.

[in]		poly
	polynomial
[returns]	poly
	resulting polynomial, possibly without some unnecessary monoms
'''
def poly_update(poly):
	updated = []
	for monom in poly:
		if constant(monom) != 0:
			if (sum(multiorder(monom)) == 0):
				updated = add(updated, [{K_NAME_FOR_CONSTANT:constant(monom)}])
			else:
				updated.append(copy.deepcopy(monom))
	return updated

'''
Prints polynomial

[in]		poly
	polynomial to be printed

[in]		new_line
	whether new line should be printed after polynomial

[in]		print_sorted
	whether variables should be sorted in any way for printing purposes
'''
def print_poly(poly, new_line=False, print_sorted=True):
	poly = poly_update(poly)
	first = True
	for monom in poly:
		if (first):
			print_monome(monom, False, print_sorted)
		else:
			print("+"),
			print_monome(monom, False, print_sorted)
		first = False
	if new_line:
		print

'''
Returns degree of variable in monom

[in]		monom
	monom

[in]		variable
	variable

[returns]	degree
	degree of variable in monom; if variable does not appear in monom - 0
'''
def order_of(monom, variable):
	if variable not in monom:
		return 0
	return monom[variable]

'''
Get's leading term of polynomial in given monomial order

[in]		poly
	polynomial
[in]		order
	monomial order

[returns]	result
	monom - copy of leading term of poly in order order
'''
def leading_term(poly, order):
	if len(poly) == 0:
		return copy.deepcopy(K_ZERO_MONOM)
	tmp = copy.deepcopy(poly);
	tmp.sort(cmp=order)
	return tmp[0]

def leading_monom(poly, order):
	if len(poly) == 0:
		return copy.deepcopy(K_ZERO_MONOM)
	lt = leading_term(poly, order)
	if K_NAME_FOR_CONSTANT in lt:
		del lt[K_NAME_FOR_CONSTANT]
	return lt

'''
Multiplies two monoms

[in]		monom_a
	monom to be multiplied

[in]		monom_b
	monom to be multiplied

[returns]	result
	monom, result of multiplication
'''
def monom_multiply(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)
	for variable in VARIABLE_DOMAIN:
		to_add = order_of(monom_a, variable) + order_of(monom_b, variable)
		if to_add == 0:
			continue
		result[variable] = to_add;
	result[K_NAME_FOR_CONSTANT] = constant(monom_a) * constant(monom_b)
	return result

'''
Multiplies monom by polynomial

[in]		monom
	monom to be multiplied

[in]		poly
	polynomial to be multiplied

[returns]	result
	polynomial, result of multiplication
'''
def poly_monom_multiply(monom, poly):
	result = copy.deepcopy(K_ZERO_POLY)
	for monom_in_poly in poly:
		result = add([monom_multiply(monom, monom_in_poly)], result)
	return result

'''
Multiplies two polynomials

[in]		poly_a
	first polynomial

[in]		poly_b
	second polynomial

[returns]	result
	result of division
'''
def poly_multiply(poly_a, poly_b):
	result = copy.deepcopy(K_ZERO_POLY)
	for monom_in_a in poly_a:
		result = add(result, poly_monom_multiply(monom_in_a, poly_b))
	return result

'''
Checks if monom is divisible with another monom

[in]		monom_a
	monom to be divided

[in]		monom_b
	monom to be divided with

[returns]	True if divisible; False otherwise
'''
def divides(monom_a, monom_b):
	for variable in monom_b:
		if variable == K_NAME_FOR_CONSTANT:
			continue
		if variable not in monom_a:
			return False
		if monom_a[variable] < monom_b[variable]:
			return False
	return True

'''
Divides two monoms if they are divisible. If not behaviour is undefined.

[in]		monom_a
	monom that is to be divided

[in]		monom_b
	monom which is divisor

[returns]	result
	result of division
'''
def monom_divide(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)
	for variable in monom_a:
		if variable == K_NAME_FOR_CONSTANT:
			result[variable] = monom_a[variable] / constant(monom_b)
		else:
			result[variable] = monom_a[variable] - order_of(monom_b, variable)
	return result

'''
Divides two polynomials in given order. If no order is given lex_compare is assumed.

[in]		poly
	polynomial to be divided

[in]		poly_list
	list of polynomials that divide polynomial

[in]		order
	monomial order in which division will be done; if none given lex_compare is assumed

[returns]	(quotient, remainder):
	quotient is list of quotients that are calculated such that quotiend[i] coresponds to poly_list[i]
	remainder is single poly that is remainder	
'''
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

'''
Finds greatest common divisor for two numbers

[in]		a
	integer number

[in]		b
	integer number

[returns]	result
	integer number, greatest common divisor of a and b
'''
def int_greatest_common_divisor(a, b):
	if a<b:
		(a, b) = (b, a)
	while b != 0:
		tmp = a
		a = b
		b = tmp % b
	return a

'''
Finds least common multiple for two numbers

[in]		a
	integer number

[in]		b
	integer number

[returns]	result
	number, least common multiple
'''
def int_least_common_multiple(a, b):
	return a*b/int_greatest_common_divisor(a, b)

'''
Finds least common multiple for two monoms

[in]		monom_a
	monom

[in]		monom_b
	monom

[returns]	result
	monom, LCM(monom_a, monom_b)
'''
def monom_least_common_multiple(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)
	
	constant_a = constant(monom_a)
	constant_b = constant(monom_b)
	constant_r = int_least_common_multiple(constant_a, constant_b)
	if not constant_r == 1:
		result[K_NAME_FOR_CONSTANT] = constant_r
	for variable in VARIABLE_DOMAIN:
		order_r = max(order_of(monom_a, variable), order_of(monom_b, variable))
		if not order_r == 0:
			result[variable] = order_r
	return result

'''
Finds greatest common divisor for two monoms

[in]		monom_a
	monom

[in]		monom_b
	monom

[returns]	result
	monom, GCD(monom_a, monom_b)
'''
def monom_greatest_common_divisor(monom_a, monom_b):
	result = copy.deepcopy(K_ZERO_MONOM)

	constant_a = constant(monom_a)
	constant_b = constant(monom_b)

	constant_r = int_greatest_common_divisor(constant_a, constant_b)
	if constant_r != 1:
		result[K_NAME_FOR_CONSTANT] = constant_r

	for variable in VARIABLE_DOMAIN:
		order_r = min(order_of(monom_a, variable), order_of(monom_b, variable))
		if not order_r == 0:
			result[variable] = order_r
	return result
'''
Finds syzygi polynomial of two polynomials in given order
'''
def syzygi_poly(poly_a, poly_b, order=lex_compare):
	lm_a = leading_monom(poly_a, order)
	lm_b = leading_monom(poly_b, order)
	lcm = monom_least_common_multiple(lm_a, lm_b)
	m_a = monom_divide(lcm, leading_term(poly_a, order))
	m_b = monom_divide(lcm, leading_term(poly_b, order))
	return minus(poly_monom_multiply(m_a, poly_a), poly_monom_multiply(m_b, poly_b))
'''
Finds groenber basis for list of polynomials in given order
'''
def groebner_basis(poly_list, order):
	gb = copy.deepcopy(poly_list)
	while True:
		g_prim = copy.deepcopy(gb)
		for p_index in range(len(g_prim)):
			p = g_prim[p_index]
			for q_index in range(p_index+1, len(g_prim)):
				q = g_prim[q_index]
				s = syzygi_poly(p, q, order)
				(_, h) = poly_divide(s, g_prim, order)
				if h!= K_ZERO_POLY:
					gb.append(h)
		if (g_prim == gb):
			break;
	return gb

def minimize_groebner_basis(poly_list, order=lex_compare):
	reduced_groebner = copy.deepcopy(poly_list)

	changes = True
	while changes:
		changes = False
		check = copy.deepcopy(reduced_groebner)
		for poly in check:
			for second in check:
				if second == poly:
					continue
				poly_lt = leading_term(poly, order)
				second_lt = leading_term(second, order)
				if divides(poly_lt, second_lt):
					changes = True
					break
			reduced_groebner = [x for x in reduced_groebner if not x==poly]
			if not changes:
				(_, remainder) = poly_divide(poly, reduced_groebner, order)
				reduced_groebner.append(remainder)
			else:
				break
	return reduced_groebner

def norm(poly, order=lex_compare):
	poly_lt = leading_term(poly, order)
	coef = constant(poly_lt)
	poly_copy = []
	for monom in poly:
		monom_copy = copy.deepcopy(monom)
		monom_copy[K_NAME_FOR_CONSTANT] = constant(monom_copy)/coef
		poly_copy.append(monom_copy)
	return poly_copy

poly_1 = [{K_NAME_FOR_CONSTANT:2, "x":1}, {"y":1}, {K_NAME_FOR_CONSTANT:-1, "z":1}, {K_NAME_FOR_CONSTANT:-8}]
poly_2 = [{K_NAME_FOR_CONSTANT:-3, "x":1}, {K_NAME_FOR_CONSTANT:-1, "y":1}, {K_NAME_FOR_CONSTANT:2, "z":1}, {K_NAME_FOR_CONSTANT:11}]
poly_3 = [{K_NAME_FOR_CONSTANT:-2, "x":1}, {"y":1}, {K_NAME_FOR_CONSTANT:2, "z":1}, {K_NAME_FOR_CONSTANT:3}]

poly_5 = [{K_NAME_FOR_CONSTANT:+2.0, "x":1}, {K_NAME_FOR_CONSTANT:-1.0, "y":1}, {K_NAME_FOR_CONSTANT:+3.0, "z":1}, {K_NAME_FOR_CONSTANT:+1.0}]
poly_6 = [{K_NAME_FOR_CONSTANT:+1.0, "x":1}, {K_NAME_FOR_CONSTANT:+2.0, "y":1}, {K_NAME_FOR_CONSTANT:-4.0, "z":1}, {K_NAME_FOR_CONSTANT:-5.0}]
poly_7 = [{K_NAME_FOR_CONSTANT:+3.0, "x":1}, {K_NAME_FOR_CONSTANT:+1.0, "y":1}, {K_NAME_FOR_CONSTANT:+2.0, "z":1}, {K_NAME_FOR_CONSTANT:-1.0}]

#print_poly(poly_1, True)
#print_poly(poly_2, True)
#print_poly(poly_3, True)
#print_poly(syzygi_poly(poly_1, poly_2), True)
#print
gb = groebner_basis([poly_5, poly_6, poly_7], lex_compare)
for poly in gb:
	print_poly(poly, True)
print
gb = minimize_groebner_basis(gb, lex_compare)
for poly in gb:
	print_poly(poly, True)
print
gb = [norm(poly, lex_compare) for poly in gb]
for poly in gb:
	print_poly(poly, True)