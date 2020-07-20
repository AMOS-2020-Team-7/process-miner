"""
Blueprint module responsible for retrieving different graph types
"""
import logging
import os

import datauri
from flask import Blueprint, request
from flask_caching import Cache
from werkzeug.utils import unescape

from process_miner.access.blueprints.request_result import get_state_response
from process_miner.access.work.request_processing import RequestManager
from process_miner.mining import graphs, metadata
from process_miner.mining.dataset_factory import DatasetFactory

log = logging.getLogger(__name__)

ARG_APPROACH = 'approach'
ARG_METHOD_TYPE = 'method_type'
ARG_ERROR_TYPE = 'error_type'
ARG_BANK = 'bank'


def create_blueprint(request_manager: RequestManager, cache: Cache,
                     dataset_factory: DatasetFactory):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('graphs', __name__, url_prefix='/graphs')

    def _get_filter_parameters():
        approach = _get_unescaped_parameter(ARG_APPROACH)
        method_type = _get_unescaped_parameter(ARG_METHOD_TYPE)
        error_type = _get_unescaped_parameter(ARG_ERROR_TYPE)
        bank = _get_unescaped_parameter(ARG_BANK)
        return approach, bank, error_type, method_type

    def _get_unescaped_parameter(parameter, default=''):
        return unescape(request.args.get(parameter, default, str))

    @cache.memoize()
    def _create_dfg(approach, method_type, error_type, bank, output_format):
        frame = dataset_factory.get_prepared_data_frame(approach,
                                                        method_type,
                                                        error_type,
                                                        bank)
        session_count = _extract_session_count(frame)
        additional_metadata = _extract_metadata(frame)
        dfg = graphs.create_directly_follows_graph(frame, output_format)
        response = _package_response(dfg.name, session_count,
                                     additional_metadata)
        os.remove(dfg.name)
        return response

    @cache.memoize()
    def _create_heuristic_net(approach, method_type, error_type, bank,
                              output_format):
        frame = dataset_factory.get_prepared_data_frame(approach,
                                                        method_type,
                                                        error_type,
                                                        bank)
        session_count = _extract_session_count(frame)
        additional_metadata = _extract_metadata(frame)
        net = graphs.create_heuristic_net(frame, output_format)
        return _package_response(net.name, session_count, additional_metadata)

    def _extract_session_count(frame):
        return len(frame.groupby('correlationId'))

    def _extract_metadata(frame):
        method_counts = metadata.get_sessions_per_method_type(frame)
        bank_counts = metadata.get_sessions_per_bank(frame)
        error_counts = metadata.get_sessions_per_error_type(frame)
        return {
            'methods': method_counts,
            'banks': bank_counts,
            'errors': error_counts
        }

    def _package_response(filename, session_count, additional_metadata):
        uri = datauri.DataURI.from_file(filename, 'utf-8')
        # make sure there are no newlines/carriage returns in the uri
        sanitized_uri = uri.replace('\n', '').replace('\r', '')
        return {
            'image': sanitized_uri,
            'numberOfSessions': session_count,
            'metadata': additional_metadata
        }

    # pylint: disable=unused-variable
    @blueprint.route('dfg/get')
    def get_dfg():
        """
        Triggers the creation of a Directly Follows Graph.
        ---
        parameters:
          - name: approach
            in: query
            type: string
            default: ''
            example: 'embedded'
            description: the approach the data used for creating the graph
                         should be limited to
          - name: method_type
            in: query
            type: string
            default: ''
            example: 'get_transactions'
            description: the method type the data used for creating the graph
                         should be limited to
          - name: error_type
            in: query
            type: string
            default: ''
            example: 'error_service_unavailable'
            description: the error type the data used for creating the graph
                         should be limited to
          - name: bank
            in: query
            type: string
            default: ''
            example: 'ADORSYS'
            description: the bank the data used for creating the graph
                         should be limited to
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
        approach, bank, error_type, method_type = _get_filter_parameters()
        output_format = _get_unescaped_parameter('format', 'svg')
        ticket = request_manager.submit_ticketed(_create_dfg, approach,
                                                 method_type, error_type, bank,
                                                 output_format)
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
            description: the approach the data used for creating the net
                         should be limited to
          - name: method_type
            in: query
            type: string
            default: ''
            example: 'get_transactions'
            description: the method type the data used for creating the net
                         should be limited to
          - name: error_type
            in: query
            type: string
            default: ''
            example: 'error_service_unavailable'
            description: the error type the data used for creating the net
                         should be limited to
          - name: bank
            in: query
            type: string
            default: ''
            example: 'ADORSYS'
            description: the bank the data used for creating the net
                         should be limited to
          - name: format
            in: query
            type: string
            default: 'svg'
        responses:
          200:
            description: The result will contain a base64 encoded DataURI
                         representing the generated net.
            schema:
              $ref: '#/definitions/RequestResponse'
        """
        approach, bank, error_type, method_type = _get_filter_parameters()
        output_format = _get_unescaped_parameter('format', 'svg')
        ticket = request_manager.submit_ticketed(_create_heuristic_net,
                                                 approach, method_type,
                                                 error_type, bank,
                                                 output_format)
        return get_state_response(ticket)

    return blueprint
