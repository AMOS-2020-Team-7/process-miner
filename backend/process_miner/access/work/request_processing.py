"""
Module for handling asynchronous request processing
"""
import threading

from flask_executor import Executor


class _TicketDispenser:
    """
    Class for keeping track of request ids in a multi-threaded environment
    """
    def __init__(self):
        self._next_ticket = 1
        self._lock = threading.Lock()

    def get_ticket(self) -> str:
        """
        Retrieves the next ticket
        :return: string representation of the ticket
        """
        with self._lock:
            ticket = self._next_ticket
            self._next_ticket += 1

        return str(ticket)


class RequestManager:
    """
    Wrapper class around Executor for accessing request states and results
    """
    def __init__(self, app=None, name=''):
        self._executor = Executor(app, name)
        self._ticket_dispenser = _TicketDispenser()

    def submit_ticketed(self, function, *args, **kwargs) -> str:
        """
        Submits a function for execution and returns an id for later access to
        the requests state and result.
        :param function: the function
        :param args: the functions arguments
        :return: the id of the submitted execution request
        """
        key = self._ticket_dispenser.get_ticket()
        self._executor.submit_stored(key, function, *args, **kwargs)
        return key

    def request_processed(self, request_id: str) -> bool:
        """
        Checks if a request has already been processed.
        :param request_id: id of the request
        :return: True if the request was processed else False
        """
        return self._executor.futures.done(request_id)

    def get_result(self, request_id: str):
        """
        Returns the result of a finished request.
        :param request_id: id of the request
        :return: the result of the request
        """
        return self._executor.futures.pop(request_id).result()
