[<< back](../README.md)

```text
Fecha : 20260206
Autor : David Vargas
```

# POO Python

En Python
* al tener "ocultación por protocolo", 
* que los objetos guardan los atributos en diccionarios,
* y que las clases guardan los métodos de instancia en diccionarios.

> Todo esto está explicado en el [post diccionario](20260108.diccionario.md)

Se llega a la "extraña", y entiendo que "poco" deseable situación (para un desarrollador POO "clásico"), que un objeto de la clase `Gato` puede utilizar los métodos de la clase `Perro`. Esto es, un "Gato" se comporta como un "Perro".

```text
¿El Gato es un Perro?
```

Ejemplo [gato-es-perro.py](./samples/gato-es-perro.py):

```python
# PASO 1: Creamos las clases
class Perro:
  def __init__(self, nombre):
    self.nombre = nombre

  def ladrar(self):
    print(f'[{self.nombre}] Guau')

class Gato:
  def __init__(self, nombre):
    self.nombre = nombre

  def mauyar(self):
    print(f'[{self.nombre}] Miau')

# PASO 2: Creamos los objetos
snoopy = Perro("Snoopy")
garfield = Gato("Garfield")

# PASO 3 : Gato es perro, usando las clases de forma "inapropiada"
snoopy.ladrar()        #=> [Snoopy] Guau
Perro.ladrar(garfield) #=> [Garfield] Guau
```

_Esto me ha hecho un "crack mental" al mismo tiempo que me ha "liberado de mis cadenas Pitónicas"_
