# About

If you find yourself having different `docker-compose` projects spreading around your
machine, and you are tired of switching the directories all then time, then `doca` is a small helper for you.

`doca` keeps track of all your project an wrapps around `docker-compose` to easyly interact with your
projects. You don't have to remember an new set of commands. Nearly all `doca` commands are the same as `docker-compose`
(because most of them are simply forwarded).

# Requirements
`doca` uses poetry for dependency management. You may follow the installation instruction at https://python-poetry.org/docs/#installation
Since `doca` is a wrapper around `docker-compose`, `docker-compose` must be installed and executable by the
user running `doca`

# Installation
Currently there is no official pypi-Package for `doca`. You have to install it by yourself. Thanks to poetry 
this is quite simple:
```
    $ git clone git@github.com:soerenbe/doca.git
    $ cd doca
    $ poetry build
    $ pip install --user dist/doca-<version>.tar.gz
```
# Configuration

By default `doca` searches your home directory for `docker-compose.yml` files and use this directories
as projects to work on. This should be sufficiant for the start and most basic configurations.

Sometimes you may with to tweek the project locations by yourself. `doca` uses following environment
variables to lookup for docker-compose projects. You may put them into your `~/.bashrc`

```
export DOCA_PATH=/home/user/git
export DOCA_EXCLUDE_PATH=/home/user/git/other
```

You can specify several paths by seperating them with `:`.

If you find yourself confused that `doca` does not find your projects or find projects you thought where
excluded, you can add some debugging output:

```
export DOCA_LOGLEVEL=debug
```

# Usage
## Listing all projects
```
$ doca ls
frontend /home/user/projects/frontend
webapp /home/user/projects/webapp
prometheus /home/user/monitoring/prometheus
```

## Editing the docker-compose.yml file
```
$ doca edit frontend
-> This will start your $EDITOR on /home/user/monitoring/prometheus/docker-compose.yml
```

## docker-compose commands
All other commands will be directly forwarded to `docker-compose`.
`doca` uses a fuzzy project name matching using [TheFuzz](https://github.com/seatgeek/thefuzz).
In most cases it is not required to specifiy the complete project name.

```
$ doca fron ps
Using project frontend in /home/user/projects/frontend
NAME                  COMMAND                  SERVICE             STATUS              PORTS
frontend-django-1     "/code/docker-entryp…"   django              running             0.0.0.0:8109->8000/tcp, :::8109->8000/tcp
frontend-postgres-1   "docker-entrypoint.s…"   postgres            running             0.0.0.0:5109->5432/tcp, :::5109->5432/tcp
```

You can use all common command like:
```
$ doca fronend ps
$ doca fronend stop
$ doca fronend start
$ doca fronend build
$ doca fronend up -d
$ doca fronend logs -f django
$ doca fronend exec django bash
```

... you get the point. ;-)



