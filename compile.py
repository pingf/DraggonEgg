#coding=utf-8
#Author : 大M君 →_→  2013 the snake year
#License Type: The MIT License (MIT)
#Copyright (c) <2013> <Fanchao-Meng>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import lex,yacc
import re
fout=None
tokens = (
    'COMMA','COLON','SEMICOLON','LPAREN','RPAREN','LBRACE','RBRACE',
    'IDENTIFIER','NUMBER','STRING','AT','DOLLAR', 
    'FUNCTION','IF','ELSE','WHILE','RETURN',
    'PLUS','MINUS','TIMES','DIV','ASSIGN',
    'GREATER','LESS','EQ','NOT_EQ','GREATER_EQ','LESS_EQ',
    'COMMENT',
    )
t_COMMA = r','
#t_COLON = r':'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
#t_LBRACKET = r'\['
#t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_EQ = r'=='
t_NOT_EQ = r'!='
t_GREATER_EQ = r'>='
t_LESS_EQ = r'<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_AT = r'\@'
t_DOLLAR = r'\$'
t_DIV = r'/(?!\*)'
reserved_words = { 
    'while' : 'WHILE', 
    'break' : 'BREAK','continue' : 'CONTINUE',  
    'if' : 'IF',  'else' : 'ELSE',  
    'goto' : 'GOTO', 
    'function' : 'FUNCTION', 'return' : 'RETURN',    
}

def t_IDENTIFIER(t):
    r'[A-Za-z_][\w]*'
    if reserved_words.has_key(t.value):
        t.type = reserved_words[t.value]
    return t 
def t_NUMBER(t):
    r'0(?!\d)|([1-9]\d*)'
    return t
def t_STRING(t):
    r'"[^\n]*?(?<!\\)"'
    temp_str = t.value.replace(r'\\', '')
    m = re.search(r'\\[^n"]', temp_str)
    if m != None:
        print >>fout,  "string none detected"
        return
    return t
def t_WHITESPACE(t):
    r'[ \t]+'
    pass
def t_NEWLINE(t):
    r'\n+'
    t.lineno += len(t.value)
def t_COMMENT(t):
    r'/\*[\w\W]*?\*/'
    t.lineno += t.value.count('\n')
    pass
def t_error(p):
    print >>fout,  "error"
    pass

class Node(object):
    def __init__(self, parent=None): 
        self.parent = parent  
        self.name = None
        self.value = None
        self.type = None 
    def accept(self, visitor):  
        return self._accept(self.__class__, visitor) 
    def _accept(self, klass, visitor):  
        visitor_method = getattr(visitor,"visit%s" % klass.__name__,None)
        if visitor_method == None:
            bases = klass.__bases__
            last = None
            for i in bases:
                last = self._accept(i, visitor)
            return last
        else:
            return visitor_method(self) 

class ListNode(Node): 
    def __init__(self, node=None):
        super(ListNode, self).__init__()
        #Node.__init__(self, None)
        self.nodes = []
        if node != None:
            self.add(node)

    def add(self, node):
        self.nodes.append(node)

def p_program(p):
    '''program :  function_list'''
    p[0]=p[1] 
      
class FunctionListNode(ListNode): 
    def __init__(self,node):
        super(FunctionListNode, self).__init__(node)  
        self.type="FunctionList" 
def p_function_list_01(p):
    '''function_list : function_definition ''' 
    p[0]=FunctionListNode(p[1]) 
     
def p_function_list_02(p):
    '''function_list : function_list function_definition   '''  
    p[1].add(p[2])
    p[0]=p[1] 
     
class FunctionDefinitionNode(Node): 
    def __init__(self,name,l,st):
        super(self.__class__, self).__init__()
        self.type="FunctionDefinition" 
        self.name=name
        self.parameters=l
        self.statements=st
def p_function_definition(p):
    '''function_definition : FUNCTION IDENTIFIER LPAREN parameter_list RPAREN compound_statement ''' 
    p[0]=FunctionDefinitionNode(p[2],p[4],p[6]) 
     
class ParameterListNode(ListNode): 
    def __init__(self,node=None):
        super(self.__class__, self).__init__(node)  
        self.type="ParameterList"
def p_parameter_list_01(p):
    '''parameter_list : IDENTIFIER'''
    p[0]=ParameterListNode(IdentifierNode(p[1]))
     
