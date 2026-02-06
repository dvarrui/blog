
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

snoopy = Perro("Snoopy")
snoopy.ladrar()  #=> [Snoopy] Guau

garfield = Gato("Garfield")
Perro.ladrar(garfield) #=> [Garfield] Guau
