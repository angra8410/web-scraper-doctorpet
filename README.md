# Web Scraper para DoctorPet.co - Categoría Alimentos

> 🎯 **Orientado a desarrolladores junior** - Este proyecto incluye documentación detallada y explicaciones paso a paso para facilitar el aprendizaje.

## 📋 Descripción

Este es un web scraper en Python diseñado para extraer información de productos de la categoría "Alimentos" del sitio web [DoctorPet.co](https://doctorpet.co/producto-category/alimentos/).

### ¿Qué es un web scraper?

Un web scraper es un programa que automáticamente visita páginas web y extrae información específica de ellas. Piensa en él como un "robot lector" que puede:
- Abrir páginas web
- Leer su contenido HTML
- Buscar información específica (como nombres de productos, precios, etc.)
- Guardar esa información en un formato estructurado (como CSV)

## ✨ Características

El scraper extrae la siguiente información de cada producto:
- ✅ **Nombre del producto**
- ✅ **Precio** (incluyendo precios en oferta)
- ✅ **Disponibilidad** (Disponible/Agotado)
- ✅ **Enlace** al producto
- ✅ **Imagen** del producto

Además, incluye:
- 🔄 **Manejo automático de paginación** - Recorre todas las páginas de la categoría
- ⏱️ **Delays entre peticiones** - Evita sobrecargar el servidor y ser bloqueado
- 🔁 **Reintentos automáticos** - Si una petición falla, lo intenta de nuevo
- 📊 **Exportación a CSV** - Resultados en formato fácil de abrir en Excel
- 📝 **Logging detallado** - Muestra el progreso y ayuda a detectar problemas

## 🎓 Patrones de Diseño Aplicados

Este proyecto implementa dos patrones importantes para facilitar el onboarding y comprensión:

### 1. Chain of Thought Pattern (Cadena de Pensamiento)

Cada sección del código incluye comentarios detallados explicando **por qué** se tomó cada decisión técnica, no solo **qué** hace el código.

**Ejemplo:**
```python
# Chain of Thought: Usamos Session en lugar de requests.get() directo porque:
# - Reutiliza conexiones (más eficiente)
# - Mantiene cookies automáticamente
# - Permite configurar comportamiento común para todas las peticiones
self.session = requests.Session()
```

Este patrón ayuda a:
- Entender el razonamiento detrás de las decisiones
- Aprender mejores prácticas
- Facilitar futuras modificaciones

### 2. Persona Pattern (Orientado a Desarrollador Junior)

Toda la documentación y comentarios están escritos asumiendo que el lector es un **desarrollador junior** que puede estar aprendiendo:
- Python
- Web scraping
- Peticiones HTTP
- Manejo de archivos CSV

**Ejemplo:**
```python
# Nota para junior: CSV = Comma Separated Values (Valores Separados por Comas)
# Es un formato universal, fácil de abrir en Excel/Google Sheets
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.7 o superior instalado en tu sistema
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/angra8410/web-scraper-doctorpet.git
cd web-scraper-doctorpet
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

**¿Qué se instalará?**
- `requests` - Para hacer peticiones HTTP (visitar páginas web)
- `beautifulsoup4` - Para analizar y extraer datos del HTML
- `lxml` - Parser rápido para BeautifulSoup

## 📖 Uso

### Uso básico

Simplemente ejecuta el script:

```bash
python scraper.py
```

El scraper:
1. Visitará la página de alimentos de DoctorPet.co
2. Extraerá información de todos los productos
3. Navegará por todas las páginas disponibles
4. Guardará los resultados en un archivo CSV con nombre automático como: `doctorpet_alimentos_20240930_143025.csv`

### Uso avanzado

Si quieres usar el scraper desde otro script Python:

```python
from scraper import DoctorPetScraper

# Crear instancia del scraper
scraper = DoctorPetScraper()

# Scrapear solo las primeras 2 páginas (útil para testing)
productos = scraper.scrape_category(max_pages=2)

# Guardar en un archivo específico
scraper.save_to_csv(productos, filename="mis_productos.csv")
```

## 📂 Estructura de Archivos

```
web-scraper-doctorpet/
│
├── scraper.py           # Script principal del scraper
├── test_scraper.py      # Script de pruebas con HTML de ejemplo
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── .gitignore          # Archivos a ignorar en git
│
└── doctorpet_alimentos_*.csv  # Archivos CSV generados (ignorados por git)
```

## 🧪 Testing

El proyecto incluye un script de pruebas (`test_scraper.py`) que valida la funcionalidad del scraper usando HTML de ejemplo.

Para ejecutar las pruebas:

```bash
python test_scraper.py
```

Esto validará:
- ✅ Extracción correcta de información de productos
- ✅ Manejo de diferentes formatos de precio (regular y en oferta)
- ✅ Detección de disponibilidad (disponible/agotado)
- ✅ Generación correcta del archivo CSV

**¿Por qué es importante testing?**

El testing con HTML de ejemplo nos permite:
1. Verificar que la lógica de extracción funciona correctamente
2. No depender de la disponibilidad del sitio web real
3. Detectar problemas antes de ejecutar el scraper completo
4. Documentar el comportamiento esperado del código

## 📊 Formato del CSV

El archivo CSV generado tiene las siguientes columnas:

| nombre | precio | disponibilidad | enlace | imagen |
|--------|--------|----------------|--------|--------|
| Alimento Perro Adulto 15kg | $45.000 | Disponible | https://... | https://... |
| Alimento Gato Cachorro 3kg | $28.000 | Agotado | https://... | https://... |

Puedes abrir este archivo con:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc
- Cualquier editor de texto

## 🔧 Modificación del Scraper

### Cambiar la categoría a scrapear

Modifica la constante `BASE_URL` en `scraper.py`:

```python
# En lugar de alimentos, scrapear otra categoría
BASE_URL = "https://doctorpet.co/producto-category/juguetes/"
```

### Ajustar los delays (pausas)

Si el sitio te está bloqueando, aumenta los delays:

```python
DELAY_BETWEEN_REQUESTS = 5  # En lugar de 2 segundos
DELAY_BETWEEN_PRODUCTS = 1  # En lugar de 0.5 segundos
```

**¿Por qué son importantes los delays?**
- Evitan sobrecargar el servidor del sitio web
- Previenen que tu IP sea bloqueada
- Son una práctica ética de web scraping

### Extraer información adicional

Si quieres extraer más datos (por ejemplo, categorías, SKU, etc.), modifica el método `_extract_product_info()`:

```python
def _extract_product_info(self, product_element):
    product_data = {
        'nombre': 'N/A',
        'precio': 'N/A',
        # ... campos existentes ...
        'categoria': 'N/A',  # Nuevo campo
    }
    
    # Extraer categoría
    category_element = product_element.find('span', class_='product-category')
    if category_element:
        product_data['categoria'] = category_element.get_text(strip=True)
    
    # ... resto del código ...
```

No olvides actualizar también el método `save_to_csv()`:

```python
fieldnames = ['nombre', 'precio', 'disponibilidad', 'enlace', 'imagen', 'categoria']
```

## 🐛 Troubleshooting (Solución de Problemas)

### Problema 1: "No se encontraron productos"

**Posibles causas:**
1. El sitio web cambió su estructura HTML
2. El sitio está bloqueando el scraper
3. Problemas de conectividad

**Soluciones:**
1. Inspecciona manualmente la página web:
   - Abre https://doctorpet.co/producto-category/alimentos/ en tu navegador
   - Click derecho > "Inspeccionar elemento"
   - Verifica que los productos tengan `class="product"`
   
2. Aumenta los delays entre peticiones
3. Verifica tu conexión a internet

### Problema 2: "Error de conexión" o "Timeout"

**Posibles causas:**
- Problemas de red
- El sitio web está caído
- Tu IP puede estar bloqueada

**Soluciones:**
1. Verifica que puedes acceder al sitio desde tu navegador
2. Espera unos minutos y vuelve a intentar
3. Aumenta el `REQUEST_TIMEOUT`:
   ```python
   REQUEST_TIMEOUT = 60  # En lugar de 30 segundos
   ```

### Problema 3: "La estructura HTML ha cambiado"

Los sitios web cambian frecuentemente. Si el scraper deja de funcionar:

1. Inspecciona la página web actual
2. Identifica las nuevas clases CSS o estructura
3. Actualiza los selectores en `_extract_product_info()`

**Ejemplo:**
Si antes era:
```python
title_element = product_element.find('h2', class_='woocommerce-loop-product__title')
```

Y ahora es:
```python
title_element = product_element.find('h2', class_='product-name')
```

### Problema 4: El archivo CSV tiene caracteres raros

Asegúrate de abrir el CSV con codificación UTF-8. En Excel:
1. Datos > Desde texto/CSV
2. Selecciona el archivo
3. Origen del archivo: 65001: Unicode (UTF-8)

## ⚠️ Consideraciones Éticas y Legales

### Buenas prácticas de web scraping:

1. **Respeta el robots.txt**: Verifica https://doctorpet.co/robots.txt
2. **No sobrecargues el servidor**: Usa delays apropiados
3. **Respeta los términos de servicio**: Lee los términos del sitio web
4. **No hagas scraping de datos personales**: Solo información pública de productos
5. **Identifícate apropiadamente**: El User-Agent incluye información real del navegador

### Limitaciones técnicas encontradas:

Durante el desarrollo se identificaron los siguientes puntos:

- **DNS/Conectividad**: En algunos entornos (como ambientes de CI/CD, contenedores, o redes corporativas), el dominio `doctorpet.co` puede no resolver correctamente debido a:
  - Configuraciones de red restrictivas
  - Restricciones DNS
  - Firewalls que bloquean ciertos dominios
  - El sitio puede estar temporalmente inaccesible
  
- **Solución implementada**: El código incluye:
  - Reintentos automáticos (hasta 3 intentos por petición)
  - Manejo robusto de errores de conexión
  - Logging detallado para facilitar diagnóstico
  - Mensajes informativos sobre posibles causas de fallo

- **Cómo probar**: Si encuentras problemas de conectividad:
  1. Verifica que puedes acceder a https://doctorpet.co desde tu navegador
  2. Ejecuta `test_scraper.py` para validar que la lógica de extracción funciona
  3. Si el sitio es accesible desde navegador pero no desde el script, puede ser necesario ajustar headers o usar proxies

### Ejemplo de salida exitosa:

Cuando el scraper funciona correctamente, verás una salida similar a:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                   DOCTORPET.CO WEB SCRAPER                              ║
║                    Categoría: Alimentos                                 ║
╚══════════════════════════════════════════════════════════════════════════╝

2025-09-30 18:03:56 - INFO - Scraper inicializado para: https://doctorpet.co/producto-category/alimentos/
2025-09-30 18:03:56 - INFO - INICIANDO SCRAPING DE CATEGORÍA
2025-09-30 18:03:56 - INFO - --- Página 1 ---
2025-09-30 18:03:58 - INFO - ✓ Petición exitosa: 200
2025-09-30 18:03:58 - INFO - Encontrados 24 productos en esta página
2025-09-30 18:04:02 - INFO - ✓ Extraídos 24 productos de esta página
2025-09-30 18:04:02 - INFO - Total acumulado: 24 productos
2025-09-30 18:04:02 - INFO - → Siguiente página encontrada
...
2025-09-30 18:05:15 - INFO - SCRAPING FINALIZADO: 72 productos totales
2025-09-30 18:05:15 - INFO - ✓ Archivo guardado exitosamente: doctorpet_alimentos_20250930_180515.csv
2025-09-30 18:05:15 - INFO - 🎉 ¡Scraping completado exitosamente!
```

## 📚 Recursos para Aprender Más

Si eres nuevo en web scraping, estos recursos te ayudarán:

1. **Python Requests**: https://docs.python-requests.org/
2. **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
3. **CSS Selectors**: https://www.w3schools.com/cssref/css_selectors.asp
4. **Ética en Web Scraping**: https://www.scraperapi.com/blog/web-scraping-laws-ethics/

## 🤝 Contribuciones

Si encuentras un bug o tienes una mejora:

1. Abre un Issue describiendo el problema
2. Si tienes una solución, crea un Pull Request
3. Asegúrate de documentar tu cambio siguiendo el patrón Chain of Thought

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 👥 Autor

Desarrollado como ejemplo educativo para onboarding de desarrolladores junior en web scraping.

---

**¿Preguntas o problemas?** Abre un issue en el repositorio y te ayudaremos.

