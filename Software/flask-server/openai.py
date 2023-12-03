import openai
import json
import requests
import sys

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

plant = sys.arg[1]

# Your question
question = f'''what is the ideal ph, ideal electrical conductivity, and ideal temperature 
of water and ideal hours of light for {plant} to grow in hydroponically. 
please give the answer as a json object with min ph, max ph, min electrical conductivity,
max electrical conductivity  (where the is max difference between min and max ec is 0.5), min hours of light, max hours of light, min temperature, max temperature'''

# Make the API call
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=question,
    temperature=0.7,
    max_tokens=200
)

# Extract the generated text from the response
answer_text = response["choices"][0]["text"]

# Print the answer
print("Answer:")
print(answer_text)

# Parse the answer into a JSON object
json_answer = json.loads(answer_text)

# Print the JSON object
print("\nJSON Object:")
print(json.dumps(json_answer, indent=2))