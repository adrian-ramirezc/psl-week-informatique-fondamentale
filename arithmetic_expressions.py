import math
from abc import ABC, abstractmethod
from numbers import Number
from typing import Dict


class Expr(ABC):
    """ This class is abstract and serves as a superclass for all Expressions
    """

    @abstractmethod
    def eval(self) -> Number:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Litteral(Expr):
    """ This class represents the constant expressions. It inherits from AExpr and, unlike AExpr,
        it is a concrete class (because 'eval' is implemented).
    """
    def __init__(self, v: Number = 0):
        super().__init__()
        self._value = v

    def eval(self) -> Number:
        return self._value
    
    def __str__(self) -> str:
        return f"{self.eval()}"

class Variable(Expr):
    vars = dict() 
    
    def __init__(self, name: str = None, value: Expr = None):
        super().__init__()
        self._name = name
        self._value = value
        self.vars[self._name] = self._value

    def eval(self) -> Number:
        '''
        vars: it contains all program variables created by user
        '''
        try:
            return self.vars[self._name].eval()
        except KeyError:
            print("Variable was not found")
        except AttributeError:
            return None
        except Exception as e:
            print(f"Error: {e}")
    
    def __str__(self) -> str:
        return f"{self._name}"


class BExpr(Expr):
    """ This class represents the binary expressions and, by inheritance, it is abstract.
        The reason is that the 'eval' abstract method is not yet implemented.
        This class has four concrete subclasses that represent 
        addition, subtraction, multiplication and division expressions.
    """

    def __init__(self, l: Expr = None, r: Expr = None) -> None:
        super().__init__()
        self._left = l
        self._right = r


class UExpr(Expr):
    def __init__(self, v: Expr = None):
        super().__init__()
        self._v = v
    
class PolyExpr(Expr):
    def __init__(self, var: str, expr: Expr):
        self._var = var
        self._expr = expr
    
    def eval(self, value = Expr):
        Variable(self._var, value)
        eval = self._expr.eval()
        Variable(self._var) # Reset var to None
        return eval
    
    def __str__(self):
        return f"Poly({self._var}, {self._expr})"
    
class AddExpr(BExpr):
    """ Now come the concrete instances of binary expressions
    """

    def eval(self):
        return self._left.eval() + self._right.eval()
    
    def __str__(self):
        return f"({self._left} + {self._right})"


class SubExpr(BExpr):
    def eval(self):
        return self._left.eval() - self._right.eval()
    
    def __str__(self):
        return f"({self._left} - {self._right})"


class MulExpr(BExpr):
    def eval(self):
        return self._left.eval() * self._right.eval()
    
    def __str__(self):
        return f"({self._left} * {self._right})"


class DivExpr(BExpr):
    def eval(self):
        return self._left.eval() / self._right.eval()

    def __str__(self):
        return f"({self._left} / {self._right})"

class PowExpr(BExpr):
    def eval(self):
        return self._left.eval() ** self._right.eval()
    
    def __str__(self):
        return f"({self._left} ^ {self._right})"

class SinExpr(UExpr):
    def eval(self):
        return math.sin(self._v.eval()) 
    
    def __str__(self):
        return f"sin({self._v})"

class CosExpr(UExpr):
    def eval(self):
        return math.cos(self._v.eval()) 
    
    def __str__(self):
        return f"cos({self._v})"

class LogExpr(UExpr):
    def eval(self):
        return math.log(self._v.eval()) 
    
    def __str__(self):
        return f"log({self._v})"
    
class ExpExpr(UExpr):
    def eval(self):
        return math.exp(self._v.eval()) 
    
    def __str__(self):
        return f"exp({self._v})"

class SqrtExpr(UExpr):
    def eval(self):
        return math.sqrt(self._v.eval()) 
    
    def __str__(self):
        return f"sqrt({self._v})"

class OppExpr(UExpr):
    def eval(self):
        return -1 * self._v.eval()
    
    def __str__(self):
        return f"(-{self._v})"

    

## TODO 0: define the object representing the expression (2 + (2 + 2))
##         then, define the object representing the expression ((2 + 2) + 2)

## TODO 1: implement the eval methods of the SubExpr, MulExpr and DivExpr classes

## TODO 2: perform the test at line 81, and check that it passes. Add a few more tests.

## TODO 3: add an abstract class for unary expressions,
## and one concrete subclass for "Opposites" -1 will be represented as "OppExpr(Litteral(1))"

## TODO 4: add an abstract __str__ method to AExpr and implement it 
## for all concrete classes (add parentheses everywhere when it is necessary)

## TODO (Not now. Later) : add variables. What do you need to change?

if __name__ == "__main__":
    onePlusTwo = AddExpr(Litteral(1), Litteral(2))
    print(f"Hello, World {onePlusTwo.eval()}")

    expr_1 = AddExpr(Litteral(2), AddExpr(Litteral(2),Litteral(2)))
    assert expr_1.eval() == 6
    print(expr_1)

    expr_2 = OppExpr(Litteral(1))
    assert expr_2.eval() == -1
    print(expr_2)

    expr_3 = SubExpr(Litteral(4), OppExpr(Litteral(2)))
    assert expr_3.eval() == 6
    print(expr_3)

    expr_4 = MulExpr(Litteral(5), Litteral(4))
    assert expr_4.eval() == 20
    print(expr_4)

    expr_5 = DivExpr(Litteral(12), Litteral(3))
    assert expr_5.eval() == 4    
    print(expr_5)

    expr_6 = AddExpr(OppExpr(Litteral(5)), DivExpr(Litteral(12), SubExpr(Litteral(7), MulExpr(Litteral(5), Litteral(1)))))
    assert expr_6.eval() == 1
    assert str(expr_6) == "(-5 + (12 / (7 - (5 * 1))))"

    e = MulExpr(AddExpr(Litteral(1),Litteral(2)),DivExpr(Litteral(2),Litteral(2)))
    assert e.eval() == 3
    print(e)
