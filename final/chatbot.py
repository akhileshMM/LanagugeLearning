import anthropic
import streamlit as st
import os
import requests
from io import StringIO

class LightweightSemanticLanguageLearningAssistant:
    def __init__(self, english_file_url, kannada_file_url):
        # Load API key securely (compatible with both Streamlit & CLI)
        api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("API key is missing! Set it in environment variables or Streamlit secrets.")

        # Claude Client
        self.client = anthropic.Anthropic(api_key=api_key)

        # Load Parallel Corpus
        self.parallel_corpus = self.load_parallel_corpus(english_file_url, kannada_file_url)

        # System Prompt
        self.system_prompt = """You are Dhwani, an AI assistant designed to help users learn Kannada in a practical and conversational manner. Your role is to assist users with:
1. Learning the Kannada language through engaging and helpful interactions.
2. Answering user queries about Kannada words, phrases, grammar, culture, and pronunciation.

RESPONSE GUIDELINES:
1. Always provide responses in this structured format:
   - Kannada text
   - English transliteration (Latin script)
   - English translation
   - Pronunciation guide (simple English phonetics)
   - Additional notes (cultural context, practical usage, or fun trivia)

2. Ensure accuracy in translations, contextual use, and pronunciation guidance.
3. Encourage curiosity and interaction by offering tips or follow-up phrases the user can practice.
4. When the user asks general questions, clarify your response using Kannada wherever possible to keep it relevant to learning.
5. Simplify explanations where necessary to help non-native speakers understand effortlessly.

Your focus is on helping the user feel confident and enthusiastic about learning Kannada."""

    def load_parallel_corpus(self, en_file_url, kn_file_url):
        try:
            en_response = requests.get(en_file_url)
            kn_response = requests.get(kn_file_url)
            
            if en_response.status_code != 200 or kn_response.status_code != 200:
                raise ValueError("Failed to download corpus files. Check the provided Google Drive links.")

            english_lines = [line.strip() for line in StringIO(en_response.text).readlines() if line.strip()]
            kannada_lines = [line.strip() for line in StringIO(kn_response.text).readlines() if line.strip()]

            if len(english_lines) != len(kannada_lines):
                raise ValueError("Line count mismatch in corpus files!")

            return list(zip(english_lines, kannada_lines))
        except Exception as e:
            raise RuntimeError(f"Error loading corpus: {e}")

    def generate_conversational_response(self, user_input):
        try:
            completion = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"I want to learn how to communicate in a specific scenario. Here's the context: {user_input}  \n                        Please provide:\n                        1. A practical conversation snippet in Kannada\n                        2. English transliteration of the Kannada text\n                        3. Clear English translation\n                        4. Detailed pronunciation guide using English phonetics\n                        5. Cultural or contextual tips for using this phrase"}
                ]
            )

            return completion.content[0].text
        except Exception as e:
            return f"Oops! Something went wrong. Please try again later."

    def chat_with_dhwani(self):
        print("Welcome to Dhwani! Let's learn Kannada together. Type 'exit' to end the chat.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print("Goodbye! Keep practicing and have fun learning!")
                break

            # Generate conversational response
            response = self.generate_conversational_response(user_input)

            print("Dhwani:", response)
            print("\n")

# Run the chat function
if __name__ == "__main__":
    english_file_url = "YOUR_GOOGLE_DRIVE_ENGLISH_FILE_URL"
    kannada_file_url = "YOUR_GOOGLE_DRIVE_KANNADA_FILE_URL"
    assistant = LightweightSemanticLanguageLearningAssistant(english_file_url, kannada_file_url)
    assistant.chat_with_dhwani()
