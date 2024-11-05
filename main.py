import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def read_file_and_query_openai(question):
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
                {"role": "user", "content": f"Here is the content of the file:\n\n{file_content}\n\n{question}"}
            ],
            max_tokens=1000,  # Set an appropriate token limit
            temperature=0.7  # Adjust as per your preference
        )

        # Output the result
        print(completion.choices[0].message.content)  # Access the 'content' field of the message

    except Exception as e:
        print(f"Error reading the file or making the request: {e}")

if __name__ == '__main__':

            # List of questions to ask
    questions = [
        "Hogyan tudom meghatározni a súlyozott tanulmányi átlagomat?",
        "Mi a TVSZ hatálya?",
        "Ki jogosult a hallgatói jogviszony megszüntetésére tanulmányi okból?",
        "Mikor lehet kérvényezni a passzív félévet szülés, baleset vagy váratlan esemény miatt?",
        "Mit jelent a Tanulmányi Bizottság (TB) hatásköre?",
        "Hogyan lehet kérelmet benyújtani a Neptun rendszeren keresztül?",
        "Ki dönt a kreditátvitelről, ha más intézményben szerzett kreditről van szó?",
        "Milyen feltételekkel lehet passzív félévet kérni az első tanulmányi időszak előtt?",
        "Mi a következménye annak, ha egy kérelmet határidőn túl nyújtanak be?",
        "Mi történik, ha a Neptun rendszerben hibás címet ad meg a hallgató?",
        "Hogyan történik a beiratkozás az első félévre?",
        "Mit jelent a tantárgyfelvétel szabályozása a mintatanterv alapján?",
        "Mi a különbség a CV és az EV kurzus között?",
        "Mely tantárgyakhoz tartozhatnak előfeltételek?",
        "Hány féléves szorgalmi időszakot szabályoz a TVSZ?",
        "Mi a hallgatói jogviszony keletkezésének folyamata?",
        "Milyen esetekben kell dékáni engedély a hallgatói jogviszony szüneteléséhez?",
        "Mik a következményei annak, ha a hallgató nem fizeti meg az önköltség összegét időben?",
        "Mit kell tennie a hallgatónak, ha változik a lakcíme vagy más személyes adata?",
        "Hány félév szüneteltethető egyben hallgatói jogviszony alatt?",
        "Milyen esetekben törölhetők a hallgató által felvett tantárgyak?",
        "Hogyan lehet mentesítést kérni a tanulmányi kötelezettségek alól?",
        "Milyen jogosultságokat veszít el a hallgató a hallgatói jogviszony szünetelése alatt?",
        "Mi a specializáció és hogyan lehet rá jelentkezni?",
        "Mit jelent a minor program, és kötelező-e elvégezni?",
        "Mik a szünetelő hallgatói jogviszony szabályai?",
        "Milyen szabályok vonatkoznak a vizsgakurzus felvételére?",
        "Milyen típusú kurzusok tartoznak a tantárgyakhoz?",
        "Milyen határidők vonatkoznak a tantárgyfelvételre?",
        "Hogyan lehet halasztott beiratkozást vagy bejelentkezést kérni?",
        "Milyen dokumentumokat kell benyújtani beiratkozáskor?"
    ]
    for question in questions:
        print("\nAsking:",question,"\n")
        read_file_and_query_openai(question)