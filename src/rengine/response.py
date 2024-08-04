from fractions import Fraction

class Response:
    def __init__(self, answer, assumptions, confidence):
        self.answer = answer
        self.assumptions = assumptions
        self.confidence = confidence

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        if type(value) not in (str, float, int, bool, Fraction):
            raise ValueError("Answer must be either a string, number, or boolean.")
        self._answer = value

    @property
    def assumptions(self):
        return self._assumptions

    @assumptions.setter
    def assumptions(self, value):
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError("Assumptions must be a list of strings.")
        self._assumptions = value

    @property
    def confidence(self):
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if not isinstance(value, float) or not (0 <= value <= 1):
            raise ValueError("Confidence must be a float between 0 and 1.")
        self._confidence = value

    def __str__(self):
        return self.answer
