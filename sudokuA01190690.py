# Autor: Iker Arbulu Lozano
# v1.0 Mar/13/2016
# Tarea 5 de Sistemas Inteligentes
# Solving Every Sudoku Puzzle - Peter Norvig

# Terminos a considerar:
# Columnas van del 1 al 9
# Renglones van de la A a la I
# Cada coleccion de 9 casillas se les llamara unidad
# Las unidades van a nivel renglon, a nivel columna y a nivel cuadrante (3X3)

# Empezamos definiendolos metodos para crear el grid de juego

# Metodo para hacer el producto cruz
def cross(A, B):
    # Utilizamos comprension de listas para crear el producto cruz
    return [a+b for a in A for b in B]

# Variables globales para el grid
digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
# Cada una de las casillas
squares = cross(rows, cols)

unitlist = ([cross(rows, c) for c in cols] + # Se crean los renglones
            [cross(r, cols) for r in rows] + # Se crean las columnas
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) #Se crean los cuadrantes

# Se crea un diccionario para todas las unidades esto se crea al saber que
# units es un diccionario donde cada cuadrado mapea a la lista de unidades que conforman
# el cuadrado
units = dict((s, [u for u in unitlist if s in u])
            for s in squares)

# Se crea un diccionario para todos los vecinos de la unidad
# donde cada cuadrado s mapea a la serie de cuadrados formados por la union
# de cuadrados en la unidad de s, pero sin s
peers = dict((s, set(sum(units[s],[]))-set([s]))
            for s in squares)

# Creamos las pruebas para que cumpla con las reglas del juego
def test():
    # Revisar que haya 81 cuadrados
    assert len(squares) == 81
    # Revisar que haya un total de 27 sets (cuadrantes + renglones + columnas)
    assert len(unitlist) == 27
    # Revisar que tenga 3 unidades con las cuales relacionarse (1 cuadrante + 1 renglon + 1 columna)
    assert all(len(units[s]) == 3 for s in squares)
    # Revisar que cuente con 20 otras casillas con las cuales relacionarse
    assert all(len(peers[s]) == 20 for s in squares)
    # Probar cuales son las unidades de una casilla
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], # Su renglon
                            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],# Su columna
                            ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']] # Su cuadrante
    # Probar cuales son las casillas companeras de una casilla
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', # En el renglon
                                'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', # En la columna
                                'A1', 'A3', 'B1', 'B3']) #En su cuadrante
    print 'All tests pass.'


# Para la estructura de datos se utilizara un diccionario, donde cada
# llave es cad una de las casillas y el valor para esta llave seria un string
# con su numero, o los numeros posibles, esto recibe de entrada un grid o matriz
def parse_grid(grid):
    # Values es el diccionario que tiene todos los valores posibles para una casilla
    values = dict((s, digits) for s in squares)
    # Hacemos la revision para cada item de grid_values que es un diccionario
    for s,d in grid_values(grid).items():
        # Hacemos una asignacion de todos los valores posibles en nuestro diccionario (s llaves y d valores)
        # revisando que d este dentro de los digitos posibles (que no haya basura)
        if d in digits and not assign(values, s, d):
            # Regresamos falso en caso de no poder asignar el numero en la casilla y por lo tanto
            # los valores iniciales lo hacen ser sin solucion
            return False
    # Regresa el diccionario con solucion
    return values

# Funcion que traduce los numeros del grid a diccionario de casillas con chars
def grid_values(grid):
    # Convertimos el grid que entra a sus restricciones o vacios todo a chars
    chars = [c for c in grid if c in digits or c in '0.']
    # Checar que tengamos 81 caracteres
    assert len(chars) == 81
    # Entonces hacemos las parejas de llaves con los valores de cada char para esa llave
    return dict(zip(squares, chars))

