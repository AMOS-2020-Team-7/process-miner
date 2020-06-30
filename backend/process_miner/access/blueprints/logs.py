"""
Blueprint module that allows triggering log retrieval from Graylog
"""
import logging

from flask import Blueprint

from process_miner.access.blueprints.request_result import get_state_response

log = logging.getLogger(__name__)


def create_blueprint(executor, cache, log_retriever):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('logs', __name__, url_prefix='/logs')

    def _refresh_logs():
        log.info('log data retrieval triggered')
        log_retriever.retrieve_logs()
        log.info('clearing cache')
        cache.clear()  # TODO use a more fine grained approach?
        return {}

    # pylint: disable=unused-variable
    @blueprint.route('refresh')
    def refresh():
        """
        Triggers the retrieval of logs from Graylog.
        ---
        parameters:
          - name: force
            in: query
            type: boolean
            default: 'False'
            description: force retrieval of logs that were already downloaded
        responses:
          200:
            description: The result will not contain any value after retrieval.
            application/json:
              schema:
                $ref: '#/definitions/RequestResponse'
        """
        ticket = executor.submit_ticketed(_refresh_logs)
        return get_state_response(ticket)

    return blueprint
