from dataclasses import dataclass, field
from typing import Any, override


@dataclass
class Libro:
    titulo: str
    id: int | None = None
    paginas_totales: int = 0
    paginas_leidas: int = 0

    @property
    def porcentaje_leido(self) -> float:
        if self.paginas_totales == 0 or self.paginas_leidas == 0:
            return 0.0
        return round((self.paginas_leidas * 100) / self.paginas_totales, 2)

    @override
    def __repr__(self) -> str:
        return (
            f"Libro(id={self.id},"
            f"titulo='{self.titulo}', "
            f"paginas_leidas={self.paginas_leidas}, "
            f"paginas_totales={self.paginas_totales}, "
            f"porcentaje_leido={self.porcentaje_leido}%)"
        )

    @override
    def __setattr__(self, name: str, value: Any, /) -> None:
        if name == "paginas_leidas":
            totales = getattr(self, "paginas_totales", 0)
            if value > totales:
                raise ValueError(
                    f"Paginas leidas {value} excede el valor de paginas totales {self.paginas_totales}"
                )
        super().__setattr__(name, value)


if __name__ == "__main__":
    librx = Libro(titulo="Amigos mios", paginas_leidas=10, paginas_totales=20)
    print(librx)
