[<< back](../README.md)

```
Fecha: 20260108
Autor: David Vargas
```

# El diccionario es la base

## 1. Definición de ocultación

La ocultación es un principio de diseño de software que consiste en proteger y esconder los detalles internos de cómo funciona una estructura de datos (o un objeto), **permitiendo que sólo se pueda interactuar con él a través de una interfaz controlada**. Su objetivo es la abstracción: que el resto del programa no dependa de cómo se guardan los datos.

Podemos tener:
* **Ocultación de Datos**: Impide que el estado interno (las variables) sea modificado directamente desde fuera.
* **Ocultación de Implementación**: Esconde los algoritmos o la lógica compleja. Esto es, que al usuario del objeto solo le importa el resultado de la interacción con el objeto, no los pasos intermedios.

Supongamos el ejemplo de "conducir un coche". Aquí la ocultación separa los pedales y el volante (la interfaz) del motor y la inyección (la implementación). Esto nos ayuda a conseguir los siguiente:
* **Mantenibilidad**: Si el fabricante decide cambiar el motor de gasolina por uno eléctrico no me afecta en la forma de conducir. Tú sigues usando los mismos pedales y volante. El sistema no se "rompe" porque los cambios de la implementación están ocultos tras la interfaz.
* **Seguridad de Estado**: Evita que alguien ponga el contador de velocidad en -100 km/h directamente. El objeto solo permite cambios a través de métodos que validan las peticiones/acciones sobre el objeto.
* **Reducción de la Complejidad**: El programador que usa tu objeto no necesita entender 500 líneas de código interno; solo necesita saber qué mensaje enviar. De la misma forma, no necesitamos conocer los detalles internos de la mecánica del coche para conducirlo.

> **NOTA**: A menudo se confunde la **encapsulamiento** con la ocultación. Aunque ahora nos vamos a centrar en la segunda, añadiremos un poco de acalaración:
> * Encapsulamiento: Es el acto de agrupar los datos y los métodos en una misma "cápsula" (cuerpo, célula, etc.).
> * Ocultación: Es el acto de restringir el acceso a esa cápsula para que algunas partes sean privadas y otras públicas.
>
> En resumen: El encapsulamiento es la caja, y la ocultación es el candado que decide quién puede mirar dentro de la caja.

## 2. Tipos de ocultación

Los lenguaje de programación entienden/aplicán la ocultación de distinta. Veamos algunas categorías:
* **Privacidad explícita**: es necesario usar keywords como "public" o "private" para especificar la ocultación. Ejemplo: C++. Java, Simula 72.
* **Privacidad por defecto**: Los atributos son siempre privados. Es necesario crear "getters/setters" para acceder a los atributos. Ejemplo: Smalltalk, Ruby.
* **Privacidad por convención**: Los atributos son siempre visibles pero por "protocolo" los programadores deciden respetar la privacidada. Ejemplo: Python, Perl, Simula 67.

Históricamente podemos decir que Simula 67 fue el primer lenguaje en introducir los conceptos de clases y objetos, pero en sus primeras implementaciones no tenía ocultación explícita. Si tenía herencia pero era "herencia simple", para garantizar que el camino hacia arriba en la jerarquía fuera único y predecible.

A medida que el lenguaje evolucionó (en revisiones posteriores de los años 70), se dieron cuenta de que necesitaban un control más fino para proteger la integridad de los datos e introdujeron las palabras clave HIDDEN (private) y PROTECTED.

## 3. Ocultación por "protocolo"

Mientras algunos lenguajes (como C++ o Java) crean una estructura rígida en memoria para una clase, en Python, éstas se implementan mediante diccionarios. Si miramos el atributo `__dict__`. La "apariencia" de objeto es en realidad una capa sintáctica sobre una búsqueda en un diccionario (tabla hash).

Python permite añadir atributos a un objeto en tiempo de ejecución ya que el objeto se basa en un diccionario abierto. Por ejemplo, cuando hacemos `self.nombre = "Vader"`, entre bastidores ocurre lo siguiente:

```python
# Lo que escribes:
usuario.nombre = "Vader"

# Lo que ocurre:
usuario.__dict__["nombre"] = "Vader"
```

Es conveniente que no exista ocultación en el lenguaje para que funcione la creación de atributos específicos del objeto en tiempo de ejecución. Por ejemplo:

