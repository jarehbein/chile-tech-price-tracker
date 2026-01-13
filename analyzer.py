import pandas as pd
from datetime import datetime
import os

def analizar_precios():
    """Analiza el historial de precios y detecta cambios importantes"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv. Ejecuta scraper.py primero.")
        return
    
    # Leer datos
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("=" * 70)
    print("ANÁLISIS DE PRECIOS - Chile Tech Price Tracker")
    print("=" * 70)
    print(f"\nPeríodo: {df['fecha'].min().strftime('%Y-%m-%d')} → {df['fecha'].max().strftime('%Y-%m-%d')}")
    print(f"Total de registros: {len(df)}")
    print(f"Tiendas monitoreadas: {', '.join(df['tienda'].unique())}")
    print(f"Productos únicos: {df['producto'].nunique()}")
    
    print("\n" + "=" * 70)
    print("RESUMEN POR PRODUCTO")
    print("=" * 70)
    
    for producto in df['producto'].unique():
        df_prod = df[df['producto'] == producto].sort_values('fecha')
        
        precio_actual = df_prod.iloc[-1]['precio']
        precio_minimo = df_prod['precio'].min()
        precio_maximo = df_prod['precio'].max()
        precio_promedio = df_prod['precio'].mean()
        
        print(f"\n- {producto}")
        print(f"   Precio actual:  ${precio_actual:,.0f}")
        print(f"   Precio mínimo:  ${precio_minimo:,.0f}")
        print(f"   Precio máximo:  ${precio_maximo:,.0f}")
        print(f"   Promedio:       ${precio_promedio:,.0f}")
        
        # Detectar cambios de precio
        if len(df_prod) > 1:
            cambios = detectar_cambios(df_prod)
            if cambios:
                print(f"   Cambios detectados: {len(cambios)}")
                for cambio in cambios[-3:]:  # Últimos 3 cambios
                    emoji = "" if cambio['tipo'] == 'bajada' else ""
                    print(f"      {emoji} {cambio['fecha']}: ${cambio['precio_anterior']:,.0f} → ${cambio['precio_nuevo']:,.0f} ({cambio['porcentaje']:+.1f}%)")
        
        # Alerta de precio bajo
        if precio_actual == precio_minimo and len(df_prod) > 1:
            print(f"   ¡PRECIO MÍNIMO HISTÓRICO!")
        elif precio_actual <= precio_minimo * 1.05:  # 5% sobre el mínimo
            ahorro = precio_maximo - precio_actual
            print(f"   Buen momento para comprar (Ahorras ${ahorro:,.0f} vs precio máximo)")

def detectar_cambios(df_producto):
    """Detecta cambios de precio en el historial de un producto"""
    cambios = []
    
    for i in range(1, len(df_producto)):
        precio_anterior = df_producto.iloc[i-1]['precio']
        precio_nuevo = df_producto.iloc[i]['precio']
        
        if precio_anterior != precio_nuevo:
            porcentaje = ((precio_nuevo - precio_anterior) / precio_anterior) * 100
            cambios.append({
                'fecha': df_producto.iloc[i]['fecha'].strftime('%Y-%m-%d %H:%M'),
                'precio_anterior': precio_anterior,
                'precio_nuevo': precio_nuevo,
                'porcentaje': porcentaje,
                'tipo': 'bajada' if porcentaje < 0 else 'subida'
            })
    
    return cambios

def mejores_ofertas():
    """Identifica los productos con mejor relación precio actual vs histórico"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv")
        return
    
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("\n" + "=" * 70)
    print("MEJORES OFERTAS ACTUALES")
    print("=" * 70)
    
    ofertas = []
    
    for producto in df['producto'].unique():
        df_prod = df[df['producto'] == producto].sort_values('fecha')
        
        if len(df_prod) < 2:
            continue
        
        precio_actual = df_prod.iloc[-1]['precio']
        precio_minimo = df_prod['precio'].min()
        precio_maximo = df_prod['precio'].max()
        
        # Calcular qué tan cerca está del mínimo
        if precio_maximo != precio_minimo:
            score = ((precio_maximo - precio_actual) / (precio_maximo - precio_minimo)) * 100
        else:
            score = 100
        
        ofertas.append({
            'producto': producto,
            'precio_actual': precio_actual,
            'precio_minimo': precio_minimo,
            'ahorro_vs_maximo': precio_maximo - precio_actual,
            'score': score
        })
    
    # Ordenar por score (mayor score = mejor oferta)
    ofertas.sort(key=lambda x: x['score'], reverse=True)
    
    if ofertas:
        for i, oferta in enumerate(ofertas[:5], 1):  # Top 5
            print(f"\n{i}. {oferta['producto']}")
            print(f"   Precio: ${oferta['precio_actual']:,.0f}")
            
            if oferta['precio_actual'] == oferta['precio_minimo']:
                print(f"   ¡PRECIO MÍNIMO HISTÓRICO!")
            else:
                diff = oferta['precio_actual'] - oferta['precio_minimo']
                print(f"    Está ${diff:,.0f} sobre el mínimo histórico")
            
            if oferta['ahorro_vs_maximo'] > 0:
                print(f"   Ahorras ${oferta['ahorro_vs_maximo']:,.0f} vs precio máximo")
            
            # Barrita visual del score
            barra = "█" * int(oferta['score'] / 10) + "░" * (10 - int(oferta['score'] / 10))
            print(f"   Score: [{barra}] {oferta['score']:.0f}%")
    else:
        print("\n  No hay suficientes datos para comparar (necesitas al menos 2 registros por producto)")

def estadisticas_generales():
    """Muestra estadísticas generales del scraping"""
    
    if not os.path.exists('precios.csv'):
        print("No se encontró precios.csv")
        return
    
    df = pd.read_csv('precios.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS GENERALES")
    print("=" * 70)
    
    # Agrupar por día
    df['dia'] = df['fecha'].dt.date
    registros_por_dia = df.groupby('dia').size()
    
    print(f"\nDías con registros: {len(registros_por_dia)}")
    print(f"Promedio de productos por día: {registros_por_dia.mean():.1f}")
    print(f"Día con más registros: {registros_por_dia.max()} ({registros_por_dia.idxmax()})")
    
    # Último rastreo
    ultimo_rastreo = df['fecha'].max()
    print(f"\nÚltimo rastreo: {ultimo_rastreo.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Días desde el último rastreo
    dias_desde_ultimo = (datetime.now() - ultimo_rastreo).days
    if dias_desde_ultimo == 0:
        print(f"   Actualizado hoy")
    elif dias_desde_ultimo == 1:
        print(f"   Última actualización: hace 1 día")
    else:
        print(f"   Última actualización: hace {dias_desde_ultimo} días")

if __name__ == "__main__":
    analizar_precios()
    mejores_ofertas()
    estadisticas_generales()
    
    print("\n" + "=" * 70)
    print("Análisis completado")
    print("=" * 70)
    print("\nTip: Ejecuta 'python visualize.py' para ver gráficos de tendencias\n")
