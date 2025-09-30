#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Scraper para DoctorPet.co - Categoría Alimentos

Este scraper está diseñado para extraer información de productos de la categoría
de alimentos del sitio web DoctorPet.co y guardarla en formato CSV.

PATRONES APLICADOS:
- Chain of Thought Pattern: Cada sección del código incluye comentarios detallados
  explicando el razonamiento detrás de las decisiones técnicas.
- Persona Pattern: La documentación está orientada a desarrolladores junior,
  explicando conceptos básicos y mejores prácticas.

AUTOR: Scraper generado para onboarding de desarrolladores
ORIENTADO A: Desarrollador Junior
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================
# Explicación para desarrolladores junior:
# - requests: Biblioteca para hacer peticiones HTTP (como abrir una página web)
# - BeautifulSoup: Biblioteca para analizar y extraer datos de HTML
# - csv: Biblioteca estándar de Python para trabajar con archivos CSV
# - time: Para añadir pausas entre peticiones (evitar bloqueos)
# - datetime: Para añadir timestamps a los archivos generados

import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
from typing import List, Dict, Optional
import logging

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
# Chain of Thought: Usamos logging en lugar de print() porque:
# 1. Permite diferentes niveles de mensajes (DEBUG, INFO, WARNING, ERROR)
# 2. Podemos guardar los logs en archivos si es necesario
# 3. Es más profesional y facilita el debugging en producción

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONSTANTES DE CONFIGURACIÓN
# ============================================================================
# Chain of Thought: Definimos constantes al inicio del archivo porque:
# 1. Facilita la modificación de valores sin buscar en todo el código
# 2. Hace el código más mantenible y legible
# 3. Evita "magic numbers" dispersos en el código

# URL base de la categoría que queremos scrapear
BASE_URL = "https://doctorpet.co/producto-category/alimentos/"

# Headers para simular un navegador real
# Chain of Thought: Los sitios web a veces bloquean requests sin User-Agent
# porque parecen bots. Simulamos ser un navegador real para evitar bloqueos.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Configuración de delays (pausas) entre peticiones
# Chain of Thought: Añadimos delays porque:
# 1. Evita sobrecargar el servidor del sitio web
# 2. Previene que nos bloqueen por hacer muchas peticiones rápidas
# 3. Es una práctica ética de web scraping
DELAY_BETWEEN_REQUESTS = 2  # segundos entre peticiones de páginas
DELAY_BETWEEN_PRODUCTS = 0.5  # segundos al procesar cada producto

# Timeout para las peticiones HTTP
# Chain of Thought: Si una petición tarda mucho, es mejor cancelarla
# y reintentar que esperar indefinidamente
REQUEST_TIMEOUT = 30  # segundos

# Número máximo de reintentos si falla una petición
MAX_RETRIES = 3


# ============================================================================
# CLASE PRINCIPAL DEL SCRAPER
# ============================================================================
# Chain of Thought: Usamos una clase en lugar de funciones sueltas porque:
# 1. Agrupa lógica relacionada en un solo lugar
# 2. Permite reutilizar configuración (headers, session, etc.)
# 3. Facilita testing y extensión del código

