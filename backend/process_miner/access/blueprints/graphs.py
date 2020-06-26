"""
Blueprint module responsible for retrieving different graph types
"""

import datauri
from flask import Blueprint, request
from flask_caching import Cache

from process_miner.access.blueprints.request_result import get_state_response
from process_miner.access.work.request_processing import RequestManager
from process_miner.mining.graph_factory import GraphFactory


def create_blueprint(request_manager: RequestManager, cache: Cache,
                     graph_factory: GraphFactory):
    """
    Creates an instance of the blueprint.
    """
    blueprint = Blueprint('graphs', __name__, url_prefix='/graphs')

    @cache.memoize()
    def _create_dfg(approach):
        graph = graph_factory.get_directly_follows_graph(approach)
        return _package_response(graph)

    @cache.memoize()
    def _create_heuristic_net(approach, threshold, output_format):
        graph = graph_factory.get_heuristic_net(approach, threshold,
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
        approach = request.args.get('approach', '', str).lower()
        ticket = request_manager.submit_ticketed(_create_dfg, approach)
        return get_state_response(ticket)

    @blueprint.route('hn/get')
    def get_hn():
        """
        Triggers the creation of a Heuristic net.
        """
        approach = request.args.get('approach', '', str).lower()
        threshold = request.args.get('threshold', 0.0, float)
        output_format = request.args.get('format', 'svg', str).lower()
        ticket = request_manager.submit_ticketed(_create_heuristic_net,
                                                 approach, threshold,
                                                 output_format)
        return get_state_response(ticket)

    return blueprint
