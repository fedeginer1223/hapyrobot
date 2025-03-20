from datetime import datetime
import re

# from .bigquery import check_api_token_gcs_secret

def validate_token(parameters: dict):
    """
    Validates the input parameters based on specific criteria.
    Args:
        parameters (dict): A dictionary containing the parameters to be validated.
        route_name (str): The name of the route.
        route_endpoint (str): The endpoint of the route.
    Raises:
        ValueError: If any of the parameters do not meet the required format.
    """

    # If it should include the token parameter
    if 'token' not in parameters.keys():
        raise ValueError('Token is required for this service')

    # Check token
    for param, value in parameters.items():
        
        if param == 'token':

            if not type(value) == str:
                raise ValueError('Invalid token format. Not a string')
            elif len(value) == 0:
                raise ValueError('Invalid token format. Length 0')
            
            # ## CHECKEAR API TOKEN
            # if not check_api_token_gcs_secret(value):
            #     raise ValueError('Invalid API token')