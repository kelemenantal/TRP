import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # Use the environment variable for the API key
)

def read_file_and_query_openai():
    try:
        # Construct the path to the .txt file
        file_path = os.path.join(os.path.dirname(__file__), 'files', 'TVSZ.txt')

        # Read the content of the .txt file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Use the chat completion endpoint, as gpt-4 is a chat model
        completion = client.chat.completions.create(
            model="gpt-4o",  # Use the correct chat model
            messages=[
                {"role": "system", "content": "You are a helpful assistant who reads the provided content and answers questions about it."},
                {"role": "user", "content": f"Here is the content of the file:\n\n{file_content}\n\nHogyan tudom meghatározni a súlyozott tanulmányi átlagomat?"}
            ],
            max_tokens=1000,  # Set an appropriate token limit
            temperature=0.7  # Adjust as per your preference
        )

        # Output the result
        print(completion.choices[0].message.content)  # Access the 'content' field of the message

    except Exception as e:
        print(f"Error reading the file or making the request: {e}")

if __name__ == '__main__':
    read_file_and_query_openai()