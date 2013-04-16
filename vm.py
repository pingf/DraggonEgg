#coding=utf-8
#Author : ´óM¾ı ¡ú_¡ú Fanchao-Meng 2013 the snake year
import lex,yacc
import re
import time 
tokens = (
    'OBRACK','CBRACK','COMMA','SHARP','LABEL','DOT',
    'IDENTIFIER','INSTRUCTION','REGISTER','LBRACE','RBRACE','NUMBER',
    'COMMENT','NEWLINE','AT'
    ) 
t_AT=r'@'
t_COMMA = r','
t_OBRACK = r'\['
t_CBRACK = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SHARP = r'\#'
regs=['r0','r1','r7','sp','pc','lr','r6','cp']
inss=['mov','ldr','str','add','sub','mul','div','push','pop','bl','ble','b','cmp','bne']

def t_DOT(t):
    r'\.'
    pass
def t_LABEL(t):
    r'[.A-Za-z_][a-zA-Z0-9]*:' 
    return t
def t_IDENTIFIER(t):
    r'[A-Za-z_][a-zA-Z0-9]*' 
    if t.value in inss:
        t.type='INSTRUCTION'
        return t
    if t.value in regs:
        t.type='REGISTER'
        return t
    return t 
def t_NUMBER(t):
    r'0(?!\d)|([1-9]\d*)'
    return t
def t_NEWLINE(t):
    r'\n+'  
    return t
def t_WHITESPACE(t):
    r'[ \t]+'
    pass
def t_COMMENT(t):
    r'[/][/][\w\W]*?\n+'
    pass
def t_error(t):
    return t
 
