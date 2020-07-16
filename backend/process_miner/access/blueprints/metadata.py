"""
Blueprint module responsible for retrieving different graph types
"""
from flask import Blueprint
from flask_caching import Cache

from process_miner.access.blueprints.request_result import get_state_response
from process_miner.access.work.request_processing import RequestManager
from process_miner.mining import metadata
from process_miner.mining.dataset_factory import DatasetFactory


def create_blueprint(request_manager: RequestManager, cache: Cache,
                     dataset_factory: DatasetFactory):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('metadata', __name__, url_prefix='/metadata')

    @cache.memoize()
    def _get_method_types_per_approach():
        frame = dataset_factory.get_prepared_data_frame()
        return metadata.get_method_type_count_per_approach(frame)

    @cache.memoize()
    def _get_approach_type_counts():
        frame = dataset_factory.get_prepared_data_frame()
        return metadata.get_approach_type_count(frame)

    # pylint: disable=unused-variable
    @blueprint.route('method/count')
    def get_method_count():
        """
        Triggers calculation of number of method types per approach.
        ---
        response:
          200:
            description: The retrieved result will be a JSON object
                         representing the number of different method types per
                         approach.
            application/json:
              schema:
                $ref: '#/definitions/RequestResponse'
        """
        ticket = request_manager.submit_ticketed(
            _get_method_types_per_approach)
        return get_state_response(ticket)

    @blueprint.route('approaches/count')
    def get_approach_count():
        """
        Computes which approach types are present in the available data and how
        many sessions each of them was used in.
        ---
        response:
          200:
            description: The retrieved result will be a JSON object
                         representing the number of sessions each approach was
                         used in.
            application/json:
              schema:
                $ref: '#/definitions/RequestResponse'
        """
        ticket = request_manager.submit_ticketed(_get_approach_type_counts)
        return get_state_response(ticket)

    return blueprint