def p_parameter_list_02(p):
    '''parameter_list : parameter_list COMMA IDENTIFIER'''
    p[1].add(IdentifierNode(p[3]))
    p[0]=p[1]  
def p_parameter_list_03(p):
    '''parameter_list : '''
    p[0]=ParameterListNode()
     
class ArgumentListNode(ListNode): 
    def __init__(self,node=None):
        super(self.__class__, self).__init__(node) 
        self.type="ArgumentList" 
def p_argument_list_01(p):
    '''argument_list : expression '''
    p[0]=ArgumentListNode(p[1])
     
def p_argument_list_02(p):
    '''argument_list : argument_list COMMA expression''' 
    p[1].add(p[3])
    p[0]=p[1] 
     
def p_argument_list_03(p):
    '''argument_list :  ''' 
    p[0]=ArgumentListNode()
     
class StatementListNode(ListNode): 
    def __init__(self,node=None):
        super(StatementListNode, self).__init__(node) 
        self.type="StatementList"
def p_statement_list_01(p):
    '''statement_list : statement'''
    p[0]=StatementListNode(p[1])
     
def p_statement_list_02(p):
    '''statement_list : statement_list statement  ''' 
    p[1].add(p[2])
    p[0]=p[1] 
       
def p_statement_list_03(p):
    '''statement_list : ''' 
    p[0]=StatementListNode()

#class StatementNode(ListNode): 
#    def __init__(self):
#        super(self.__class__, self).__init__() 
#        self.type="Statement"
#oops no statement node for it's abstract
def p_statement_01(p):
    '''statement : assignement_statement ''' 
    p[0]=p[1]    
def p_statement_02(p):
    '''statement : function_call_statement SEMICOLON'''
    p[0]=p[1]
def p_statement_03(p):
    '''statement : if_statement '''
    p[0]=p[1]
def p_statement_04(p):
    '''statement : while_statement'''
    p[0]=p[1]
def p_statement_05(p):
    '''statement : return_statement SEMICOLON'''
    p[0]=p[1]
def p_statement_06(p):
    '''statement : compound_statement'''
    p[0]=p[1]
     
class AssignStatementNode(Node): 
    def __init__(self,n,d,t):
        super(self.__class__, self).__init__()
        self.type="AssignStatement"
        self.name=n
        self.data=d
        self.subtype=t
def p_assignement_statement_01(p):
    '''assignement_statement : IDENTIFIER ASSIGN expression SEMICOLON '''
    p[0]=AssignStatementNode(p[1],p[3],"normal")
def p_assignement_statement_02(p):
    '''assignement_statement : LESS IDENTIFIER ASSIGN expression SEMICOLON '''
    p[0]=AssignStatementNode(p[2],p[4],"left")
def p_assignement_statement_03(p):
    '''assignement_statement : GREATER IDENTIFIER ASSIGN expression SEMICOLON '''
    p[0]=AssignStatementNode(p[2],p[4],"right")     
def p_assignement_statement_04(p):
    '''assignement_statement : IDENTIFIER ASSIGN STRING SEMICOLON '''
    p[0]=AssignStatementNode(p[1],StringNode(p[3]),"string")    
     
class FunctionCallStatementNode(Node): 
    def __init__(self,name,l):
        super(self.__class__, self).__init__()
        self.type="FunctionCallStatement"
        self.name=name
        self.argument_list=l 
def p_function_call_statement(p):
    '''function_call_statement : IDENTIFIER LPAREN argument_list RPAREN '''
    p[0]=FunctionCallStatementNode(p[1],p[3])  
      
class TrueFalseNode(Node):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.type="TrueFalse" 

class IfStatementNode(Node): 
    def __init__(self,e,true,false=None):
        super(self.__class__, self).__init__()
        self.type="FunctionCallStatement" 
        self.expression=e
        self.true=true  
        if false!=None:
            self.false=false
        else:
            self.false=TrueFalseNode()

def p_if_statement_01(p):
    '''if_statement : IF LPAREN expression RPAREN compound_statement ELSE compound_statement'''
    p[0]=IfStatementNode(p[3],p[5],p[7])  
def p_if_statement_02(p):
    '''if_statement : IF LPAREN expression RPAREN compound_statement'''
    p[0]=IfStatementNode(p[3],p[5])  
     
