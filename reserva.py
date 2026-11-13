# Importamos la clase base EntidadSistema y la clase Cliente
from modelos import Cliente, EntidadSistema
# Importamos la clase base Servicio
from servicios import Servicio
# Importamos las excepciones de negocio
from excepciones import (
    DatosInvalidosError,
    OperacionReservaError,
    ServicioNoDisponibleError,
)


class Reserva(EntidadSistema):
    """Clase que vincula un Cliente con un Servicio y administra su ciclo de vida."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        # Validamos el ID de la reserva mediante la superclase
        super().__init__(id_reserva)
        # Verificamos que los objetos recibidos correspondan a las clases esperadas
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        # Toda reserva inicia en estado PENDIENTE hasta ser procesada
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva (PENDIENTE, CONFIRMADA, CANCELADA)."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Devuelve el valor total calculado para la reserva."""
        return self._costo_total

    def procesar_y_confirmar(self, descuento: float = 0.0) -> None:
        """Valida disponibilidad, calcula el costo total y cambia el estado a CONFIRMADA."""
        if self._estado == "CANCELADA":
            raise OperacionReservaError("No se puede confirmar una reserva que ya fue cancelada.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no se encuentra disponible."
            )

        # Calcula el costo aplicando polimorfismo según el tipo de servicio
        self._costo_total = self._servicio.calcular_costo_final(
            self._duracion_horas, descuento=descuento
        )
        # Cambia el estado de la reserva y marca el servicio como ocupado
        self._estado = "CONFIRMADA"
        self._servicio.disponible = False

    def cancelar(self) -> None:
        """Cancela una reserva activa y vuelve a habilitar el servicio."""
        if self._estado == "CANCELADA":
            raise OperacionReservaError(f"La reserva {self.id} ya se encuentra cancelada.")
        self._estado = "CANCELADA"
        self._servicio.disponible = True

    def obtener_resumen(self) -> str:
        """Retorna una descripción completa del estado y costo de la reserva."""
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} ({self._duracion_horas}h) | Total: ${self._costo_total:,.2f}"
        )
