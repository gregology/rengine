from typing import List
from dotenv import load_dotenv

load_dotenv()

class Strategy:
    description: str = ''
    example_questions: List[str]  = []
    required_models: List[List[str]]  = []

    def __init__(self):
        self._validate_desctiption()
        self._validate_example_questions()
        self._validate_required_models()
        
    def _validate_desctiption(self):
        if not self.description or not isinstance(self.description, str):
            raise NotImplementedError(f"{self.__class__.__name__} must include a 'description' string class variable.")
        
    def _validate_example_questions(self):
        if not self.example_questions or not isinstance(self.example_questions, list):
            raise NotImplementedError(f"{self.__class__.__name__} must include an 'example_questions' list of strings class variable.")

        for example_question in self.example_questions:
            if not isinstance(example_question, str):
                raise NotImplementedError(f"{self.__class__.__name__} must include an 'example_questions' list of strings class variable.")
            
    def _validate_required_models(self):
        if not self.required_models or not isinstance(self.required_models, list):
            raise NotImplementedError(f"{self.__class__name__} must include a 'required_models' list of lists of strings class variable.")
        
        for required_model in self.required_models:
            if not isinstance(required_model, list):
                raise NotImplementedError(f"{self.__class__name__} must include a 'required_models' list of lists of strings class variable.")
            for model in required_model:
                if not isinstance(model, str):
                    raise NotImplementedError(f"{self.__class__name__} must include a 'required_models' list of lists of strings class variable.")
    
    def reason(self, input):
        raise NotImplementedError("Each strategy must implement the 'reason()' function.")