# Funcion que revisa cuales son las asignaciones posibles para el diccionario
def assign(values, s, d):
    # Guardamos en un string de otros valores eliminando la d de nuestro string de nuestra llave a analizar
    other_values = values[s].replace(d, '')
    # Mandamos a eliminar todos los valores que no sean d de nuestro string, si se pudieron eliminar
    if all(eliminate(values, s, d2) for d2 in other_values):
        # Regresa los valores
        return values
    else:
        # Sino regresa Falso
        return False

# Funcion que elimina los d valores de un string
def eliminate(values, s, d):
    # Checar si ya estan eliminados
    if d not in values[s]:
        # Ya estan eliminados a regresar los valores tal cual
        return values
    # Remplaza todos los valores por e vacio
    values[s] = values[s].replace(d,'')


    ## Tactica 1: Si una casilla s se reduce a un valor, entonces elimina este valor de sus companeros.

    # Checar que no quede vacio
    if len(values[s]) == 0:
        # Si queda vacio es un error
        return False
    # Si queda uno solo tomamos la tactica 1
    elif len(values[s]) == 1:
        # Tomamos el valor que quedo
        d2 = values[s]
        # Pasamos a eliminar este valor de sus companeros
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            # Si no pudimos eliminarlo de sus companeros entonces hay contradiccion
            return False

    ## Tactica 2: Si una unidad tiene una sola casilla disponible para un valor, entonces asignalo ahi.

    # Para cada una en la unidad a analizar de nuestra llave
    for u in units[s]:
        # Checar todas las posibilidades para un valor en especifico de esta unidad de la llave
        dplaces = [s for s in u if d in values[s]]
    # Si la longitud es 0 no hay lugar para este valor
    if len(dplaces) == 0:
        # Esto es un error
        return False
    # Si la longitud es 1 entonces solo hay una posibilidad entonces
    elif len(dplaces) == 1:
        # Asignala ahi y revisa que se pueda
        if not assign(values, dplaces[0], d):
            # Si no se puede es un error
            return False
    # Regresa los valores resultantes
    return values

# Hacemos un metodo para desplegar nuestro sudoku de manera 2-D
def display(values):
    # Definimos nuestro ancho con la longitud de los valores de s que esten dentro de nuestros cuadrados
    width = 1+max(len(values[s]) for s in squares)
    # Separamos los cuadrantes con un + en sus esquinas y con un - en sus renglones
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        # Separamos las columnas entre cuadrantes con un menos si es el espacio 3 o 6
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                    for c in cols)
        # Imprimir una linea para cada C o F, para que se imprima despues y separe
        if r in 'CF': print line
    print

# Debido a que existen algunos sudokus que no tienen soluciones claras con la tactica 1 y 2
# tendremos que usar satisfaccion de restricciones y busqueda a profundidad para llegar a la solucion

# Metodo a llamar para resolver cualquier sudoku, utiliza el metodo parse_grid anterior
def solve(grid): return search(parse_grid(grid))

# Metodo que hace la busqueda por profundidad utilizando las restricciones
def search(values):
    # El sudoku es imposible de resolver como se plantea
    if values is False:
        return False
    # Si ya esta resuelto con las tacticas 1 y 2 dejalo asi
    if all(len(values[s]) == 1 for s in squares):
        return values
    # Vamos a utilizar la tecnica de minimum remaining values para saber por que rama irnos primero
    # siempre y cuando esta rama tenga mas de una posibilidad
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    # Realiamos una copia de los valores para no tener que guardar estados y hacemos la busqueda
    # dentro de la nueva asignacion que nos regresa la secuencia que sea cierta
    return some(search(assign(values.copy(), s, d))
            for d in values[s])

# Regresa algun elemento de la secuencia que sea cierto
def some(seq):
    # Regresar alguna secuencia que sea cierta
    for e in seq:
        if e: return e
    return False

# Ejemplo sencillo que se resuelve con la tecnica 1 y 2
grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

display(solve(grid1))

# Ejemplo dificil
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

display(solve(grid2))
