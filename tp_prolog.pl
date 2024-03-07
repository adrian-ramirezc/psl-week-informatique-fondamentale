% Egalité
eq(z,z).
eq(s(X), s(Y)) :- eq(X,Y).

test_eq :- eq(s(s(z)), s(s(z))).

% Incrementation
incr(z, s(z)).
incr(s(X), s(Y)) :- incr(X,Y).

test_incr :- incr(s(z),X), incr(s(X),s(s(X))), incr(s(z),z).

% Addition
add(z, X, X).
add(s(X), Y, s(Z)) :- add(X, Y, Z).

test_add :- add(s(s(z)), s(s(z)), Result).

% Multiplication
mult(z, X, z).
mult(s(X), Y, Z) :- mult(X,Y, Z1), add(Y,Z1,Z).

test_mul :- mult(s(z), s(z), X).

% Element
element(X, [X | _]).
element(X, [_ | Q]) :- element(X, Q).

test_element :- element(a, [d, c, b, a]).

% Max: find max, compare
max([X], X).
max([X , Y | Rest], Max) :- (X > Y ->
        max([X | Rest], Max)
    ;
        max([Y | Rest], Max)
    ).

test_max :- max([1, 2, 4, 3], 4).

% Longueur