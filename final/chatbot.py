import anthropic
import streamlit as st
import os

class LightweightSemanticLanguageLearningAssistant:
    def __init__(self, english_file, kannada_file):
        # Load API key securely (compatible with both Streamlit & CLI)
        api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError("API key is missing! Set it in environment variables or Streamlit secrets.")

        # Claude Client
        self.client = anthropic.Anthropic(api_key=api_key)

        # Load Parallel Corpus
        self.parallel_corpus = self.load_parallel_corpus(english_file, kannada_file)

        # System Prompt
        self.system_prompt = (
            "You are Dhwani, an AI assistant designed to help users learn Kannada in a practical and conversational manner."
            "\n\nYour role is to assist users with:\n"
            "1. Learning the Kannada language through engaging and helpful interactions.\n"
            "2. Answering user queries about Kannada words, phrases, grammar, culture, and pronunciation."
            "\n\nRESPONSE GUIDELINES:\n"
            "- Provide structured responses:\n"
            "  1. Kannada text\n  2. English transliteration\n  3. English translation\n  4. Pronunciation guide\n  5. Cultural/context tips"
            "\n- Ensure accurate translations, pronunciation, and usage examples."
            "\n- Encourage curiosity with follow-up practice phrases."
        )

    def load_parallel_corpus(self, en_file, kn_file):
        try:
            with open(en_file, 'r', encoding='utf-8') as en, open(kn_file, 'r', encoding='utf-8') as kn:
                english_lines = [line.strip() for line in en.readlines() if line.strip()]
                kannada_lines = [line.strip() for line in kn.readlines() if line.strip()]

                if len(english_lines) != len(kannada_lines):
                    raise ValueError("Line count mismatch in corpus files!")

                return list(zip(english_lines, kannada_lines))
        except FileNotFoundError:
            raise FileNotFoundError("Corpus file not found. Ensure both English and Kannada files exist.")

    def generate_conversational_response(self, user_input):
        try:
            completion = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"I want to learn Kannada for this scenario: {user_input}\n"
                     "Provide:\n1. A practical conversation snippet\n2. English transliteration\n3. English translation\n4. Pronunciation guide\n5. Cultural tips."}
                ]
            )
            return completion.content[0].text
        except Exception as e:
            return "Oops! Something went wrong. Please try again later."

# Streamlit Interface
def main():
    st.title("Dhwani - Kannada Learning Assistant")
    st.write("Type a scenario to learn how to communicate in Kannada!")
    
    assistant = LightweightSemanticLanguageLearningAssistant('kannada_en.txt', 'kannada_kn.txt')
    
    user_input = st.text_input("Enter a scenario:")
    if st.button("Get Response") and user_input:
        response = assistant.generate_conversational_response(user_input)
        st.write(response)

if __name__ == "__main__":
    main()
