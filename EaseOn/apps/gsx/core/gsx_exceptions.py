class GSXResourceNotAvailableError(Exception):
    """Exception raised if gsx cert and key not available.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Unable to locate GSX Cert or Key Files"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

class GSXUnauthorizdError(Exception):
    """Exception raised if we recieve Unauthorized Response.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Received Unauthorizd Message from GSX"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'