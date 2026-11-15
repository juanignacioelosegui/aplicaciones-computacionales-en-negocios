Aplicaciones Computacionales en Negocios
Trabajo Pr´actico 2 - Octubre de 2026
El objetivo del trabajo pr´actico es plantear un modelo de lot sizing para planificar la pro-
ducci´on en una f´abrica. La planificaci´on es mensual, y consiste en determinar qu´e cantidad
fabricar de cada producto en cada mes, durante los pr´oximos 24 meses. Se tienen cinco pro-
ductos y se tiene una estimaci´on de la demanda por producto y mes (que se especifica en
la Tabla 1). Suponemos que las cantidades demandadas de todos los productos est´an en las
mismas unidades. La planificaci´on est´a sujeta a las siguientes restricciones:
1. Cada producto tiene una capacidad de producci´on m´axima de 120 unidades por mes.
2. Los productos se deben fabricar en lotes de 10 unidades cada uno. Es decir, la pro-
ducci´on de cada producto en cada mes debe ser un nu´mero perteneciente al conjunto
{0,10,20,30,...,120}.
3. El depo´sito tiene una capacidad total de 900 unidades, entre todos los productos. Se
puedeguardarstockfabricadoenunmesparacubrirlademandadelosmesessiguientes.
4. Al inicio de la planificaci´on no se tiene stock inicial de ningu´n producto.
5. La producci´on de una unidad de cada producto tiene un costo de $ 370 (el mismo costo
por unidad para todos los productos).
El objetivo de la planificaci´on es determinar qu´e cantidad fabricar de cada producto en cada
mes, de modo tal de cumplir la demanda minimizando los costos de fabricaci´on. Suponemos
que no hay costos de almacenamiento de stock. Sobre la base de esta descripci´on, el trabajo
pr´actico consiste de los siguientes puntos:
1. Plantear y resolver un modelo de programaci´on lineal entera mixta para este problema,
con el objetivo de minimizar los costos totales de producci´on.
2. Supongamos que tenemos un l´ımite de producci´on de 300 unidades por mes (es decir, la
producci´ontotalentretodoslosproductosnodebesuperarlas300unidadesmensuales).
¿C´omo cambia el modelo en este caso? ¿Se puede cumplir con la demanda total?
3. Supongamosqueadem´asdelas300unidadespormes, podemostercerizarlafabricaci´on
de hasta 200 unidades por mes, con un costo de $ 540 por unidad. ¿C´omo cambia el
modelo en este caso? (suponemos que tenemos que cumplir toda la demanda de cada
mes)
4. Supongamos adem´as que no se puede tercerizar la fabricaci´on de cualquier cantidad de
cadaproducto,sinoquesisetercerizalafabricaci´ondeunproductoenunmes, sedeben
solicitar al menos 20 unidades de ese producto en ese mes. ¿C´omo cambia el costo total
en este caso?
1

5. El l´ımite de 900 unidades en stock en el dep´osito es demasiado costoso y necesitamos
reducir el espacio disponible en el dep´osito. ¿Cu´al es la m´ınima capacidad del dep´osito
que hace que el problema sea factible? ¿Se puede buscar este valor sin hacer bu´squeda
| binaria | manualmente? |     |
| ------- | ------------ | --- |
Condiciones de entrega: El trabajo pr´actico se debe entregar a trav´es del campus virtual.
La entrega debe incluir un breve informe detallando el o los modelos planteados, junto con
todos los archivos necesarios para ejecutar el modelo. El trabajo pr´actico se puede hacer en
| grupos | de hasta cuatro | personas.                |
| ------ | --------------- | ------------------------ |
| Fecha  | de entrega:     | Viernes 20 de noviembre. |
2

| Mes    | Prod. A         | Prod. B | Prod.   | C Prod. D     | Prod. E |
| ------ | --------------- | ------- | ------- | ------------- | ------- |
| Ene/27 | 20              | 30      | 10      | 15            | 15      |
| Feb/27 | 25              | 40      | 15      | 20            | 15      |
| Mar/27 | 30              | 40      | 15      | 20            | 20      |
| Abr/27 | 40              | 45      | 20      | 20            | 25      |
| May/27 | 60              | 90      | 30      | 45            | 70      |
| Jun/27 | 100             | 140     | 50      | 70            | 100     |
| Jul/27 | 180             | 210     | 90      | 105           | 150     |
| Ago/27 | 210             | 250     | 105     | 125           | 160     |
| Sep/27 | 150             | 170     | 75      | 85            | 140     |
| Oct/27 | 60              | 60      | 30      | 30            | 70      |
| Nov/27 | 30              | 40      | 15      | 20            | 40      |
| Dic/27 | 20              | 25      | 10      | 15            | 20      |
| Ene/28 | 20              | 30      | 10      | 15            | 15      |
| Feb/28 | 25              | 40      | 15      | 20            | 15      |
| Mar/28 | 30              | 40      | 15      | 20            | 20      |
| Abr/28 | 40              | 45      | 20      | 20            | 25      |
| May/28 | 60              | 90      | 30      | 45            | 70      |
| Jun/28 | 100             | 140     | 50      | 70            | 100     |
| Jul/28 | 180             | 210     | 90      | 105           | 150     |
| Ago/28 | 210             | 250     | 105     | 125           | 160     |
| Sep/28 | 150             | 170     | 75      | 85            | 140     |
| Oct/28 | 60              | 60      | 30      | 30            | 70      |
| Nov/28 | 30              | 40      | 15      | 20            | 40      |
| Dic/28 | 20              | 25      | 10      | 15            | 20      |
| Table  | 1: Estimaciones | de      | demanda | por producto. |         |
3
