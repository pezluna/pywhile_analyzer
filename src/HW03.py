from __future__ import annotations
from dataclasses import dataclass
from typing import *

from AST import *
from HW02 import *

import json

Env = Dict[VarName, Tuple[Type, Const]]

class Interp:
    def __init__(self, prog: Prog) -> None:
        self.prog = prog
        self.env = {}
        self.init_env()

    def init_env(self) -> Dict[VarName, Tuple[Type, Const]]:
        for decl in self.prog.progDecls:
            self.env[decl[1]] = (decl[0], None)
        return self.env
    
    def get_next_comm(self) -> Comm:
        for comm in self.prog.progComms:
            yield comm

    def type_checker(self, value, env) -> Type:
        if type(value) == int:
            return TyInt
        if type(value) == bool:
            return TyBool
        if isinstance(value, Const):
            ret = self.type_checker(value.value, env)
            return ret

        raise Exception(f"Unknown type: {value}")
    
    def calculate_expr(self, expr, env) -> Const:
        if isinstance(expr, ECst):
            return expr.value
        
        if isinstance(expr, EVar):
            try:
                return env[expr.var_name][1]
            except:
                raise Exception(f"Variable {expr.var_name} not defined")
        
        if isinstance(expr, EBinOp):
            left = self.calculate_expr(expr.left, env)
            right = self.calculate_expr(expr.right, env)

            if isinstance(left, Const):
                left = left.value
            if isinstance(right, Const):
                right = right.value

            op = expr.op

            if self.type_checker(left, env) != self.type_checker(right, env):
                raise Exception(f"Types of {left} and {right} are not equal")
            
            if isinstance(op, OpAdd):
                return left + right
            if isinstance(op, OpSub):
                return left - right
            if isinstance(op, OpMul):
                return left * right
            if isinstance(op, OpDiv):
                return left // right
            if isinstance(op, OpMod):
                return left % right
            if isinstance(op, OpLessThan):
                return left < right
            if isinstance(op, OpEqual):
                return left == right
            if isinstance(op, OpAnd):
                return left and right
            if isinstance(op, OpOr):
                return left or right

        if isinstance(expr, EUnaryOp):
            b = self.calculate_expr(expr.expr, env)
            op = expr.op

            if self.type_checker(b, env) != TyBool:
                raise Exception(f"Type of {b} is not bool")
            
            if isinstance(op, OpNot):
                return not b
            
        raise Exception(f"Unknown expression type: {expr}")

    def execute_comm(self, comm, env) -> Env:
        if isinstance(comm, CSkip):
            return env
        
        if isinstance(comm, CSeq):
            env = self.execute_comm(comm.comm1, env)
            env = self.execute_comm(comm.comm2, env)
            self.env = env
            return env
        
        if isinstance(comm, CAssign):
            expr = self.calculate_expr(comm.expr, env)
            env[comm.var_name] = (env[comm.var_name][0], expr)
            self.env = env
            return env
        
        if isinstance(comm, CRead):
            value = input()
            var_type = env[comm.var_name][0]

            if isinstance(var_type, TyInt):
                value = int(value)
            elif isinstance(var_type, TyBool):
                value = bool(value)
            else:
                raise Exception(f"Unknown type: {var_type}")

            env[comm.var_name] = (var_type, value)
            self.env = env

            return env
        
        if isinstance(comm, CWrite):
            print(self.calculate_expr(comm.expr, env))
            return env
        
        if isinstance(comm, CIf):
            if self.calculate_expr(comm.expr, env):
                env = self.execute_comm(comm.comm1, env)
            else:
                env = self.execute_comm(comm.comm2, env)
            self.env = env
            return env
        
        if isinstance(comm, CWhile):
            while self.calculate_expr(comm.expr, env):
                env = self.execute_comm(comm.comm, env)
            self.env = env
            return env
        
        if isinstance(comm, CAssert):
            assert self.calculate_expr(comm.expr, env), f"Assertion failed: {comm.expr}"
            self.env = env
            return env
        
        raise Exception(f"Unknown command type: {comm}")

    def execute_comms(self) -> None:
        for comm in self.get_next_comm():
            self.execute_comm(comm, self.env)

if __name__ == "__main__":
    json_path = "../json/HW02.json"

    with open(json_path, 'r') as f:
        data = json.load(f)

    ast = from_data_to_class(data)

    interp = Interp(ast)

    interp.execute_comms()