# Modelo petroleo

var X >= 0;
var xc >= 0;
var xa >= 0;
var xcp >= 0;
var xap >= 0;

maximize beneficio:
    60*xc + 40*xa + 130*xcp + 90*xa - 40*X;

subto max_compra:
    X <= 20;

subto horas:
    60*xcp + 45*xap <= 8*60;

subto produccion_total:
    xc + xcp + xa + xap == X;

subto igualdad:
    xc + xcp == xa + xap;