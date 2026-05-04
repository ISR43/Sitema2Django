import math
import re

# ==================== DATOS Y CONSTANTES ====================
ARTICULOS = {
    '954': 'PVC 10MM BLANCO 0.2X4MTS',
    '955': 'PVC 10 MM BLANCO 0.2X5MTS',
    '956': 'PVC 10 MM BLANCO X 0.2X6 MTS',
    '953': 'PVC BORDE 10MM BLANCO X 3 MTS',
    '957': 'PVC 10MM UNION "H" BLANCO X 3 MTS',
    '545': 'SOLERAS 35 MM X 2,6 MTS',
    '67': 'MONTANTE 34 MM X 2,4 MTS',
    't8': 'TORNILLO FIX 8x1x3/4',
    '1157': 'TARUGO 6 mm SIN TOPE',
    't1': 'TORNILLO T1 AGUJA 8x9/16',
    '185': 'PVC AIS 200X10MM VALENCIA X 4 MTS',
    '186': 'PVC AIS 200X10MM VALENCIA X 6 MTS',
    '187': 'PVC AIS PERFIL F DE BORDE X 3 MTS',
    '1398': 'PVC AIS UNION H X 3 MTS',
    '876602': 'LANA KNAUF Earthwool 39 ALU 50 mm (24 m²)',
    '876604': 'LANA KNAUF Earthwool 39 ALU 70 mm (14,4 m²)'
}

# ==================== FUNCIONES AUXILIARES ====================
def round_up_50(num):
    return math.ceil(num / 50.0) * 50

def es_entero(num):
    return abs(num - round(num)) < 1e-9

# ==================== CÁLCULOS BASE ====================
def calcular_tablas_y_desperdicio(largo, ancho, orientacion, C):
    if orientacion == 'corto':
        N = math.ceil(largo / 0.2)
        req_len = ancho
    else:
        N = math.ceil(ancho / 0.2)
        req_len = largo

    if req_len <= C:
        piezas_por_tabla = math.floor(C / req_len)
        if piezas_por_tabla == 0: piezas_por_tabla = 1
        tables = math.ceil(N / piezas_por_tabla)
    else:
        tablas_por_fila = math.ceil(req_len / C)
        tables = N * tablas_por_fila

    total_needed = N * req_len
    total_bought = tables * C
    waste = total_bought - total_needed
    
    return {'tables': tables, 'N': N, 'req_len': req_len, 'waste': waste, 'total_needed': total_needed, 'total_bought': total_bought, 'C': C}

def mejor_largo(largo, ancho, orientacion, longitudes_disponibles):
    mejor = None
    menor_desperdicio = float('inf')
    mejor_resultado = None

    for C in longitudes_disponibles:
        res = calcular_tablas_y_desperdicio(largo, ancho, orientacion, C)
        if res['waste'] < menor_desperdicio or (res['waste'] == menor_desperdicio and mejor is not None and C > mejor):
            menor_desperdicio = res['waste']
            mejor = C
            mejor_resultado = res
            
    return mejor_resultado

def calcular_montantes(largo, ancho, orientacion):
    if orientacion == 'corto':
        div1 = ancho / 0.4
        paso1 = (div1 + 1) if es_entero(div1) else (math.ceil(div1) + 1)
        paso2 = paso1 * largo
        
        div3 = largo / 1.2
        if div3 < 2:
            paso3 = max(0, math.floor(div3) - 1)
        elif es_entero(div3):
            paso3 = max(0, div3 - 1)
        else:
            paso3 = max(0, math.floor(div3) - 1)
        paso4 = paso3 * ancho
    else:
        div1 = largo / 0.4
        paso1 = (div1 + 1) if es_entero(div1) else (math.ceil(div1) + 1)
        paso2 = paso1 * ancho
        
        div3 = ancho / 1.2
        if div3 < 2:
            paso3 = max(0, math.floor(div3) - 1)
        elif es_entero(div3):
            paso3 = max(0, div3 - 1)
        else:
            paso3 = max(0, math.floor(div3) - 1)
        paso4 = paso3 * largo
        
    return math.ceil((paso2 + paso4) / 2.6)

def calcular_perfil_h(largo, ancho, orientacion, C, req_len):
    if req_len <= C:
        return 0
    if orientacion == 'corto':
        return math.ceil(largo / 3)
    else:
        return math.ceil(ancho / 3)

