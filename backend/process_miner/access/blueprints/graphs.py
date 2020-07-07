"""
Blueprint module responsible for retrieving different graph types
"""
import logging
from typing import List

import datauri
from flask import Blueprint, request
from flask_caching import Cache

from process_miner.access.blueprints.request_result import get_state_response
from process_miner.access.work.request_processing import RequestManager
from process_miner.mining import graphs, metadata
from process_miner.mining.dataset_factory import DatasetFactory

log = logging.getLogger(__name__)

ARG_APPROACH = 'approach'
ARG_CONSENT_TYPE = 'consent_type'


def create_blueprint(request_manager: RequestManager, cache: Cache,
                     dataset_factory: DatasetFactory):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('graphs', __name__, url_prefix='/graphs')

    def _get_checked_approach():
        valid_approach_types = _wrapper_get_approach_types()
        return _get_checked_str_arg(ARG_APPROACH, valid_approach_types, '')

    @cache.memoize()
    def _wrapper_get_approach_types():
        frame = dataset_factory.get_prepared_data_frame()
        return metadata.get_approach_types(frame)

    def _get_checked_consent():
        valid_consent_types = _wrapper_get_consent_types()
        return _get_checked_str_arg(ARG_CONSENT_TYPE, valid_consent_types, '')

    @cache.memoize()
    def _wrapper_get_consent_types():
        frame = dataset_factory.get_prepared_data_frame()
        return metadata.get_consent_types(frame)

    def _get_checked_str_arg(arg: str, valid_values: List[str],
                             default_value: str):
        value = request.args.get(arg, default_value, str).lower()
        if value == default_value or value in valid_values:
            return value
        log.warning('unknown value "%s" for argument "%s"; using default "%s"',
                    value, arg, default_value)
        return default_value

    @cache.memoize()
    def _create_dfg(approach):
        event_log = dataset_factory.get_prepared_event_log(approach)
        graph = graphs.create_directly_follows_graph(event_log)
        return _package_response(graph)

    @cache.memoize()
    def _create_heuristic_net(approach, consent_type, threshold,
                              output_format):
        event_log = dataset_factory.get_prepared_event_log(approach,
                                                           consent_type)
        graph = graphs.create_heuristic_net(event_log, threshold,
                                            output_format)
        return _package_response(graph)

    def _package_response(graph):
        uri = datauri.DataURI.from_file(graph.name, 'utf-8')
        # make sure there are no newlines/carriage returns in the uri
        sanitized_uri = uri.replace('\n', '').replace('\r', '')
        return {
            'image': sanitized_uri
        }

    # pylint: disable=unused-variable
    @blueprint.route('dfg/get')
    def get_dfg():
        """
        Triggers the creation of a Directly Follows Graph.
        """
        approach = _get_checked_approach()
        ticket = request_manager.submit_ticketed(_create_dfg, approach)
        return get_state_response(ticket)

    @blueprint.route('hn/get')
    def get_hn():
        """
        Triggers the creation of a Heuristic net.
        ---
        parameters:
          - name: approach
            in: query
            type: string
            default: ''
            example: 'embedded'
            description: the approach the data used for creating the graph
                         should be limited to
          - name: consent_type
            in: query
            type: string
            default: ''
            example: 'get_transactions'
            description: the consent type the data used for creating the graph
                         should be limited to
          - name: threshold
            in: query
            type: float
            minimum: 0
            maximum: 1
            default: '0'
          - name: format
            in: query
            type: string
            default: 'svg'
        responses:
          200:
            description: The result will contain a base64 encoded DataURI
                         representing the generated graph.
            schema:
              $ref: '#/definitions/RequestResponse'
        """
        approach = _get_checked_approach()
        consent_type = _get_checked_consent()
        threshold = request.args.get('threshold', 0.0, float)
        # TODO check output_format parameter
        output_format = request.args.get('format', 'svg', str).lower()
        ticket = request_manager.submit_ticketed(_create_heuristic_net,
                                                 approach, consent_type,
                                                 threshold,
                                                 output_format)
        return get_state_response(ticket)

    return blueprint
