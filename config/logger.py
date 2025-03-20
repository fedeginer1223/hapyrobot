import yaml

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

 
class LoggerSettings(BaseSettings):
    """
    Configuracion del logger para la API
    """

    log_level: str
    log_file: str
    rotation: str
    retention: str

    @classmethod
    def load_config_from_yaml(cls, file_path: str):
        """
        Cargar la configuración del logger desde un fichero yaml
        """
        try:
            # Parsear el fichero yaml
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

            # Devolver la clase instanciada con la configuración especificada en le fichero
            return cls(**data)

        except Exception as e:
            raise Exception(f'Error cargando el archivo de configuración: {e}')

def configure_logging(logger_settings: LoggerSettings):
    """
    Configurar el logger con la configuración especificada
    """
    # Eliminar los handlers por defecto
    logger.remove()

    # Añadir segun la configuracion
    logger.add(
        logger_settings.log_file,
        level=logger_settings.log_level,
        rotation=logger_settings.rotation,
        retention=logger_settings.retention
    )
    logger.info('Logger configurado correctamente')

# Instanciar la configuración
logger_config_file_path = 'config/files/logger_config.yml'
logger_settings = LoggerSettings.load_config_from_yaml(logger_config_file_path)

# Configurar el logger
configure_logging(logger_settings)