def calcular_lana(area):
    if area > 29:
        return {'codigo': '876602', 'desc': ARTICULOS['876602'], 'cantidad': math.ceil(area / 24)}
    
    r50 = math.ceil(area / 24)
    w50 = (r50 * 24) - area
    
    r70 = math.ceil(area / 14.4)
    w70 = (r70 * 14.4) - area
    
    if w50 <= w70:
        return {'codigo': '876602', 'desc': ARTICULOS['876602'], 'cantidad': r50}
    else:
        return {'codigo': '876604', 'desc': ARTICULOS['876604'], 'cantidad': r70}

def calcular_materiales(largo, ancho, orientacion, color=False):
    longitudes = [4, 6] if color else [4, 5, 6]
    mejor = mejor_largo(largo, ancho, orientacion, longitudes)
    
    C = mejor['C']
    tables = mejor['tables']
    req_len = mejor['req_len']
    waste = mejor['waste']
    total_needed = mejor['total_needed']
    
    waste_pct = round((waste / total_needed * 100), 2) if total_needed > 0 else 0

    perimetro = 2 * (largo + ancho)
    borde = math.ceil(perimetro / 3)
    h = calcular_perfil_h(largo, ancho, orientacion, C, req_len)

    if orientacion == 'corto':
        soleras = math.ceil((ancho * 2) / 2.6)
    else:
        soleras = math.ceil((largo * 2) / 2.6)

    montantes = calcular_montantes(largo, ancho, orientacion)
    area = largo * ancho
    base_tyt = area + 4 * soleras
    t8 = round_up_50(base_tyt)
    tarugos = round_up_50(base_tyt)

    paso1_t1 = 6 * montantes
    paso2_t1 = (tables * C) / 0.4
    t1 = round_up_50(paso1_t1 + paso2_t1)

    if color:
        codigo_placa = '185' if C == 4 else '186'
    else:
        codigo_placa = {4: '954', 5: '955', 6: '956'}.get(C, '956')
        
    desc_placa = ARTICULOS[codigo_placa]

    return {
        'orientacion': orientacion,
        'color': color,
        'C': C,
        'tables': tables,
        'codigo_placa': codigo_placa,
        'desc_placa': desc_placa,
        'borde': borde,
        'h': h,
        'soleras': soleras,
        'montantes': montantes,
        't8': t8,
        'tarugos': tarugos,
        't1': t1,
        'waste_pct': waste_pct,
        'area': area,
        'largo': largo,
        'ancho': ancho
    }

# ==================== PARSEO Y SUMA ====================
def parsear_medidas(input_str):
    tiene_multiples = '+' in input_str or '-' in input_str
    
    if not tiene_multiples:
        nums = [float(s.replace(',', '.')) for s in re.split(r'[^\d.,]+', input_str) if s.strip()]
        if len(nums) < 2: raise ValueError('Ingrese dos medidas válidas')
        a, b = nums[0], nums[1]
        return {'multiple': False, 'cielorrasos': [{'largo': max(a, b), 'ancho': min(a, b)}]}
    
    partes = re.split(r'[+\-]+', input_str)
    cielorrasos = []
    
    for parte in partes:
        if not parte.strip(): continue
        nums = [float(s.replace(',', '.')) for s in re.split(r'[^\d.,]+', parte) if s.strip()]
        if len(nums) >= 2:
            a, b = nums[0], nums[1]
            cielorrasos.append({'largo': max(a, b), 'ancho': min(a, b)})
            
    if not cielorrasos: raise ValueError('No se pudieron interpretar las medidas')
    return {'multiple': len(cielorrasos) > 1, 'cielorrasos': cielorrasos}

