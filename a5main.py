import sys
import tpg
import pdb

class AnalError(Exception):
    """Class of exceptions raised when an error occurs during analysis."""

# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes."""

    # For each class of nodes, store names of the fields for children nodes.
    fields = []

    def __init__(self, *args):
        """Populate fields named in "fields" with values in *args."""
        assert(len(self.fields) == len(args))
        for f, a in zip(self.fields, args): setattr(self, f, a)

# subclasses of Node for expressions

class Var(Node):
    """Class of nodes representing accesses of variable."""
    fields = ['name']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        if self.name not in global_var_env | local_var_env:
            print('Use of undeclared variable')
        print('Use of variable ',self.name)
class Int(Node):
    """Class of nodes representing integer literals."""
    fields = ['value']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):pass
class String(Node):
    """Class of nodes representing string literals."""
    fields = ['value']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):pass
class Array(Node):
    """Class of nodes representing array literals."""
    fields = ['elements']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        for e in self.elements:
            e.anlz_vars(local_var_env,is_global)
class Index(Node):
    """Class of nodes representing indexed accesses of arrays or strings."""
    fields = ['indexable', 'index']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        self.indexable.anlz_vars(local_var_env,is_global)
        self.index.anlz_vars(local_var_env,is_global)
class BinOpExp(Node):
    """Class of nodes representing binary-operation expressions."""
    fields = ['left', 'op', 'right']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        self.left.anlz_vars(local_var_env,is_global)
        self.right.anlz_vars(local_var_env,is_global)
class UniOpExp(Node):
    """Class of nodes representing unary-operation expressions."""
    fields = ['op', 'arg']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        self.arg.anlz_vars(local_var_env,is_global)
# subclasses of Node for statements

class Print(Node):
    """Class of nodes representing print statements."""
    fields = ['exp']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        self.exp.anlz_vars(local_var_env,is_global)
class Assign(Node):
    """Class of nodes representing assignment statements."""
    fields = ['left', 'right']
    def anlz_procs(self):
        pass    
    def anlz_procs_called(self):pass
    def anlz_vars(self,local_var_env,is_global):
        self.right.anlz_vars(local_var_env,is_global)
        if isinstance(self.left,Var):
            if is_global: global_var_env.add(self.left.name)
            else: local_var_env.add(self.left.name)
            print('Definition of variable ',self.left.name)
            if not is_global and self.left.name in global_var_env:
                print('Shadowing of global variable', self.left.name)
        if isinstance(self.left,Index):
            self.left.anlz_vars(local_var_env,is_global)
            
class Block(Node):
    """Class of nodes representing block statements."""
    fields = ['stmts']
    def anlz_procs(self):
        for s in self.stmts:
    	    s.anlz_procs()
    def anlz_procs_called(self):
        for s in self.stmts:
            s.anlz_procs_called()
    def anlz_vars(self,local_var_env,is_global):
        for s in self.stmts:
            s.anlz_vars(local_var_env,is_global)
class If(Node):
    """Class of nodes representing if statements."""
    fields = ['exp', 'stmt']
    def anlz_procs(self):
        self.stmt.anlz_procs()
    def anlz_procs_called(self):
        self.stmt.anlz_procs_called()
    def anlz_vars(self,local_var_env,is_global):
        self.exp.anlz_vars(local_var_env,is_global)
        self.stmt.anlz_vars(local_var_env,is_global)
class While(Node):
    """Class of nodes representing while statements."""
    fields = ['exp', 'stmt']
    def anlz_procs(self):
    	self.stmt.anlz_procs()
    def anlz_procs_called(self):
        self.stmt.anlz_procs_called()
    def anlz_vars(self,local_var_env,is_global):
        self.exp.anlz_vars(local_var_env,is_global)
        self.stmt.anlz_vars(local_var_env,is_global)
class Def(Node):
    """Class of nodes representing procedure definitions."""
    fields = ['name', 'params', 'body']
    def anlz_procs(self):
        if self.name in procs_defined:
        	print('method already defined!')
        print('Definition of procedure',self.name)
        procs_defined.add(self.name)
        self.body.anlz_procs()
    def anlz_procs_called(self):
        self.body.anlz_procs_called()
    def anlz_vars(self,local_var_env,is_global):
        new_local_var_env = set(self.params)
        print('Locals of procedure', self.name+':', ', '.join(self.params))
        for v in new_local_var_env & global_var_env:
            print('Shadowing of global variable',v)
        self.body.anlz_vars(new_local_var_env,False)
class Call(Node):
    """Class of nodes representing precedure calls."""
    fields = ['name', 'args']
    def anlz_procs(self):
        pass
    def anlz_procs_called(self):
        print('Call of procedure ',self.name)
        procs_called.add(self.name)
    def anlz_vars(self,local_var_env,is_global):
        for a in self.args:
            a.anlz_vars(local_var_env,is_global)
