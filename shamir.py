import random
from functools import reduce

# función para encontrar el inverso modular 
def inverso_modular(a, p):
    return pow(a, p-2, p)

# función para generar un polinomio aleatorio de grado (t-1)
def generar_polinomio(secreto, t):
    coeffs = [secreto] + [random.randint(0, 1000) for _ in range(t-1)] 
    # se incluye el secreto y coeficientes aleatorios
    
    polinomio_str = "f(x) = " + " + ".join([f"{coeff}x^{i}" if i > 0 
    else f"{coeff}" for i, coeff in enumerate(coeffs)])
    print(f"Polinomio generado: {polinomio_str}")
    # se imprimie el polinomio generado
    return coeffs

# evaluación del polinomio en un punto x
def evaluar_puntos_polinomio(coeffs, x, p):
    return sum([coeff * (x ** i) % p for i, coeff in enumerate(coeffs)]) % p

# generar las partes de la clave usando el esquema de Shamir
def split_secret(secret, n, t, p=2083):  # número primo mayor para manejar 
    # valores grandes (p), este valor puede ser ajustado segun las necesidades
    """
    secret: El secreto a compartir
    n: El número de partes (fragmentos) a generar
    t: El número mínimo de partes necesarias para reconstruir el secreto (umbral)
    p: Un número primo mayor que el secreto (para la aritmética modular)
    """
    coeffs = generar_polinomio(secret, t)
    shares = [(i, evaluar_puntos_polinomio(coeffs, i, p)) for i in range(1, n+1)]
    return shares

# reconstruir el secreto usando el esquema de Shamir
def reconstruir_secreto(shares, p=2083):  # usar el mismo número primo aquí
    """
    shares: Lista de partes del secreto (fragmentos)
    p: El número primo utilizado (debe ser el mismo que el usado para dividir el secreto)
    """
    def interpolacion_lagrange(x, x_s, y_s, p):
        def producto(vals):
            return reduce(lambda a, b: a * b % p, vals, 1)
        total = 0
        for i in range(len(y_s)):
            xi, yi = x_s[i], y_s[i]
            terms = [(x - xj) * inverso_modular(xi - xj, p) % p for j, xj in 
            enumerate(x_s) if i != j]
            total += yi * producto(terms) % p
        return total % p

    x_s, y_s = zip(*shares)
    return interpolacion_lagrange(0, x_s, y_s, p)

# ejemplo de uso
if __name__ == "__main__":
    secreto = int(input("Ingrese el secreto a compartir: "))  
    n = int(input("Ingrese la cantidad de puntos a generar: "))  
    t = int(input("Ingrese el umbral mínimo de fragmentos para reconstruir el secreto: ")) 
    print("------------------------------------------------------------------------------")
    # dividir el secreto en fragmentos
    fragmentos = split_secret(secreto, n, t)
    print(f"Fragmentos generados: {fragmentos}")

    # se selecciona algunos fragmentos para reconstruir el secreto
    fragmentos_seleccionados = random.sample(fragmentos, t)
    print(f"Fragmentos seleccionados para reconstrucción: {fragmentos_seleccionados}")

    # reconstruccion del secreto
    secreto_reconstruido = reconstruir_secreto(fragmentos_seleccionados)
    print(f"Secreto reconstruido: {secreto_reconstruido}")
