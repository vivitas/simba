# f1 =             x^3 -           1
# f2 =       x^4 + x^3 -       x - 1
# f3 = x^5 +                   x + 1
poly1 = [-1,  0,  0,  1]
poly2 = [-1, -1,  0,  1,  1]
poly3 = [ 1,  1,  0,  0,  0,  1] 
def poly_print(poly):
	i = len(poly)-1
	first = True
	for a in poly[::-1]:
		if a!=0:
			if (first):	
				print("%d * x^%d" % (a, i)),
				first = False
			else:
				print("  +  %d * x^%d" % (a, i)),
		i -= 1
	if (first):
		print(" 0 "),
	print

def first_is_greater(a, b):
	if (len(a) != len(b)):
		return len(a) > len(b)
	for (member_a, member_b) in zip(a, b)[::-1]:
		if (member_a != member_b):
			return member_a > member_b
	return False

def same(first, second):
	if (len(first) != len (second)):
		return False
	for (x, y) in zip(first, second):
		print(x, y)
		if (x != y):
			return False
	return True

def monom(P):
    count = 0
    for i in P:
        if (i!=0):
            count += 1
    return count <= 1

def is_zero(P):
    for i in P:
        if (not i==0):
            return False
    return True

def get_degree(P):
    deg = 0
    max_deg = 0
    for i in P:
        if (not i == 0):
            max_deg = deg
        deg += 1
    return max_deg

def leading_terms_divisible(P, Q):
    deg_p = get_degree(P)
    deg_q = get_degree(Q)
    return deg_p >= deg_q

def get_leading_term(P):
    deg_p = get_degree(P)
    result = [0]*(deg_p+1)
    result[deg_p] = P[deg_p]
    return result

def create_poly_of_degree(degree):
    result = []
    for i in range(0, degree + 1):
        result.append(0)
    return result;

def monom_division(P, Q):
    deg_p = get_degree(P)
    deg_q = get_degree(Q)

    deg_r = deg_p - deg_q
    coef_r = P[deg_p]/Q[deg_q]

    result = create_poly_of_degree(deg_r)
    result[deg_r] = coef_r

    return ([0], result);

def add(P, Q):
    deg_r = max(get_degree(P), get_degree(Q))
    R = create_poly_of_degree(deg_r)
    for i in range(0, get_degree(P) + 1):
        R[i] = P[i]
    for i in range(0, get_degree(Q) + 1):
        R[i] += Q[i]
    return R

def substract(P, Q):
    deg_r = max(get_degree(P), get_degree(Q))
    R = create_poly_of_degree(deg_r)
    for i in range(0, get_degree(P) + 1):
        R[i] = P[i]
    for i in range(0, get_degree(Q) + 1):
        R[i] -= Q[i]
    return R

def multiply(P, Q):
    deg_r = get_degree(P) + get_degree(Q)
    R = create_poly_of_degree(deg_r)

    for i in range(0, get_degree(P) + 1):
        for j in range(0, get_degree(Q) + 1):
            R[i+j] += P[i] * Q[j]

    return R

def get_remainder_quotient(P, Q):
	if (monom(P) and monom(Q)):
		return monom_division(P, Q)
	B = [0]
	R = P
	while (not is_zero(R) and leading_terms_divisible(R, Q)):
		(rem, coef) = get_remainder_quotient(get_leading_term(R), get_leading_term(Q))
		B = add(coef, B)
		R = substract(R, multiply(Q, coef))
	return (B, R)

def find_gcd(first, second):
	a = first
	b = second
	if (not first_is_greater(a, b)):
		(a, b) = (b, a)
	while (not same(a, b)):
		(q, r) = get_remainder_quotient(a, b)
	return a

def main():
	poly_print(find_gcd(poly1, poly2))
	poly_print(find_gcd(poly2, poly3))
	poly_print(find_gcd(poly3, poly1))
if (__name__=='__main__'):
	main()