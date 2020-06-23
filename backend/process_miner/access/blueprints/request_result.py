"""
Blueprint module for accessing request states and results
"""
import logging

from flask import abort, Blueprint, jsonify, url_for

log = logging.getLogger(__name__)

USE_EXTERNAL_URLS = True


def get_state_response(ticket_id: str):
    """
    Creates a response containing a valid url for the state of the request
    associated with the supplied ticket id.
    :param ticket_id: the ticket id
    :return: JSON representation of the state url response
    """
    return jsonify({
        'stateUrl': url_for('requests.get_state',
                            request_id=ticket_id,
                            _external=USE_EXTERNAL_URLS)
    })


def create_blueprint(request_manager):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('requests', __name__, url_prefix='/requests')

    # pylint: disable=unused-variable
    @blueprint.route('<request_id>/state')
    def get_state(request_id):
        """
        Retrieves the state of the specified request.
        :param request_id: id of the request
        :return: JSON object representing the requests state
        """
        # TODO 404 on invalid request_id or no futures
        return jsonify({
            'done': request_manager.request_processed(request_id),
            'resultUrl':
                url_for('requests.get_result',
                        request_id=request_id,
                        _external=USE_EXTERNAL_URLS)
        })

    @blueprint.route('<request_id>/result')
    def get_result(request_id):
        """
        Retrieves the result of the specified request.
        :param request_id: request_id: id of the request
        :return: JSON object representing the requests state
        """
        if not request_manager.request_processed(request_id):
            log.info('request "%s" not done or result already retrieved',
                     request_id)
            abort(404)
        result = request_manager.get_result(request_id)
        log.debug(result)
        if not result:
            return jsonify({})
        return jsonify(result)

    return blueprint
