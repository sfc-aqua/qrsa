from abc import ABCMeta


class AbstractConnectionManager(metaclass=ABCMeta):
    async def respond_to_connection_setup_request():
        """
        Responding to connection setup request only used in responder
        """
        pass

    async def forward_connection_setup_request():
        """
        Forward incoming connection setup request to next hop
        """
        pass

    async def reject_connection_setup_request():
        """
        Reject connection setup
        """
        pass
