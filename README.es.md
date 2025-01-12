# API Average

Es un proyecto que se encarga de calcular el promedio de una lista de números, por medio de 3 APIs:

- API Add: Se encarga de sumar una lista de números.
- API Divide: Se encarga de dividir un número por otro.
- API Average: Se encarga de calcular el promedio de una lista de números.

El objetivo es que el promedio se pueda calcular de manera distribuida, es decir, que cada API se encargue de su tarea y luego se haga la división, es un enfoque sencillo para poder entender el concepto de microservicios.


## Diagrama de secuencia


```mermaid
sequenceDiagram
    %% El usuario inicia la llamada al endpoint /average
    participant Usuario as Usuario (Cliente)
    participant APIAverage as api_average
    participant APIAdd as api_add
    participant APIDivide as api_divide

    %% 1. El usuario realiza una petición POST /average con la lista de números
    Usuario ->> APIAverage: POST /average<br>Body: { numbers: [...] }

    note over APIAverage: <b>api_average</b><br>Recibe la lista de números.<br>Necesita obtener la suma y luego el promedio.

    %% 2. api_average solicita la suma de los números a api_add
    APIAverage ->> APIAdd: POST /add<br>Body: { numbers: [...] }

    note over APIAdd: <b>api_add</b><br>Calcula la suma de todos los<br>números recibidos y retorna el resultado.

    %% 3. api_add responde con la suma de los números
    APIAdd -->> APIAverage: 200 OK<br>Body: { result: suma }

    note over APIAverage: <b>api_average</b><br>Recibe la suma (sum_numbers).

    %% 4. api_average solicita la división (sum_numbers ÷ total_números) a api_divide
    APIAverage ->> APIDivide: POST /divide<br>Body: { divide: sum_numbers,<br>  divindend: len(numbers) }

    note over APIDivide: <b>api_divide</b><br>Realiza la operación de división y<br>retorna el resultado.

    %% 5. api_divide responde con el promedio
    APIDivide -->> APIAverage: 200 OK<br>Body: { result: average }

    note over APIAverage: <b>api_average</b><br>Recibe el promedio y lo devuelve<br>al usuario final.

    %% 6. api_average retorna el promedio al usuario
    APIAverage -->> Usuario: 200 OK<br>Body: { result: average }
```
