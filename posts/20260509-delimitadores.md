[<< back](../README.md)

```text
Fecha : 20260509
Autor : David Vargas
```

# Delimitadores

**Bloques de código**

En la época de Dijsktra de formalizó la idea de que a la hora de programar necesitamos crear bloques de código. La idea de que el "goto" era dañino de alguna manera viene a decir que en programación tenemos unas estructuras básicas (o bloques): secuencial, condicional e iterativo, y por tanto debemos programar respetando estas estructuras. El uso manual del "goto" es potencialmente un peligro porque se puede infringir o no respetar estas estructuras o bloques (Código espagueti).

Al programar tenemos bloques de código. Cada bloque implica un ámbito. Hay bloques en los condicionales, en bucles, en las funciones/métodos, clases, módulos. 

Todos los lenguajes de programación que han surgido desde el artículo de Dijsktra definen bloques, pero los defienen de manera diferente.

# 1. Marcado de inicio y final

En estos lenguajes se usa una marca para el inicio del bloque (scope) y otra marca para el final del bloque.

Ejemplos de marcado inicio-fin con llaves:

* C/C++
* Java
* Rust
* Javascript
* Typescript

Ejemplos de marcado inicio-fin con `begin ... end`.

* Pascal
* Algol

Ejemplos de marcado inicio-fin con paréntesis:

* List
* Scheme
* Closure

```c
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

Resumiendo:

* Estos lenguajes marcan de forma explícita el inicio y el final de cada bloque.
* Se usan 2 tokens (keywords) extras para delimitar cada bloque.

# 2. Marca de inicio implícito y final explícito

Hay otros lenguajes que según el contexto no es necesario marcar el inicio de bloque porque esté implícito pero sí necesitan marcar el final del bloque. Por ejemplo Ruby.

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

Por ejemplo, cuando se inicia un `while` o un `if`, ya se sabe que empieza un bloque y no es necesario especificar nada más. Ponerlo añadiría redundancia innecesaria. Y sólo hay que usar el `end` para definir el cierre del bloque.

Resumiendo:

* Se marca de forma implícita el inicio y de forma explícita el final.
* Se usa 1 token (keyword) extra para delimitar cada bloque.

> **NOTA**: Ruby también tiene algunos casos de bloques con marcado principio-fin usando llaves y/o usando `do...end`.

## 3. La indentación define el bloque

La _Regla del Margen_ (Off-side Rule) establece que el alcance (scope) de una declaración se determina por su indentación (el espacio en blanco al principio de la línea). Esto es, se usa el sangrado o indentación como sistema para marcar los bloques.

Ejemplos:
* ABC
* Python
* Haskell
* F#
* Nim
* etc

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

Argumentos para tomar esta decisión de diseño:

1. **Forzar al programador a realizar el sangrado**: En el siglo pasado podía tener sentido (editores de texto con pocas funcionalidades) para obligar a que los programadores que no fueran descuidados. Hoy en día ya no tiene sentido ya que los linters e IDEs lo hacen automáticamente por nosotros.
2. **Elimina el "ruido visual"**: En el sentido de que al no tener las marcas de inicio-fin de bloque entonces hay menos texto que leer y esto se supone aumenta la "limpieza visual".

Si nos fijamos en la forma de crear los bloques vemos que si existe un marcado de bloques. Se dice que no hay nada a la vista, y que al no verse por tanto no existe y si no existe no hay. Pero esto no es del todo correcto.

Si es visual, pero lo que se visualiza son los espacios. Hay que ver los espacios, si no hay espacios no funciona. Los espacios son lo que marca el bloque, por tanto los espacios tienen sentido y utilidad. Actúan como keywords del lenguaje.

Siendo estrictos generan más ruido visual que el marcado de bloque inicio-fin. Porque en lugar de 2 tokens (keywords) al inicio y al final, tienen tantos tokens (keywords) como líneas tenga el bloque. Es un ruido visual de espacios. No podemos despreocuparnos de esos espacios porque tienen sentido y utilidad en la programación.

Estos espacios son un "keyword" no visible.
3. **Es una apuesta por la limpieza visual**: Es una "limpieza" en el sentido de "ocultación visual" de algo que si existe. Ejemplo usando un lenguaje inventado:

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

4. **Eliminando la redundancia de las llaves**: Elimina la redundacia de las llaves pero incluye redundacia de los espacios con significado.

Resumiendo:

* Se marca con espacios cada una de las líneas del bloque.
* Se usan N tokens (keyword) extra para marcar cada bloque. Tantos como líneas tenga el bloque.
