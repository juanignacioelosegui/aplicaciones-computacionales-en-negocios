# TP2 - Punto 1: modelo de lot sizing (MILP).
#
# Minimiza el costo total de produccion sujeto a:
#   - lotes de 10 unidades por producto y mes,
#   - capacidad de 120 unidades/mes por producto,
#   - capacidad total de deposito de 900 unidades,
#   - stock inicial nulo,
#   - satisfaccion de toda la demanda.
#
# Ejecutar:  scip -f punto1.zpl

set P  := { "A", "B", "C", "D", "E" };   # productos
set T  := { 1 .. 24 };                   # meses (1 = Ene/27, ..., 24 = Dic/28)
set T0 := { 0 .. 24 };                   # meses + mes 0 (stock inicial)

param d[T*P] := read "demanda.txt" as "<1n,2s> 3n" comment "#";

param c      := 370;   # $ por unidad producida
param L      := 10;    # unidades por lote
param K      := 12;    # lotes maximos por producto y mes (120 / 10)
param capDep := 900;   # capacidad del deposito (unidades)

var y[P*T]  integer >= 0 <= K;   # lotes del producto i en el mes t
var s[P*T0] real    >= 0;        # stock del producto i al final del mes t

minimize costo: sum <i,t> in P*T: c * L * y[i,t];

subto inicial: forall <i> in P:
   s[i,0] == 0;

subto balance: forall <i,t> in P*T:
   s[i,t-1] + L * y[i,t] - s[i,t] == d[t,i];

subto deposito: forall <t> in T:
   sum <i> in P: s[i,t] <= capDep;
