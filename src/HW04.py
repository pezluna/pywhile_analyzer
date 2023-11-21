from typing import Dict, Tuple
import json

from AST import *
from HW02 import from_data_to_class

Env = Dict[VarName, Const]
TyEnv = Dict[VarName, Type]

class Interp:
    def __init__(self, prog: Prog) -> None:
        self.prog = prog
        self.env: Env = {}
        self.tyenv: TyEnv = {}
        self.init_env()

    def init_env(self) -> None:
        for decl in self.prog.progDecls:
            self.env[decl[1]] = None
            self.tyenv[decl[1]] = decl[0]
    
    def calculate_expr(self, expr: Expr, env: Env, tyenv: TyEnv) -> Tuple[Const, TyEnv]:
        if isinstance(expr, ECst):
            return expr.value
        
        if isinstance(expr, EVar):
            try:
                return env[expr.var_name]
            except KeyError:
                raise Exception(f"Variable {expr.var_name} not defined")
        
        if isinstance(expr, EBinOp):
            left = self.calculate_expr(expr.left, env, tyenv)
            right = self.calculate_expr(expr.right, env, tyenv)
            
            if isinstance(left, Const):
                left_value = left.value
            else:
                raise Exception(f"Expected const, got {left}")
            if isinstance(right, Const):
                right_value = right.value
            else:
                raise Exception(f"Expected const, got {right}")

            op = expr.op
            
            if isinstance(op, OpAdd):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                return CInt(left_value + right_value)
            if isinstance(op, OpSub):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                return CInt(left_value - right_value)
            if isinstance(op, OpMul):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                return CInt(left_value * right_value)
            if isinstance(op, OpDiv):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                if right_value == 0:
                    raise Exception(f"Division by zero")
                return CInt(left_value // right_value)
            if isinstance(op, OpMod):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                if right_value == 0:
                    raise Exception(f"Division by zero")
                return CInt(left_value % right_value)
            if isinstance(op, OpLessThan):
                if isinstance(left, CBool) or isinstance(right, CBool):
                    raise Exception(f"Expected int, got {left} and {right}")
                return CBool(left_value < right_value)
            if isinstance(op, OpEqual):
                if isinstance(left, CBool) and isinstance(right, CBool):
                    return CBool(left_value == right_value)
                if isinstance(left, CInt) and isinstance(right, CInt):
                    return CBool(left_value == right_value)
                raise Exception(f"Expected same types, got {left} and {right}")
            if isinstance(op, OpAnd):
                if isinstance(left, CInt) or isinstance(right, CInt):
                    raise Exception(f"Expected bool, got {left} and {right}")
                return CBool(left_value and right_value)
            if isinstance(op, OpOr):
                if isinstance(left, CInt) or isinstance(right, CInt):
                    raise Exception(f"Expected bool, got {left} and {right}")
                return CBool(left_value or right_value)

        if isinstance(expr, EUnaryOp):
            b = self.calculate_expr(expr.expr, env, tyenv)
            op = expr.op

            if isinstance(b, CBool):
                b = b.value
            else:
                raise Exception(f"Expected bool, got {b}")
            
            if isinstance(op, OpNot):
                return CBool(not b)
            
        raise Exception(f"Unknown expression type: {expr}")

    def execute_comm(self, comm: Comm, env: Env, tyenv: TyEnv) -> Tuple[Env, TyEnv]:
        if isinstance(comm, CSkip):
            return env, tyenv
        
        if isinstance(comm, CSeq):
            env, tyenv = self.execute_comm(comm.comm1, env, tyenv)
            env, tyenv = self.execute_comm(comm.comm2, env, tyenv)
            return env, tyenv
        
        if isinstance(comm, CAssign):
            expr = self.calculate_expr(comm.expr, env, tyenv)
            var_type = tyenv[comm.var_name]

            if isinstance(var_type, TyBool):
                if isinstance(expr, CInt):
                    raise Exception(f"Expected bool, got {expr}")
                env[comm.var_name] = expr
            elif isinstance(var_type, TyInt):
                if isinstance(expr, CBool):
                    raise Exception(f"Expected int, got {expr}")
                env[comm.var_name] = expr
            else:
                raise Exception(f"Unknown type: {var_type}")
            return env, tyenv
        
        if isinstance(comm, CRead):
            value = input(">>> ")
            var_type = tyenv[comm.var_name]
            
            if isinstance(var_type, TyBool):
                if value == "True":
                    env[comm.var_name] = CBool(True)
                elif value == "False":
                    env[comm.var_name] = CBool(False)
                else:
                    raise Exception(f"Expected bool, got {value}")
            elif isinstance(var_type, TyInt):
                try:
                    env[comm.var_name] = CInt(int(value))
                except ValueError:
                    raise Exception(f"Expected int, got {value}")
            else:
                raise Exception(f"Unknown type: {var_type}")

            return env, tyenv
        
        if isinstance(comm, CWrite):
            print(self.calculate_expr(comm.expr, env, tyenv).value)
            return env, tyenv
        
        if isinstance(comm, CIf):
            if self.calculate_expr(comm.expr, env, tyenv):
                env, tyenv = self.execute_comm(comm.comm1, env, tyenv)
            else:
                env, tyenv = self.execute_comm(comm.comm2, env, tyenv)
            return env, tyenv
        
        if isinstance(comm, CWhile):
            expr_type = self.calculate_expr(comm.expr, env, tyenv)
            if isinstance(expr_type, CInt):
                raise Exception(f"Expected bool, got {expr_type}")
            while self.calculate_expr(comm.expr, env, tyenv).value == True:
                env, tyenv = self.execute_comm(comm.comm, env, tyenv)
            return env, tyenv
        
        if isinstance(comm, CAssert):
            assert self.calculate_expr(comm.expr, env, tyenv), f"Assertion failed: {comm.expr}"
            return env, tyenv
        
        raise Exception(f"Unknown command type: {comm}")

    def execute_comms(self) -> None:
        env = self.env
        tyenv = self.tyenv
        for comm in self.prog.progComms:
            env, tyenv = self.execute_comm(comm, env, tyenv)

if __name__ == "__main__":
    json_path = "../json/HW02.json"

    with open(json_path, 'r') as f:
        data = json.load(f)

    ast = from_data_to_class(data)

    interp = Interp(ast)

    interp.execute_comms()