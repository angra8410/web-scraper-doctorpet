#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script para validar la funcionalidad del scraper con HTML de ejemplo

Este script prueba:
1. Extracción de información de productos
2. Generación de CSV
3. Manejo de diferentes estructuras HTML

Orientado a: Desarrollador Junior
"""

from bs4 import BeautifulSoup
from scraper import DoctorPetScraper
import os

# HTML de ejemplo simulando la estructura de DoctorPet/WooCommerce
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <ul class="products">
        <li class="product">
            <a href="https://doctorpet.co/producto/alimento-perro-adulto-15kg/">
                <img src="https://doctorpet.co/images/producto1.jpg" alt="Producto 1"/>
                <h2 class="woocommerce-loop-product__title">Alimento Perro Adulto 15kg</h2>
                <span class="price">
                    <span class="woocommerce-Price-amount">45.000&nbsp;<span class="woocommerce-Price-currencySymbol">$</span></span>
                </span>
            </a>
            <a href="#" class="add_to_cart_button">Añadir al carrito</a>
        </li>
        
        <li class="product">
            <a href="https://doctorpet.co/producto/alimento-gato-cachorro-3kg/">
                <img src="https://doctorpet.co/images/producto2.jpg" alt="Producto 2"/>
                <h2 class="woocommerce-loop-product__title">Alimento Gato Cachorro 3kg</h2>
                <span class="price">
                    <del><span class="woocommerce-Price-amount">35.000&nbsp;$</span></del>
                    <ins><span class="woocommerce-Price-amount">28.000&nbsp;$</span></ins>
                </span>
            </a>
            <span class="stock">Agotado</span>
        </li>
        
        <li class="product">
            <a href="https://doctorpet.co/producto/snacks-naturales-perro/">
                <img data-src="https://doctorpet.co/images/producto3.jpg" alt="Producto 3"/>
                <h3>Snacks Naturales para Perro</h3>
                <span class="price">
                    <span class="woocommerce-Price-amount">12.500&nbsp;$</span>
                </span>
            </a>
            <a href="#" class="add_to_cart_button">Añadir al carrito</a>
        </li>
    </ul>
</body>
</html>
"""

def test_product_extraction():
    """
    Prueba la extracción de información de productos
    """
    print("=" * 70)
    print("TEST: Extracción de Información de Productos")
    print("=" * 70)
    
    # Crear instancia del scraper
    scraper = DoctorPetScraper()
    
    # Parsear HTML de ejemplo
    soup = BeautifulSoup(SAMPLE_HTML, 'lxml')
    products = soup.find_all('li', class_='product')
    
    print(f"\nProductos encontrados en HTML de prueba: {len(products)}")
    
    # Extraer información de cada producto
    extracted_products = []
    for i, product in enumerate(products, 1):
        print(f"\n--- Producto {i} ---")
        product_data = scraper._extract_product_info(product)
        
        if product_data:
            extracted_products.append(product_data)
            print(f"✓ Nombre: {product_data['nombre']}")
            print(f"✓ Precio: {product_data['precio']}")
            print(f"✓ Disponibilidad: {product_data['disponibilidad']}")
            print(f"✓ Enlace: {product_data['enlace']}")
            print(f"✓ Imagen: {product_data['imagen']}")
        else:
            print("✗ No se pudo extraer información")
    
    print(f"\n{'='*70}")
    print(f"Productos extraídos exitosamente: {len(extracted_products)}/{len(products)}")
    
    return extracted_products


def test_csv_generation(products):
    """
    Prueba la generación del archivo CSV
    """
    print("\n" + "=" * 70)
    print("TEST: Generación de Archivo CSV")
    print("=" * 70)
    
    scraper = DoctorPetScraper()
    
    # Generar CSV con nombre de prueba
    test_filename = "test_productos.csv"
    
    try:
        filename = scraper.save_to_csv(products, filename=test_filename)
        print(f"\n✓ CSV generado: {filename}")
        
        # Verificar que el archivo existe
        if os.path.exists(test_filename):
            file_size = os.path.getsize(test_filename)
            print(f"✓ Tamaño del archivo: {file_size} bytes")
            
            # Mostrar primeras líneas del CSV
            print("\n--- Contenido del CSV (primeras 5 líneas) ---")
            with open(test_filename, 'r', encoding='utf-8-sig') as f:
                for i, line in enumerate(f):
                    if i < 5:
                        print(line.rstrip())
                    else:
                        break
            
            print(f"\n✓ Test de CSV exitoso")
            return True
        else:
            print("✗ El archivo CSV no se creó")
            return False
            
    except Exception as e:
        print(f"✗ Error en generación de CSV: {e}")
        return False


def main():
    """
    Ejecuta todos los tests
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║               TEST SUITE - DOCTORPET SCRAPER                            ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: Extracción de productos
    products = test_product_extraction()
    
    if products:
        # Test 2: Generación de CSV
        csv_success = test_csv_generation(products)
        
        print("\n" + "=" * 70)
        print("RESUMEN DE TESTS")
        print("=" * 70)
        print(f"✓ Extracción de productos: {len(products)} productos")
        print(f"{'✓' if csv_success else '✗'} Generación de CSV: {'Exitosa' if csv_success else 'Fallida'}")
        print("=" * 70)
        
        # Limpiar archivo de prueba
        if os.path.exists("test_productos.csv"):
            os.remove("test_productos.csv")
            print("\n✓ Archivo de prueba limpiado")
    else:
        print("\n✗ No se pudieron extraer productos del HTML de prueba")
        print("Revisa la lógica de extracción en scraper.py")


if __name__ == "__main__":
    main()
