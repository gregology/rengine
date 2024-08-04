from rengine.strategies import SimpleMath
import pytest
import vcr
import os
from litellm import completion
from fractions import Fraction
from ...helpers import assert_assumptions, scrub_request

@pytest.fixture(scope='session', autouse=True)
def set_openai_api_key():
    if 'OPENAI_API_KEY' not in os.environ:
        os.environ['OPENAI_API_KEY'] = 'foo'

vcr_cassette = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/strategies/simple_math/fixtures/vcr_cassettes",
    record_mode="once",
    match_on=["body"],
    filter_query_parameters=["uri"],
    filter_headers=["authorization", "host"],
    before_record_request=scrub_request,
)

@vcr_cassette.use_cassette('test_simple_addition.yaml')
def test_simple_addition():
    strategy = SimpleMath()
    question = "What is 2 + 2?"
    response = strategy.reason(question)
    assert response.answer == 4

@vcr_cassette.use_cassette('test_assumptions.yaml')
def test_assumptions():
    strategy = SimpleMath()
    question = "John has a pet octopus. The octopus has lost 2 legs. John and the octopus are in an elevator. How many legs are in the elevator?"
    response = strategy.reason(question)

    assert response.answer == 8

    expected_assumptions = [
        "John has 2 legs",
        "The octopus originally had 8 legs",
        "There is no one else in the elevator"
    ]

    assert_assumptions(
        assumptions=response.assumptions,
        expected_assumptions=expected_assumptions
    )

@vcr_cassette.use_cassette('test_hex_multiplications.yaml')
def test_hex_multiplication():
    strategy = SimpleMath()
    question = "double 0x3E8"
    response = strategy.reason(question)

    assert response.answer in (2000, '0x7D0')

    expected_assumptions = [
        "The numbers are hexadecimal"
    ]

    assert_assumptions(
        assumptions=response.assumptions,
        expected_assumptions=expected_assumptions
    )

@vcr_cassette.use_cassette('test_fractions.yaml')
def test_fractions():
    strategy = SimpleMath()
    question = "What is three fifths divided by seven thirteenths?"
    response = strategy.reason(question)

    assert response.answer == Fraction(39, 35)

@vcr_cassette.use_cassette('test_area_calculations.yaml')
def test_area_calculations():
    strategy = SimpleMath()
    question = "A circle has a diameter of 100 inches. What is the area in square meters to 5 decimal places?"
    response = strategy.reason(question)

    assert response.answer == 5.06707

@vcr_cassette.use_cassette('test_boolean_response.yaml')
def test_boolean_response():
    strategy = SimpleMath()
    question = "is the cube root of 48000 larger than pi to the power of pi?"
    response = strategy.reason(question)

    assert response.answer == False