def sumar_materiales(lista_resultados, usar_lana):
    total = {}
    area_total = 0
    total_needed_global = 0
    waste_total = 0

    for res in lista_resultados:
        area_total += res['area']
        total_needed_global += res['tables'] * res['C'] * 0.20
        waste_total += (res['tables'] * res['C'] * 0.20) - res['area']

        items = [
            {'cod': res['codigo_placa'], 'cant': res['tables'], 'desc': res['desc_placa']},
            {'cod': '187' if res['color'] else '953', 'cant': res['borde'], 'desc': ARTICULOS['187' if res['color'] else '953']},
            {'cod': '1398' if res['color'] else '957', 'cant': res.get('h', 0), 'desc': ARTICULOS['1398' if res['color'] else '957']},
            {'cod': '545', 'cant': res['soleras'], 'desc': ARTICULOS['545']},
            {'cod': '67', 'cant': res['montantes'], 'desc': ARTICULOS['67']},
            {'cod': 't8', 'cant': res['t8'], 'desc': ARTICULOS['t8']},
            {'cod': '1157', 'cant': res['tarugos'], 'desc': ARTICULOS['1157']},
            {'cod': 't1', 'cant': res['t1'], 'desc': ARTICULOS['t1']}
        ]

        for item in items:
            if item['cant'] > 0:
                if item['cod'] not in total:
                    total[item['cod']] = {'cant': 0, 'desc': item['desc']}
                total[item['cod']]['cant'] += item['cant']

    if usar_lana:
        lana_info = calcular_lana(area_total)
        total[lana_info['codigo']] = {'cant': lana_info['cantidad'], 'desc': lana_info['desc']}

    waste_pct_global = round((waste_total / total_needed_global) * 100, 2) if total_needed_global > 0 else 0
    return {'total': total, 'area_total': area_total, 'waste_pct_global': waste_pct_global}

def calcular_pvc(medidas_input, orientacion_int, color_opc, lana_opc):
    orientacion = 'corto' if orientacion_int == 1 else 'largo'
    resultado_parseo = parsear_medidas(medidas_input)
    cielorrasos_medidas = resultado_parseo['cielorrasos']
    es_multiple = resultado_parseo['multiple']

    resultados_individuales = []
    
    for c in cielorrasos_medidas:
        res = calcular_materiales(c['largo'], c['ancho'], orientacion, color=color_opc)
        
        # Estructura simplificada por cielorraso con nombres completos y códigos
        cielorraso_data = {
            "orientacion": orientacion,
            "color": color_opc,
            "C": res['C'],
            "tables": res['tables'],
            "codigo_placa": res['codigo_placa'],
            "desc_placa": res['desc_placa'],
            
            "borde_codigo": color_opc and '187' or '953',
            "borde_nombre": ARTICULOS[color_opc and '187' or '953'],
            "borde_cant": res['borde'],
            
            "h_codigo": color_opc and '1398' or '957',
            "h_nombre": ARTICULOS[color_opc and '1398' or '957'],
            "h_cant": res['h'],
            
            "soleras_codigo": "545",
            "soleras_nombre": ARTICULOS["545"],
            "soleras_cant": res['soleras'],
            
            "montantes_codigo": "67",
            "montantes_nombre": ARTICULOS["67"],
            "montantes_cant": res['montantes'],
            
            "t8_codigo": "t8",
            "t8_nombre": ARTICULOS["t8"],
            "t8_cant": res['t8'],
            
            "tarugos_codigo": "1157",
            "tarugos_nombre": ARTICULOS["1157"],
            "tarugos_cant": res['tarugos'],
            
            "t1_codigo": "t1",
            "t1_nombre": ARTICULOS["t1"],
            "t1_cant": res['t1'],
            
            "waste_pct": res['waste_pct'],
            "area": res['area'],
            "largo": res['largo'],
            "ancho": res['ancho'],
            "articulos": ARTICULOS
        }

        if lana_opc:
            lana_res = calcular_lana(res['area'])
            cielorraso_data['lana_codigo'] = lana_res['codigo']
            cielorraso_data['lana_nombre'] = lana_res['desc']
            cielorraso_data['lana_cant'] = lana_res['cantidad']
        
        cielorraso_data['borde'] = res['borde']
        cielorraso_data['h'] = res['h']
        cielorraso_data['soleras'] = res['soleras']
        cielorraso_data['montantes'] = res['montantes']
        cielorraso_data['t8'] = res['t8']
        cielorraso_data['tarugos'] = res['tarugos']
        cielorraso_data['t1'] = res['t1']
        
        resultados_individuales.append(cielorraso_data)
    
    final_output = {
        'multiple': es_multiple,
        'cielorrasos': resultados_individuales,
        'orientacion_str': orientacion,
        'area_total': sum(r['area'] for r in resultados_individuales),
        'articulos': ARTICULOS
    }

    if es_multiple:
        total_data = sumar_materiales(resultados_individuales, lana_opc)
        final_output['consolidado'] = total_data
    
    return final_output
