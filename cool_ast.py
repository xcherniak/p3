#3aeee2ffb6bdcec698011572b6bbcaf180807419
##### AST classes

class CoolProgram:
    def __init__(self, class_list):
        self.class_list = class_list

    def __repr__(self):
        ret = "{}\n".format(len(self.class_list))
        for c in self.class_list:
            ret += repr(c)
        return ret


class CoolClass:
    def __init__(self, name, feature_list , superclass=None):
        self.name = name
        self.superclass = superclass
        self.feature_list = feature_list

    def __repr__(self):
        ret = repr(self.name)
        if self.superclass is None:
            ret += "no_inherits\n"
        else:
            ret += "inherits\n{}".format(repr(self.superclass))
        ret += "{}\n{}".format(
            len(self.feature_list),
            #list comprehension (map)
            "".join([repr(f) for f in self.feature_list])
        )
        return ret

class CoolIdentifier:
    def __init__(self, lineno, name):
        self.lineno = lineno
        self.name = name

    def __repr__(self):
        #output lineno
        #then the identifier as a string
        return "{}\n{}\n".format(self.lineno,self.name)

class CoolAttribute:
    def __init__(self,name, typ, init=None):
        self.name = name
        self.typ = typ
        self.init = init

    def __repr__(self):
        if self.init is None:
            #No initializer
            return "attribute_no_init\n{}{}".format(repr(self.name),repr(self.typ))
        else:
            #With Initializer
            #attribute_init \n name:identifier type:identifier init:exp
            return "attribute_init\n{}{}{}".format(repr(self.name),repr(self.typ),repr(self.init))

class CoolMethod:
    def __init__(self, name, formal_list, typ, expr  ):
        self.name = name
        self.typ = typ
        self.expr = expr
        self.formal_list = formal_list

    def __repr__(self):
        #method \n name:identifier formals-list \n type: identifier body:exp
        ret = "{}\n".format(len(self.formal_list))
        for c in len(self.formal_list):
            ret += repr(c)
        
        return "method\n{}{}\n{}{}".format(repr(self.name),ret,repr(self.typ),repr(self.expr))


class CoolFormal:
    def __init__(self,name, typ):
        self.name = name
        self.typ = typ

    #Output the name as an identifier on a line and then the type as an identifier on a line.
    def __repr__(self):
        return "{}\n{}\n".format(repr(self.name),repr(self.typ))

#Output the line number of the expression and then a newline. Output the name of the expression and 
#then a newline and then any subparts, as given below
class CoolAssign:
    def __init__(self, lineno, name, var, rhs):
        self.lineno= lineno
        self.name= name
        self.var = var
        self.rhs = rhs

    def __repr__(self):
        return "{}\n{}\nassign\n{}{}".format(self.lineno,self.name,repr(self.var),repr(self.rhs))

class CoolDispatch:
    def __init__(self, lineno, name, method, args, e = None, typ = None):
        self.lineno = lineno
        self.name = name
        self.method = method
        self.args = args
        self.e = e
        self.typ = typ

    def __repr__(self):
        ret = "{}\n".format(len(self.args))


        for c in len(self.args):
            ret += repr(c)

        if self.e == None:
            return "{}\n{}\nself_dispatch\n{}{}".format(self.lineno, self.name,repr(self.method),ret)

        elif self.typ != None:
            return "{}\n{}\nstatic_dispatch\n{}{}{}{}".format(self.lineno,self.name,repr(self.e),repr(self.typ),repr(self.method),ret)

        else:
            return "{}\n{}\ndynamic_dispatch\n{}{}{}".format(self.lineno,self.name,repr(self.e),repr(self.method),ret)

class CoolIf:
    def __init__(self, lineno, name, predicate, then, els):
        self.lineno = lineno
        self.name = name
        self.predicate = predicate
        self.then = then
        self.els = els

    def __repr__(self):
        return "{}\n{}\nif\n{}{}{}".format(self.lineno, self.name, repr(self.predicate), repr(self.then), repr(self.els))

class CoolWhile:
    def __init__(self, lineno, name, predicate, body):
        self.lineno= lineno
        self.name = name
        self.predicate = predicate
        self.body = body

    def __repr__(self):
        return "{}\n{}\nwhile\n{}{}".format(self.lineno, self.name, repr(self.predicate), repr(self.body))

class CoolBlock:
    def __init__(self, lineno, name, body):
        self.lineno = lineno
        self.name = name
        self.body = body

    def __repr__(self):
        ret = "{}\n".format(len(self.body))
        for c in len(self.body):
            ret += repr(c)
        return "{}\n{}\nblock\n{}".format(self.lineno, self.name, ret)

class CoolLet:
    def __init__(self, lineno, binding , expr):
        self.lineno = lineno
        self.binding = binding
        self.expr = expr

    def __repr__(self):
        ret = ""
        for c in len(self.binding):
            ret += repr(c)
        
        return "{}\nlet\n{}{}".format(self.lineno,ret, repr(self.expr))

class CoolBinding:
    def __init__(self,variable, typ, value= None):
        self.variable = variable
        self.typ = typ
        self.value = value

    def __repr__(self):
        if self.value != None:
            return "let_binding_init\n{}{}{}".format(self.variable,self.typ,self.value)
        else:
            return "let_binding_no_init\n{}{}".format(self.variable,self.typ)

class CoolArithmatic:
    def __init__(self,lineno, name, x, y, sign):
        self.lineno = lineno
        self.name = name
        self.x = x
        self.y = y
        self.sign = sign

    def __repr__(self):
        if self.sign == 0:
            ret = "plus"
        
        if self.sign == 1:
            ret = "minus"

        if self.sign == 2:
            ret = "times"

        if self.sign == 3:
            ret = "divide"

        return "{}\n{}\n{}\n{}{}".format(self.lineno,self.name,ret,repr(self.x),repr(self.y))

class CoolExpIdentifier:
    def __init__(self,lineno, name, var):
        self.lineno = lineno
        self.name = name
        self.var = var

    def __repr__(self):
        return "{}\n{}\nidentifier\n{}".format(self.lineno, self.name,repr(self.var))

class CoolInteger:
    def __init__(self,lineno, name, theInt):
        self.lineno = lineno
        self.name = name
        self.theInt = theInt

    def __repr__(self):
        return "{}\n{}\ninteger\n{}\n".format(self.lineno,self.name,self.theInt)

class CoolString:
    def __init__(self,lineno, name, theString):
        self.lineno = lineno
        self.name= name
        self.theString = theString

    def __repr__(self):
        return "{}\n{}\nstring\n{}\n".format(self.lineno, self.name, self.theString)

class CoolBool:
    def __init__(self,lineno, name, bol, num):
        self.lineno = lineno
        self.name = name
        self.bol = bol
        self.num = num

    def __repr__(self):
        if self.num == 0:
            ret = "true"
        
        if self.num == 1:
            ret = "false"

        return "{}\n{}\n{}\n".format(self.lineno, self.name, ret)

class CoolNew:
    def __init__(self, lineno,name,clas):
        self.lineno=lineno
        self.name=name
        self.clas = clas

    def __repr__(self):
        return "{}\n{}\nnew\n{}".format(self.lineno,self.name,repr(self.clas))
