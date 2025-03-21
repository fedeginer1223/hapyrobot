from flask import Blueprint, request, abort, Response, jsonify
from loguru import logger
import requests
import json

from services import validate_params
from pandas import read_csv

## Name of the route
ROUTE_NAME = 'loads'

# Create recommendations blueprint
loads_bp = Blueprint(ROUTE_NAME, __name__)

### Endpoints
# getting load information
@loads_bp.route('', methods=['GET'])
def get_load_by_ref():
    """
    Retrieves load details given the landing post reference number.
    """
    # Read parameters
    params = request.args.to_dict()

    # Validate input parameters
    logger.info('Request to get load details. Validating params...')
    
    try:
        validate_params(
            params
        )
    except ValueError as e:
        logger.error(f'Error validating inputs: {e}')
        abort(400, description=f'Error validating inputs: {e}')
    
    logger.info('Params and Token validated successfully.')

    logger.info('Fetching load data...')

    load_data=read_csv(r"data/loads_data.csv", sep=";")

    try:
        results=load_data[load_data["reference_number"]==params.get("reference_number")]
        load_data_referenced = results.to_dict(orient="records")[0]
        logger.info('Load data fetched successfully.')

        response = jsonify({"load_data": load_data_referenced})
        return response, 200

    except Exception as e:
        abort(404, description=f'The referenced value has not been found')

# getting carrier information
@loads_bp.route('/fmcsa', methods=['GET'])
def get_carrier_info():
    """
    Returns carrier information
    """
    # Get request arguments
    params = request.args.to_dict()

    # Make request to FMCSA API
    url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/{params.get('mc_number', '999999')}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    fmcsa_params = {"webKey": params.get("webKey", "cdc33e44d693a3a58451898d4ec9df862c65b954")}

    logger.info(f'Requesting to FMCSA API {url}')

    response = requests.get(url, headers=headers, params=fmcsa_params)

    if response.status_code == 200:

        logger.info(f'Success FMCSA API response')

        # Generate response
        response_json = response.json().get("content").get("carrier")
        carrier_info = {
                "carrier_id": str(response_json.get("dotNumber")),
                "status": response_json.get("statusCode"),
                "carrier_name": response_json.get("legalName")
            }

        response = jsonify({"carrier": carrier_info})
        return response, 200

    else:
        print(f"Error: {response.status_code}, {response.text}")