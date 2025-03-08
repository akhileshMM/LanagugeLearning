import anthropic
import streamlit as st  # Import Streamlit for secrets

class LightweightSemanticLanguageLearningAssistant:
    def __init__(self, english_file, kannada_file):  
        # Load API key securely from Streamlit Secrets
        api_key = st.secrets["ANTHROPIC_API_KEY"]

        if not api_key:
            raise ValueError("API key is missing! Set it in .streamlit/secrets.toml or Streamlit Cloud Secrets.")

        # Claude Client
        self.client = anthropic.Anthropic(api_key=api_key)

        # Load Parallel Corpus
        self.parallel_corpus = self.load_parallel_corpus(english_file, kannada_file)

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

    def load_parallel_corpus(self, en_file, kn_file):
        with open(en_file, 'r', encoding='utf-8') as en, \
             open(kn_file, 'r', encoding='utf-8') as kn:
            english_lines = [line.strip() for line in en.readlines() if line.strip()]
            kannada_lines = [line.strip() for line in kn.readlines() if line.strip()]

            assert len(english_lines) == len(kannada_lines), "Line count mismatch"
            return list(zip(english_lines, kannada_lines))

    def generate_conversational_response(self, user_input):
        try:
            completion = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""I want to learn how to communicate in a specific scenario. Here's the context: {user_input}  
                        Please provide:
                        1. A practical conversation snippet in Kannada
                        2. English transliteration of the Kannada text
                        3. Clear English translation
                        4. Detailed pronunciation guide using English phonetics
                        5. Cultural or contextual tips for using this phrase"""
                    }
                ],
                system=self.system_prompt
            )

            return completion.content[0].text
        except Exception as e:
            return f"Oops! Something went wrong: {e}"

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
    assistant = LightweightSemanticLanguageLearningAssistant('https://drive.google.com/file/d/1CfEjk00-gQsPfjaPtDRgzC47jV1dgvqc/view?usp=drive_link', 'https://drive.google.com/file/d/1vD8zNxF5eG6NvWwkvirymPEHQGbbwPss/view?usp=drive_link')
    assistant.chat_with_dhwani()
