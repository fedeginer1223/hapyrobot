from flask import Blueprint, request, jsonify, abort
from loguru import logger

from services import validate_token
from pandas import read_csv

## Name of the route
ROUTE_NAME = 'loads'

# Create recommendations blueprint
loads_bp = Blueprint(ROUTE_NAME, __name__)

### Endpoints
# getting load information
@loads_bp.route('/<string:ref_number>', methods=['GET'])
def get_load_by_ref(ref_number):
    """
    Retrieves load details given the landing post reference number.
    """
    # Read parameters
    params = request.args.to_dict()

    # Validate input parameters
    logger.info('Request to get load details. Validating params...')

    if not ref_number:
        abort(400, description="Reference number is required.")
    
    # Validate token
    logger.info('Checking token')

    try:
        validate_token(
            params
        )
    except ValueError as e:
        logger.error(f'Error validating inputs: {e}')
        abort(400, description=f'Error validating inputs: {e}')
    
    logger.info('Params and Token validated successfully.')

    logger.info('Fetching load data...')

    load_data=read_csv(r"data\loads_data.csv", sep=";")

    try:
        results=load_data[load_data["reference_number"]==ref_number]
        load_data_referenced = results.to_dict(orient="records")[0]
        logger.info('Load data fetched successfully.')
        return load_data_referenced

    except Exception as e:
        abort(404, description=f'The referenced value has not been found')