[<< back](../README.md)

```text
Fecha : 20260209
Autor : David Vargas
```

# OOP Python (parte 2)

Ya habíamos visto en el [post anterior](./20260206.python-oop.md) que `un Gato es un Perro`, y que, todo esto es posible porque:

* los objetos son diccionarios de atributos, 
* y las clases son diccionarios de funciones.

> Lo habíamos comentado en el [post diccionario](./20260108.diccionario.md).

Siguiendo con "nuestra locura mental" y "retorciendo" el lenguaje vamos a seguir un poco más realizando una "operación de cirujía", donde vamos coger código del Perro para "trasplantarlo" en Gato.

Ejemplo [gato-es-perro2.py](./samples/gato-es-perro2.py):

En la primera parte, tenemos las definiciones de clases y objetos.

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
```

En este último paso, "cogemos" la función `ladrar()` del `Perro`, y la "trasplamos" en `Gato`.

```python
# PASO 3 : Gato es perro por "modificación genética"

ladrar = Perro.__dict__["ladrar"]
setattr(Gato, 'ladrar', ladrar)

garfield.ladrar() #=> [Garfield] Guau
```

```text
Y... ¡el gato vuelve a ladrar!
```

_Sé que todo esto no sirve para nada, pero es muy interesante/entretenido/divertido._

> ¡Perdona Garfield, por todas las "perrerías" que te estoy haciendo!