```python
class Persona:
  def __init__(self, nombre):
    self.nombre = nombre

vader = Persona("Vader")
type(vader)     #=> <class '__main__.Persona'>
vader.__dict__  #=> {'nombre': 'Vader'}

# CREACION DE UN ATRIBUTO DE OBJETO QUE NO ESTA EN LA CLASE
vader.rol = "sith"
vader.__dict__  #=> {'nombre': 'Vader', 'rol': 'sith'}

vader.__dict__['film'] = 'Starwars'
vader.__dict__  #=> {'nombre': 'Vader', 'rol': 'sith', 'film': 'Starwars'}
```

Pero las clases también se basan en diccionarios. Cuando se llama al "método" `usuario.saludar()`, ocurre lo siguiente:

```python
usuario.saludar()
# ├── usuario.__class__                    #=> class '__main__.Persona'>
# ├── Persona.saludar(usuario)             #=> Azúcar sintáctico como llamada de funciones
# ├── Persona.__dict__["saludar"]          #=> Se localiza la función
# └── Persona.__dict__["saludar"](usuario) #=> Se ejecuta la función
```

Resumen del proceso:
1. Se obtiene la referencia de la clase del objeto.
2. Se aplica azúcar sintáctico.
3. Se busca en el `__dict__` de la clase la función `saludar()`, buscando la cadena 'saludar' en las claves del diccionario.
4. Si no se encuentra, entonces se busca en el `__dict__` de la siguiente clase en la jerarquí de ancestros.
5. Se ejecuta la función pasando como parámetro el objeto "invocador".

Tanto los objetos como las clases se basan en diccionarios:
* El Objeto: Guarda sus datos (atributos de instancia) en un diccionario.
* La Clase: Guarda el comportamiento (las funciones) en un diccionario.

# 4. La "herencia" múltiple

Sabía que C++ tenía herencia mútiple pero recientemente descubrí que Python también lo tenía. ¿Cómo se gestiona el problema de la herencia en diamante? Veamos.

Supongamos que tenemos el siguiente ejemplo: 
* la Clase A es el padre
* B y C heredan de A, 
* y la Clase D hereda de B y C.

```python
class A:
    def saludar(self): print("Hola desde A")

class B(A):
    def saludar(self): print("Hola desde B")

class C(A):
    def saludar(self): print("Hola desde C")

class D(B, C):
    pass

d = D()
d.saludar() #=> Hola desde B
```

En el objeto D tendremos el siguiente orden de diccionarios en los que se debe buscar: D -> B -> C -> A -> object.

> **OJO**: El orden es importante. Si se cambia `class D(B, C)` por `class D(C, B)`, el comportamiento del programa cambia.

## 5. El super() método

En la mayoría de los lenguajes, `super()` significa "llama a mi padre". En Python, `super()` significa "llama al siguiente en la lista de los ancestros".

* Situación esperada: Cuando la clase B llama a `super().saludar()`, se espera que llame a A (su padre).
* Situacion sorpresa: Pero si estás en la clase D, el `super()` de B ¡salta a la clase C! (que es su "hermana", no su padre).

Ejemplo:

```python
class A:
  def saludar(self): print("Hola desde A")
 
class B(A):
  def saludar(self): super().saludar()
 
class C(A):
  def saludar(self): print("Hola desde C")
 
class D(B, C):
  pass
 
d = D()
d.saludar() #=> Hola desde C
```

Si un desarrollador lee la clase B de forma aislada, creyendo entender el flujo, pensará que su ancestro directo es su padre, pero no es así. Lo que ocurre es que ese flujo es "alterado" por el orden de resolución de métodos de la clase que herede de ella. 

Todo esto, hace que la tarea de entender y predecir el comportamiento de un método solo leyendo la clase sea imposible. Es necesario conocer toda la jerarquía de herencia de todos los ancestros y calcular el orden del listado de ancestros para poder saber qué diccionario se consultará  en el siguiente paso de la herencia.

# Conclusión

* El diccionario es un elemento muy importante en la implementación de los objetos y clases de Python.
* La herencia múltiple, quizás no es muy buena idea.

---

# ANEXO

* Blog 20251205: [The Hidden Cost of Python Dictionaries (And 3 Safer Alternatives)](https://codecut.ai/hidden-cost-python-dictionaries-safer-alternatives/)

