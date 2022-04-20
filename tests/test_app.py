import pytest

from todoo.app import Todo, Todoo


@pytest.fixture
def app():
    app = Todoo()
    app.add("buy milk")
    app.add("walk the dog")
    return app


def test_new_app_from_scratch():
    app = Todoo()
    assert not list(app.list())


def test_new_app_import_data():
    data = [
        {"idx": 3, "title": "backup", "done": False, "timestamp": 1650491200},
        {"idx": 6, "title": "restore", "done": True, "timestamp": 1650491500},
    ]
    app = Todoo(data)
    expected = [
        Todo(idx=6, title="restore", done=True, timestamp=1650491500),
        Todo(idx=3, title="backup", done=False, timestamp=1650491200),
    ]
    assert list(app.list()) == expected


def test_list_todos(app):
    expected_list = [Todo(idx=1, title="walk the dog"), Todo(idx=0, title="buy milk")]
    assert list(app.list()) == expected_list


def test_search_todos(app):
    expected_list = [Todo(idx=0, title="buy milk")]
    assert list(app.search("buy")) == expected_list


def test_add_todo(app):
    app.add("wash the car")
    expected_list = [
        Todo(idx=2, title="wash the car"),
        Todo(idx=1, title="walk the dog"),
        Todo(idx=0, title="buy milk"),
    ]
    assert list(app.list()) == expected_list


def test_add_todo_invalid(app):
    with pytest.raises(ValueError):
        app.add("play")


def test_edit_todo(app):
    app.edit(0, "buy almond milk")
    expected_list = [
        Todo(idx=1, title="walk the dog"),
        Todo(idx=0, title="buy almond milk"),
    ]
    assert list(app.list()) == expected_list


def test_edit_todo_invalid(app):
    with pytest.raises(ValueError):
        app.edit(1, "sing")


def test_delete_todo(app):
    app.delete(0)
    expected_list = [Todo(idx=1, title="walk the dog")]
    assert list(app.list()) == expected_list
