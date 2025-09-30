# Ejemplo de Salida CSV

Este archivo muestra un ejemplo de cómo se vería el CSV generado por el scraper.

## Formato

El CSV contiene las siguientes columnas:
- **nombre**: Nombre del producto
- **precio**: Precio del producto (puede incluir precio en oferta)
- **disponibilidad**: Estado del producto (Disponible/Agotado)
- **enlace**: URL completa del producto
- **imagen**: URL de la imagen del producto

## Ejemplo de contenido:

```csv
nombre,precio,disponibilidad,enlace,imagen
Alimento Perro Adulto 15kg,45.000$,Disponible,https://doctorpet.co/producto/alimento-perro-adulto-15kg/,https://doctorpet.co/images/producto1.jpg
Alimento Gato Cachorro 3kg,28.000 $,Agotado,https://doctorpet.co/producto/alimento-gato-cachorro-3kg/,https://doctorpet.co/images/producto2.jpg
Snacks Naturales para Perro,12.500 $,Disponible,https://doctorpet.co/producto/snacks-naturales-perro/,https://doctorpet.co/images/producto3.jpg
```

## Cómo usar el CSV

### En Excel:
1. Abre Excel
2. Archivo > Abrir
3. Selecciona el archivo CSV
4. Si los caracteres especiales no se ven bien:
   - Datos > Desde texto/CSV
   - Origen del archivo: 65001: Unicode (UTF-8)

### En Google Sheets:
1. Abre Google Sheets
2. Archivo > Importar
3. Selecciona el archivo CSV
4. Configuración de importación: UTF-8

### En Python:
```python
import pandas as pd

# Leer el CSV
df = pd.read_csv('doctorpet_alimentos_20250930_180515.csv')

# Ver primeras filas
print(df.head())

# Filtrar solo productos disponibles
disponibles = df[df['disponibilidad'] == 'Disponible']

# Ordenar por precio (necesitarás limpiar el formato primero)
```

### Con LibreOffice Calc:
1. Abre LibreOffice Calc
2. Archivo > Abrir
3. Selecciona el archivo CSV
4. En el diálogo de importación:
   - Conjunto de caracteres: UTF-8
   - Separador: Coma
