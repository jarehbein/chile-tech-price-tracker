import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# Configuración para textos en español
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

def visualizar_tendencias():
    """Genera gráficos de tendencias de precios para todos los productos"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv. Ejecuta scraper.py primero.")
        return
    
    # Leer datos
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    productos = df['producto'].unique()
    num_productos = len(productos)
    
    if num_productos == 0:
        print("No hay productos en la base de datos")
        return
    
    print(f"Generando gráficos para {num_productos} producto(s)...\n")
    
    # Crear figura con subplots
    fig, axes = plt.subplots(num_productos, 1, figsize=(12, 5 * num_productos))
    
    # Si solo hay un producto, axes no es una lista
    if num_productos == 1:
        axes = [axes]
    
    for idx, producto in enumerate(productos):
        df_prod = df[df['producto'] == producto].sort_values('fecha')
        
        ax = axes[idx]
        
        # Plotear línea de tendencia
        ax.plot(df_prod['fecha'], df_prod['precio'], 
                marker='o', linewidth=2, markersize=6, 
                color='#2E86AB', label='Precio')
        
        # Líneas de referencia
        precio_min = df_prod['precio'].min()
        precio_max = df_prod['precio'].max()
        precio_promedio = df_prod['precio'].mean()
        
        ax.axhline(y=precio_min, color='green', linestyle='--', 
                   alpha=0.7, label=f'Mínimo: ${precio_min:,.0f}')
        ax.axhline(y=precio_max, color='red', linestyle='--', 
                   alpha=0.7, label=f'Máximo: ${precio_max:,.0f}')
        ax.axhline(y=precio_promedio, color='orange', linestyle=':', 
                   alpha=0.7, label=f'Promedio: ${precio_promedio:,.0f}')
        
        # Marcar el precio actual
        precio_actual = df_prod.iloc[-1]['precio']
        fecha_actual = df_prod.iloc[-1]['fecha']
        ax.scatter([fecha_actual], [precio_actual], 
                   color='red', s=150, zorder=5, 
                   label=f'Actual: ${precio_actual:,.0f}')
        
        # Configurar título y labels
        ax.set_title(f'Tendencia de Precio - {producto}', 
                     fontweight='bold', pad=15)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Precio (CLP)')
        
        # Formatear eje Y con separadores de miles
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Formatear eje X con fechas
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Grid para mejor lectura
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
        # Leyenda
        ax.legend(loc='best', framealpha=0.9)
        
        # Resaltar si está en mínimo histórico
        if precio_actual == precio_min and len(df_prod) > 1:
            ax.text(0.02, 0.98, '¡PRECIO MÍNIMO!', 
                    transform=ax.transAxes,
                    fontsize=11, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        print(f"Gráfico generado para: {producto}")
    
    plt.tight_layout()
    
    # Crear carpeta de gráficos si no existe
    if not os.path.exists('graficos'):
        os.makedirs('graficos')
    
    # Guardar gráfico
    filename = f'graficos/tendencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nGráfico guardado en: {filename}")
    
    # Mostrar gráfico
    plt.show()

def visualizar_comparacion():
    """Genera un gráfico comparativo de todos los productos"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv")
        return
    
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    productos = df['producto'].unique()
    
    if len(productos) < 2:
        print("Necesitas al menos 2 productos para hacer una comparación")
        return
    
    print(f"Generando comparación de {len(productos)} productos...\n")
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']
    
    for idx, producto in enumerate(productos):
        df_prod = df[df['producto'] == producto].sort_values('fecha')
        color = colores[idx % len(colores)]
        
        ax.plot(df_prod['fecha'], df_prod['precio'], 
                marker='o', linewidth=2, markersize=5,
                color=color, label=producto, alpha=0.8)
        
        print(f"Agregado: {producto}")
    
    ax.set_title('Comparación de Precios - Todos los Productos', 
                 fontweight='bold', fontsize=14, pad=20)
    ax.set_xlabel('Fecha', fontweight='bold')
    ax.set_ylabel('Precio (CLP)', fontweight='bold')
    
    # Formatear eje Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Formatear eje X
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', framealpha=0.95, fontsize=9)
    
    plt.tight_layout()
    
    # Guardar
    if not os.path.exists('graficos'):
        os.makedirs('graficos')
    
    filename = f'graficos/comparacion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nGráfico comparativo guardado en: {filename}")
    
    plt.show()

def visualizar_estadisticas():
    """Genera gráfico de barras con estadísticas de precios"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv")
        return
    
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    productos = df['producto'].unique()
    
    print(f"Generando estadísticas de {len(productos)} producto(s)...\n")
    
    # Calcular estadísticas
    stats = []
    for producto in productos:
        df_prod = df[df['producto'] == producto]
        stats.append({
            'producto': producto,
            'actual': df_prod.sort_values('fecha').iloc[-1]['precio'],
            'minimo': df_prod['precio'].min(),
            'maximo': df_prod['precio'].max(),
            'promedio': df_prod['precio'].mean()
        })
    
    df_stats = pd.DataFrame(stats)
    
    # Gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(len(df_stats))
    width = 0.2
    
    ax.bar([i - width*1.5 for i in x], df_stats['minimo'], width, 
           label='Mínimo', color='#2E86AB', alpha=0.8)
    ax.bar([i - width*0.5 for i in x], df_stats['actual'], width, 
           label='Actual', color='#F18F01', alpha=0.8)
    ax.bar([i + width*0.5 for i in x], df_stats['promedio'], width, 
           label='Promedio', color='#6A994E', alpha=0.8)
    ax.bar([i + width*1.5 for i in x], df_stats['maximo'], width, 
           label='Máximo', color='#C73E1D', alpha=0.8)
    
    ax.set_title('Estadísticas de Precios por Producto', 
                 fontweight='bold', fontsize=14, pad=20)
    ax.set_ylabel('Precio (CLP)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([p[:30] + '...' if len(p) > 30 else p 
                        for p in df_stats['producto']], 
                       rotation=45, ha='right')
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Guardar
    if not os.path.exists('graficos'):
        os.makedirs('graficos')
    
    filename = f'graficos/estadisticas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Gráfico de estadísticas guardado en: {filename}\n")
    
    plt.show()

if __name__ == "__main__":
    print("=" * 70)
    print("GENERADOR DE GRÁFICOS - Chile Tech Price Tracker")
    print("=" * 70)
    print()
    
    # Generar todos los gráficos
    visualizar_tendencias()
    print("\n" + "-" * 70 + "\n")
    
    visualizar_comparacion()
    print("\n" + "-" * 70 + "\n")
    
    visualizar_estadisticas()
    
    print("=" * 70)
    print("Todos los gráficos han sido generados")
    print("Revisa la carpeta 'graficos/' para ver las imágenes")
    print("=" * 70)
