from controller import Controller  # pyright: ignore[reportImplicitRelativeImport]
from ventana_principal import iniciar_ventana  # pyright: ignore[reportImplicitRelativeImport]


def main():
    controller = Controller()
    iniciar_ventana(controller)


if __name__ == "__main__":
    main()
