#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Dict, List

DB_IDX_SEQ_INIT_VAL = -1
DB_DEFAULT_PATH = ".todoodb.json"
DB_PATH = os.environ.get("TODOO_DB_PATH", DB_DEFAULT_PATH)


@dataclass
class Todo:
    idx: int
    title: str
    done: bool = False
    timestamp: int = int(time.time())


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


def main():

    try:
        with open(DB_DEFAULT_PATH, "r") as r:
            todoo = Todoo.from_json(r.read())
    except FileNotFoundError:
        todoo = Todoo()

    todoo.add("buy milk")

    with open(DB_DEFAULT_PATH, "w") as w:
        w.write(todoo.to_json())


if __name__ == "__main__":
    main()
