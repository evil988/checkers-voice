"""Pequeno utilitário para testar reconhecimento de voz isoladamente."""

import os
import sys
import ast
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def load_voice_commands() -> list[str]:
    """Retorna a lista de comandos de voz definidos no projeto."""
    path = Path(__file__).resolve().parent.parent / "menu" / "menu.py"
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "VOICE_COMMANDS":
                    return ast.literal_eval(node.value)
    return []


VOICE_COMMANDS = load_voice_commands()
from speech.commands import CommandParser
from speech.recognizer import SpeechRecognizer


def build_grammar() -> list[str]:
    """Retorna a lista completa de comandos reconhecíveis."""
    parser = CommandParser()
    numbers = parser.numbers

    move_cmds = [f"linha {r} coluna {c}" for r in numbers for c in numbers]
    extras = ["cancelar", "reiniciar", "voltar ao menu principal"]

    return move_cmds + extras + VOICE_COMMANDS


def main() -> None:
    grammar = build_grammar()
    recognizer = SpeechRecognizer(grammar)
    parser = CommandParser()

    print("Fale um comando reconhecido (ex: 'linha um coluna dois')")
    try:
        while True:
            text = recognizer.read_audio()
            if not text:
                continue

            print("🎧 Texto capturado:", text)
            cmd_menu = parser.parse_menu(text)
            if cmd_menu:
                print("✅ Comando de menu:", cmd_menu)
                continue

            cmd_move = parser.parse_move(text)
            if isinstance(cmd_move, tuple):
                print("✅ Movimento:", cmd_move)
            elif cmd_move in ("cancelar", "reiniciar", "voltar ao menu principal"):
                print("✅ Comando especial:", cmd_move)
    except KeyboardInterrupt:
        print("\nEncerrando reconhecimento.")
    finally:
        recognizer.close()


if __name__ == "__main__":
    main()