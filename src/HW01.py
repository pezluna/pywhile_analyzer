from __future__ import annotations
from typing import *

class WProg:
    def __init__(self, progDecls: WDecls, progComms: WComms) -> None:
        self.progDecls = progDecls
        self.progComms = progComms
    
    def __str__(self) -> str:
        return f'Prog {{ {self.progDecls}, {self.progComms} }}'

class WType:
    def __init__(self, type: Union[WTyInt, WTyBool]) -> None:
        self.type = type
    
    def __str__(self) -> str:
        return f'{self.type}'

class WTyInt:
    def __str__(self) -> str:
        return 'int'
    
class WTyBool:
    def __str__(self) -> str:
        return 'bool'

class WComm:
    def __init__(self, comm: Union[WCAssign, WCSkip, WCSeq, WCIf, WCWhile]) -> None:
        self.comm = comm
    
    def __str__(self) -> str:
        return f'{self.comm}'

class WCSkip:
    def __str__(self) -> str:
        return 'CSkip'
    
class WCSeq:
    def __init__(self, comm1: WComm, comm2: WComm) -> None:
        self.comm1 = comm1
        self.comm2 = comm2
    
    def __str__(self) -> str:
        return f'CSeq {self.comm1} {self.comm2}'
    
class WCAssign:
    def __init__(self, varName: WVarName, expr: WExpr) -> None:
        self.varName = varName
        self.expr = expr
    
    def __str__(self) -> str:
        return f'CAssign {self.varName} {self.expr}'
    
class WCRead:
    def __init__(self, varName: WVarName) -> None:
        self.varName = varName
    
    def __str__(self) -> str:
        return f'CRead {self.varName}'

class WWrite:
    def __init__(self, expr: WExpr) -> None:
        self.expr = expr
    
    def __str__(self) -> str:
        return f'CWrite {self.expr}'
    
class WCIf:
    def __init__(self, expr: WExpr, comm1: WComm, comm2: WComm) -> None:
        self.expr = expr
        self.comm1 = comm1
        self.comm2 = comm2
    
    def __str__(self) -> str:
        return f'CIf {self.expr} {self.comm1} {self.comm2}'
    
class WCWhile:
    def __init__(self, expr: WExpr, comm: WComm) -> None:
        self.expr = expr
        self.comm = comm
    
    def __str__(self) -> str:
        return f'CWhile {self.expr} {self.comm}'

class WCAssert:
    def __init__(self, expr: WExpr) -> None:
        self.expr = expr
    
    def __str__(self) -> str:
        return f'CAssert {self.expr}'

class WExpr:
    def __init__(self, expr: Union[WECst, WEVar, WEBinOp, WEUnaryOp]) -> None:
        self.expr = expr
    
    def __str__(self) -> str:
        return f'{self.expr}'

class WECst:
    def __init__(self, cst: Const) -> None:
        self.cst = cst
    
    def __str__(self) -> str:
        return f'ECst {self.cst}'

class WEVar:
    def __init__(self, varName: WVarName) -> None:
        self.varName = varName
    
    def __str__(self) -> str:
        return f'EVar {self.varName}'

class WEBinOp:
    def __init__(self, op: WOp, expr1: WExpr, expr2: WExpr) -> None:
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2
    
    def __str__(self) -> str:
        return f'EBinOp {self.op} {self.expr1} {self.expr2}'

class WEUnaryOp:
    def __init__(self, op: WOp, expr: WExpr) -> None:
        self.op = op
        self.expr = expr
    
    def __str__(self) -> str:
        return f'EUnaryOp {self.op} {self.expr}'

class Const():
    def __init__(self, value: Union[int, bool]) -> None:
        self.value = value
    
    def __repr__(self) -> str:
        if type(self.value) == int:
            return f'CInt {self.value}'
        elif type(self.value) == bool:
            return f'CBool {self.value}'
        else:
            raise Exception('Const value must be int or bool')
        
class WOp:
    def __init__(self, op: Union[WOpAdd, WOpSub, WOpMul, WOpDiv, WOpMod, WOpLessThan, WOpEqual, WOpAnd, WOpOr, WOpNot]) -> None:
        self.op = op
    
    def __str__(self) -> str:
        return f'{self.op}'
    
class WOpAdd:
    def __str__(self) -> str:
        return 'OpAdd'
    
class WOpSub:
    def __str__(self) -> str:
        return 'OpSub'
    
class WOpMul:
    def __str__(self) -> str:
        return 'OpMul'
    
class WOpDiv:
    def __str__(self) -> str:
        return 'OpDiv'
    
class WOpMod:
    def __str__(self) -> str:
        return 'OpMod'
    
class WOpLessThan:
    def __str__(self) -> str:
        return 'OpLessThan'

class WOpEqual:
    def __str__(self) -> str:
        return 'OpEqual'
    
class WOpAnd:
    def __str__(self) -> str:
        return 'OpAnd'
    
class WOpOr:
    def __str__(self) -> str:
        return 'OpOr'
    
class WOpNot:
    def __str__(self) -> str:
        return 'OpNot'
    
class WVarName:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return f'"{self.name}"'

WDecl = Tuple[WType, WVarName]
WDecls = List[WDecl]
WComms = List[WComm]