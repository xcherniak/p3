#3aeee2ffb6bdcec698011572b6bbcaf180807419
import lexer 
import ply.yacc as yacc

from cool_ast import * 


###################
# Parser for cool #
###################

tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE' , 'LPAREN' , 'RPAREN' , 'COMMA' , 'IDENTIFIER' , 'INT' , 'AT' , 'CASE' , 'CLASS' ,
 'COLON' , 'DOT' , 'ELSE' , 'EQUALS' , 'ESAC' , 'FALSE' , 'FI' , 'IF' , 'IN' , 'INHERITS' , 'ISVOID' , 'LARROW' , 'LBRACE' , 
 'LE' , 'LT' , 'LET' , 'LOOP' , 'IT' , 'NEW' , 'NOT' , 'OF' , 'POOL' , 'RARROW' , 'RBRACE' , 'SEMI' , 'STRING' , 
 'THEN' , 'TILDE' , 'TRUE' , 'TYPE' , 'WHILE' ]

def p_program(p):
    """program : class SEMI class_list"""
    p[0] = CoolProgram([p[1]] + p[3])

def p_class_list(p):
    """class_list : class SEMI class_list
                  | empty"""
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

#FIXME this is not fully accurate for Cool 
#I think this is fixed. Not completely sure.
def p_class(p):
    """class : CLASS TYPE LBRACE feature_list RBRACE
             | CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE"""
    if len(p) == 6:
        p[0] = CoolClass(CoolIdentifier(p.lineno(2), p[2]), p[4]) 
    else:
        p[0] = CoolClass(CoolIdentifier(p.lineno(2), p[2]), p[6], CoolIdentifier(p.lineno(4), p[4]))

def p_feature_list(p):
    """feature_list : feature SEMI feature_list
                    | empty"""
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

#FIXME add method declaration definiton and option attribute def
#𝙸𝙳( [ formal[[,formal]]∗ ]):𝚃𝚈𝙿𝙴 { expr }
def p_feature(p):
    """feature : IDENTIFIER COLON TYPE
               | IDENTIFIER COLON TYPE LARROW expr
               | IDENTIFIER LPAREN formal_list RPAREN COLON TYPE LBRACE expr RBRACE
               | IDENTIFIER LPAREN formal RPAREN COLON TYPE LBRACE expr RBRACE"""
    if len(p) == 4:
        p[0] = CoolAttribute(CoolIdentifier(p.lineno(1), p[1]), CoolIdentifier(p.lineno(3), p[3]))
        
    elif len(p) == 6:
        p[0] = CoolAttribute(CoolIdentifier(p.lineno(1),p[1]), CoolIdentifier(p.lineno(3), p[3]), p[5])

    else:
        p[0] = CoolMethod(CoolIdentifier(p.lineno(1),p[1]), p[3], CoolIdentifier(p.lineno(6),p[6]), p[8])

def p_formal_list(p):
    """formal_list : formal COMMA formal_list 
                   | empty"""
    
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

def p_formal(p):
    """formal : IDENTIFIER COLON TYPE"""
    p[0] = CoolFormal(CoolIdentifier(p.lineno(1),p[1]), CoolIdentifier(p.lineno(3), p[3]))



#TODO Make all of the expressions from the syntax
def p_expr_assign(p):
    """expr : IDENTIFIER LARROW expr"""
    # IDENTIFIER LARROW expr
    
    p[0] = CoolAssign(p.lineno(0),p[0] , CoolIdentifier(p.lineno(1),p[1]) , p[3] )

