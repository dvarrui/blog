[<< back](../README.md)

```text
Fecha : 20260509
Autor : David Vargas
```

# Delimitadores

**Los bloques de código**

En la época de Dijsktra de formalizó la idea de que a la hora de programar necesitamos definir bloques de código. En el artículo "el goto es dañino" no dice que podemos y debemos programar usando las estructuras básicas (o bloques): secuencial, condicional e iterativo. El uso del "goto" es un peligro porque no respeta estas estructuras o bloques, y se genera el infame "código espagueti".

* Tenemos bloques de código al programar.
* Cada bloque implica un ámbito.
* Hay bloques en los condicionales, en bucles, en las funciones/métodos, clases, módulos. 

Todos los lenguajes de programación de alto nivel surgidos desde el artículo de Dijsktra evitan el goto y definen bloques, pero los delimitan de manera diferente. Es un tema de sintaxis, no se semántica.

# 1. Marcado de inicio y final

En estos lenguajes se usa una marca para el inicio del bloque y otra marca para el final del bloque.

- Lenguajes de marcado "inicio-fin" con llaves:
    * C/C++
    * Java
    * Rust
    * Javascript
    * Typescript
- Lenguajes de marcado "inicio-fin" con `begin ... end`.
    * Pascal
    * Algol
- Lenguajes de marcado "inicio-fin" con paréntesis:
    * List
    * Scheme
    * Closure

Ejemplos

```c
// C
#include <stdio.h>

int main() {
  int contador = 1;

  while (contador <= 5) {
    if (contador % 2 == 0) {
      printf("%d es par\n", contador);
    } else {
      printf("%d es impar\n", contador);
    }
      
    contador++;
  }
  return 0;
}
```

```rust
// Rust
fn main() {
  let mut contador = 1;

  while contador <= 5 {
    if contador % 2 == 0 {
      println!("{} es par", contador);
    } else {
      println!("{} es impar", contador);
    }

    contador += 1;
  }
}
```

```javascript
// Javascript
let contador = 1;

while (contador <= 5) {
  if (contador % 2 === 0) {
    console.log(`${contador} es par`);
  } else {
    console.log(`${contador} es impar`);
  }

  contador++;
}
```

# 2. Marca de inicio implícito y final explícito

Hay otros lenguajes que según el contexto no es necesario marcar el inicio de bloque porque está implícito, pero sí necesitan marcar el final del bloque. Por ejemplo Ruby.

```ruby
# Ruby
contador = 1

while(contador <= 5)
  if contador % 2 == 0 
    puts "#{contador} es par"
  else
    puts "#{contador} es par"
  end

  contador += 1
end
```

* Cuando se inicia un `while` o un `if`, ya se sabe que empieza un bloque y no es necesario especificar nada más. Ponerlo añade redundancia innecesaria.
* Sólo hay que usar el `end` para definir el cierre del bloque.

_**NOTA**: Ruby también tiene algunos casos de bloques con marcado principio-fin usando `{...}` y otros usando `do...end`._

## 3. La indentación define el bloque

La _Regla del Margen_ (Off-side Rule) establece que el bloque se determina por su indentación (el espacio en blanco al principio de la línea). Esto es, se usa el sangrado o indentación como sistema para definir/marcar los bloques.

Lenguajes:
* ABC
* Python
* Haskell
* F#
* Nim
* GDScript

```python
# Python
contador = 1

while(contador <= 5):
  if (contador % 2 == 0): 
    print(f"{contador} es par")
  else:
    print(f"{contador} es par")

  contador += 1
```

```python
# Nim
import strformat
var contador = 1

while contador <= 5:
  if contador % 2 == 0:
    echo &"{contador} es par"
  else:
    echo &"{contador} es impar"

  inc contador
```

```python
# GDScript
extends Node

func _ready():
  var contador = 1
    
  while contador <= 5:
    if contador % 2 == 0:
      print(str(contador) + " es par")
    else:
      print(str(contador) + " es impar")
            
    contador += 1
```

Argumentos para tomar esta decisión de diseño:

1. **Forzar al programador a realizar el sangrado**: En el siglo pasado podía tener sentido (editores de texto con pocas funcionalidades) obligar a los programadores descuidados a sangrar el código. Hoy en día no tiene sentido. Los linters e IDEs lo hacen automáticamente por nosotros.
2. **Elimina el "ruido visual"**: Se supone que no escribir marcas de "inicio-fin" de bloque hay menos texto que leer y por consiguiente, se supone que aumenta la "limpieza visual".
    - Si nos fijamos en la estructura y la forma de los bloques vemos que si existe un marcado de bloques. Se dice que no hay nada a la vista, y que al no verse por tanto no existe y si no existe no hay. Pero esto no es del todo correcto.
    - Si es visual, pero lo que se visualiza son los espacios. Hay que ver los espacios, si no hay espacios no funciona. Los espacios son lo que marca el bloque, por tanto los espacios tienen significado y afectan a la semántica del programa. Actúan como keywords no visibles del lenguaje.
    - Siendo estrictos generan más ruido visual que el marcado de bloque "inicio-fin". Porque en lugar de 2 tokens (keywords) al inicio y al final, se tienen tantos tokens (keywords) como líneas tenga el bloque. Es un "ruido visual de espacios" o verbosidad semántica. No podemos despreocuparnos de esos espacios porque tienen significado y da sentido al programa.
    - Estos espacios son un "keyword" no visible.
3. **Es una apuesta por la limpieza visual**: Es una "limpieza" en el sentido de "ocultación visual" de algo que si existe.
    - Realmente no hay "limpieza visual". Es hacer no visible algo que si tiene que existir.
    - Ejemplo usando un lenguaje inventado:

```python
# Lenguaje inventado para mostrar números en lugar de "espacios-con-significado-bloque"
0 import strformat
0 var contador = 1
0 while contador <= 5:
1 if contador % 2 == 0:
2 echo &"{contador} es par"
1 else:
2 echo &"{contador} es impar"
0 inc contador
```
4. **Eliminando la redundancia de las llaves**: Elimina la redundacia de las llaves pero incluye redundacia de los "espacios con significado".

# Resumen

| Marcado | Descripción                                          | Tokens(keywords) |
| ------- | ---------------------------------------------------- | ---------------- |
| Tipo 1  | Marcar de forma explícita el inicio y el final de cada bloque    | 2 |
| Tipo 2  | Marca de forma implícita el inicio y de forma explícita el final | 1 |
| Tipo 3  | Marcar con espacios cada una de las líneas del bloque            | N |
