from loguru import logger
from google.cloud import secretmanager

# Api Token name
API_TOKEN_NAME = 'happy_robot_api_token'

def check_api_token_gcs_secret(api_token):
    """
    Comprueba si el token de la API se encuentra en el secreto de GCS.
    Args:
        api_token (str): El token de la API a comprobar.
    Returns:
        bool: True si el token se encuentra en el secreto, False en caso contrario.
    """

    logger.info("Verifying API token in GCS Secret Manager.")

    #credentials, _ = google.auth.default()

    # secret_client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_client = secretmanager.SecretManagerServiceClient()

    # Define the sectret name
    secret_name = f'projects/909775733702/secrets/{API_TOKEN_NAME}/versions/latest'

    try:
        response = secret_client.access_secret_version(name=secret_name)
        secret_payload = response.payload.data.decode('UTF-8')

        # Comprobar si el token coincide
        if secret_payload == api_token:
            logger.info('API token verification passed.')
            return True
        else:
            logger.error('API token verification failed.')
            return False

    except Exception as e:
        logger.error(f'Error accessing secret {API_TOKEN_NAME}: {e}')
        return False