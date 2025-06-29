import pytest

from speech.commands import CommandParser


def test_parse_move_valid():
    parser = CommandParser()
    assert parser.parse_move("linha dois coluna cinco") == (4, 1)
    assert parser.parse_move("linha oito coluna um") == (0, 7)


def test_parse_move_special_and_invalid():
    parser = CommandParser()
    assert parser.parse_move("cancelar") == "cancelar"
    assert parser.parse_move("linha zero coluna um") is None
    assert parser.parse_move(None) is None


def test_parse_menu():
    parser = CommandParser()
    assert parser.parse_menu("Um Jogador") == "um jogador"
    assert parser.parse_menu("dois jogadores") == "dois jogadores"
    assert parser.parse_menu("sair") == "sair"
    assert parser.parse_menu("foo") is None