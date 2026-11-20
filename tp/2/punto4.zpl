# TP2 - Punto 4: modelo del punto 3 + si se terceriza un producto en un mes,
# se deben pedir al menos 20 unidades de ese producto en ese mes.
#
# Ejecutar:  scip -f punto4.zpl

set P  := { "A", "B", "C", "D", "E" };
set T  := { 1 .. 24 };
set T0 := { 0 .. 24 };

param d[T*P] := read "demanda.txt" as "<1n,2s> 3n" comment "#";

param c       := 370;
param L       := 10;
param K       := 12;
param capDep  := 900;
param limProp := 300;
param cT      := 540;
param W       := 200;
param minTerc := 20;    # pedido minimo tercerizado por producto y mes

var y[P*T]  integer >= 0 <= K;
var w[P*T]  integer >= 0 <= W;
var u[P*T]  binary;               # 1 si se terceriza el producto i en el mes t
var s[P*T0] real    >= 0;
var k[P*T]  integer >= 0;      # lotes propios acumulados (auxiliar)

minimize costo: sum <i,t> in P*T: (c * L * y[i,t] + cT * w[i,t]);

subto inicial: forall <i> in P:
   s[i,0] == 0;

subto balance: forall <i,t> in P*T:
   s[i,t-1] + L * y[i,t] + w[i,t] - s[i,t] == d[t,i];

subto deposito: forall <t> in T:
   sum <i> in P: s[i,t] <= capDep;

subto limite: forall <t> in T:
   sum <i> in P: L * y[i,t] <= limProp;

subto limiteTerc: forall <t> in T:
   sum <i> in P: w[i,t] <= W;

# w = 0, o bien minTerc <= w <= W.
subto minimoTerc: forall <i,t> in P*T:
   w[i,t] >= minTerc * u[i,t];

subto activaTerc: forall <i,t> in P*T:
   w[i,t] <= W * u[i,t];

# Restriccion redundante (no cambia las soluciones enteras) que ayuda a SCIP:
# la produccion propia acumulada hasta t es  s[i,t] + sum_{r<=t} (d - w)  y,
# por la lotificacion, es multiplo de L. Hacerlo explicito con la entera k
# permite que SCIP razone sobre la paridad de lo tercerizado; sin ella la
# cota dual queda trabada y algunas instancias del punto 5 no cierran el gap.
subto acumulado: forall <i,t> in P*T:
   s[i,t] + sum <r> in T with r <= t: (d[r,i] - w[i,r]) == L * k[i,t];