class WhileStatementNode(Node): 
    def __init__(self,e,true,false=None):
        super(self.__class__, self).__init__()
        self.type="FunctionCallStatement" 
        self.expression=e
        self.true=true  
        if false!=None:
            self.false=false
        else:
            self.false=TrueFalseNode()
def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN compound_statement'''
    p[0]=WhileStatementNode(p[3],p[5])  
     
class ReturnStatementNode(Node): 
    def __init__(self,e):
        super(self.__class__, self).__init__()
        self.type="ReturnStatement" 
        self.expression=e 
def p_return_statement(p):
    '''return_statement : RETURN expression''' 
    p[0]= ReturnStatementNode(p[2])  
     
class CompoundStatementNode(Node): 
    def __init__(self,l):
        super(self.__class__, self).__init__()
        self.type="FunctionCallStatement" 
        self.compound_list=l     
def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE''' 
    p[0]= CompoundStatementNode(p[2])  
     
precedence = ( 
    ('left','RPAREN'),
    ('left','COMMA'),
    ('left','LESS','GREATER','EQ','NOT_EQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV'),
    ('left','LPAREN') , 
    #('right','UMINUS'),
    )
 
class ExpressionNode(Node): 
    def __init__(self, l,op=None,r=None):
        super(self.__class__, self).__init__()  
        self.type="Expression"
        if op!=None:
            self.subtype="lor"
            self.left=l
            self.op=op
            self.right=r
        else:
            self.subtype="data"
            self.data=l 
        
def p_expression_01(p):
    '''expression : NUMBER'''
    p[0]=ExpressionNode(NumberNode(p[1])) 
def p_expression_02(p):
    '''expression : function_call_statement'''
    p[0]=ExpressionNode(p[1]) 
def p_expression_03(p):
    '''expression : IDENTIFIER'''
    p[0]=ExpressionNode(IdentifierNode(p[1])) 
def p_expression_04(p):
    '''expression : left_identifier'''
    p[0]=ExpressionNode(p[1]) 
def p_expression_05(p):
    '''expression : right_identifier'''
    p[0]=ExpressionNode(p[1]) 
def p_expression_06(p):
    '''expression : specific_identifier'''
    p[0]=ExpressionNode(p[1]) 
