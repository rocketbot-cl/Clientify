# Clientify
  
Módulo para interactuar con Clientify.  

*Read this in other languages: [English](Manual_Clientify.md), [Português](Manual_Clientify.pr.md), [Español](Manual_Clientify.es.md)*
  
![banner](imgs/Banner_Clientify.png)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Descripción de los comandos

### Conectar a Clientify
  
Conectar a Clientify
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Nombre de usuario|Nombre de usuario de la cuenta Clientify|usuario|
|Password|Password de usuario de la cuenta Clientify|********|
|Asignar resultado a variable|Variable a la cual asignar el resultado. Traera un JSON.|Variable|

### Obtener oportunidad con filtros
  
Obtiene oportunidad con filtros
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro especifico|Filtro especifico de busqueda; ej nombre de la oportunidad, nombre de la compañía, nombre de contacto, apellido de contacto|Rocket|
|Nombre del propietario|Filtro por nombre de propietario.|Carlos|
|Filtro mayor que|Selector para usar con fecha de cierre mayor que.||
|Fecha de cierre|Fecha de cierre mayor que. Formato yyyy/mm/dd|2021/08/23|
|Filtro menor que|Selector para usar con fecha de cierre menor que.||
|Fecha de cierre|Fecha de cierre menor que. Formato yyyy/mm/dd|2021/08/23|
|Estado|Estado de la oportunidad. Ej Won (ganada), Lost (perdida).||
|Flujo|Filtro de flujo de la oportunidad.|Venta|
|Tipo de filtro de fecha|Filtro de fecha, creada o modificada.||
|Filtro mayor que|Selector para usar con fecha de creacion o modificacion mayor que.||
|Fecha|Fecha de creacion o modificacion mayor que. Formato yyyy/mm/dd|2021/08/23|
|Filtro menor que|Selector para usar con fecha de creacion o modificacion menor que.||
|Fecha|Fecha de creacion o modificacion menor que. Formato yyyy/mm/dd|2021/08/23|
|Asignar resultado a variable|Variable a la cual asignar el resultado. Traera un JSON.|Variable|

### Obtener oportunidad por ID
  
Obtiene todas las propiedades de una oportunidad por ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Identificador de la oportunidad|Identificador de la oportunidad. Puedes obtenerla al listar las oportunidades o en la url en Clientify|2704232|
|Asignar resultado a variable|Variable a la cual asignar el resultado. Traera un JSON.|Variable|

### Obtener productos
  
Este comando te permite obtener todos los productos de Clientify
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Asignar resultado a variable|Variable a la cual asignar el resultado.|Variable|

### Obtener compañías por query
  
Este comando te permite obtener compañías por nombre, fecha de creación o fecha de modificación
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Tipo de filtro|Tipo de filtro a aplicar. Si se selecciona Fecha de creación o fecha de modificación, traerá todas las compañías que hayan sido creadas o modificadas después de la fecha seleccionada.||
|Valor a buscar|Valor a buscar en el filtro.|Rocketbot|
|Asignar resultado a variable|Variable a la cual asignar el resultado.|Variable|

### Obtener contactos por query
  
Este comando permite obtener contactos por nombre, teléfono o email.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Tipo de filtro|Tipo de filtro a aplicar. ||
|Valor a buscar|Valor a buscar en el filtro.|example@rocketbot.com|
|Asignar resultado a variable|Variable a la cual asignar el resultado.|Variable|

### Crear oportunidad
  
Este comando permite crear una oportunidad.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Nombre de la oportunidad|Nombre de la oportunidad a crear.|venta|
|Monto de la oportunidad|Monto de la oportunidad a crear.|1500|
|ID de contacto|ID del contacto al cual asignar la oportunidad.|39562459|
|ID de compañia|ID de la compañia a la cual asignar la oportunidad.|39562459|
|Fecha de cierre|Fecha de cierre de la oportunidad.|2023-03-20|
|Productos|Lista de productos de la oportunidad.|[{"product_id":"4048412","quantity":1}, {"product_id":"4048413","quantity":2}]|
|Custom fields|Lista de campos personalizados de la oportunidad.|[{"field": "nombre_campo","value": "valor_campo"}, {"field": "nombre_campo","value": "valor_campo"}]|
|Asignar resultado a variable|Variable a la cual asignar el resultado.|Variable|
