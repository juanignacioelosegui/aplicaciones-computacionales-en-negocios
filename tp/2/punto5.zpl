# TP2 - Punto 5: minima capacidad del deposito que hace factible el problema.
#
# En lugar de una busqueda binaria, la capacidad del deposito pasa a ser una
# variable de decision Dep, y se minimiza:
#     sum_i s[i,t] <= Dep   para todo t,      min Dep
# El optimo Dep* es exactamente la menor capacidad factible (un unico MILP).
#
# Con los parametros por defecto las restricciones son las del punto 4. Se
# pueden cambiar sin editar el archivo con la opcion -D de Zimpl (ver
# correr.py): con minTerc = 0 son las del punto 3, y con W = 0, limProp = 600
# las del punto 1.
#
# Segunda etapa (plan mas barato con ese deposito): resolver el modelo del
# punto correspondiente (punto1/3/4.zpl) con el parametro capDep = Dep*.
# correr.py lo hace automaticamente.
#
# Ejecutar:  scip -f punto5.zpl

set P  := { "A", "B", "C", "D", "E" };
set T  := { 1 .. 24 };
set T0 := { 0 .. 24 };

param d[T*P] := read "demanda.txt" as "<1n,2s> 3n" comment "#";

param L       := 10;
param K       := 12;
param limProp := 300;
param W       := 200;
param minTerc := 20;

var y[P*T]  integer >= 0 <= K;
var w[P*T]  integer >= 0 <= W;
var u[P*T]  binary;
var s[P*T0] real    >= 0;
var k[P*T]  integer >= 0;      # lotes propios acumulados (auxiliar)
var Dep     real    >= 0;      # capacidad del deposito (ahora es una variable)

minimize capacidad: Dep;

subto inicial: forall <i> in P:
   s[i,0] == 0;

subto balance: forall <i,t> in P*T:
   s[i,t-1] + L * y[i,t] + w[i,t] - s[i,t] == d[t,i];

# La capacidad del deposito ahora es la variable Dep.
subto deposito: forall <t> in T:
   sum <i> in P: s[i,t] - Dep <= 0;

subto limite: forall <t> in T:
   sum <i> in P: L * y[i,t] <= limProp;

subto limiteTerc: forall <t> in T:
   sum <i> in P: w[i,t] <= W;

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