def p_expression_07(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIV expression
                | expression LESS expression
                | expression GREATER expression
                | expression EQ expression
                | expression NOT_EQ expression
                | expression GREATER_EQ expression
                | expression LESS_EQ expression''' 
    p[0]=ExpressionNode(p[1],p[2],p[3])
def p_expression_08(p):
    '''expression : LPAREN expression RPAREN''' 
    p[0]=p[2]
     
class LeftIdentifierNode(Node):
    """A list of nodes.  This is an abstract base class.""" 
    def __init__(self,n):
        super(Node, self).__init__()  
        self.type="LeftIdentifier" 
        self.name=n
def p_left_identifier(p):
    '''left_identifier : LESS IDENTIFIER'''
    p[0]=LeftIdentifierNode(p[2])
     
class RightIdentifierNode(Node):
    """A list of nodes.  This is an abstract base class.""" 
    def __init__(self,n):
        super(Node, self).__init__()  
        self.type="RightIdentifier" 
        self.name=n 
def p_right_identifier(p):
    '''right_identifier : GREATER IDENTIFIER'''
    p[0]=RightIdentifierNode(p[2])
      
class SpecificIdentifierNode(Node): 
    def __init__(self,n):
        super(Node, self).__init__()  
        self.type="SpecificIdentifier" 
        self.name=n
def p_specific_identifier(p):  
    '''specific_identifier : AT 
                           | DOLLAR'''
    p[0]=SpecificIdentifierNode(p[1])
     
class StringNode(Node):
    """A list of nodes.  This is an abstract base class.""" 
    def __init__(self,s):
        super(self.__class__, self).__init__()  
        self.type="String" 
        self.value=s

class NumberNode(Node): 
    def __init__(self,v):
        super(self.__class__, self).__init__()  
        self.type="Number" 
        self.value=v
class IdentifierNode(Node): 
    def __init__(self,n):
        super(self.__class__, self).__init__()  
        self.type="Identifier" 
        self.name=n
        
def p_error(p):
    print >>fout,  "error" 
    #yacc.errok()

class Visitor:  
    def __init__(self):
        self.warnings = 0
        self.errors = 0
    def _visitList(self, l): 
        last = None
        for i in l:
            last = i.accept(self)
        return last
    def visit(self, node): 
        return node.accept(self)
    def warning(self, str):  
        print >>fout,  "warning: %s" % str
        self.warnings += 1
    def error(self, str): 
        print >>fout,  "error: %s" % str
        self.errors += 1
    def has_errors(self): 
        return self.errors > 0
    
class CommentNode(Node): 
    def __init__(self,str):
        super(CommentNode, self).__init__()  
        self.type="Comment"
        self.str=str 
def p_comment(p):
    '''comment :  COMMENT'''
    p[0]=CommentNode(p[1])
    
class SymbolTable(object): 
    def __init__(self, parent=None): 
        self.entries = {}
        self.pal=[]
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []
    def add(self, name, value): 
        if self.get(name) == None:
            self.pal.append(name) 
        self.entries[name] = value
    def get(self, name): 
        if self.entries.has_key(name):
            return self.entries[name]
        else:
            if self.parent != None:
                return self.parent.get(name)
            else:
                return None

class AbstractVisitor(Visitor):
    def visitNode(self, node):
        pass
    def visitNodeList(self, node):
        self._visitList(node.nodes)
    def visitFunctionListNode(self, node):
        self.visitNodeList(node) 
    def visitParameterListNode(self,node):
        self.visitNodeList(node) 
    def visitStatementListNode(self,node):
        self.visitNodeList(node)
    def visitArgumentListNode(self,node): 
        self.visitNodeList(node)
    def visitFunctionDefinitionNode(self, node): 
        pass
    def visitAssignStatementNode(self,node):  
        pass 
    def visitFunctionCallStatementNode(self,node): 
        pass
    def visitIfStatementNode(self,node):
        pass
    def visitWhileStatementNode(self,node):
        pass
    def visitReturnStatementNode(self,node):
        pass 
    def visitCompoundStatementNode(self,node): 
        pass
    def visitExpressionNode(self,node):  
        pass
    def visitIdentifierNode(self,node):
        pass
    def visitNumberNode(self,node):
        pass
    def visitStringNode(self,node):
        pass 
    def visitLeftIdentifierNode(self,node):
        pass
    def visitRightIdentifierNode(self,node):
        pass
class SymbolTableVisitor(AbstractVisitor):
    def add(self, node):
        self.current_symbol_table.add(node.name, node)
    def get(self,name):
        return self.current_symbol_table.get(name)
    def push(self, node): 
        self.current_symbol_table = SymbolTable(self.current_symbol_table)
        node.symbol_table = self.current_symbol_table
    def pop(self): 
        self.current_symbol_table = self.current_symbol_table.parent
    def visitFunctionListNode(self, node):
        self.root_symbol_table = SymbolTable()
        self.current_symbol_table = self.root_symbol_table 
        self.root_symbol_table.label_cnt=0
        self.visitNodeList(node)
        node.symbol_table = self.root_symbol_table
    def visitFunctionDefinitionNode(self, node): 
        self.var_max=0
        self.add(node)  
        self.push(node) 
        node.var_max=0
        node.sp_max=0
        node.parameters.accept(self)  
        node.statements.accept(self) 
        self.pop() 
        node.var_max=self.var_max
        node.sp_max=self.var_max
    def visitParameterListNode(self,node):
        node.param_num = 0
        for param in node.nodes: 
            param.accept(self)
            self.add(param)
            param.param_num = node.param_num
            node.param_num += 1
    def visitAssignStatementNode(self,node):  
        t=self.get(node.name)
        if t==None:
            self.var_max+=1 
            self.add(node) 
            node.rep=None 
        else:
            self.current_symbol_table.add(node.name, t)   
            node.rep=t    
        node.data.accept(self)   
    def visitFunctionCallStatementNode(self,node): 
        if node.argument_list!=None:
            for (i,n) in enumerate(node.argument_list.nodes): 
                n.accept(self) 
            node.argument_list.accept(self) 
        f=self.current_symbol_table.get(node.name) 
        node.var_max=f.var_max
    def visitIfStatementNode(self,node):
        node.expression.accept(self)
        node.true.accept(self)
        node.true.value=".L%d"%(self.root_symbol_table.label_cnt)
        self.root_symbol_table.label_cnt+=1  
        node.false.accept(self)
        node.false.value=".L%d"%(self.root_symbol_table.label_cnt)
        self.root_symbol_table.label_cnt+=1
    def visitWhileStatementNode(self,node):
        node.expression.accept(self)
        node.true.accept(self)
        node.true.value=".L%d"%(self.root_symbol_table.label_cnt)
        self.root_symbol_table.label_cnt+=1 
        node.false.accept(self)
        node.false.value=".L%d"%(self.root_symbol_table.label_cnt)
        self.root_symbol_table.label_cnt+=1
    def visitReturnStatementNode(self,node):
        node.expression.accept(self)
    def visitCompoundStatementNode(self,node): 
        self.push(node)   
        node.compound_list.accept(self)
        self.pop()  
    def visitExpressionNode(self,node):   
        if node.subtype is "lor":
            node.left.accept(self)
            node.right.accept(self) 
        else:
            node.data.accept(self) 
    def visitIdentifierNode(self,node):
        symbol = self.current_symbol_table.get(node.name)
        if symbol != None:
            node.symbol = symbol
        else: 
            self.add(node) 
            node.rep=None  
    def visitLeftIdentifierNode(self,node):
        symbol = self.current_symbol_table.get(node.name) 
        if symbol != None: 
            node.symbol = symbol
        else:
            print >>fout,  'id not found'
    def visitRightIdentifierNode(self,node):
        symbol = self.current_symbol_table.get(node.name)
        if symbol != None:
            node.symbol = symbol
        else:
            print >>fout,  'id not found'
    def visitSpecificIdentifierNode(self,node):
        pass
class CodeGenVisitor(AbstractVisitor):
    def visitFunctionListNode(self, node):  
        self.visitNodeList(node) 
    def visitFunctionDefinitionNode(self, node):  
        push_offset=2;
        param_num=len(node.symbol_table.entries) 
        self.spec_at=param_num
        self.spec_dollar=node.var_max
        self.fp=param_num
        print >>fout,  "%s:"%(node.name)    
        node.parameters.accept(self)  
        print >>fout,  "    push    {r7, lr}"
        print >>fout,  "    sub     sp, sp, #%d"%((node.sp_max)*4)
        print >>fout,  "    mov     r7, sp" 
        for (i,n) in enumerate(node.parameters.nodes):
            n.loc="[r7, #%d]"%((param_num-i+node.var_max+push_offset-1)*4)  
        node.statements.accept(self)   
        print >>fout,  "    mov     sp, r7"
        print >>fout,  "    add     sp, sp, #%d"%((node.sp_max)*4)
        print >>fout,  "    pop     {r7, pc}"
    def visitAssignStatementNode(self,node):
        node.data.accept(self)
        node.value=node.data.value  
        if node.rep!=None:  
            if node.subtype=='normal':
                print >>fout,  "    str     r0, %s     //%s"%(node.rep.loc,node.rep.name)  
            elif node.subtype=='right':
                print >>fout,  "    ldr     r1, %s     //%s"%(node.rep.loc,node.rep.name) 
                print >>fout,  "    add     r7, r1"
                print >>fout,  "    str     r0, [r7, #0]"
                print >>fout,  "    sub     r7, r1"
            elif node.subtype=='left':
                print >>fout,  "    //left rep"
                node.rep.loc="[r7, #%s]"%(node.value)
            else:
                print >>fout,  "assign error"
        else:  
            if node.subtype=='normal':
                print >>fout,  "    str     r0, %s     //%s"%(node.loc,node.name)  
            elif node.subtype=='left':
                print >>fout,  "    //left rep"
                node.loc="[r7, #%s]"%(node.value)
            else:
                print >>fout,  "assign error"
        print >>fout,  '//    [%s=%s]'%(node.name,node.value)
    def visitFunctionCallStatementNode(self,node): 
        param_num=len(node.argument_list.nodes)   
        back_at=self.spec_at
        back_dollar=self.spec_dollar
        self.spec_at=param_num
        self.spec_dollar=node.var_max
        for (i,n) in enumerate(node.argument_list.nodes): 
            n.accept(self)   
            if n.subtype=='lor':
                if n.left.type=='LeftIdentifier' or n.right.type=='LeftIdentifier':
                    print >>fout,  "    add     r0, #%s"%((2+param_num+node.var_max)*4)
            else:
                if n.data.type=='LeftIdentifier' : 
                    print >>fout,  "    add     r0, #%s"%((2+param_num+node.var_max)*4)
            print >>fout,  "    push    {r0}"  
        self.spec_at=back_at
        self.spec_dollar=back_dollar
        print >>fout,  "    bl      %s"%(node.name)  
        print >>fout,  "    add     sp, sp, #%s"%((param_num)*4) 
        node.value="r0"
    def visitIfStatementNode(self,node):
        node.expression.accept(self)
        op=node.expression.op
        op_rev={'>':'ble','<':'bgt','>=':'ble','<=':'bgt','!=':'beq','==':'bne'} 
        if node.false.type!='TrueFalse':
            print >>fout,  "    %s     %s"%(op_rev[op],node.true.value)
            node.true.accept(self) 
            print >>fout,  "    b       %s"%(node.false.value)
            print >>fout,  "%s:"%(node.true.value) 
            node.false.accept(self) 
            print >>fout,  "%s:"%(node.false.value) 
        else: 
            print >>fout,  "    %s     %s"%(op_rev[op],node.true.value)
            node.true.accept(self) 
            print >>fout,  "%s:"%(node.true.value)  
    def visitWhileStatementNode(self,node):
        op=node.expression.op 
        op_nom={'>':'bgt','<':'blt','>=':'bge','<=':'blt','!=':'bne','==':'beq'}
        print >>fout,  "    b       %s"%(node.false.value)
        print >>fout,  "%s:"%(node.true.value)
        node.true.accept(self) 
        print >>fout,  "%s:"%(node.false.value)  
        node.false.accept(self)
        node.expression.accept(self)
        print >>fout,  "    %s     %s"%(op_nom[op],node.true.value)
    def visitReturnStatementNode(self,node):
        node.expression.accept(self)
        #if node.expression.value !='r0':
            #print >>fout,  "    mov     r0, #%s"%(node.expression.value) 
        node.value='r0'
    def visitCompoundStatementNode(self,node):  
        param_num=len(node.symbol_table.pal) 
        for (i,n) in enumerate(node.symbol_table.pal):
            t=node.symbol_table.get(n)
            if t.type=='AssignStatement': 
                t.loc="[r7, #%d]"%((i)*4)   
        #+ is after the for loop
        self.fp+=param_num 
        node.compound_list.accept(self)   
        #self.fp-=param_num  
    def visitExpressionNode(self,node): 
        if node.subtype=='data':
            #node.value=node.data.value
            if node.data.type == 'FunctionCallStatement': 
                node.data.accept(self)  
                node.value="r0"
            elif node.data.type == 'Number':
                print >>fout,  '    mov     r0, #%s'%(node.data.value)
                node.value=node.data.value 
            elif node.data.type == 'Identifier':  
                print >>fout,  "    ldr     r0, %s     //%s"%(node.data.symbol.loc,node.data.name)
                node.value="r0"
            elif node.data.type == 'Expression':
                node.value=node.data.value
            elif node.data.type == 'LeftIdentifier':  
                # print >>fout,  "    ldr     r0, %s     //%s"%(node.data.symbol.loc,node.data.name)
                #print >>fout,  node.data.name,node.data.symbol.name,node.data.symbol.loc
                if node.data.symbol.loc[6:-1]!='r0':  
                    print >>fout,  "    mov     r0, #%d"%(int(node.data.symbol.loc[6:-1]))
                ##fixme
                    node.value=int(node.data.symbol.loc[6:-1])
                else :  
                    node.value='r0'
            elif node.data.type == 'RightIdentifier':  
                print >>fout,  "    ldr     r1, %s     //%s"%(node.data.symbol.loc,node.data.name)
                #print >>fout,  "    mov     r1, #4"
                #print >>fout,  "    mul     r0, r0, r1"
                print >>fout,  "    add     r7, r1"
                print >>fout,  "    ldr     r0, [r7, #0]"
                print >>fout,  "    sub     r7, r1"
                node.value="r0"
            elif node.data.type == 'SpecificIdentifier':
                if node.data.name=='@':
                    print >>fout,  "    mov     r0, #%d"%((self.spec_at))
                elif node.data.name=='$':
                    print >>fout,  "    mov     r0, #%d"%((self.spec_dollar))
                node.value="r0"
            else: 
                node.value="x0"
        else: 
            op_calc={'+':'add','-':'sub','*':'mul','/':'div'} 
            op_cmp=['>','<','>=','<=','!=','==']
            op_rev=['<','>','<=','>=','!=','==']
            node.left.accept(self) 
            #if node.left.value!='r0':
                #print >>fout,  '    mov     r0, #%s'%(node.left.value) 
            print >>fout,  "    push    {r0}" 
            node.right.accept(self)  
            #if node.right.value!='r0':
                #print >>fout,  '    mov     r0, #%s'%(node.right.value) 
            print >>fout,  "    pop     {r1}"   
            if node.left.value != "r0" and node.right.value !="r0": 
                if node.op in op_cmp: 
                    node.value=int(eval("%s%s%s"%(node.left.value,node.op,node.right.value))) 
                else:  
                    node.value=eval("%s%s%s"%(node.left.value,node.op,node.right.value))  
                print >>fout,  "    mov     r0, #%s"%(node.value)
                #print >>fout,  node.ret_value
            elif node.left.value != "r0"  and node.right.value =="r0": 
                if node.op in op_cmp: 
                    print >>fout,  "    mov     r1, r0"
                    print >>fout,  "    mov     r0, #%s"%(node.left.value)
                    node.op=op_rev[op_cmp.index(node.op)]  
                    if node.op=='>':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='<':
                        print >>fout,  "    cmp     r1, #%d"%(int(node.right.value)-1)
                    elif node.op=='>=':
                        print >>fout,  "    cmp     r1, #%d"%(int(node.right.value)-1)
                    elif node.op=='<=':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='==':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='!=':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    else:
                        print >>fout,  'error'
                elif node.op=='+' or node.op=='-':
                    print >>fout,  "    %s     r1, r0"%(op_calc[node.op])#,node.left.value)  
                    print >>fout,  "    mov     r0, r1"
                elif node.op=='*' or node.op=='/':
                    #print >>fout,  "    mov     r1, %s"%(node.left.value)
                    print >>fout,  "    %s     r0, r1, r0"%(op_calc[node.op]) 
                node.value="r0"
            elif node.left.value =="r0" and node.right.value != "r0" :
                if node.op in op_cmp: 
                    if node.op=='>':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='<':
                        print >>fout,  "    cmp     r1, #%d"%(int(node.right.value)-1)
                    elif node.op=='>=':
                        print >>fout,  "    cmp     r1, #%d"%(int(node.right.value)-1)
                    elif node.op=='<=':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='==':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    elif node.op=='!=':
                        print >>fout,  "    cmp     r1, #%s"%(node.right.value)
                    else:
                        print >>fout,  'error'
                elif node.op=='+' or node.op=='-':
                    print >>fout,  "    %s     r1, r0"%(op_calc[node.op])#,node.left.value)  
                    print >>fout,  "    mov     r0, r1"
                    #print >>fout,  "    %s     r0, r1, #%s"%(op_calc[node.op],node.right.value)  
                elif node.op=='*' or node.op=='/':
                    #print >>fout,  "    mov     r1, #%s"%(node.right.value)
                    print >>fout,  "    %s     r0, r1, r0"%(op_calc[node.op]) 
                node.value="r0"
            else: 
                if node.op in op_cmp:
                    print >>fout,  "    cmp     r0, r1" 
                else:
                    print >>fout,  "    %s     r0, r1, r0"%(op_calc[node.op]) 
                node.value="r0"
            print >>fout,  "//    [%s%s%s]"%(node.left.value,node.op,node.right.value)

import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

def run_lexer(strings): 
    lex.input(strings)
    while 1:
        token = lex.token()       # Get a token
        if not token: break        # No more tokens 
def run_parser(strings): 
    result = parser.parse(strings) 
    SymbolTableVisitor().visit(result) 
    CodeGenVisitor().visit(result) 
    #result.show() 

lex.lex()
parser = yacc.yacc(debug=True)#,debuglog=log)
if __name__ == '__main__':
    fpath = "test.de" 
    f = open(fpath,"r") 
    fout = open("test.deout","w")
    file=f.read()
    run_lexer(file) 
    run_parser(file)
    f.close()
    fout.close()
