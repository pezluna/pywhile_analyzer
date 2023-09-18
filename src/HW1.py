from abc import *
from typing import List

# Program
def Prog():
    def __init__(self, progDecls:Decls, progComms:Comms):
        self.progDecls = progDecls
        self.progComms = progComms

def Decls():
    def __init__(self, decls:List[Decl]):
        self.decls = decls

def Comms():
    def __init__(self, comms:List[Comm]):
        self.comms = comms

def Decl():
    def __init__(self, decl:Tuple[Type, VarName]):
        self.decl = decl

# Type
def Type():
    def __init__(self, Type):
        self.Type = Type

def VarName():
    def __init__(self, value:string):
        self.value = value

# Statement
def Comm():
    def __init__(self, comm):
        self.comm = comm

# Expression
def Expr():
    def __init__(self, expr):
        self.expr = expr

def Const(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, value):
        self.value = value

def CInt(Const)
    def __init__(self, value:int):
        super().__init__(value)

def CBool(Const):
    def __init__(self, value:boolean):
        super().__init__(value)

def Op():
    def __init__(self, op):
        self.op = op

def OpAdd():
    def __init__(self, op):
        super().__init__()
