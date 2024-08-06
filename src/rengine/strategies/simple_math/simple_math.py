from rengine.strategy import Strategy
from rengine.response import Response
from rengine.helpers import dirty_json_parser
from jinja2 import Environment, FileSystemLoader
from litellm import completion
import re
import os

import math
import numpy
import scipy
import datetime
import decimal
import fractions

class SimpleMath(Strategy):
    description = """
    A strategy capable of answering simple math problems.
    """

    example_questions = [
        "What is 2 + 2?",
        "What is three fifths divided by seven thirteenths?",
        "What is 4 / 2?",
        "Is the cube root of 48000 larger than pi to the power of pi?"
    ]

    required_models = [['ollama/mistral-large:123b'], ['openai/gpt-4o-mini']]

    def load_template(self, template):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(script_dir))
        return env.get_template(f"templates/{template}.j2")

    def reason(self, input : str) -> Response:
        create_formula_template = self.load_template("create_formula")
        create_formula_prompt = create_formula_template.render(input=input)

        raw_response = completion(
            model="openai/gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": create_formula_prompt
                }
            ],
            format = "json"
        )
        message_content = raw_response.choices[0].message.content
        llm_response = dirty_json_parser(message_content)

        exec(llm_response['function'], globals())

        try:
            function_result = formula(**llm_response['function_inputs'])
        except Exception as e:
            print(llm_response)
            if llm_response.get('function'):
                print(f"Function:\n{llm_response['function']}")
            raise

        return Response(
            answer=function_result,
            assumptions=llm_response['assumptions'],
            confidence=0.75 # todo, generate a useful confidence score
        )
