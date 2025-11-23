# En este programa implementamos un AFD (Autómata Finito Determinístico)
# que reconoce cadenas binarias que:
# 1) Contienen la subcadena "011" en cualquier parte.
# 2) Terminan en "0", lo cual indica que son pares.
# Estas condiciones se comprueban de forma lógica, simulando el autómata.

def accepts_contains_011_and_even(s: str) -> bool:
    # Primero verificamos si la cadena contiene el patrón "011".
    # Esto indica que el autómata llegó a su estado de aceptación por subcadena.
    contiene_011 = ("011" in s)

    # Luego comprobamos si la cadena termina en 0.
    # Si termina en 0, el número binario es par.
    termina_en_0 = (len(s) > 0 and s[-1] == '0')

    # La cadena solo se acepta si cumple ambas condiciones.
    return contiene_011 and termina_en_0


# Probamos el autómata con algunas cadenas de ejemplo para validar su funcionamiento.
tests = [
    "", "0", "011", "0110", "10110", "110",
    "1010110", "010", "00110", "0111", "1011"
]

print("=== Pruebas del autómata ===")
for t in tests:
    print(f"Cadena: {t!r:8} -> Aceptada: {accepts_contains_011_and_even(t)}")


# A continuación incluimos otra versión del autómata,
# donde simulamos de forma más “manual” los estados.
# Esta versión es útil para entender la teoría de autómatas
# desde el punto de vista del curso de Matemática Discreta.

def accepts_product_afds(s: str) -> bool:
    # Estados para detectar la subcadena "011"
    # 0 = q0 (no coincidencia)
    # 1 = q1 (hemos visto '0')
    # 2 = q2 (hemos visto '01')
    # 3 = q3 (hemos reconocido '011' -> estado aceptador)
    estado_sub = 0

    # Estado para control de paridad (último caracter leído)
    # None = cadena vacía (aún no evaluable)
    # 0 = último fue '0' → cadena potencialmente par
    # 1 = último fue '1' → cadena impar
    estado_par = None

    # Recorremos la cadena carácter por carácter
    for ch in s:
        # Transiciones del AFD para subcadena "011"
        if estado_sub == 0:
            if ch == '0': estado_sub = 1
            else: estado_sub = 0
        elif estado_sub == 1:
            if ch == '0': estado_sub = 1
            else: estado_sub = 2
        elif estado_sub == 2:
            if ch == '0': estado_sub = 3  # Hemos completado "011"
            else: estado_sub = 0
        elif estado_sub == 3:
            # Una vez que se encontró "011", se queda aceptando.
            estado_sub = 3

        # Actualizamos el estado de paridad
        if ch == '0':
            estado_par = 0
        else:
            estado_par = 1

    # Para aceptar la cadena debemos:
    # - Haber llegado al estado_sub = 3 (subcadena encontrada)
    # - Haber terminado en 0 (estado_par = 0)
    return (estado_sub == 3) and (estado_par == 0)


print("\n=== Pruebas del autómata determinista (producto de AFDs) ===")
for t in tests:
    print(f"Cadena: {t!r:8} -> Aceptada: {accepts_product_afds(t)}")
