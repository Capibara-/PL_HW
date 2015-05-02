"""
Natural Operational Semantics (NOS) of statements

Implemented according to
http://www.daimi.au.dk/~bra8130/Wiley_book/wiley.pdf (the book).

"""

from while_ast import *
from expr import *

def nos(S, s):
    """
    Natural Operational Semantics (NOS) of statements

    Returns s' such that <S, s> --> s'

    Implements Table 2.1 from the book.

    --- MODIFY THIS FUNCTION QUESTIONS 1, 3 ---
    """

    if type(S) is Skip:
        return s

    elif type(S) is Assign:
        sp = s.copy()
        sp[S.lhs] = eval_arith_expr(S.rhs, s)
        return sp

    elif type(S) is Comp:
        sp = nos(S.S1, s)
        spp = nos(S.S2, sp)
        return spp

    elif type(S) is If and eval_bool_expr(S.b, s) is tt:
        sp = nos(S.S1, s)
        return sp

    elif type(S) is If and eval_bool_expr(S.b, s) is ff:
        sp = nos(S.S2, s)
        return sp

    elif type(S) is While and eval_bool_expr(S.b, s) is tt:
        sp = nos(S.S, s)
        spp = nos(While(S.b, S.S), sp)
        return spp

    elif type(S) is While and eval_bool_expr(S.b, s) is ff:
        return s

    elif type(S) is Repeat and eval_bool_expr(S.b, s) is ff:
        sp = nos(S.S, s)
        if eval_bool_expr(S.b, sp) is ff:
            spp = nos(Repeat(S.S, S.b), sp)
            return spp
        else:
            return sp

    elif type(S) is Repeat and eval_bool_expr(S.b, s) is tt:
        sp = nos(S.S, s)
        return sp

    else:
        assert ff  # Error


if __name__ == '__main__':
    # y = 1; while (x != 1) { y = y * x; x = x - 1 }
    prog1 = Comp(Assign('y', ALit(1)),
                While(Not(Eq(Var('x'), ALit(1))),
                      Comp(Assign('y', Times(Var('y'), Var('x'))),
                           Assign('x', Minus(Var('x'), ALit(1))))))

    print nos(prog1, {'x': 5})

    # x = 55; repeat x := x - 10 until x < 10
    prog2 = Comp(Assign('x', ALit(55)),
                 Repeat(Comp(Assign('x', Minus(Var('x'), ALit(10))), Skip()),
                        And(LE(Var('x'), ALit(10)),
                            Not(Eq(Var('x'), ALit(10))))))

    print nos(prog2, {'x' : 55})

    prog3 = Comp(Assign('x', ALit(1)), While(And(LE(Var('x'), ALit(10)),
                            Not(Eq(Var('x'), ALit(10)))), Comp(Assign('x', Plus(Var('x'), ALit(1))), Assign('x', Plus(Var('x'), ALit(1))))))
    print nos(prog3, {'x' : 1})