class Parser(tpg.Parser):
    r"""
    token int:         '\d+' ;
    token string:      '\"[^\"]*\"' ;
    token ident:       '[a-zA-Z_][\w]*' ;
    separator spaces:  '\s+' ;
    separator comment: '#.*' ;

    START/s -> Stmt/s ;

    Stmt/s ->
    ( 'print' Exp/e ';'  $s = Print(e)$
    | Exp/l '=(?!=)' Exp/r ';'  $ s = Assign(l, r) $
    | '\{'  $ s=[] $  ( Stmt/s2  $ s.append(s2) $  )* '\}'  $s = Block(s)$
    | 'if' '\(' Exp/e '\)' Stmt/s  $ s = If(e, s) $
    | 'while' '\(' Exp/e '\)' Stmt/s  $ s = While(e, s) $
    | 'def' ident/f '\('  $l=[]$  ( ident/i  $l.append(i)$
                                    ( ',' ident/i  $l.append(i)$  )*)? '\)'
      Stmt/s2  $s=Def(f,l,s2)$
    | ident/f '\('  $l=[]$  ( Exp/e  $l.append(e)$
                              ( ',' Exp/e  $l.append(e)$  )*)? '\)' ';'
      $s=Call(f,l)$
    ) ;

    Exp/e -> Or/e ;
    Or/e  -> And/e ( 'or'  And/e2  $e=BinOpExp(e,'or', e2)$  )* ;
    And/e -> Not/e ( 'and' Not/e2  $e=BinOpExp(e,'and',e2)$  )* ;
    Not/e -> 'not' Not/e  $e=UniOpExp('not', e)$  | Cmp/e ;
    Cmp/e -> Add/e ( CmpOp Add/e2  $e=BinOpExp(e,CmpOp,e2)$  )* ;
    Add/e -> Mul/e ( AddOp Mul/e2  $e=BinOpExp(e,AddOp,e2)$  )* ; 
    Mul/e -> Index/e ( MulOp Index/e2  $e=BinOpExp(e,MulOp,e2)$  )* ;
    Index/e -> Atom/e ( '\[' Exp/e2 '\]'  $e=Index(e,e2)$  )* ;
    Atom/e -> '\(' Exp/e '\)'
    | int/i     $e=Int(int(i))$
    | string/s  $e=String(s[1:-1])$
    | '\['  $e=[]$  ( Exp  $e.append(Exp)$  ( ',' Exp  $e.append(Exp)$  )*)?
      '\]'  $e=Array(e)$
    | ident     $e=Var(ident)$
    ;
    CmpOp/r -> '=='/r | '<'/r | '>'/r ;
    AddOp/r -> '\+'/r | '-'/r ;
    MulOp/r -> '\*'/r | '/'/r ;
    """

def parse(code):
    # This makes a parser object, which acts as a parsing function.
    parser = Parser()
    return parser(code)


def anlz_procs_imp(node):
    """Analyze procedure definitions and calls."""
    if isinstance(node, (Print, Assign)): pass
    elif isinstance(node, Block):
        for s in node.stmts: anlz_procs_imp(s)
    elif isinstance(node, (If, While)):
        anlz_procs_imp(node.stmt)
    elif isinstance(node, Def):
        if node.name in proc_defined: 
        	try:
        		raise AnalError()
        	except AnalError:
        		print('Error4')
        print('Definition of procedure', node.name)
        proc_defined.add(node.name)
        anlz_procs_imp(node.body)
    elif isinstance(node, Call):
        print('Call of procedure', node.name)
        proc_called.add(node.name)
    else: 
    	try:
    		raise Exception("Not implemented.")
    	except Exception:
    		print('Oops! analysis error.')
    
def anlz_procs_fun(node,procs_defined,procs_called):
	if isinstance(node,(Print,Assign)):
		return set(),set()
	elif isinstance(node,Block):
		return a_block_p_fun(node,procs_defined,procs_called,0)
	elif isinstance(node,(If,While)):
		return anlz_procs_fun(node.stmt,procs_defined,procs_called)
	elif isinstance(node,Def):
		return a_def_p_fun(node,procs_defined,procs_called)
	elif isinstance(node,Call):
		return a_call_p_fun(node,procs_defined,procs_called)
	else:
		return set(),set()
		
def a_block_p_fun(node,procs_defined,procs_called,x):
	if x == len(node.stmts):
		return set(),set()
	else:
		a,b=anlz_procs_fun(node.stmts[x],procs_defined,procs_called) 
		c,d = a_block_p_fun(node,procs_defined,procs_called,x+1)
		return a|c,b|d

