# Importamos logging para registros internos de depuración
import logging
# Importamos anotaciones de tipo para mayor claridad del código
from typing import List, Optional
# Importamos todas nuestras clases y excepciones de los módulos del proyecto
from excepciones import ErrorSistemaFJ, OperacionReservaError, registrar_evento
from modelos import Cliente
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria usando listas internas."""

    def __init__(self):
        # Listas en memoria que reemplazan cualquier motor de base de datos
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

    def registrar_cliente(
        self, id_c: str, nombre: str, correo: str, telefono: str
    ) -> Optional[Cliente]:
        """Intenta crear y guardar un cliente usando estructura completa try/except/else/finally."""
        try:
            cliente = Cliente(id_c, nombre, correo, telefono)
        except ErrorSistemaFJ as e:
            # Captura errores de validación sin detener el programa
            registrar_evento("error", f"Fallo al registrar cliente ({id_c}): {e}")
            return None
        else:
            # Solo se ejecuta si el bloque try no lanzó ninguna excepción
            self._clientes.append(cliente)
            registrar_evento("info", f"Cliente registrado con éxito -> {cliente.obtener_resumen()}")
            return cliente
        finally:
            # Se ejecuta siempre para dejar constancia del cierre de la operación
            logging.debug(f"Cierre de transacción de registro de cliente {id_c}.")

    def registrar_servicio(self, servicio_obj: Servicio) -> bool:
        """Agrega un servicio válido a la lista interna del sistema."""
        try:
            if not isinstance(servicio_obj, Servicio):
                raise ErrorSistemaFJ("El objeto recibido no es un servicio válido.")
            self._servicios.append(servicio_obj)
        except ErrorSistemaFJ as e:
            registrar_evento("error", f"Fallo al registrar servicio: {e}")
            return False
        else:
            registrar_evento("info", f"Servicio agregado -> {servicio_obj.obtener_resumen()}")
            return True

    def crear_reserva(
        self,
        id_r: str,
        cliente: Optional[Cliente],
        servicio: Optional[Servicio],
        horas: int,
        descuento: float = 0.0,
    ) -> Optional[Reserva]:
        """Procesa una reserva y maneja errores esperados e inesperados con encadenamiento."""
        try:
            reserva = Reserva(id_r, cliente, servicio, horas)
            reserva.procesar_y_confirmar(descuento=descuento)
        except ErrorSistemaFJ as e:
            registrar_evento("error", f"Reserva [{id_r}] rechazada: {e}")
            return None
        except Exception as e:
            # Captura cualquier fallo imprevisto y lo encadena con nuestra excepción de negocio
            err_encadenado = OperacionReservaError(f"Error crítico procesando reserva {id_r}")
            registrar_evento("error", f"{err_encadenado} -> Causa técnica: {e}")
            return None
        else:
            self._reservas.append(reserva)
            registrar_evento("info", f"Reserva confirmada -> {reserva.obtener_resumen()}")
            return reserva
        finally:
            logging.debug(f"Auditoría de transacción de reserva {id_r} finalizada.")


def ejecutar_simulacion() -> None:
    """Ejecuta más de 10 operaciones completas (válidas e inválidas) demostrando estabilidad."""
    print("=" * 80)
    print("INICIANDO SISTEMA INTEGRAL SOFTWARE FJ (GESTIÓN EN MEMORIA + ARCHIVO DE LOGS)")
    print("=" * 80)

    sistema = GestorSoftwareFJ()

    # 1. Registro válido de cliente 1
    c1 = sistema.registrar_cliente("C-01", "Laura Gómez", "laura.gomez@empresa.com", "3104567890")

    # 2. Registro válido de cliente 2
    c2 = sistema.registrar_cliente("C-02", "Carlos Méndez", "cmendez@tech.co", "3209876543")

    # 3. Registro inválido de cliente (correo sin arroba)
    sistema.registrar_cliente("C-03", "Andrés Rojas", "://arroba.com", "3001112233")

    # 4. Registro inválido de cliente (teléfono demasiado corto)
    sistema.registrar_cliente("C-04", "Marta Díaz", "marta@correo.com", "123")

    # 5. Creación válida de servicio tipo Sala
    s1 = None
    try:
        s1 = ReservaSala("S-01", "Sala Juntas Ejecutiva", 80000, capacidad=25)
        sistema.registrar_servicio(s1)
    except ErrorSistemaFJ as e:
        registrar_evento("error", f"Error creando sala: {e}")

    # 6. Creación válida de servicio tipo Equipo
    s2 = None
    try:
        s2 = AlquilerEquipo("S-02", "Servidor Portátil GPU", 50000, cantidad_unidades=4)
        sistema.registrar_servicio(s2)
    except ErrorSistemaFJ as e:
        registrar_evento("error", f"Error creando equipo: {e}")

    # 7. Creación válida de servicio tipo Asesoría
    s3 = None
    try:
        s3 = AsesoriaEspecializada("S-03", "Arquitectura Cloud", 120000, "DevOps & AWS")
        sistema.registrar_servicio(s3)
    except ErrorSistemaFJ as e:
        registrar_evento("error", f"Error creando asesoría: {e}")

    # 8. Creación inválida de servicio (tarifa negativa)
    try:
        s_invalido = ReservaSala("S-04", "Sala Fantasma", -50000, capacidad=10)
        sistema.registrar_servicio(s_invalido)
    except ErrorSistemaFJ as e:
        registrar_evento("error", f"Creación de servicio bloqueada por validación: {e}")

    # 9. Reserva EXITOSA de Sala con 10% de descuento
    r1 = sistema.crear_reserva("R-101", c1, s1, horas=4, descuento=0.10)

    # 10. Reserva FALLIDA (intenta reservar la misma sala que ya está ocupada)
    sistema.crear_reserva("R-102", c2, s1, horas=2)

    # 11. Reserva FALLIDA (alquiler de equipo por 1 hora, incumple mínimo de 2 horas)
    sistema.crear_reserva("R-103", c2, s2, horas=1)

    # 12. Reserva EXITOSA de Asesoría + prueba de método sobrecargado con diccionario
    sistema.crear_reserva("R-104", c2, s3, horas=6)
    if s3:
        costo_dict = s3.calcular_costo_final({"horas": 6, "impuesto": 0.19, "recargo_fijo": 25000})
        registrar_evento("info", f"Cálculo sobrecargado (dict) para {s3.nombre}: ${costo_dict:,.2f}")

    # 13. Cancelación exitosa de reserva y prueba de error por doble cancelación
    if r1:
        try:
            r1.cancelar()
            registrar_evento("info", f"Reserva cancelada correctamente -> {r1.obtener_resumen()}")
            r1.cancelar()  # Lanza OperacionReservaError de forma controlada
        except OperacionReservaError as e:
            registrar_evento("error", f"Operación no permitida en reserva: {e}")

    print("=" * 80)
    print("SIMULACIÓN COMPLETADA SIN CAÍDAS. REVISE 'software_fj_eventos.log'")
    print("=" * 80)


# Punto de entrada principal del programa
if __name__ == "__main__":
    ejecutar_simulacion()
