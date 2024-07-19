from litellm import completion
from rengine.helpers import dirty_json_parser
import pytest

def assert_assumptions(expected_assumptions, assumptions, model='openai/gpt-4o-mini'):
    for expected_assumption in expected_assumptions:
        prompt = f"""
        Is the following assumption
        
        "{expected_assumption}"

        in this list of assumptions or apparent from multiple assumptions?

        {assumptions}

        Respond with a JSON object that contains a single boolean value called `exists`. For example;
        `{{"exists": true}}`
        """

        raw_response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format = "json"
        )

        message_content = raw_response.choices[0].message.content
        llm_response = dirty_json_parser(message_content)
        if llm_response['exists']:
            pass
            # add something here so that these "assertions" are counted as tests
        else:
            pytest.fail(f"This expected assumption '{expected_assumption}' was not found in these given assumptions {assumptions}")

def scrub_request(request):
    request.uri = 'REDACTED'
    return request