def a_def_p_fun(node,procs_defined,procs_called):
	if node.name in procs_defined: print('Error2')
	print('Definition of procedure',node.name)
	return set([node.name]) | anlz_procs_fun(node.body,procs_defined,procs_called)[0],procs_called


def a_call_p_fun(node,procs_defined,procs_called):
	print('Call of procedure', node.name)
	return procs_defined,procs_called | set([node.name])

def anlz_vars_imp(node, local_var_env, is_global):
    """Analyze variable definitions and uses."""
    if isinstance(node, Var):
        if node.name not in local_var_env | global_var_env: print('Error3')
        print('Use of variable', node.name)
    elif isinstance(node, (Int, String)): pass
    elif isinstance(node, Array):
        for e in node.elements: anlz_vars_imp(e, local_var_env, is_global)
    elif isinstance(node, Index):
        anlz_vars_imp(node.indexable, local_var_env, is_global)
        anlz_vars_imp(node.index, local_var_env, is_global)
    elif isinstance(node, BinOpExp):
        anlz_vars_imp(node.left, local_var_env, is_global)
        anlz_vars_imp(node.right, local_var_env, is_global)
    elif isinstance(node, UniOpExp):
        anlz_vars_imp(node.arg, local_var_env, is_global)
    elif isinstance(node, Print):
        anlz_vars_imp(node.exp, local_var_env, is_global)
    elif isinstance(node, Assign):
        anlz_vars_imp(node.right, local_var_env, is_global)
        if isinstance(node.left, Var):
            if is_global: global_var_env.add(node.left.name)
            else: local_var_env.add(node.left.name)
            print('Definition of variable', node.left.name)
            if not is_global and node.left.name in global_var_env:
                print('Shadowing of global variable', node.left.name)
        if isinstance(node.left, Index):
            anlz_vars_imp(node.left, local_var_env, is_global)
    elif isinstance(node, Block):
        for s in node.stmts: anlz_vars_imp(s, local_var_env, is_global)
    elif isinstance(node, (If, While)):
        anlz_vars_imp(node.exp, local_var_env, is_global)
        anlz_vars_imp(node.stmt, local_var_env, is_global)
    elif isinstance(node, Def):
        new_local_var_env = set(node.params)
        print('Locals of procedure', node.name+':', ', '.join(node.params))
        for v in new_local_var_env & global_var_env:
        #& is intersection | is union of sets y = set(iterable)
            print('Shadowing of global variable', v)
        anlz_vars_imp(node.body, new_local_var_env, False)
    elif isinstance(node, Call):
        for a in node.args: anlz_vars_imp(a, local_var_env, is_global)
    else: 
    	try:
    		raise Exception("Not implemented.!")
    	except Exception:
    		print('Oops. that is not supported@')
	
def anlz_vars_fun(node,global_var_env,local_var_env,is_global):
	if isinstance(node,Var):
		if node.name not in global_var_env | local_var_env:print('Error1')
		print('Use of variable ',node.name)
		return set(),set()
	elif isinstance(node,(Int,String)):
		return set(),set()
	elif isinstance(node,Array):
		return a_array_v_f(node,global_var_env,local_var_env,is_global,0)
	elif isinstance(node, Index):
		a,b=anlz_vars_fun(node.indexable,global_var_env,local_var_env,is_global)
		c,d=anlz_vars_fun(node.index,global_var_env,local_var_env,is_global)
		return a|c,b|d
	elif isinstance(node, BinOpExp):
		a,b=anlz_vars_fun(node.left,global_var_env,local_var_env,is_global)
		c,d=anlz_vars_fun(node.right,global_var_env,local_var_env,is_global)
		return a|c,b|d
	elif isinstance(node, UniOpExp):
		return anlz_vars_fun(node.arg,global_var_env,local_var_env,is_global)
	elif isinstance(node,Print):
		return anlz_vars_fun(node.exp,global_var_env,local_var_env,is_global)
	elif isinstance(node,Assign):
		#pdb.set_trace()
		a,b = anlz_vars_fun(node.right,global_var_env,local_var_env,is_global)
		if isinstance(node.left,Var):
			print('Definition of variable', node.left.name)
			if not is_global and node.left.name in global_var_env:
				print('Shadowing of global variable', node.left.name)
			if is_global:
				return a|{node.left.name}, b
			else:
				return a,b|{node.left.name}
		elif isinstance(node.left,Index):
			c,d = anlz_vars_fun(node.left,global_var_env,local_var_env,is_global)
			if is_global:
				return a|c, b|d
			else:
				return a|c,b|d
	elif isinstance(node,Block):
		return a_block_v_f(node,global_var_env,local_var_env,is_global,0)
	elif isinstance(node,(If,While)):
		a,b = anlz_vars_fun(node.exp,global_var_env,local_var_env,is_global)
		c,d = anlz_vars_fun(node.stmt,global_var_env,local_var_env,is_global)
		return a|c,b|d
	elif isinstance(node,Def):
		#pdb.set_trace()
		new_local_var_env = set(node.params)
		print('Locals of procedure',node.name+':',', '.join(node.params))
		a_def_v_p(new_local_var_env&global_var_env,0)
		return anlz_vars_fun(node.body,global_var_env,new_local_var_env|set(node.params),False)
	elif isinstance(node,Call):
		return a_call_v_p(node,global_var_env,local_var_env,is_global,0)
	else:print('Error7')
			
