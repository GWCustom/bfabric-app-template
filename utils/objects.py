from bfabric import Bfabric
import os
import json
from typing import List, Dict


try:
    from PARAMS import CONFIG_FILE_PATH
except ImportError:
    CONFIG_FILE_PATH = "~/.bfabricpy.yml"


class Logger:
    log_cache: Dict[int, List[str]] = {}  # Shared log cache for all Logger instances (keyed by jobid)

    def __init__(self, jobid: int, username: str):
        """
        Initialize a logger for a specific job and user.
        """
        self.jobid = jobid
        self.username = username
        self.power_user_wrapper = self._get_power_user_wrapper()
        if jobid not in Logger.log_cache:
            Logger.log_cache[jobid] = []  # Initialize cache for this job ID

    def to_json(self) -> str:
        """
        Convert the log cache to a JSON.
        """

        # TODO Implement this method
        pass

    def _get_power_user_wrapper(self) -> Bfabric:
        """
        Initializes a B-Fabric wrapper using the power user's credentials.

        Returns:
            A B-Fabric wrapper instance authenticated as the power user.
        """
        power_user_wrapper = Bfabric.from_config(
            config_path=os.path.expanduser(CONFIG_FILE_PATH)
        )
        return power_user_wrapper

    def log_operation(self, operation: str, message: str, make_log_api_call: bool = False):
        """
        Generic log function for any operation.

        Args:
            operation: The type of operation being logged (e.g., "read", "save", "bug").
            message: The log message.
            make_log_api_call: Whether to send the log to the API (default: False).
        """
        log_entry = f"USER: {self.username} | {operation.upper()} - {message}"
        Logger.log_cache[self.jobid].append(log_entry)  # Add to the shared log cache

        if make_log_api_call:
            self.flush_logs()  # Flush all logs to the API if an API call is made

    def flush_logs(self):
        """Send all accumulated logs to the API and clear the cache."""
        if not Logger.log_cache[self.jobid]:
            return  # No logs to flush

        try:
            full_log_message = "\n".join(Logger.log_cache[self.jobid])
            self.power_user_wrapper.save("job", {"id": self.jobid, "logthis": full_log_message})
            Logger.log_cache[self.jobid] = []  # Clear the cache after successful flush
        except Exception as e:
            print(f"Failed to save log to B-Fabric: {e}")

    def get_logs(self) -> str:
        """
        Retrieve all stored logs for this job as a single string.
        """
        return json.dumps(Logger.log_cache[self.jobid], indent=2)
    

def logthis(jobid: int, username: str, api_call: callable, *args, make_log_api_call: bool = True, **kwargs) -> any:

    # TODO Implement this function as an instance method of the Logger class
    """
    Generic logging function to wrap any API call.

    Args:
        jobid: The job ID for logging.
        username: The username for logging.
        api_call: The actual API call to execute (e.g., wrapper.read or wrapper.save).
        *args: Positional arguments for the API call.
        make_log_api_call: Whether to log this operation via an API call (default: True).
        **kwargs: Keyword arguments for the API call.

    Returns:
        The result of the original API call.
    """
    log = Logger(jobid, username)

    # Construct a message describing the API call
    call_args = ', '.join([repr(arg) for arg in args])
    call_kwargs = ', '.join([f"{key}={repr(value)}" for key, value in kwargs.items()])
    log_message = f"{api_call.__name__}({call_args}, {call_kwargs})"

    # Execute the actual API call
    result = api_call(*args, **kwargs)

    # Log the operation
    if make_log_api_call:
        # Log and flush all accumulated logs to the database
        log.log_operation(api_call.__name__, log_message, make_log_api_call=True)
    else:
        # Log locally without flushing to the database
        log.log_operation(api_call.__name__, log_message, make_log_api_call=False)

    return result