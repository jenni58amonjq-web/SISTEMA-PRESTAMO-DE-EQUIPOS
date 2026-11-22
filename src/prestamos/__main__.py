from .cli import LoanShell


def main():
    shell = LoanShell()
    shell.stdout.write(
        "Sistema de préstamos de equipos. Escribe 'ayuda' para ver los comandos.\n"
    )
    shell.cmdloop()


if __name__ == "__main__":
    main()
