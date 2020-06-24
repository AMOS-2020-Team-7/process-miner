"""
Blueprint module responsible for retrieving different graph types
"""
from flask import Blueprint
from flask_caching import Cache

from process_miner.access.blueprints.request_result import get_state_response
from process_miner.access.work.request_processing import RequestManager
from process_miner.mining.metadata_factory import MetadataFactory


def create_blueprint(request_manager: RequestManager, cache: Cache,
                     metadata_factory: MetadataFactory):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('metadata', __name__, url_prefix='/metadata')

    @cache.memoize()
    def _count_consent_type_counts():
        return metadata_factory.get_consent_types_per_approach()

    @cache.memoize()
    def _count_approach_type_counts():
        return metadata_factory.get_approach_type_count()

    # pylint: disable=unused-variable
    @blueprint.route('consent/count')
    def get_consent_count():
        """
        Triggers calculation of number of consent types per approach.
        """
        ticket = request_manager.submit_ticketed(_count_consent_type_counts)
        return get_state_response(ticket)

    @blueprint.route('approaches/count')
    def get_approach_count():
        """
        Computes which approach types are present in the available data and how
        many sessions each of them was used in.
        """
        ticket = request_manager.submit_ticketed(_count_approach_type_counts)
        return get_state_response(ticket)

    return blueprint
