import pdb


def monadic_print(x):
#	pdb.set_trace()
	print(x) if (x != 'quit' and pr(x)) else 0	
	return x


#echo_FP = lambda: monadic_print(input('Enter'))=='quit' or echo_FP()
#pdb.set_trace()
#echo_FP()

def echo_IMP():
	while 1:
		x = input("Enter:")
		if x == 'quit':
			break
		else:
			print(x)
			
#echo_IMP()
#pdb.set_trace()
a1,a2,a3,a4 = set([1,2]),set([3,4]),set([11]),set([12])
def anlz(a1,a2):
	return (set([4,5,6]),set([1,2,3]))|({11},{12})
def un(a1,a2):
	return a1.union(a2)
#(a1,a2)=anlz(a1,a2)
for x in map(un,[a1,a2],[a3,a4]):
	print(x)
#print(a1)
#print(a2)