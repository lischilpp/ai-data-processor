import logging
from groq import Groq
from django.conf import settings


logger = logging.getLogger(__name__)

class GroqApiClient:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = 'llama-3.3-70b-versatile'

    def generate_python_code(self, input_files_description, instruction):
        """Generate Python code using the specified model."""
        logger.info("Generating Python code.")
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""
                        You are a machine that only generates Python code without any comments or explanations.
                        Write all processed files in the code you generate in the directory 'output/'.
                        If the instruction is to create a website, write a python program that writes an HTML file.
                        The input files are: {input_files_description}.
                        Use those descriptions to understand their contents structure.
                        ALWAYS READ THE DATA FROM THE ACTUAL FILES!
                        ALWAYS WRITE ONE OR MULTIPLE OUTPUT FILES IN THE 'output/' DIRECTORY.
                        Only output valid python code without any comments or explanations.
                        The description of the python code to generate is will be provided in the next message.
                    """
                },
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            model=self.model,  # Specify the model
        )
        
        generated_code = chat_completion.choices[0].message.content.strip()
        generated_code = generated_code.strip("`").replace("python", "").strip()
        return generated_code

    def request_dependencies(self, generated_code):
        """Request to list dependencies required to run the generated code."""
        logger.info("Requesting dependencies.")
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        You are a helpful assistant that lists Python package dependencies.
                        List all dependencies required to run the following Python code: {generated_code}. 
                        Provide the output as a comma-separated list without any explanations or comments. 
                        Omit preinstalled packages. If there are no dependencies, return the word 'None'.
                    """
                }
            ],
            model=self.model,
        )
        
        dependencies = chat_completion.choices[0].message.content.strip().split(",")
        return [dep.strip() for dep in dependencies if dep.strip()]  # Clean and return dependencies

    def fix_generated_code(self, generated_code, error_output):
        """Fix the generated Python code based on the error output."""
        logger.info("Requesting to fix Python code based on error output.")
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        You are an machine that generates Python code based on the old code and an error message.
                        You can only output valid python code without any comments or explanations.
                        The old python code and its error will be provided in the next message.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                        The following Python code generated an error:\n\n{generated_code}\n\n
                        The error message is:\n\n{error_output}\n\n
                    """
                }
            ],
            model=self.model,
        )

        generated_code = chat_completion.choices[0].message.content.strip()
        generated_code = generated_code.strip("`").replace("python", "").strip()
        
        return generated_code