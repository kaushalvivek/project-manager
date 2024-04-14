'''
Decider is an intelligent servie. It exposes methods to help make the best choice.
'''
import openai
import json

class Decider:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        pass

    # This method should return the best option provided the decision criteria and the options
    def get_best_option(self, context: str, options: list[str], criteria: list[str]):
        formatted_options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(options)])
        formatted_criteria = "\n".join([f"{i+1}. {criterion}" for i, criterion in enumerate(criteria)])
        system_instruction = f'''
# Mission
You are an expert at deciding the best option for any situation. Your mission is to return the best option out of a \
given set of options by carefully considering the decision criteria.

# Context
{context}

# Decision Criteria (sorted by importance)
{formatted_criteria}

# Instructions
1. Think carefully from first principles and provide the best option based on the context and the decision criteria.
2. You MUST respond in the given output format.
3. Your response MUST be a valid JSON.

# Format

## Input
Options:
1. Option 1
2. Option 2
... (as many as the number of options)

## Output
{{
    "chain_of_thought": (the chain of thought that led to the decision),
    "best_option": (index of the best option)
}}
'''
        response = openai.chat.completions.create(
            model = self.model,
            messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Options:\n{formatted_options}"}
            ],
            temperature=0
        )
        print(formatted_options)
        print(response.choices[0].message.content)
        response_json = json.loads(response.choices[0].message.content)
        return response_json["best_option"]-1

    # This method should return whether to proceed with an action or not, along with follow-ups if any
    def should_proceed(self):
        pass