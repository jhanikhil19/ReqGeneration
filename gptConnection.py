import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

import sys
print(sys.path)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# response = model.generate_content("Explain how AI works")
# print(response.text)