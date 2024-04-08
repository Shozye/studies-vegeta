/* Mateusz Pełechaty 261737 */

param n;
set Range := 1..n;

param A{i in Range, j in Range} := 1 / (i+j-1);
param c{i in Range} := sum{j in Range} 1 / (i+j-1);
param b{i in Range} := sum{j in Range} 1 / (i+j-1);

var x{j in Range} >= 0;

/* b = Ax */
subject to matrix_multiplication{i in Range}:
    b[i] = sum{j in Range} (A[i, j] * x[j]);

/* min c^T * x */
minimize cTtimesX: sum{i in Range} c[i] * x[i];

solve;
display n;
display x;
printf 'Błąd względny wyrażenia: %g\n', sqrt(sum{i in Range} ((x[i]-1)**2)) / sqrt(sum{i in Range} 1);
end;