class VirtualMachine(object):
    def __init__(self,ins,lab,max): 
        self.regs = {'r0':0, 'r1':0, 'r7':0, 'sp':max,'pc':0,'lr':0,'r6':0,'cp':0}
        self.ins=ins
        self.lab=lab 
        self.stack=[0]*max
        self.lines=len(ins)
        self.regs['pc']=self.lab['main:']  
        self.jump=0
        self.regs['lr']=self.lines 
        v=self.ins[self.regs['pc']]
        i=0
        while v!=None: 
            vmethod = getattr(self, "%s" % v[0], None) 
            if vmethod!=None: 
                vmethod(v[1:]) 
            else:
                print v[0],'not found' 
            v=self.next()
            i+=1
        print 'total ins :',i
    def next(self):
        id= self.regs['pc']
        if id == None :
            return id 
        
        if self.jump==0:
            id+=1 
            if id+1>self.lines:
                #print self.lines,'next limit reached'
                print "ans :",self.regs['r0']
                return None
            self.regs['pc']= id
            return self.ins[id]
        else:
            self.jump=0
            return self.ins[self.regs['pc']]
    def push(self,data):
        l=len(data)
        id=self.regs['sp']
        id-=l
        self.regs['sp']=id   
        for i,v in enumerate(data):
            if self.regs[v]!=None:
                self.stack[id+i]=self.regs[v] 
            else:
                print 'push error'  
    def pop(self,data):
        l=len(data)
        id=self.regs['sp']
        for i,v in enumerate(data):
            if self.stack[id+i]!=None:  
                #print '>>',id,i,self.stack[id+i+1],v,self.regs[v] 
                self.regs[v]=self.stack[id+i]
                #self.stack[id+i]=0
            else:  
                print 'pop error' 
        id+=l  
        self.regs['sp']=id 
    def sub(self,data): 
        l=len(data)
        if l==2:
            t0=self.regs[data[0]]
            if data[1][0].isdigit():
                t1=int(data[1])
                if data[0]=='sp' or data[0]=='r7':
                    t1=t1/4
            else:
                t1=self.regs[data[1]]
                if data[0]=='sp' or data[0]=='r7':
                    if data[1]!='sp' and data[1]!='r7':
                        t1=t1/4 
            self.regs[data[0]]=t0-t1
        elif l==3:   
            t1=self.regs[data[1]]
            if data[2][0].isdigit():
                t2=int(data[2])
                if data[1]=='sp' or data[1]=='r7':
                    t2=t2/4
            else:
                t2=self.regs[data[2]]
            self.regs[data[0]]=t1-t2
        else:
            pass
    def mov(self,data): 
        l=len(data)
        if l==2:
            if data[1][0].isdigit():
                t1=int(data[1])
                if data[0]=='sp' or data[0]=='r7' or data[0]=='r6':
                    t1=t1/4
            else:
                t1=self.regs[data[1]]
            self.regs[data[0]]=t1 
        else:
            pass
    def str(self,data): 
        l=len(data)
        if l==3:   
            t1=self.regs[data[1]] 
            t2=int(data[2])/4 
            self.stack[t1+t2]=self.regs[data[0]]  
        else:
            pass
    def ldr(self,data): 
        l=len(data)
        if l==3:   
            t1=self.regs[data[1]] 
            t2=int(data[2])/4   
            self.regs[data[0]]=self.stack[t1+t2] 
        else:
            pass
    def add(self,data): 
        l=len(data)
        if l==2:
            t0=self.regs[data[0]]
            if data[1][0].isdigit():
                t1=int(data[1]) 
                if data[0]=='sp' or data[0]=='r7':
                    t1=t1/4
            else:
                t1=self.regs[data[1]]
                if data[0]=='sp' or data[0]=='r7':
                    if data[1]!='sp' and data[1]!='r7':
                        t1=t1/4       
            self.regs[data[0]]=t0+t1
        elif l==3:   
            t1=self.regs[data[1]]
            if data[2][0].isdigit():
                t2=int(data[2])
                
                if data[1]=='sp' or data[1]=='r7':
                    t2=t2/4
            else:
                t2=self.regs[data[2]]
            self.regs[data[0]]=t1+t2
        else:
            pass 
    def mul(self,data): 
        l=len(data)
        if l==2:
            t0=self.regs[data[0]]
            if data[1][0].isdigit():
                t1=int(data[1])
                
                if data[0]=='sp' or data[0]=='r7':
                    t1=t1/4
            else:
                t1=self.regs[data[1]]
            self.regs[data[0]]=t0+t1
        elif l==3:   
            t1=self.regs[data[1]]
            if data[2][0].isdigit():
                t2=int(data[2]) 
                if data[1]=='sp' or data[1]=='r7':
                    t2=t2/4
            else:
                t2=self.regs[data[2]]
            self.regs[data[0]]=t1*t2
        else:
            pass 
    def bl(self,data): 
        if data[0]==None:
            print 'bl error'
        self.regs['lr']=self.regs['pc']
        self.regs['pc']=self.lab[data[0]+':']
        self.jump=1
    
    def cmp(self,data):
        t0=self.regs[data[0]]
        if data[1][0].isdigit():
            t1=int(data[1])
        else:
            t1=self.regs[data[1]]
        self.regs['cp']=t0-t1
    def ble(self,data):
        if data[0]==None:
            print 'ble error'
        cp=self.regs['cp']
        if cp<=0:
            self.regs['pc']=self.lab[data[0]+':']
            
            self.jump=1
    def bne(self,data):
        if data[0]==None:
            print 'bne error'
        cp=self.regs['cp']
        if cp!=0:
            self.regs['pc']=self.lab[data[0]+':']
            self.jump=1
    def b(self,data):
        if data[0]==None:
            print 'ble error'
        self.regs['pc']=self.lab[data[0]+':'] 
        self.jump=1
def run_lexer(): 
    tokens_neglect=(
    'OBRACK','CBRACK','COMMA','SHARP',
    'LBRACE','RBRACE'
    )  
    st=[]
    lb={}
    fpath = "test.deout" 
    f = open(fpath,"r") 
    file = f.read() 
    lex.input(file)
    f.close()
    i=0
    flag=0
    while 1:
        token = lex.token()       # Get a token 
        if not token: break       # No more tokens
        if token.type=='INSTRUCTION': 
            st.append([token.value]) 
            flag=1
            i+=1
        elif token.type=='NEWLINE':
            if flag==1:
                flag=0 
        elif token.type=='LABEL':
            lb[token.value]=i
        elif token.type == 'NUMBER' or token.type == 'REGISTER' \
            or token.type == 'IDENTIFIER': 
            if flag==1:
                st[-1].append(token.value)
        elif token.type in tokens_neglect:
            pass
        else :
            pass 
    return st,lb
 
lex.lex()   
if __name__ == '__main__':
    st,lb=run_lexer()   
    s=time.clock()
    vm=VirtualMachine(st,lb,500)
    e=time.clock() 
    print "time :",e-s
