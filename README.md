# WiFindBar
Trabajo práctico Nº 1 - Ingeniería de Software 1+2 - FCEN, UBA


## Quickstart

    git clone git@github.com:francofrizzo/isw-tp1
    cd isw-tp1
    mkvirtualenv --python=python3 wifindbar
    pip install -U -r requirements.txt
    ./manage.py migrate
    ./manage.py loaddata wifindbar/fixtures/initial_data.json
    ./manage.py runserver

## Not-so-quick start

Si quieren, para evitar tener que instalar cosas en la máquina solo para hacer
este tp, pueden usar el dockerfile que armé. Para ello, instalen docker en
primer lugar (sobra información en internet para hacerlo). Luego, estando en el
repo de la materia, creen una carpeta `ssh` que contenga la clave ssh que
utilizan para acceder a github, ie, `mkdir ssh ; cp ~/.ssh/id_rsa{,.pub} ssh`.
Una vez hecho esto,

    docker build -t isw/tp1 .
    # espero pacientemente que se instale...
    docker run -it --rm -p 8000:8000 --name=isw isw/tp1

les dará un shell en el root del repo. Una vez ahí, con tan solo correr `source
wifindbar/bin/activate` podrán desarrollar el TP. No es necesario que corran los
comandos del quickstart a partir de `pip install...`, salvo que se hayan hecho
modificaciones a la db o se hayan cambiado los requerimientos.

Para ver los resultados, conectense a `http://localhost:8000`, después de correr
`./manage.py runserver 0.0.0.0`.