def a_call_v_p(node,global_var_env,local_var_env,is_global,x):
	if x == len(node.args):
		return set(),set()
	else:
		a,b = anlz_vars_fun(node.args[x],global_var_env,local_var_env,is_global)
		c,d = a_call_v_p(node,global_var_env,local_var_env,is_global,x+1)
		return a|c,b|d
	
def a_def_v_p(a,x):
	if x == len(a):
		return
	else:
		print('Shadowing of global variable',a[x])
		a_def_v_p(a,x+1)
def a_block_v_f(node,global_var_env,local_var_env,is_global,x):
	if x == len(node.stmts):
		return set(),set()
	else:
		a,b = anlz_vars_fun(node.stmts[x],global_var_env,local_var_env,is_global)
		c,d = a_block_v_f(node,a|global_var_env,b|local_var_env,is_global,x+1)
		return a|c,b|d
	
def a_array_v_f(node,global_var_env,local_var_env,is_global,x):
	if x == len(node.elements):
		return set(),set()
	else:
		a,b = anlz_vars_fun(node.elements[x],global_var_env,local_var_env,is_global)
		c,d= a_array_v_f(node,global_var_env|a,b|local_var_env,is_global,x+1)
		return a|c,b|d
		
# Below is the driver code, which parses a given MustScript program
# and analyzes the definitions and uses of procedures and variables

# Open the input file, and read in the input program.
prog = open(sys.argv[1]).read()

try:
    # Try to parse the program.
    print('Parsing...')
    node = parse(prog)

    # Try to analyze the program.
    print('Analyzing...')

    # set up and call method for analyzing procedures (imperative)
    proc_defined, proc_called = set(), set()
    anlz_procs_imp(node)
    if {p for p in proc_called if p not in proc_defined}:
    	#A call to procedure p but not defined, thus dictionary {} not empty returns true
        try:
            raise AnalError('containing call to undefined procedure')
        except AnalError:
             print('Error8')
    if {p for p in proc_defined if p not in proc_called}: # bonus dead code
        try:
            raise AnalError('containing definition of not-called procedure')
        except AnalError:
    	    print('Error9')

    # set up and call method for analyzing variables (imperative)
    global_var_env, local_var_env, is_global = set(), set(), True
    anlz_vars_imp(node, local_var_env, is_global)

    # set up and call method for analyzing procedures (functional)
    #pdb.set_trace()
    procs_defined,procs_called = set(),set()
    procs_defined,procs_called = anlz_procs_fun(node,procs_defined,procs_called)
    if {p for p in procs_called if p not in procs_defined}:
    	try:
    		raise AnalError('Call to undefined procedure')
    	except AnalError:
    		print('Errorrr')
    
    global_var_env, local_var_env, is_global = set(),set(),True
    global_var_env,local_var_env = anlz_vars_fun(node,global_var_env,local_var_env,is_global)

    
    # set up and call method for analyzing variables (functional)
    # your methods could be named anlz_procs_fun and anlz_vars_fun 
	
	
    # set up and call method for analyzing procedures (object-oriented):
    procs_defined,procs_called = set(),set()
    node.anlz_procs()
    node.anlz_procs_called()
    if {p for p in proc_called if p not in proc_defined}:
        print('call to undefined proc')
    global_var_env, local_var_env, is_global = set(),set(),True
    node.anlz_vars(local_var_env,True)
    # set up and call method for analyzing variables (object-oriented):
    # your methods could be named anlz_procs_obj and anlz_vars_obj

# If an exception is rasied, print the appropriate error.
except tpg.Error:
    print('Parsing Error')

    # Uncomment the next line to re-raise the parsing error,
    # displaying where the error occurs.  Comment it for submission.

    # raise

except AnalError as e:
    print('Analysis Error')

    # Uncomment the next line to re-raise the evaluation error, 
    # displaying where the error occurs.  Comment it for submission.

    raise
