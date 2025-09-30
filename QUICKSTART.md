# Guía de Inicio Rápido - Web Scraper DoctorPet

> 📚 **Para desarrolladores junior** - Esta guía te llevará paso a paso desde la instalación hasta tu primer scraping exitoso.

## 🎯 ¿Qué vas a aprender?

Al seguir esta guía aprenderás:
1. Cómo instalar y configurar el scraper
2. Cómo ejecutar tu primer scraping
3. Cómo interpretar los resultados
4. Cómo solucionar problemas comunes
5. Cómo modificar el scraper para tus necesidades

## 📦 Paso 1: Preparar el Entorno

### 1.1 Verifica que tienes Python instalado

Abre tu terminal (CMD en Windows, Terminal en Mac/Linux) y ejecuta:

```bash
python3 --version
```

Deberías ver algo como: `Python 3.7.0` o superior.

**Si no tienes Python:**
- Windows: Descarga desde https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3 python3-pip`

### 1.2 Clona el repositorio

```bash
# Navega a donde quieres guardar el proyecto
cd ~/Documentos  # o la carpeta que prefieras

# Clona el repositorio
git clone https://github.com/angra8410/web-scraper-doctorpet.git

# Entra al directorio
cd web-scraper-doctorpet
```

### 1.3 Instala las dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `requests` - para hacer peticiones HTTP
- `beautifulsoup4` - para analizar HTML
- `lxml` - parser rápido para HTML

**Si tienes errores de permisos**, prueba con:
```bash
pip install --user -r requirements.txt
```

## 🧪 Paso 2: Prueba que Todo Funciona

Antes de hacer scraping real, vamos a probar con datos de ejemplo:

```bash
python3 test_scraper.py
```

Deberías ver:
```
✓ Extracción de productos: 3 productos
✓ Generación de CSV: Exitosa
```

**¿Qué acabas de probar?**
- Que todas las bibliotecas se instalaron correctamente
- Que la lógica de extracción funciona
- Que puedes generar archivos CSV

## 🚀 Paso 3: Tu Primer Scraping Real

¡Ahora sí! Vamos a scrapear datos reales:

```bash
python3 scraper.py
```

### ¿Qué está pasando?

El scraper:
1. **Se conecta** a https://doctorpet.co/producto-category/alimentos/
2. **Extrae** información de cada producto
3. **Navega** a la siguiente página automáticamente
4. **Guarda** todo en un archivo CSV

Verás mensajes como:
```
INFO - Haciendo petición a: https://doctorpet.co/...
INFO - Encontrados 24 productos en esta página
INFO - ✓ Extraídos 24 productos de esta página
```

### ⏱️ ¿Por qué es lento?

El scraper espera entre peticiones (2 segundos) para:
- No sobrecargar el servidor
- Evitar que nos bloqueen
- Ser respetuosos con el sitio web

**Esto es NORMAL y NECESARIO** - no lo aceleres sin razón.

## 📊 Paso 4: Encuentra y Abre tu CSV

### Encuentra el archivo

El CSV se guarda con nombre automático:
```
doctorpet_alimentos_20250930_180515.csv
```

El número es la fecha y hora: `AÑOMESDIA_HORAMINUTOSEGUNDO`

### Abre el archivo

**Con Excel:**
1. Abre Excel
2. Archivo > Abrir
3. Selecciona el CSV
4. Si ves caracteres raros: Datos > Desde texto/CSV > UTF-8

**Con Google Sheets:**
1. Abre Google Sheets
2. Archivo > Importar
3. Arrastra el CSV
4. Importar datos

**Con Python/Pandas:**
```python
import pandas as pd
df = pd.read_csv('doctorpet_alimentos_20250930_180515.csv')
print(df.head())
```

## 🔧 Paso 5: Personaliza el Scraper

### Cambiar la categoría

Edita `scraper.py` línea 62:

```python
# Cambiar de alimentos a juguetes
BASE_URL = "https://doctorpet.co/producto-category/juguetes/"
```

### Scrapear solo 2 páginas (para testing)

Edita `scraper.py` línea 457:

```python
# En lugar de:
productos = scraper.scrape_category()

# Usar:
productos = scraper.scrape_category(max_pages=2)
```

### Ajustar las pausas

Edita `scraper.py` líneas 82-83:

```python
DELAY_BETWEEN_REQUESTS = 3  # Más lento, más seguro
DELAY_BETWEEN_PRODUCTS = 1  # Pausa entre cada producto
```

## 🐛 Solución de Problemas Comunes

### Problema: "No se encontraron productos"

**Causa:** El sitio puede estar caído o bloqueando el scraper.

**Solución:**
1. Abre https://doctorpet.co en tu navegador - ¿funciona?
2. Si funciona, ejecuta primero `test_scraper.py` para verificar que el código funciona
3. Espera 5 minutos y reintenta

### Problema: "Error de conexión"

**Causa:** Problemas de red o el sitio no está disponible.

**Solución:**
```bash
# Verifica tu conexión
ping google.com

# Verifica que el sitio existe
curl -I https://doctorpet.co
```

### Problema: El CSV está vacío o incompleto

**Causa:** El scraper puede haberse interrumpido.

**Solución:**
- Revisa los logs en pantalla
- Si se interrumpió (Ctrl+C), reinícialo
- Los datos se guardan solo AL FINAL

### Problema: Caracteres raros en el CSV (�, �)

**Causa:** Problema de encoding.

**Solución:**
- Abre el CSV especificando UTF-8 (ver "Paso 4")
- El archivo está correcto, solo necesita abrirse bien

## 📚 Próximos Pasos

### Aprende más sobre web scraping:
1. Lee los comentarios en `scraper.py` - están pensados para enseñar
2. Modifica el scraper para extraer más datos
3. Lee el README.md completo para funcionalidad avanzada

### Proyecto de práctica:
Intenta modificar el scraper para:
1. Extraer también la categoría de cada producto
2. Filtrar solo productos disponibles
3. Ordenar por precio en el CSV

### Recursos recomendados:
- [Documentación de BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Guía de CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp)
- [Python Requests Tutorial](https://docs.python-requests.org/)

## ❓ ¿Necesitas Ayuda?

1. **Lee primero** el README.md - tiene troubleshooting detallado
2. **Revisa** los logs - el scraper te dice qué está pasando
3. **Ejecuta** test_scraper.py - verifica que el código básico funciona
4. **Abre un issue** en GitHub describiendo tu problema

## ✅ Checklist de Éxito

Marca cada paso que completes:

- [ ] Python instalado y funcionando
- [ ] Repositorio clonado
- [ ] Dependencias instaladas
- [ ] test_scraper.py ejecutado exitosamente
- [ ] scraper.py ejecutado al menos una vez
- [ ] CSV generado y abierto correctamente
- [ ] Entendido por qué son importantes los delays
- [ ] Leídos los comentarios en scraper.py

¡Si marcaste todo, estás listo para ser un web scraper! 🎉

---

**¿Tienes sugerencias para mejorar esta guía?** Abre un Pull Request o Issue.
