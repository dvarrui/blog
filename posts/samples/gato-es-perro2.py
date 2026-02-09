#!/usr/bin/env python3
# El Gato es Perro v2

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

# PASO 3 : Gato es perro por "modificación genética"

ladrar = Perro.__dict__["ladrar"]
setattr(Gato, 'ladrar', ladrar)

garfield.ladrar() #=> [Garfield] Guau

