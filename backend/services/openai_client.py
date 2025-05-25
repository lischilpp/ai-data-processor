import openai
import logging
from django.conf import settings
import json

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY  # Set OpenAI API key from settings

    def generate_python_code(self, input_files_description, instruction):
        """Generate Python code using OpenAI based on the instruction."""
        logger.info("Generating Python code using OpenAI with structured outputs.")
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content":
                f"""
                    You are a helpful assistant that generates Python code. 
                    Write all processed files in the code you generate in the directory 'output/'.
                    If the instruction is to create a website, write a python program that writes an HTML file.
                    The input files are: {input_files_description}.
                    Use those descriptions to understand their contents structure.
                    ALWAYS READ THE DATA FROM THE ACTUAL FILES!
                    The description of the python code to generate is:
                """},
                {"role": "user", "content": f"{instruction}"}
            ],
            functions=[{
                "name": "generate_code_output",
                "description": "Generates Python code in a structured output format",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "python_code": {
                            "type": "string",
                            "description": "Generated valid Python code"
                        }
                    },
                    "required": ["python_code"]
                }
            }],
            function_call={"name": "generate_code_output"}
        )
        
        # Handle structured output
        generated_code = json.loads(response.choices[0].message.function_call.arguments)["python_code"]
        return generated_code.strip()
    
    def request_dependencies(self, generated_code):
        """Request to list dependencies required to run the generated code."""
        logger.info("Requesting dependencies from OpenAI.")
        response_dependencies = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that lists Python package dependencies."},
                {"role": "user", "content": f"List all dependencies required to run the following Python code: {generated_code}. Provide the output as a comma-separated list without any explanations or comments. Omit preinstalled packages. If there are no dependencies, return the word 'None'."}
            ],
        )
        dependencies = response_dependencies.choices[0].message.content.strip().split(",")
        return [dep.strip() for dep in dependencies]  # Clean up dependency names

    def fix_generated_code(self, generated_code, error_output):
        """Fix the generated Python code based on the error output."""
        logger.info("Requesting to fix Python code based on error output.")
        
        response_fix = openai.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You are an expert Python developer tasked with fixing code based on the error message."},
                {"role": "user", "content": f"The following Python code generated an error:\n\n{generated_code}\n\nThe error message is:\n\n{error_output}\n\nPlease provide a corrected version of the code."}
            ],
            functions=[{
                "name": "fix_code_output",
                "description": "Fixes the provided Python code based on the error output",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fixed_code": {
                            "type": "string",
                            "description": "Fixed version of the Python code"
                        }
                    },
                    "required": ["fixed_code"]
                }
            }],
            function_call={"name": "fix_code_output"}
        )
        
        # Handle structured output
        fixed_code = json.loads(response_fix.choices[0].message.function_call.arguments)["fixed_code"]
        return fixed_code.strip()
