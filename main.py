import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from prestamos.cli import LoanShell


def main():
    shell = LoanShell()
    shell.stdout.write(
        "Sistema de préstamos de equipos. Escribe 'ayuda' para ver los comandos.\n"
    )
    shell.cmdloop()


if __name__ == "__main__":
    main()
