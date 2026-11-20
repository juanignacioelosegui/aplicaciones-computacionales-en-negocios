# TP2 - Punto 2: modelo del punto 1 + limite de produccion total de
# 300 unidades/mes entre todos los productos.
#
# Ejecutar:  scip -f punto2.zpl      (SCIP reporta que es infactible)

set P  := { "A", "B", "C", "D", "E" };
set T  := { 1 .. 24 };
set T0 := { 0 .. 24 };

param d[T*P] := read "demanda.txt" as "<1n,2s> 3n" comment "#";

param c       := 370;
param L       := 10;
param K       := 12;
param capDep  := 900;
param limProp := 300;   # produccion propia maxima por mes (unidades)

var y[P*T]  integer >= 0 <= K;
var s[P*T0] real    >= 0;

minimize costo: sum <i,t> in P*T: c * L * y[i,t];

subto inicial: forall <i> in P:
   s[i,0] == 0;

subto balance: forall <i,t> in P*T:
   s[i,t-1] + L * y[i,t] - s[i,t] == d[t,i];

subto deposito: forall <t> in T:
   sum <i> in P: s[i,t] <= capDep;

# Nueva familia de restricciones del punto 2.
subto limite: forall <t> in T:
   sum <i> in P: L * y[i,t] <= limProp;
