# Importamos ABC y abstractmethod para definir clases y métodos abstractos
from abc import ABC, abstractmethod
# Importamos datetime para registrar la fecha y hora exacta de creación de cada objeto
from datetime import datetime
# Importamos nuestras excepciones personalizadas desde el módulo excepciones.py
from excepciones import DatosInvalidosError, ParametroFaltanteError


class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad del sistema Software FJ."""

    def __init__(self, id_entidad: str):
        # Validamos que el identificador no sea None ni una cadena vacía
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio.")
        # Almacenamos el ID limpio en un atributo protegido
        self._id = str(id_entidad).strip()
        # Guardamos la marca de tiempo en que se instanció la entidad
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Getter de solo lectura para consultar el identificador de la entidad."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio que cada clase hija debe sobrescribir."""
        pass


class Cliente(EntidadSistema):
    """Representa a un cliente con encapsulación estricta y validaciones de datos."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Invocamos el constructor de la clase padre EntidadSistema para validar el ID
        super().__init__(id_cliente)
        # Asignamos los atributos a través de sus setters para activar las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Devuelve el nombre completo del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida que el nombre tenga al menos 3 caracteres antes de guardarlo."""
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Devuelve el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida la estructura básica del correo (@ y dominio con punto)."""
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Devuelve el número telefónico del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga solo dígitos y tenga mínimo 7 números."""
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosInvalidosError(f"Teléfono inválido (mínimo 7 dígitos): '{valor}'.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen de datos del cliente."""
        return f"Cliente [{self.id}]: {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"
