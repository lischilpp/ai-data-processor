import subprocess
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PodmanExecutor:
    def __init__(self):
        self.container_name = "python-container"

    def build_container(self, container_name):
        """Build a container from the local directory."""
        try:
            image_build_directory = Path("podman-image")

            # Ensure the image build directory exists
            if not image_build_directory.is_dir():
                logger.error(f"The specified image build directory does not exist: {image_build_directory}")
                return False

            # Build the container from the specified directory
            subprocess.run(
                ["podman", "build", "-t", self.container_name, str(image_build_directory)],
                check=True
            )
            logger.info(f"Built the container: {self.container_name}")
            return True  # Return the container name upon success

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build container: {str(e)}")
            return None

    def execute_script(self, shared_directory):
        """Build and run the container which executes the Python code in the Dockerfile."""
        
        # Build the container first
        if not self.build_container(self.container_name):
            return False ,"Container build failed."

        logger.info(f"Running the container: {self.container_name}")
        try:
            # Run the container; capture both stdout and stderr to handle errors directly
            result = subprocess.run(
                ["podman", "run", "--rm", "--name", self.container_name, "-v", f"{shared_directory}:/app", self.container_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            logger.info(f"Container ran successfully: {self.container_name}")
            return True, result.stdout.decode()

        except subprocess.CalledProcessError as e:
            # Capture the error output directly from the exception
            error_output = e.stderr.decode() if e.stderr else "No error output"

            return False, error_output

    def remove_container(self):
        """Remove the persistent Podman container."""
        logger.info(f"Removing container: {self.container_name}")
        subprocess.run(
            ["podman", "rm", "-f", self.container_name],
            check=True
        )