class DoctorPetScraper:
    """
    Scraper para extraer información de productos de DoctorPet.co
    
    Esta clase maneja:
    - Peticiones HTTP con reintentos automáticos
    - Extracción de datos de productos
    - Manejo de paginación
    - Exportación a CSV
    
    Uso básico:
        scraper = DoctorPetScraper()
        productos = scraper.scrape_category()
        scraper.save_to_csv(productos)
    """
    
    def __init__(self, base_url: str = BASE_URL):
        """
        Inicializa el scraper
        
        Args:
            base_url: URL de la categoría a scrapear
            
        Explicación para junior:
            __init__ es el constructor, se ejecuta cuando creamos un objeto.
            Aquí inicializamos variables que usaremos en toda la clase.
        """
        self.base_url = base_url
        self.headers = HEADERS
        
        # Chain of Thought: Usamos Session en lugar de requests.get() directo porque:
        # - Reutiliza conexiones (más eficiente)
        # - Mantiene cookies automáticamente
        # - Permite configurar comportamiento común para todas las peticiones
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        logger.info(f"Scraper inicializado para: {base_url}")
    
    def _make_request(self, url: str, retries: int = MAX_RETRIES) -> Optional[requests.Response]:
        """
        Hace una petición HTTP con reintentos automáticos
        
        Args:
            url: URL a consultar
            retries: Número de reintentos si falla
            
        Returns:
            Response object si tiene éxito, None si falla
            
        Chain of Thought: Separamos la lógica de peticiones en un método privado porque:
        1. Evita repetir código de manejo de errores
        2. Centraliza la lógica de reintentos
        3. Hace el código más testeable
        
        Nota para junior: El prefijo _ en el nombre indica que es un método privado,
        no debe usarse fuera de esta clase.
        """
        for attempt in range(retries):
            try:
                logger.info(f"Haciendo petición a: {url} (Intento {attempt + 1}/{retries})")
                
                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=True  # Seguir redirecciones automáticamente
                )
                
                # Chain of Thought: Verificamos el status code porque:
                # - 200 = éxito
                # - 404 = página no encontrada
                # - 500 = error del servidor
                # - etc.
                response.raise_for_status()
                
                logger.info(f"✓ Petición exitosa: {response.status_code}")
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"⚠ Timeout en intento {attempt + 1}/{retries}")
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"⚠ Error de conexión en intento {attempt + 1}/{retries}")
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"✗ Error HTTP: {e}")
                # Si es un error 404 o similar, no tiene sentido reintentar
                if response.status_code in [404, 403, 401]:
                    return None
                    
            except Exception as e:
                logger.error(f"✗ Error inesperado: {e}")
            
            # Chain of Thought: Esperamos más tiempo entre reintentos
            # (exponential backoff) para no saturar el servidor
            if attempt < retries - 1:
                wait_time = DELAY_BETWEEN_REQUESTS * (attempt + 1)
                logger.info(f"Esperando {wait_time}s antes de reintentar...")
                time.sleep(wait_time)
        
        logger.error(f"✗ Fallo después de {retries} intentos")
        return None
    
    def _extract_product_info(self, product_element) -> Optional[Dict[str, str]]:
        """
        Extrae información de un elemento de producto
        
        Args:
            product_element: Elemento BeautifulSoup que contiene un producto
            
        Returns:
            Diccionario con la información del producto o None si falla
            
        Chain of Thought: Este método es el corazón del scraper.
        Aquí definimos QUÉ datos extraer y CÓMO encontrarlos en el HTML.
        
        La estructura típica de un producto en WooCommerce (que usa DoctorPet) es:
        <li class="product">
            <a href="...">
                <img src="..." />
                <h2>Nombre</h2>
                <span class="price">$XX</span>
            </a>
        </li>
        
        Nota para junior: Esta estructura puede variar según el sitio.
        Siempre inspecciona el HTML primero (click derecho > Inspeccionar en el navegador)
        """
        try:
            # Inicializamos el diccionario con valores por defecto
            # Chain of Thought: Usamos valores por defecto para evitar errores
            # si algún campo no se encuentra
            product_data = {
                'nombre': 'N/A',
                'precio': 'N/A',
                'disponibilidad': 'N/A',
                'enlace': 'N/A',
                'imagen': 'N/A'
            }
            
            # Extraer enlace del producto
            # Chain of Thought: Buscamos el tag <a> dentro del producto
            # porque típicamente el producto completo es clickeable
            link_element = product_element.find('a', href=True)
            if link_element:
                product_data['enlace'] = link_element['href']
            
            # Extraer nombre del producto
            # Chain of Thought: El nombre suele estar en <h2> o <h3>
            # También puede estar en un tag con class="product-title"
            title_element = (
                product_element.find('h2', class_='woocommerce-loop-product__title') or
                product_element.find('h3', class_='woocommerce-loop-product__title') or
                product_element.find('h2') or
                product_element.find('h3')
            )
            if title_element:
                product_data['nombre'] = title_element.get_text(strip=True)
            
            # Extraer precio
            # Chain of Thought: WooCommerce usa la clase 'price' para precios
            # Puede haber precios regulares y en oferta, tomamos el visible
            price_element = product_element.find('span', class_='price')
            if price_element:
                # Chain of Thought: Si hay precio en oferta, tomamos ese
                ins_price = price_element.find('ins')
                if ins_price:
                    amount = ins_price.find('span', class_='woocommerce-Price-amount')
                else:
                    amount = price_element.find('span', class_='woocommerce-Price-amount')
                
                if amount:
                    product_data['precio'] = amount.get_text(strip=True)
                else:
                    # Fallback: tomar todo el texto del precio
                    product_data['precio'] = price_element.get_text(strip=True)
            
            # Extraer imagen
            # Chain of Thought: Las imágenes de productos suelen ser el primer <img>
            # dentro del elemento del producto
            img_element = product_element.find('img')
            if img_element:
                # Chain of Thought: Las imágenes pueden estar en 'src' o 'data-src'
                # (lazy loading). Intentamos ambas.
                product_data['imagen'] = (
                    img_element.get('src') or 
                    img_element.get('data-src') or 
                    'N/A'
                )
            
            # Extraer disponibilidad
            # Chain of Thought: La disponibilidad puede estar en varios lugares:
            # - Botón "Añadir al carrito" = disponible
            # - Texto "Agotado" / "Out of stock" = no disponible
            # - Badge de stock
            add_to_cart = product_element.find('a', class_='add_to_cart_button')
            out_of_stock = product_element.find(string=lambda text: 
                text and ('agotado' in text.lower() or 'out of stock' in text.lower())
            )
            
            if out_of_stock:
                product_data['disponibilidad'] = 'Agotado'
            elif add_to_cart:
                product_data['disponibilidad'] = 'Disponible'
            else:
                # Intentar encontrar un badge de stock
                stock_badge = product_element.find('span', class_='stock')
                if stock_badge:
                    product_data['disponibilidad'] = stock_badge.get_text(strip=True)
            
            # Chain of Thought: Solo retornamos el producto si al menos
            # tenemos nombre y enlace (datos mínimos requeridos)
            if product_data['nombre'] != 'N/A' or product_data['enlace'] != 'N/A':
                return product_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error extrayendo información del producto: {e}")
            return None
    
    def _get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """
        Encuentra la URL de la siguiente página si existe paginación
        
        Args:
            soup: BeautifulSoup object de la página actual
            current_url: URL de la página actual
            
        Returns:
            URL de la siguiente página o None si no hay más páginas
            
        Chain of Thought: La paginación puede implementarse de varias formas:
        1. Enlaces <a> con class="next" o similar
        2. Enlaces numerados (1, 2, 3...)
        3. Parámetro ?paged=X en la URL
        
        Necesitamos detectar cuál usa este sitio e implementarlo.
        """
        # Buscar botón/enlace "Siguiente" o "Next"
        next_button = (
            soup.find('a', class_='next') or
            soup.find('a', class_='next-page') or
            soup.find('a', text=lambda t: t and 'siguiente' in t.lower()) or
            soup.find('a', text=lambda t: t and 'next' in t.lower())
        )
        
        if next_button and next_button.get('href'):
            next_url = next_button['href']
            # Chain of Thought: Si la URL es relativa, la convertimos a absoluta
            if not next_url.startswith('http'):
                from urllib.parse import urljoin
                next_url = urljoin(current_url, next_url)
            return next_url
        
        # Buscar paginación numérica
        pagination = soup.find('nav', class_='woocommerce-pagination')
        if pagination:
            current_page = pagination.find('span', class_='current')
            if current_page:
                # Buscar el siguiente número
                next_page_link = current_page.find_next('a', href=True)
                if next_page_link:
                    next_url = next_page_link['href']
                    if not next_url.startswith('http'):
                        from urllib.parse import urljoin
                        next_url = urljoin(current_url, next_url)
                    return next_url
        
        return None
    
    def scrape_category(self, max_pages: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Scrapea todos los productos de la categoría
        
        Args:
            max_pages: Número máximo de páginas a scrapear (None = todas)
            
        Returns:
            Lista de diccionarios con información de productos
            
        Chain of Thought: Este es el método principal que orquesta todo:
        1. Hace petición a la primera página
        2. Extrae productos
        3. Busca siguiente página
        4. Repite hasta que no haya más páginas
        
        Nota para junior: Esta es la función que llamarías desde el main()
        """
        all_products = []
        current_url = self.base_url
        page_number = 1
        
        logger.info("=" * 70)
        logger.info("INICIANDO SCRAPING DE CATEGORÍA")
        logger.info("=" * 70)
        
        while current_url:
            # Chain of Thought: Verificamos max_pages para permitir testing
            # sin scrapear todo el sitio
            if max_pages and page_number > max_pages:
                logger.info(f"Alcanzado límite de {max_pages} páginas")
                break
            
            logger.info(f"\n--- Página {page_number} ---")
            logger.info(f"URL: {current_url}")
            
            # Hacer petición a la página
            response = self._make_request(current_url)
            if not response:
                logger.error(f"No se pudo obtener la página {page_number}")
                break
            
            # Parsear HTML
            # Chain of Thought: Usamos 'lxml' como parser porque es más rápido
            # que el parser por defecto 'html.parser'
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Buscar productos en la página
            # Chain of Thought: WooCommerce usa <li class="product"> para productos
            products = soup.find_all('li', class_='product')
            logger.info(f"Encontrados {len(products)} productos en esta página")
            
            # Si no hay productos, algo puede estar mal
            if not products:
                logger.warning("⚠ No se encontraron productos. Posibles causas:")
                logger.warning("  - Estructura HTML diferente a la esperada")
                logger.warning("  - Página sin productos")
                logger.warning("  - Sitio bloqueando el scraper")
                # Guardamos muestra del HTML para debugging
                logger.debug(f"HTML preview: {soup.prettify()[:500]}")
                break
            
            # Extraer información de cada producto
            page_products = 0
            for product in products:
                product_data = self._extract_product_info(product)
                if product_data:
                    all_products.append(product_data)
                    page_products += 1
                    logger.debug(f"  ✓ Producto: {product_data['nombre']}")
                
                # Chain of Thought: Pequeña pausa entre productos para ser amigables
                time.sleep(DELAY_BETWEEN_PRODUCTS)
            
            logger.info(f"✓ Extraídos {page_products} productos de esta página")
            logger.info(f"Total acumulado: {len(all_products)} productos")
            
            # Buscar siguiente página
            next_url = self._get_next_page_url(soup, current_url)
            
            if next_url and next_url != current_url:
                logger.info(f"→ Siguiente página encontrada")
                current_url = next_url
                page_number += 1
                
                # Chain of Thought: CRÍTICO - Pausa entre páginas para no saturar el servidor
                logger.info(f"Esperando {DELAY_BETWEEN_REQUESTS}s antes de la siguiente página...")
                time.sleep(DELAY_BETWEEN_REQUESTS)
            else:
                logger.info("✓ No hay más páginas, scraping completado")
                current_url = None
        
        logger.info("=" * 70)
        logger.info(f"SCRAPING FINALIZADO: {len(all_products)} productos totales")
        logger.info("=" * 70)
        
        return all_products
    
    def save_to_csv(self, products: List[Dict[str, str]], filename: Optional[str] = None) -> str:
        """
        Guarda los productos en un archivo CSV
        
        Args:
            products: Lista de diccionarios con información de productos
            filename: Nombre del archivo (se genera automáticamente si no se provee)
            
        Returns:
            Nombre del archivo generado
            
        Chain of Thought: Guardamos en CSV porque:
        1. Es un formato universal, fácil de abrir en Excel/Google Sheets
        2. Es legible por humanos (texto plano)
        3. Es fácil de procesar con Python o cualquier otro lenguaje
        
        Nota para junior: CSV = Comma Separated Values (Valores Separados por Comas)
        """
        if not products:
            logger.warning("⚠ No hay productos para guardar")
            return ""
        
        # Generar nombre de archivo con timestamp si no se provee uno
        # Chain of Thought: Incluir timestamp evita sobrescribir archivos previos
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"doctorpet_alimentos_{timestamp}.csv"
        
        logger.info(f"\n--- Guardando resultados ---")
        logger.info(f"Archivo: {filename}")
        logger.info(f"Productos: {len(products)}")
        
        try:
            # Chain of Thought: Usamos 'utf-8-sig' para que Excel abra
            # correctamente los caracteres especiales (acentos, ñ, etc.)
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                # Las columnas del CSV serán las keys del diccionario
                fieldnames = ['nombre', 'precio', 'disponibilidad', 'enlace', 'imagen']
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escribir encabezados
                writer.writeheader()
                
                # Escribir cada producto
                for product in products:
                    writer.writerow(product)
            
            logger.info(f"✓ Archivo guardado exitosamente: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"✗ Error guardando CSV: {e}")
            raise


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================
def main():
    """
    Función principal que ejecuta el scraper
    
    Chain of Thought: Separamos la lógica en main() porque:
    1. Permite usar el scraper como módulo importable
    2. Facilita el testing
    3. Es una buena práctica en Python
    
    Nota para junior: Esta función se ejecuta cuando corres el script directamente:
    python scraper.py
    """
    logger.info("""
╔══════════════════════════════════════════════════════════════════════════╗
║                   DOCTORPET.CO WEB SCRAPER                              ║
║                    Categoría: Alimentos                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Crear instancia del scraper
        scraper = DoctorPetScraper()
        
        # Ejecutar scraping
        # Chain of Thought: Puedes limitar páginas para testing:
        # productos = scraper.scrape_category(max_pages=2)
        productos = scraper.scrape_category()
        
        # Guardar resultados
        if productos:
            filename = scraper.save_to_csv(productos)
            logger.info(f"\n🎉 ¡Scraping completado exitosamente!")
            logger.info(f"📁 Revisa el archivo: {filename}")
        else:
            logger.warning("\n⚠ No se encontraron productos para guardar")
            logger.warning("Posibles causas:")
            logger.warning("  1. El sitio web está bloqueando las peticiones")
            logger.warning("  2. La estructura HTML ha cambiado")
            logger.warning("  3. Problemas de conectividad")
            logger.warning("\nRevisa los logs arriba para más detalles")
    
    except KeyboardInterrupt:
        logger.info("\n\n⚠ Scraping interrumpido por el usuario (Ctrl+C)")
        logger.info("Los productos extraídos hasta ahora no se guardaron")
    
    except Exception as e:
        logger.error(f"\n\n✗ Error inesperado: {e}")
        logger.error("Stack trace completo:", exc_info=True)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================
# Chain of Thought: Este bloque se ejecuta solo si corremos el script directamente,
# no si lo importamos como módulo
if __name__ == "__main__":
    main()
