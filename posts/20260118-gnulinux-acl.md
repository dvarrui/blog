[<< back](../README.md)

```
Fecha: 20260108
Autor: David Vargas
```

# Las ACL en GNU/Linux

Las ACL son listas de control de accesos. Es otra forma de asignar permisos con otro nivel de detalle similar al empleado en los Routers Cisco y en el sistema de ficheros NTFS.

Hay que instalar el paquete `acl`, que contiene los comandos:
* `getfacl`, consultar las ACL.
* `setfacl`, modificar las ACL.

# 1. El paquete ACL de la distribución

> Enlace de interés:
> * [Actividad: permisos ACL en Debian](https://github.com/dvarrui/libro-de-actividades/blob/master/actividades/sistemas.2/permisos/permisos-acl-debian.md)
>
> Repo paquete ACL: 
> * https://cgit.git.savannah.gnu.org/cgit/acl.git
> * git://git.git.savannah.gnu.org/acl.git
> * ssh://git.savannah.gnu.org/srv/git/acl.git

## 1.1 Ejemplo

Veamos un ejemplo del clásico permiso user-group-others:

```bash
$ vdir
total 4
-rwxr-xr-x 1 david david 19 2011-02-03 22:52 holamundo*
```

Ahora veamos un ejemplo de permisos ACL con getfacl:
```bash
$ getfacl holamundo
# file: holamundo
# owner: david
# group: david
user::rwx
group::r-x
other::r-x
```

## 1.2 Activación manual

ACL añade más detalle al sistema clásico de permisos, pero para poder usar el comando `setfacl`, los ficheros deben estar en un sistema de ficheros montado con la opción `acl`. Por ejemplo si intentamos establecer permisos ACL sin haber activado antes el sistema de ficheros en modo `acl` veremos un error como este: `setfacl: holamundo: La operación no está soportada`.

Si quisiéramos habilitar ACL de manera temporal para la sesión actual, ejecutamos el siguiente comando:

```bash
mount /dev/partition -o defaults,acl /punto/de/montaje
```

Ahora podemos usar el comando mount sin parámetros para verificar que todo está montado según nuestras intenciones. Ya podemos usar el comando `setfacl` para añadir permiso de lectura
al usuario `invitado` sobre el fichero `holamundo`.

```
$ vdir
total 4
-rwxr-xr-x 1 david david 19 2011-02-03 22:52 holamundo*
$ setfacl -m u:invitado:r holamundo
```

Explicación de los parámetros del comando:

| Parámetro | Descripción |
| --------- | ----------- |
| setfacl   | Comando para poner permisos ACL |
| -m        | Modificar ACL |
| u         | Modificar un usuario  |
| invitado  | Usuario invitado |
| r         | Permiso de lectura |
| holamundo | Nombre del fichero |

* Ejecutamos `getfacl` para comprobar que el resultado es el que esperábamos.

```bash
$ getfacl holamundo
# file: holamundo
# owner: david
# group: david
user::rwx
user:invitado:r--
group::r-x
mask::r-x
other::r-x
```

> Para quitar los permisos hacemos `setfacl -x u:invitado holamundo`. Sencillo, ¿verdad?

## 1.3 Activación automática

Para que se habiliten las ACL en la partición que elijamos de forma automática al iniciar el equipo, debemos modificar el fichero `/etc/fstab`, y luego reiniciar el equipo. Este fichero define que particiones serán montadas automáticamente al iniciar el sistema, y con qué parámetros se realizará dicho montaje automático.

Ejemplo de como editar el fichero `/etc/fstab` para activar las ACL en las particiones deseadas de manera permanente:

`/dev/partición  /punto/de/montaje ext2 defaults,acl 0 2`

> En este ejemplo se asume que la partición que estamos montando tiene formato `ext2`, pero podría ser cualquier otro (Podemos usar el comando `df -hT` para ver tipo de formato que tiene cada partición).

Tras haber modificado `/etc/fstab`, es necesario reiniciar la máquina (comando reboot) para que surtan efecto los cambios.

# 2. Simulando ACL

Reflexionando sobre las funcionalidades que nos ofrece el paquete `acl` para obtener permisos de granularidad más fina (Access Control List), se me ocurre "experimentar" con los permisos estándar de los sistemas de ficheros GNU/Linux ("owner-group-others") a ver si podemos conseguir un "efecto" similar a las ACL. Vamos allá.

## 2.1 Situación de partida

Supongamos que tenemos las siguientes carpetas de los proyectos:

```
proyectos
├── proy_a
│   └── a.txt
├── proy_b
│   └── b.txt
└── proy_c
    └── c.txt
```

## 2.2 Grupos de permisos

Ahora creamos los grupos siguientes:

| Grupo     | Permisos       | Carpeta |
| --------- | -------------- | ------- |
| proy_a_rw | Read and write | proy_a  |
| proy_a_ro | Read only      | proy_a  |
| proy_b_rw | Read and write | proy_b  |
| proy_b_ro | Read only      | proy_b  |
| proy_c_rw | Read and write | proy_c  |
| proy_c_ro | Read only      | proy_c  |

De modo que si un usuario lo ponemos en los grupos `proy_a_ro` y `pry_b_rw`, tendrá permisos de lectura en el proyecto A, lectura y escritura en el proyecto B y ningún acceso en el proyecto C. Podemos saber los permisos asignados:
* Consultando el fichero `/etc/group`
* O mediante el comando `id USERNAME`

Para que todo esto funcione, habría que poder asignar a una misma carpeta permisos diferentes para el grupo `XXX_ro` y para el grupo `XXX_rw`... pero esto no es posible. Sólo podemos asignar permisos de grupo a la carpeta una única vez... seguimos pensando otra idea...

## 2.3 Los enlaces simbólicos

Creamos un enlace simbólico a cada proyecto con el mismo nombre del proyecto pero con el sufio `_ro`. Porque usaremos las carpetas originales para asignar permisos de escritura y los enlaces simbólicos para los permisos de lectura.

```
.
├── proy_a_rw
│   └── a.txt
├── proy_a_ro -> proy_a_rw
├── proy_b_rw
│   └── b.txt
├── proy_b_ro -> proy_b_rw
├── proy_c_rw
│   └── c.txt
└── proy_c_ro -> proy_c_rw
```

Creamos los grupos del apartado 2.2

```bash
sudo groupadd proy_a_rw
sudo chgrp proy_a_rw proy_a_rw

vdir

drwxr-x--- 2 david proy_a_rw 19 ene 20 18:45 proy_a_rw
lrwxrwxrwx 1 david david      6 ene 20 18:47 proy_a_ro -> proy_a_rw
```

```bash
sudo groupadd proy_a_ro 
sudo chgrp proy_a_ro proy_a_ro

vdir

drwxr-x--- 2 david proy_a_ro 19 ene 20 18:45 proy_a_rw
lrwxrwxrwx 1 david david      6 ene 20 18:47 proy_a_ro -> proy_a_rw
```

Vaya... ¡no funciona! Al asignar los permisos al enlace simbólico realmente se lo estamos asignando a la carpeta original y lo que conseguimos en volver a cambiarlo de rw a ro y de ro a rw... esto no sirve.

## 2.4 Repositorios de Git

De momento, lo único que hemos conseguido es asignar permisos de escritura a los usuarios por proyectos, simplemente agregándolos como miemnbros de los grupos respectivos:

| Grupo     | Permisos       | Carpeta   |
| --------- | -------------- | --------- |
| proy_a_rw | Read and write | proy_a_rw |
| proy_b_rw | Read and write | proy_b_rw |
| proy_c_rw | Read and write | proy_c_rw |

¿Pero y cómo resolvemos el problema de la lectura? mmm ¡Quizás no hay que hacer nada especial! Me explico. Resulta que los proyectos los tenemos en repositorios de Git, entonces tendremos:

| Usuarios de Git                   | Usuario del sistema                     |
| --------------------------------- | --------------------------------------- |
| Con permisos de escritura en Git  | Con permisos de escritura en la carpeta |
| Con permisos de lectura en Git    | Sin permisos        |

Esto simplemente significa que los usuarios de lectura sólo pueden leer el repositorio pero no pueden leer en el sistema de ficheros. Ahora basta que los usuarios de lectura se clonen el repo en su carpeta local y listo. Ya tienen una lectura "privada".

# 3. Enlaces duros

El problema es que los enlaces duros sólo funcionan con ficheros regulares no con carpetas. Pero vamos a intentar algo. Partimos de la siguiente situación:

## 3.1 Contexto inicial

```bash
proyectos
├── proy_a_rw
│   └── a.txt
├── proy_b_rw
│   └── b.txt
└── proy_c_rw
    └── c.txt
```

Tenemos las carpetas originales asociadas a su grupo `proy_X_rw`. Los usuarios dentro de este grupo tendrán permisos de lectura/escritura en dicho proyecto.

## 3.2 Probando los enlaces duros

Creamos los enlaces:
```bash
ln proy_a_rw/a.txt proy_a_ro/a.txt
ln proy_b_rw/b.txt proy_b_ro/b.txt
ln proy_c_rw/c.txt proy_c_ro/c.txt
```

```bash
drwxr-x--- 2 david proy_a_ro 19 ene 20 19:27 proy_a_ro/
drwxr-x--- 2 david proy_a_rw 19 ene 20 19:27 proy_a_rw/
drwxr-x--- 2 david proy_b_ro 19 ene 20 19:27 proy_b_ro/
drwxr-x--- 2 david proy_b_rw 19 ene 20 19:27 proy_b_rw/
drwxr-x--- 2 david proy_c_ro 19 ene 20 19:27 proy_c_ro/
drwxr-x--- 2 david proy_c_rw 19 ene 20 19:27 proy_c_rw/
```

Además todos los archivos dentro de los `proy_?_ro/*` deben tener los permisos "640".

```bash
$ vdir proy_a_ro 
total 4
-rw-rw---- 2 david proy_a_ro 14 ene 20 19:31 a.txt
```

¡Bueno! Hemos hecho mucho curro manual pero el experimento !FUNCIONA!

## 3.3 Script que lo haga automático

Ahora que sabemos que podemos usar los enlaces duros, junto con grupos y los permisos "640" para "simular" el mismo efecto que el paquete ACL... pero hacerlo manualmente es mucho trabajo, vamos a hacernos un script que lo haga todo por nosotros.

```
(Esto es lo que más me gusta. ¡Automatizar!)
CONTINUARÁ...
```