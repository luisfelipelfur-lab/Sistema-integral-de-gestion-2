# Importamos ABC y abstractmethod para la abstracción de servicios
from abc import ABC, abstractmethod
# Importamos singledispatchmethod para implementar sobrecarga de métodos por tipo de dato
from functools import singledispatchmethod
# Importamos EntidadSistema desde modelos.py
from modelos import EntidadSistema
# Importamos las excepciones necesarias desde excepciones.py
from excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
)


class Servicio(EntidadSistema, ABC):
    """Clase abstracta que define la estructura común de todos los servicios de Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Llamamos al constructor padre para validar el ID
        super().__init__(id_servicio)
        # Validamos que el nombre del servicio no esté vacío
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self._nombre = nombre.strip()
        # Usamos el setter de tarifa_base para validar que sea un número positivo
        self.tarifa_base = tarifa_base
        # Estado booleano que indica si el servicio está libre para reservar
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        """Devuelve el nombre comercial del servicio."""
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        """Devuelve la tarifa por hora del servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida y convierte la tarifa; usa encadenamiento de excepciones si no es numérica."""
        try:
            num = float(valor)
        except (TypeError, ValueError) as exc:
            # Encadenamiento explícito: conserva el error original de Python dentro de nuestra excepción
            raise DatosInvalidosError(f"La tarifa debe ser numérica: '{valor}'.") from exc
        if num <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")
        self._tarifa_base = num

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible actualmente."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Actualiza la disponibilidad del servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        """Método abstracto para validar reglas de negocio propias de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Método abstracto para calcular el costo antes de impuestos y descuentos."""
        pass

    # --- MÉTODOS SOBRECARGADOS ---
    @singledispatchmethod
    def calcular_costo_final(
        self,
        duracion_horas: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
    ) -> float:
        """
        Variante 1 (Por defecto con int): Calcula el total aplicando parámetros opcionales
        de impuesto (19% por defecto) y descuento (0% por defecto).
        """
        # Ejecuta la validación específica de la clase hija
        self.validar_parametros(duracion_horas)
        # Calcula el subtotal polimórfico
        subtotal = self.calcular_costo_base(duracion_horas)
        # Verifica que el porcentaje de descuento esté en un rango lógico
        if not (0 <= descuento < 1):
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 0.99.")
        # Aplica descuento e impuesto
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo final calculado es inconsistente (<= 0).")
        return round(total, 2)

    @calcular_costo_final.register
    def _(self, parametros: dict) -> float:
        """
        Variante 2 (Sobrecarga con dict): Permite calcular el costo enviando un diccionario
        con 'horas', 'impuesto', 'descuento' y un 'recargo_fijo' opcional.
        """
        horas = parametros.get("horas")
        if horas is None:
            raise ParametroFaltanteError("Falta la clave 'horas' en el diccionario de cálculo.")
        impuesto = parametros.get("impuesto", 0.19)
        descuento = parametros.get("descuento", 0.0)
        recargo = parametros.get("recargo_fijo", 0.0)
        # Reutiliza la lógica de la primera variante y suma el recargo fijo
        base = self.calcular_costo_final(int(horas), float(impuesto), float(descuento))
        return round(base + float(recargo), 2)


class ReservaSala(Servicio):
    """Servicio especializado 1: Alquiler de salas físicas de reuniones."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion_horas: int) -> None:
        """Las salas solo pueden reservarse entre 1 y 12 horas seguidas."""
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatosInvalidosError("Las salas se reservan entre 1 y 12 horas por día.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Aplica un recargo del 10% si la sala supera las 20 personas de capacidad."""
        factor_capacidad = 1.10 if self._capacidad > 20 else 1.0
        return self.tarifa_base * duracion_horas * factor_capacidad

    def obtener_resumen(self) -> str:
        return f"Sala [{self.id}] '{self.nombre}' | Capacidad: {self._capacidad} pers. | ${self.tarifa_base}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de hardware y equipos de cómputo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, cantidad_unidades: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        if cantidad_unidades < 1:
            raise DatosInvalidosError("Debe haber al menos 1 equipo disponible.")
        self._cantidad_unidades = cantidad_unidades

    def validar_parametros(self, duracion_horas: int) -> None:
        """Exige un mínimo de 2 horas para alquiler de equipos."""
        if duracion_horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Suma un seguro obligatorio de $15.000 al cálculo por horas."""
        seguro = 15000.0
        return (self.tarifa_base * duracion_horas) + seguro

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id}] '{self.nombre}' | Stock: {self._cantidad_unidades} | ${self.tarifa_base}/h"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría técnica por expertos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe indicar la especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int) -> None:
        """Valida que la duración sea de al menos 1 hora."""
        if duracion_horas <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser positiva.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Otorga un 10% de descuento automático si se contratan más de 5 horas."""
        costo = self.tarifa_base * duracion_horas
        return costo * 0.90 if duracion_horas > 5 else costo

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self.id}] '{self.nombre}' ({self._especialidad}) | ${self.tarifa_base}/h"
