# todoo

Another To Do app

## Requirements

- [Poetry](https://python-poetry.org/) (tested with v1.1.3, current stable version)

## Installation

Place yourself in the root of the project and execute in a terminal the command:

```
poetry install
```

## Usage

Running the app without any command or with "h" will show the help:

```
$ poetry run todoo h
Usage: ./todoo <action> [args]
Valid actions are:
  h             : display this help
  a <title>     : adds a new todo
  e <title>     : edits the title of a todo
  t <id>        : toggles the status of a todo
  d <id>        : deletes a todo
  ls            : displays all todos
  s <keyword>   : displays all todos with 'keyword' in title
```
