"""
Blueprint module responsible for retrieving different graph types
"""
import base64

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
    def _create_dfg():
        graph = graph_factory.get_directly_follows_graph()
        return _package_response(graph)

    @cache.memoize()
    def _create_heuristic_net(threshold: float = 0.0):
        graph = graph_factory.get_heuristic_net(threshold)
        return _package_response(graph)

    def _package_response(graph):
        with open(graph.name) as file:
            contents = file.read().encode('utf-8')
        base64_bytes = base64.b64encode(contents)
        return {
            'image': 'data:image/svg+xml;base64,' + base64_bytes.decode(
                'utf-8')
        }

    @blueprint.route('dfg/get')
    def get_dfg():
        """
        Triggers the creation of a Directly Follows Graph.
        """
        ticket = request_manager.submit_ticketed(_create_dfg)
        return get_state_response(ticket)

    @blueprint.route('hn/get')
    def get_hn():
        """
        Triggers the creation of a Heuristic net.
        """
        threshold = float(request.args.get('threshold', 0))
        print(threshold)
        print(type(threshold))
        ticket = request_manager.submit_ticketed(_create_heuristic_net,
                                                 threshold)
        return get_state_response(ticket)

    return blueprint
