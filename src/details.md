-- Program
data Prog = Prog { progDecls :: Decls, progComms :: Comms }

type Decls = [ Decl ]
type Comms = [ Comm ]

type Decl  = (Type, VarName)

-- Type
data Type =
    TyInt
  | TyBool

type VarName  = String

-- Statement
data Comm =
    CSkip
  | CSeq Comm Comm
  | CAssign VarName Expr
  | CRead VarName
  | CWrite Expr
  | CIf Expr Comm Comm
  | CWhile Expr Comm
  | CAssert Expr

-- Expression
data Expr =
    ECst   Const
  | EVar   VarName
  | EBinOp Op Expr Expr
  | EUnaryOp Op Expr

data Const =
    CInt  Int
  | CBool Bool

data Op =
    OpAdd
  | OpSub
  | OpMul
  | OpDiv
  | OpMod
  | OpLessThan   -- x < y
  | OpEqual      -- x == y
  | OpAnd
  | OpOr
  | OpNot
