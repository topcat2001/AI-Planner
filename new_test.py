import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and model from environment
api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('AI_MODEL', 'o3-mini')

# Set the API key directly
openai.api_key = api_key

print(f"Testing connection to OpenAI API with model: {model}")

try:
    # Make a simple request to the API using the module-level client
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, what year is it currently?"}
        ],
        max_completion_tokens=150
    )
    
    # Print response
    print("\nConnection successful!")
    print(f"Model response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\nError connecting to OpenAI API: {e}")
