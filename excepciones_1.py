# Importamos el módulo nativo 'logging' para registrar eventos y errores en un archivo de texto
import logging

# Configuramos el archivo 'software_fj_eventos.log' donde se guardará todo el historial
logging.basicConfig(
    filename="software_fj_eventos.log",  # Nombre del archivo físico que se creará automáticamente
    level=logging.INFO,  # Nivel mínimo de registro (INFO captura información, advertencias y errores)
    format="%(asctime)s | %(levelname)-8s | %(message)s",  # Formato: Fecha/Hora | Nivel | Mensaje
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato de fecha y hora legible (Año-Mes-Día Hora:Minuto:Segundo)
    encoding="utf-8",  # Codificación UTF-8 para soportar tildes y caracteres en español
)


def registrar_evento(nivel: str, mensaje: str) -> None:
    """Función auxiliar para imprimir en pantalla y guardar en el archivo .log al mismo tiempo."""
    # Imprime el mensaje en la consola para que el usuario vea lo que ocurre en tiempo real
    print(f"[{nivel.upper()}] {mensaje}")
    # Evalúa el nivel recibido para guardarlo con la etiqueta correcta en el archivo de logs
    if nivel.lower() == "error":
        logging.error(mensaje)  # Registra un fallo o excepción controlada
    elif nivel.lower() == "warning":
        logging.warning(mensaje)  # Registra una advertencia preventiva
    else:
        logging.info(mensaje)  # Registra una operación exitosa o evento informativo


# ==============================================================================
# JERARQUÍA DE EXCEPCIONES PERSONALIZADAS PARA SOFTWARE FJ
# ==============================================================================

class ErrorSistemaFJ(Exception):
    """Excepción base (padre) de la cual heredan todos los errores propios del sistema."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato no cumple el formato esperado (ej. correo sin @ o tarifa negativa)."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando se omite un dato obligatorio o se envía vacío al crear una entidad."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar una sala, equipo o asesoría que ya está ocupada."""
    pass


class OperacionReservaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta realizar una acción no permitida (ej. cancelar dos veces)."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de tarifas o descuentos arroja un valor matemático inválido."""
    pass
