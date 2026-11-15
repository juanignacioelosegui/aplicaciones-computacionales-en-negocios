# Modelo masas - Ejemplo Juan

var xc >= 0;
var xv >= 0;

maximize ganancia:
    20*xc + 15*xv;

subto tiempo:
    20*xc + 40*xv <= 8*60;

subto huevos:
    4*xc + xv <= 30;

subto demanda_chocolate:
    xc <= 5.3;