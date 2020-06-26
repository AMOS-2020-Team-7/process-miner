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
        ---
        parameters:
          - name: request_id
            description: id of the request
            in: path
            type: string
            required: true
        definitions:
          RequestResponse:
            description: Object containing the URL of a requests state
            type: object
            properties:
              stateUrl:
                description: URL the requests state can be retrieved from
                type: string
          StateResponse:
            description: Object describing request state and result url
            type: object
            properties:
              done:
                description: whether the processing of the request is done
                type: boolean
              resultUrl:
                description: URL the requests result can be retrieved from
                type: string
        responses:
          200:
            application/json:
              schema:
                $ref: '#/definitions/StateResponse'
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
        ---
        parameters:
          - name: request_id
            description: id of the request
            in: path
            type: string
            required: true
        responses:
          200:
            application/json:
              schema:
                description: object defined by the type of request
                type: object
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
