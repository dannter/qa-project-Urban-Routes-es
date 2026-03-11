# Urban Routes Automation Tests

## Descripción 

**Urban Routes Automation Tests** es un proyecto de automatización de pruebas end-to-end para una aplicación web de Urban Routes, solicitud de taxis.

El objetivo del proyecto es validar de manera automática el flujo completo de un usuario dentro de la plataforma **Urban Routes**, incluyendo:

* Definición de ruta (origen y destino)
* Selección del tipo de servicio
* Verificación de número telefónico mediante código
* Registro de método de pago
* Envío de mensajes al conductor
* Solicitud de extras (como manta, pañuelos o helado)
* Espera de confirmación del conductor

Las pruebas automatizadas simulan la interacción real de un usuario utilizando **Selenium WebDriver** y verifican que cada paso del proceso funcione correctamente.

---

## Tecnologías Utilizadas

### Python

Lenguaje principal utilizado para escribir la lógica de automatización y las pruebas.

### Selenium WebDriver

Framework de automatización utilizado para interactuar con el navegador web y simular acciones de usuario como:

* Hacer clic en botones
* Escribir en formularios
* Esperar elementos dinámicos
* Validar contenido en pantalla

### ChromeDriver

Driver utilizado para controlar el navegador **Google Chrome** durante la ejecución de las pruebas.

### Page Object Model (POM)

Se utiliza el patrón **Page Object Model**, donde la clase `UrbanRoutesPage` encapsula:

* Selectores de elementos
* Acciones de usuario
* Métodos reutilizables

Esto mejora:

* la mantenibilidad
* la reutilización de código
* la claridad de las pruebas

### Selenium CDP (Chrome DevTools Protocol)

El proyecto utiliza **CDP logs** para capturar el **código de confirmación telefónica** desde las respuestas de red del navegador mediante la función:

```
retrieve_phone_code()
```

Esto permite automatizar el proceso de verificación SMS sin intervención manual.

---

## Estructura del Proyecto

```
project/
│
├── main.py          # Script principal con las pruebas automatizadas
├── data.py          # Datos de prueba (URL, teléfonos, tarjetas, direcciones)
└── README.md        # Documentación del proyecto
```

---

## Funcionalidades Automatizadas

Las pruebas automatizan el siguiente flujo:

1. Abrir la aplicación Urban Routes
2. Introducir dirección de origen y destino
3. Solicitar un taxi
4. Seleccionar servicio **Comfort**
5. Registrar número de teléfono
6. Recuperar automáticamente el código de confirmación
7. Agregar método de pago con tarjeta
8. Escribir mensaje para el conductor
9. Solicitar productos adicionales (helado)
10. Esperar confirmación del conductor

---

## Requisitos

Antes de ejecutar las pruebas asegúrate de tener instalado:

* Python **3.9+**
* Google Chrome
* ChromeDriver compatible con tu versión de Chrome

Instalar dependencias:

```bash
pip install selenium
```

---

## Configuración de Datos de Prueba

El archivo `data.py` debe contener variables como:

```python
urban_routes_url = "URL_DE_LA_APLICACION"

address_from = "Dirección origen"
address_to = "Dirección destino"

phone_number = "+123456789"

card_number = "1234123412341234"
card_code = "123"
```

---

## Cómo Ejecutar las Pruebas

Ejecuta el script directamente con Python:

```bash
python main.py
```

Durante la ejecución:

1. Se abrirá Chrome automáticamente
2. Se ejecutará el flujo completo de pruebas
3. Al finalizar, el navegador se cerrará automáticamente

---

## Pruebas Incluidas

### test_set_route

Esta prueba valida:

* Entrada correcta de direcciones
* Solicitud de taxi
* Verificación de teléfono
* Registro de tarjeta
* Envío de mensaje al conductor
* Selección de extras
* Confirmación de llegada del conductor

---

## Buenas Prácticas Implementadas

El proyecto implementa varias buenas prácticas de automatización:

* **Page Object Model**
* **Separación de datos de prueba**
* **Uso de esperas explícitas**
* **Validaciones con assertions**

---


## Autor

Ing. Daniel Espinosa