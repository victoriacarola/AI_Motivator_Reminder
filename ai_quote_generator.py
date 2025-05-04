# ai_quote_generator.py
from transformers import pipeline, set_seed
import random

# Use GPU if available (device=0)
generator = pipeline('text-generation', model='gpt2', device=0)
set_seed(random.randint(1, 9999))

def generate_motivational_quote():
    prompt = random.choice([
        "Believe in yourself and", 
        "You are capable of", 
        "Success comes from", 
        "Stay positive and", 
        "Every day is"
    ])
    result = generator(prompt, max_length=30, num_return_sequences=1)
    quote = result[0]['generated_text'].strip().replace("\n", " ")
    return quote.split(".")[0] + "."
