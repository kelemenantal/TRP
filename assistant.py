import os
from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override

# Ensure the environment variable is set
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key is not set in the environment variable")

client = OpenAI(api_key=api_key)

# EventHandler class for handling assistant events
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > {text}", flush=True)
      
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
      
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)
  
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'file_search':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# Function to read the content of the file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

# Main function to create the assistant, read the file, and start the stream
def run_assistant_with_file(file_path, question):
    try:
        # Read the file content
        file_content = read_file(file_path)
        if not file_content:
            return

        # Create assistant
        assistant = client.beta.assistants.create(
            name="ITK GPT",
            instructions="You are a helper for students at a university to answer questions about rules and dates, always provides equations or contact adress",
            tools=[{"type": "file_search"}],
            model="gpt-4o",
        )

        # Create a new thread for the conversation
        thread = client.beta.threads.create()

        # Send a message to the assistant that includes the file content
        user_query = f"Here is the content of the file:\n\n{file_content}\n\n{question}"

        # Start a conversation with the assistant
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )

        # Stream the response
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="You are ITK-Gpt who answers the wuearions of students at Pázmány Péter Chatolic University",
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

    except Exception as e:
        print(f"Error: {e}")

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

    # Adjust the path according to your project structure
    file_path = os.path.join(os.path.dirname(__file__), 'files', 'TVSZ.txt')
    for question in questions:
        print("\nAsking:",question,"\n")
        run_assistant_with_file(file_path, question)
