
class DeadContainerException(ChildProcessError):
    """
    Exception for when a container has died.

    Args:
        message (str): Human readable error message
        exitcode (int): The non-zero exit code of the container
        logs (str): Logs the container produced

    """
    def __init__(self, message, exitcode, logs, *args):
        super().__init__(message, *args)
        #: Exit code of container
        self.exitcode = exitcode
        #: Stdout and stderr of container
        self.logs = logs


class SingularityVersionException(ValueError):
    pass

class ApptainerVersionException(ValueError):
    pass
