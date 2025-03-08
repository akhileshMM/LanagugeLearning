import anthropic
import streamlit as st
import os
import requests

class LightweightSemanticLanguageLearningAssistant:
    def __init__(self, english_file_url, kannada_file_url):
        # Load API key securely
        api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("API key is missing! Set it in environment variables or Streamlit secrets.")

        # Claude Client
        self.client = anthropic.Anthropic(api_key=api_key)

        # Download Files from Dropbox
        en_file_path = self.download_from_dropbox(english_file_url, "train.en")
        kn_file_path = self.download_from_dropbox(kannada_file_url, "train.kn")

        # Load Parallel Corpus
        self.parallel_corpus = self.load_parallel_corpus(en_file_path, kn_file_path)

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

    def download_from_dropbox(self, file_url, filename):
        """Download a file from Dropbox and save it locally."""
        try:
            direct_url = file_url.replace("www.dropbox.com", "dl.dropboxusercontent.com")
            response = requests.get(direct_url)

            if response.status_code != 200:
                raise ValueError(f"Failed to download file from {file_url}")

            # Save the file locally
            local_path = f"/tmp/{filename}"
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            return local_path  # Return the local file path
        except Exception as e:
            raise RuntimeError(f"Error downloading file: {e}")

    def load_parallel_corpus(self, en_file_path, kn_file_path):
        """Load the English-Kannada parallel corpus."""
        try:
            print(f"Loading corpus from: {en_file_path}, {kn_file_path}")  # Debugging Line

            if not os.path.exists(en_file_path) or not os.path.exists(kn_file_path):
                raise FileNotFoundError(f"One or both files not found: {en_file_path}, {kn_file_path}")

            with open(en_file_path, "r", encoding="utf-8") as en_file:
                english_lines = [line.strip() for line in en_file.readlines() if line.strip()]

            with open(kn_file_path, "r", encoding="utf-8") as kn_file:
                kannada_lines = [line.strip() for line in kn_file.readlines() if line.strip()]

            if len(english_lines) != len(kannada_lines):
                raise ValueError(f"Line count mismatch in corpus files! English: {len(english_lines)}, Kannada: {len(kannada_lines)}")

            print("Successfully loaded corpus!")  # Debugging Line
            return list(zip(english_lines, kannada_lines))

        except Exception as e:
            print(f"Error loading corpus: {e}")  # Debugging Line
            raise RuntimeError(f"Error loading corpus: {e}")

    def generate_conversational_response(self, user_input):
        try:
            completion = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"I want to learn how to communicate in a specific scenario. Here's the context: {user_input}\nPlease provide:\n1. A practical conversation snippet in Kannada\n2. English transliteration of the Kannada text\n3. Clear English translation\n4. Detailed pronunciation guide using English phonetics\n5. Cultural or contextual tips for using this phrase"}
                ]
            )
            return completion.content[0].text
        except Exception as e:
            return "Oops! Something went wrong. Please try again later."

    def chat_with_dhwani(self):
        print("Welcome to Dhwani! Let's learn Kannada together. Type 'exit' to end the chat.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye! Keep practicing and have fun learning!")
                break

            response = self.generate_conversational_response(user_input)
            print("Dhwani:", response)
            print("\n")

# Run the chat function
if __name__ == "__main__":
    english_file_url = "https://www.dropbox.com/scl/fi/2cbcaonf616sm5wjrw60l/train.en?rlkey=hjqex9ctrc38el4f21cirh8hf&st=4904xh63&dl=0"
    kannada_file_url = "https://www.dropbox.com/scl/fi/ypb9oiw639w6fkkswzqic/train.kn?rlkey=wbop1ro83zqhrkrvd4ooso1ki&st=tm9cozhc&dl=0"
    assistant = LightweightSemanticLanguageLearningAssistant(english_file_url, kannada_file_url)
    assistant.chat_with_dhwani()
