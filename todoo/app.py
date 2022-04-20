#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from typing import Dict, Iterator, List

DB_IDX_SEQ_INIT_VAL = -1
DB_DEFAULT_PATH = ".todoodb.json"
DB_PATH = os.environ.get("TODOO_DB_PATH", DB_DEFAULT_PATH)


@dataclass
class Todo:
    idx: int
    title: str
    done: bool = False
    timestamp: int = int(time.time())

    def __post_init__(self) -> None:
        if len(self.title) < 5:
            raise ValueError("Title should be at least 5 characters long")


class Todoo:

    _todos: Dict[int, Todo]
    _seq: int = DB_IDX_SEQ_INIT_VAL

    def __init__(self, todos: List[dict] = []) -> None:
        self._todos = {int(todo["idx"]): Todo(**todo) for todo in todos}
        if self._todos:
            self._seq = max(self._todos.keys())

    def to_json(self) -> str:
        return json.dumps([asdict(todo) for todo in self._todos.values()])

    @staticmethod
    def from_json(serialized: str) -> Todoo:
        todos = json.loads(serialized)
        return Todoo(todos)

    def add(self, title: str) -> None:
        self._seq += 1
        self._todos[self._seq] = Todo(idx=self._seq, title=title)

    def edit(self, idx: int, title: str) -> None:
        self._todos[idx] = Todo(
            idx=idx,
            title=title,
            done=self._todos[idx].done,
            timestamp=self._todos[idx].timestamp,
        )

    def delete(self, idx: int) -> None:
        del self._todos[idx]

    def toggle(self, idx: int) -> None:
        self._todos[idx].done = not self._todos[idx].done

    def list(self) -> Iterator[Todo]:
        return (
            todo
            for idx, todo in sorted(
                self._todos.items(),
                key=lambda item: (item[1].timestamp, item[1].idx),
                reverse=True,
            )
        )

    def search(self, keyword: str) -> Iterator[Todo]:
        return (todo for todo in self._todos.values() if keyword in todo.title)


def print_help():
    print(f"Usage: ./{sys.argv[0]} <action> [args]")
    print("Valid actions are:")
    print("  h\t\t: display this help")
    print("  a <title>\t: adds a new todo")
    print("  e <id> <title>\t: edits the title of a todo")
    print("  t <id>\t: toggles the status of a todo")
    print("  d <id>\t: deletes a todo")
    print("  ls\t\t: displays all todos")
    print("  s <keyword>\t: displays all todos with 'keyword' in title")


def main():

    try:
        with open(DB_DEFAULT_PATH, "r") as r:
            todoo = Todoo.from_json(r.read())
    except FileNotFoundError:
        todoo = Todoo()

    action = sys.argv[1]
    if action == "a":
        todoo.add(sys.argv[2])
    elif action == "e":
        todoo.edit(int(sys.argv[2]), sys.argv[3])
    elif action == "d":
        todoo.delete(int(sys.argv[2]))
    elif action == "t":
        todoo.toggle(int(sys.argv[2]))
    elif action == "s":
        for todo in todoo.search(sys.argv[2]):
            print(todo)
    elif action == "ls":
        for todo in todoo.list():
            print(todo)
    else:
        print_help()

    with open(DB_DEFAULT_PATH, "w") as w:
        w.write(todoo.to_json())


if __name__ == "__main__":
    main()