def p_expr_dispatch(p):
    """expr : expr DOT IDENTIFIER LPAREN expr_list RPAREN
            | expr AT TYPE DOT IDENTIFIER LPAREN expr_list RPAREN
            | IDENTIFIER LPAREN expr_list RPAREN"""
    # Dispatches

    # Dynamic
    if p[2] is 'dot':
        p[0] = CoolDispatch(p.lineno(0), p[0] , CoolIdentifier(p.lineno(3),p[3]) , p[5] )
    # Static
    if p[2] is 'at':
        p[0] = CoolDispatch(p.lineno(0), p[0] , CoolIdentifier(p.lineno(5),p[5]), p[7], p[1], CoolIdentifier(p.lineno(3),p[3]))
    #self
    if len(p) is 5 :
        p[0] = CoolDispatch(p.lineno(0), p[0] , CoolIdentifier(p.lineno(1), p[1]), p[3])

def p_expr_if(p):
    """expr : IF expr THEN expr ELSE expr FI"""
    #if 
    p[0] = CoolIf(p.lineno(0), p[0] , p[2], p[4], p[6])
    
def p_expr_while(p):
    """expr : WHILE expr LOOP expr POOL"""
    #while
    p[0] = CoolWhile(p.lineno(0), p[0] , p[2], p[4])
    
def p_expr_block(p):
    """expr : LBRACE expr_list RBRACE"""
    #Block
    p[0] = CoolBlock(p.lineno(0),p[0],p[2])

def p_expr_let(p):
    """expr : LET binding_list IN expr"""
    #let
    p[0] = CoolLet(p.lineno(0), p[2], p[4])

#This catches the arithmatic and decides how to handle it. The numbers at the end are to know symbol
def p_expr_arithmatic(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr"""
    if p[2] == 'plus':
        p[0] = CoolArithmatic(p.lineno(0),p[0],p[1],p[3],1)
   
    if p[2] == 'divide':
        p[0] = CoolArithmatic(p.lineno(0),p[0],p[1],p[3],4)

    if p[2] == 'times':
        p[0] = CoolArithmatic(p.lineno(0),p[0],p[1],p[3],3)

    if p[2] == 'minus':
        p[0] = CoolArithmatic(p.lineno(0),p[0],p[1],p[3],2)

def p_expr_identifier(p):
    """expr : IDENTIFIER"""
    p[0] = CoolExpIdentifier(p.lineno(0), p[0],CoolIdentifier(p.lineno(1),p[1]))

def p_expr_integer(p):
    """expr : INT"""
    p[0] = CoolInteger(p.lineno(0),p[0],p[1])

def p_expr_string(p):
    """expr : STRING"""
    p[0] = CoolString(p.lineno(0),p[0],p[1])

def p_expr_true(p):
    """expr : TRUE"""
    p[0] = CoolBool(p.lineno(0),p[0],p[1],0)

def p_expr_false(p):
    """expr : FALSE"""
    p[0] = CoolBool(p.lineno(0),p[0],p[1],1)

def p_expr_new(p):
    """expr : NEW TYPE"""
    p[0] = CoolNew(p.lineno(0),p[0],CoolIdentifier(p.lineno(0),p[0]))


def p_binding_list(p):
    """binding_list : binding COMMA binding_list
                    | empty"""
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] +p[3]

def p_binding(p):
    """binding : IDENTIFIER COLON TYPE
               | IDENTIFIER COLON TYPE LARROW expr"""
    if len(p) == 4:
        p[0] = CoolBinding(CoolIdentifier(p.lineno(1),p[1]) , CoolIdentifier(p.lineno(3),p[3]))
    else:
        p[0] = CoolBinding(CoolIdentifier(p.lineno(1),p[1]) , CoolIdentifier(p.lineno(3),p[3]) , p[5] )
    


def p_expr_list(p):
    """expr_list : expr SEMI expr_list
                 | empty"""    
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]




def p_empty(p):
    """empty : """
    pass

def p_error(p):
    if p is None:
        print("Unexpected End of File")
        exit(0)
    else:
        # p is the token where we have the syntax error
        print("ERROR: {}: Parser: Error on token {}".format(p.lineno,p.value))
        exit(0)


# main program
if __name__ == '__main__':
    import sys
    
    lexer = lexer.Lexer(sys.stdin)
    parser = yacc.yacc()

    program = parser.parse(lexer = lexer)

    print(program, end="")
