import re
import time
import random
import sys
import json

# --- MEMORIA CENTRAL ---
memoria = {}

# --- PALETA DE COLORES ---
COLORES = {
    "rojo": "\033[31m", "verde": "\033[32m", "amarillo": "\033[33m",
    "azul": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
    "blanco": "\033[37m", "reset": "\033[0m"
}

def interprete_flexdot(codigo):
    global memoria
    lineas = codigo.split('\n')
    saltar_bloque = False 
    bloque_finalizado = False
    i = 0 
    
    while i < len(lineas):
        linea_original = lineas[i]
        linea = linea_original.strip()
        
        if not linea or linea.startswith("#"): 
            i += 1; continue 

        # --- REGISTRO DE CAMBIOS (v2.0.1 GOLD) ---
        if linea == "version-changes":
            print(f"{COLORES['cyan']}\n--- [ FLEXDOT v2.0.1 - GOLD EDITION ] ---")
            print("LÍDER DE PROYECTO: Mr.S Y Geminis.Ia")
            print("ESTADO: Estable | Parche de visualización aplicado")
            print(f"-------------------------------------------{COLORES['reset']}\n")
            print("v0.1: Motor básico y variables.")
            print("v0.2: Interfaz Android UI.")
            print("v0.3: Lógica Check/Fail.")
            print("v0.4: Comando Input y Créditos.")
            print("v0.5: Sistema de limpieza y pausas (Clear/Wait)")
            print("v0.6: Lógica condicional avanzada (Next/Fail)")
            print("v0.7: Motor matemático y Bucle Loop")
            print("v0.8: Optimizador de memoria y Auto-Show")
            print("v0.9: Extensión UI (ui:color y ui:pos 2D)")
            print("v1.0: Motor de Listas y Utilidades (Random/Chance/Sound/Loading EL SALTO PROFESIONAL Por Implementación de Exportación Universal (.txt)")
            print("  - Persistencia de datos (file:save / file:load)")
            print("  - Formato de intercambio JSON (Estándar JS)")
            print("  - Optimización de memoria para partidas largas")
            print("v1.0a Arreglo de bugs")
            i += 1; continue

        # --- GUARDADO LIMPIO (Mr.S Filter) ---
        if linea.startswith("file:save("):
            m = re.search(r'\((.*)\)', linea)
            if m:
                nombre = m.group(1).strip()
                try:
                    # Filtramos: Solo variables reales, nada de comandos o basura visual
                    mem_limpia = {k: v for k, v in memoria.items() if not any(c in k for c in [":", "(", "show", "ui"])}
                    with open(f"{nombre}.txt", "w") as f:
                        json.dump(mem_limpia, f, indent=4)
                except Exception as e: print(f"Error: {e}")
            i += 1; continue

        if linea.startswith("file:load("):
            m = re.search(r'\((.*)\)', linea)
            if m:
                nombre = m.group(1).strip()
                try:
                    with open(f"{nombre}.txt", "r") as f:
                        memoria.update(json.load(f))
                except: pass
            i += 1; continue

        # --- MOTOR DE LISTAS ---
        if (linea.startswith("<") and ">" in linea) or (":" in linea and "(" in linea and ")" in linea):
            linea_l = linea.replace("<", "").replace(">", "").replace("(", "").replace(")", "")
            partes = linea_l.split(":", 1)
            memoria[partes[0].strip()] = [item.strip() for item in partes[1].split(",")]
            i += 1; continue

        # --- UTILIDADES ---
        if linea.startswith("util:random("):
            m = re.search(r'random\((.*),(.*)\) -> (.*)', linea)
            if m:
                min_v, max_v, var_d = m.groups()
                memoria[var_d.strip()] = random.randint(int(min_v), int(max_v))
            i += 1; continue

        if linea.startswith("util:chance("):
            m = re.search(r'chance\((.*)\) -> (.*)', linea)
            if m:
                por, var_d = m.groups()
                memoria[var_d.strip()] = "true" if random.randint(1, 100) <= int(por) else "false"
            i += 1; continue

        # --- INTERFAZ (UI) ---
        if linea.startswith("ui:loading("):
            v = re.search(r'\((.*)\)', linea).group(1).strip()
            num = int(memoria.get(v, v))
            b = num // 10
            print(f"\r{COLORES['amarillo']}[{'█' * b}{'.' * (10-b)}] {num}%{COLORES['reset']}", end="", flush=True)
            if num >= 100: print() 
            i += 1; continue

        if linea.startswith("ui:color("):
            c = re.search(r'\((.*)\)', linea).group(1).strip()
            print(COLORES.get(c, COLORES["reset"]), end="")
            i += 1; continue

        # --- MATEMÁTICAS ---
        if ":" in linea and not any(k in linea for k in ["show", "check", "next", "fail", "loop", "input", "ui:", "util:", "file:"]):
            try:
                partes = linea.split(":", 1)
                n_var, expr = partes[0].strip(), partes[1].strip()
                for var, val in memoria.items():
                    if var in expr: expr = expr.replace(var, str(val))
                memoria[n_var] = eval(expr.replace("true", "True").replace("false", "False"))
            except:
                partes = linea.split(":", 1)
                memoria[partes[0].strip()] = partes[1].strip()
            i += 1; continue

        # --- SHOW DEFINITIVO (SOLUCIÓN AL MENÚ) ---
        if linea.startswith("show("):
            cont = re.search(r'\((.*)\)', linea).group(1).strip()
            palabras = cont.split()
            final = []
            for p in palabras:
                clean_p = p.replace("s.", "")
                if clean_p in memoria:
                    val = memoria[clean_p]
                    final.append(str(val) if not isinstance(val, list) else f"[{', '.join(val)}]")
                else:
                    final.append(p) # Si no es variable, se queda el texto original
            print(" ".join(final))
            i += 1; continue

        # --- OTROS COMANDOS ---
        if linea.startswith("input("):
            v_n = re.search(r'\((.*)\)', linea).group(1).strip()
            val_in = input(f"{v_n} >> ")
            try: memoria[v_n] = float(val_in) if "." in val_in else int(val_in)
            except: memoria[v_n] = True if val_in.lower()=="true" else False if val_in.lower()=="false" else val_in
            i += 1; continue

        if linea == "clear": print("\033[H\033[J", end=""); i += 1; continue
        if linea == "sound:beep": print("\a", end="", flush=True); i += 1; continue

        if linea.startswith("wait("):
            try:
                t = re.search(r'\((.*)\)', linea).group(1)
                time.sleep(float(memoria.get(t, t)))
            except: pass
            i += 1; continue

        # --- LÓGICA DE CONTROL ---
        if linea.startswith("check "):
            c = linea.replace("check ", "").rstrip(":").strip()
            for v, val in memoria.items():
                if v in c: c = c.replace(v, str(val))
            res_c = eval(c.replace("true", "True").replace("false", "False").replace("=>", ">="))
            saltar_bloque, bloque_finalizado = not res_c, res_c
            i += 1; continue
        
        elif linea.startswith("next "):
            if bloque_finalizado: saltar_bloque = True
            else:
                cn = linea.replace("next ", "").rstrip(":").strip()
                for v, val in memoria.items():
                    if v in cn: cn = cn.replace(v, str(val))
                res_n = eval(cn.replace("true", "True").replace("false", "False").replace("=>", ">="))
                saltar_bloque, bloque_finalizado = not res_n, res_n
            i += 1; continue

        elif linea.startswith("fail:"):
            saltar_bloque = bloque_finalizado
            i += 1; continue

        if linea.startswith("loop "):
            cond = linea.replace("loop ", "").rstrip(":").strip()
            for var, val in memoria.items():
                if var in cond: cond = cond.replace(var, str(val))
            if eval(cond.replace("true", "True").replace("false", "False").replace("=>", ">=")):
                i += 1; continue
            else:
                i += 1
                while i < len(lineas) and lineas[i].startswith("  "): i += 1
                continue

        if linea == "endloop":
            temp_i = i - 1
            while temp_i >= 0:
                if lineas[temp_i].strip().startswith("loop "): i = temp_i; break
                temp_i -= 1
            else: i += 1
            continue

        if saltar_bloque and linea_original.startswith("  "): i += 1; continue
        elif not linea_original.startswith("  "): saltar_bloque = False
        i += 1

def ejecutar_archivo(ruta):
    try:
        with open(ruta, 'r') as f:
            print(f"--- [ FlexDot Engine v2.0.1 | Mr.S Edition ] ---")
            interprete_flexdot(f.read())
            print("\033[0m\n--- [ Ejecución Exitosa ] ---")
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_archivo(input("Archivo .fd >> "))
