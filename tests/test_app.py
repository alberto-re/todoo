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


def test_edit_todo(app):
    app.edit(0, "buy almond milk")
    expected_list = [
        Todo(idx=1, title="walk the dog"),
        Todo(idx=0, title="buy almond milk"),
    ]
    assert list(app.list()) == expected_list


def test_delete_todo(app):
    app.delete(0)
    expected_list = [Todo(idx=1, title="walk the dog")]
    assert list(app.list()) == expected_list
