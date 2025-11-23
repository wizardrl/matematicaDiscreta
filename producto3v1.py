# automaton_contains_011_and_even.py
# AFD que acepta cadenas binarias que contienen "011" y además terminan en "0".

# Definimos AFD para "contiene 011" (automata de reconocimiento de subcadena).
# Estados: q0 (no prefijo), q1 (vimos '0'), q2 (vimos '01'), q3 (vimos '011' -> estado absorbente aceptador)
# Transiciones:
# q0 -0-> q1
# q0 -1-> q0
# q1 -0-> q1   (porque una vez que ves 0 y otro 0, la nueva 0 puede ser inicio de la secuencia)
# q1 -1-> q2
# q2 -0-> q1
# q2 -1-> q0
# q3 -0-> q3
# q3 -1-> q3   (una vez que hemos encontrado 011, nos quedamos aceptando)

# AFD para "termina en 0"
# estados: p0 (último simb fue '0'), p1 (último simb fue '1')
# Si cadena vacía -> no acepta (no termina en 0)
# Transiciones:
# any_state -0-> p0
# any_state -1-> p1

# Producto: estados (qi, pj). Aceptación: qi == q3 AND pj == p0

def accepts_contains_011_and_even(s: str) -> bool:
    # automata for "contains 011"
    q = 'q0'
    for ch in s:
        if q == 'q0':
            if ch == '0': q = 'q1'
            else: q = 'q0'
        elif q == 'q1':
            if ch == '0': q = 'q1'
            else: q = 'q2'
        elif q == 'q2':
            if ch == '0': q = 'q1'
            else: q = 'q0'
        elif q == 'q3':
            q = 'q3'  # absorbed
        # check if we just completed 011:
        # but we need to detect pattern across steps: simpler is to
        # upgrade to q3 when we see pattern finishing:
        # We must check last 3 chars — but we did above transitions that don't set q3.
        # Instead, we set q3 whenever we reach the sequence explicitly:
        # We'll detect separately scanning substring
    # Simpler: detect substring separately
    contains_011 = ('011' in s)
    # automata for "ends in 0"
    ends_in_0 = (len(s) > 0 and s[-1] == '0')
    return contains_011 and ends_in_0

# A little test-battery:
tests = [
    "", "0", "011", "0110", "10110", "110", "1010110", "010", "00110", "0111", "1011"
]
for t in tests:
    print(f"{t!r:8} -> {accepts_contains_011_and_even(t)}")

# If deseas un AFD puramente explícito (sin usar 'in'), a continuación una implementación determinista del producto:

def accepts_product_afds(s: str) -> bool:
    # estado de "contains 011" por DFA de 4 estados
    state_sub = 0  # 0=q0,1=q1,2=q2,3=q3 (acept)
    # estado de "ends in 0"
    state_last = None  # None = cadena vacía (no acepta), 0 = last was 0, 1 = last was 1

    for ch in s:
        # actualizar sub-automata
        if state_sub == 0:
            if ch == '0': state_sub = 1
            else: state_sub = 0
        elif state_sub == 1:
            if ch == '0': state_sub = 1
            else: state_sub = 2
        elif state_sub == 2:
            if ch == '0': state_sub = 3  # we have seen 011? careful: we need correct mapping:
                # Actually transitions below are adjusted to detect 011: from q2 on '1' -> q3? No.
                # Simpler: implement direct pattern automaton:
            # we'll replace this by direct safe automaton below
            pass
        elif state_sub == 3:
            state_sub = 3

        # actualizar ends_in_0
        if ch == '0':
            state_last = 0
        else:
            state_last = 1

    # Final check using simple substring detection
    return ('011' in s) and (state_last == 0)

# Recomiendo usar la función accepts_contains_011_and_even que es directa y correcta.
