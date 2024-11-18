from bfabric import Bfabric


class Logger:
    def __init__(self, jobid: int):
        """
        Initialize a logger for a specific job and user.
        """
        self.jobid = jobid
        self.power_user_wrapper = self._get_power_user_wrapper()

    def _get_power_user_wrapper(self) -> Bfabric:
        """
        Initializes a B-Fabric wrapper using the power user's credentials.

        Returns:
            A B-Fabric wrapper instance authenticated as the power user.
        """
        power_user_wrapper = Bfabric.from_config(
            config_path="~/.bfabricpy.yml"
        )
        return power_user_wrapper

    def commit_log(self, log_message: str):
        """
        Save the log data to the B-Fabric database using the power user credentials.

        Args:
            log_message: A string containing the details of the API call.
        """
        try:
            # Use the power user's wrapper to log the message
            self.power_user_wrapper.save("job", {"id": self.jobid, "logthis": log_message})
        except Exception as e:
            print(f"Failed to save log to B-Fabric: {e}")



def lread(jobid: int,wrapper, inputs: dict):
    """
    Logged read function for B-Fabric API.

    Args:
        jobid: The job ID for logging.
        wrapper: The B-Fabric user API wrapper instance.
        inputs: A dictionary containing inputs for the `read` method.

    Returns:
        The result of the original `read` call.
    """
    log = Logger(jobid)

    # Construct the log message
    log_message = f"wrapper.read(endpoint={inputs.get('endpoint')}, obj={inputs.get('obj')}, max_results={inputs.get('max_results')})"

    # Execute the original API call
    result = wrapper.read(
        endpoint=inputs.get("endpoint"),
        obj=inputs.get("obj"),
        max_results=inputs.get("max_results")
    )

    log.commit_log(log_message)

    return result


def lsave(jobid: int, wrapper, inputs: dict):
    """
    Logged save function for B-Fabric API.

    Args:
        jobid: The job ID for logging.
        wrapper: The B-Fabric user API wrapper instance.
        inputs: A dictionary containing inputs for the `save` method.

    Returns:
        The result of the original `save` call.
    """
    log = Logger(jobid)

    # Construct the log message
    log_message = f"wrapper.save(endpoint={inputs.get('endpoint')}, obj={inputs.get('obj')})"

    # Execute the original API call
    result = wrapper.save(
        endpoint=inputs.get("endpoint"),
        obj=inputs.get("obj")
    )

    log.commit_log(log_message)

    return result
