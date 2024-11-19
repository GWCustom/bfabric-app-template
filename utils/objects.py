import os
import pickle
from typing import List, Dict
from bfabric import Bfabric

try:
    from PARAMS import CONFIG_FILE_PATH
except ImportError:
    CONFIG_FILE_PATH = "~/.bfabricpy.yml"


class Logger:
    """
    A Logger class to manage and batch API call logs locally and flush them to the backend when needed.
    """
    def __init__(self, jobid: int, username: str):
        self.jobid = jobid
        self.username = username
        self.power_user_wrapper = self._get_power_user_wrapper()
        self.logs = self._load_logs_from_dcc()

    def _get_power_user_wrapper(self) -> Bfabric:
        """
        Initializes a B-Fabric wrapper using the power user's credentials.
        """
        power_user_wrapper = Bfabric.from_config(
            config_path=os.path.expanduser(CONFIG_FILE_PATH)
        )
        return power_user_wrapper

    def _load_logs_from_dcc(self) -> List[str]:
        """
        Load logs for the current job from dcc storage.
        """
        try:
            with open(f"log_cache_{self.jobid}.pkl", "rb") as f:
                logs = pickle.load(f)
            return logs
        except FileNotFoundError:
            return []

    def save_logs_to_dcc(self) -> None:
        """
        Save the current logs to dcc storage using pickle.
        """
        with open(f"log_cache_{self.jobid}.pkl", "wb") as f:
            pickle.dump(self.logs, f)

    def log_operation(self, operation: str, message: str, make_log_api_call: bool = False):
        """
        Log an operation either locally (if make_log_api_call=False) or flush to the backend.
        """
        log_entry = f"USER: {self.username} | {operation.upper()} - {message}"

        if make_log_api_call:
            self.logs.append(log_entry)  # Temporarily append for flushing
            self.flush_logs()  # Flush all logs, including the new one
        else:
            self.logs.append(log_entry)  # Append to local logs
            self.save_logs_to_dcc()  # Save locally

    def flush_logs(self):
        """
        Send all accumulated logs for this job to the backend and clear the local cache.
        """
        if not self.logs:
            return  # No logs to flush

        try:
            full_log_message = "\n".join(self.logs)
            self.power_user_wrapper.save("job", {"id": self.jobid, "logthis": full_log_message})
            self.logs = []  # Clear logs after successful flush
            self.save_logs_to_dcc()  # Save the cleared state to dcc
        except Exception as e:
            print(f"Failed to save log to B-Fabric: {e}")

    def logthis(self, api_call: callable, *args, make_log_api_call: bool = True, **kwargs) -> any:
        """
        Generic logging function to wrap any API call using a Logger instance.
        """
        # Construct a message describing the API call
        call_args = ', '.join([repr(arg) for arg in args])
        call_kwargs = ', '.join([f"{key}={repr(value)}" for key, value in kwargs.items()])
        log_message = f"{api_call.__name__}({call_args}, {call_kwargs})"

        # Execute the actual API call
        result = api_call(*args, **kwargs)

        # Log the operation
        self.log_operation(api_call.__name__, log_message, make_log_api_call=make_log_api_call)

        return result
