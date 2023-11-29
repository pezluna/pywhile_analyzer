from typing import Dict, Tuple
import json

from AST import *
from HW02 import from_data_to_class

TyEnv = Dict[VarName, Type]

class TypeChecker:
    def __init__(self) -> None:
        pass

    def init_env(prog: Prog) -> TyEnv:
        tyenv = {}
        for decl in prog.progDecls:
            tyenv[decl[1]] = decl[0]
        return tyenv
    
    def typecheckExpr(tyenv: TyEnv, expr: Expr) -> Type:
        if isinstance(expr, ECst):
            if isinstance(expr.value, CInt):
                return TyInt()
            if isinstance(expr.value, CBool):
                return TyBool()
        
        if isinstance(expr, EVar):
            try:
                return tyenv[expr.var_name]
            except KeyError:
                raise Exception(f"Variable {expr.var_name} not defined")
        
        if isinstance(expr, EBinOp):
            left = TypeChecker.typecheckExpr(tyenv, expr.left)
            right = TypeChecker.typecheckExpr(tyenv, expr.right)

            op = expr.op
            
            if isinstance(op, OpAdd):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyInt()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpSub):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyInt()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpMul):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyInt()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpDiv):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyInt()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpMod):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyInt()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpLessThan):
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyBool()
                raise Exception(f"Expected int, got {left} and {right}")
            
            if isinstance(op, OpEqual):
                if isinstance(left, TyBool) and isinstance(right, TyBool):
                    return TyBool()
                if isinstance(left, TyInt) and isinstance(right, TyInt):
                    return TyBool()
                raise Exception(f"Expected same types, got {left} and {right}")
            
            if isinstance(op, OpAnd):
                if isinstance(left, TyBool) and isinstance(right, TyBool):
                    return TyBool()
                raise Exception(f"Expected bool, got {left} and {right}")
            
            if isinstance(op, OpOr):
                if isinstance(left, TyBool) and isinstance(right, TyBool):
                    return TyBool()
                raise Exception(f"Expected bool, got {left} and {right}")
            
            raise Exception(f"Unknown operator: {op}")
        
        if isinstance(expr, EUnaryOp):
            ty = TypeChecker.typecheckExpr(tyenv, expr.expr)
            op = expr.op

            if isinstance(op, OpNot):
                if isinstance(ty, TyBool):
                    return TyBool()
            raise Exception(f"Expected bool, got {ty}")
            
        raise Exception(f"Unknown expression type: {expr}")

    def typecheckComm(tyenv: TyEnv, comm: Comm) -> None:
        if isinstance(comm, CSkip):
            return
        
        if isinstance(comm, CSeq):
            TypeChecker.typecheckComm(tyenv, comm.comm1)
            TypeChecker.typecheckComm(tyenv, comm.comm2)
            return
        
        if isinstance(comm, CAssign):
            ty = TypeChecker.typecheckExpr(tyenv, comm.expr)

            try:
                var_type = tyenv[comm.var_name]
            except KeyError:
                raise Exception(f"Variable {comm.var_name} not defined")
            
            if type(ty) == type(var_type):
                return
            else:
                raise Exception(f"Expected the same types: {ty} != {var_type}")
        
        if isinstance(comm, CRead):
            try:
                var_type = tyenv[comm.var_name]
            except KeyError:
                raise Exception(f"Variable {comm.var_name} not defined")
            
            return 
        
        if isinstance(comm, CWrite):
            ty = TypeChecker.typecheckExpr(tyenv, comm.expr)
            return
        
        if isinstance(comm, CIf):
            ty = TypeChecker.typecheckExpr (tyenv, comm.expr)
            if isinstance(ty, TyBool):
                TypeChecker.typecheckComm(tyenv, comm.comm1)
                TypeChecker.typecheckComm(tyenv, comm.comm2)
                return
            raise Exception(f"Expression {comm.expr} is of type {ty}, not of type bool")
        
        if isinstance(comm, CWhile):
            ty = TypeChecker.typecheckExpr(tyenv, comm.expr)
            if isinstance(ty, TyBool):
                TypeChecker.typecheckComm(tyenv, comm.comm)
                return
            raise Exception(f"Expression {comm.expr} is of type {ty}, not of type bool")
        
        if isinstance(comm, CAssert):
            ty = TypeChecker.typecheckExpr(tyenv, comm.expr)
            if isinstance(ty, TyBool):
                return
            raise Exception(f"Expression {comm.expr} is of type {ty}, not of type bool")
        
        raise Exception(f"Unknown command type: {comm}")

    def typeCheckProgram(self, prog: Prog) -> None:
        tyenv = TypeChecker.init_env(prog)
        for comm in prog.progComms:
            TypeChecker.typecheckComm(tyenv, comm)

if __name__ == "__main__":
    json_path = "../json/HW02.json"

    with open(json_path, 'r') as f:
        data = json.load(f)

    ast = from_data_to_class(data)

    typeChecker = TypeChecker()
    typeChecker.typeCheckProgram(ast)
