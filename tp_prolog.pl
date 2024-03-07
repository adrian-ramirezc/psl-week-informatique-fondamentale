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
len([], 0).
len([X | Q], L) :- len(Q, L1), L is L1 + 1.

test_longueur :- len([1,2,3,4], 4).

% Manipulations symboliques
pere(jean, michel).
pere(michel, jacques).
mere(michel, marie).
ancetre(X, Y) :- pere(X,Y) ; mere(X, Y).
ancetre(X, Y) :- ancetre(X,Z), ancetre(Z, Y).

test_ancetre :- ancetre(jean,X); ancetre(X, jacques)