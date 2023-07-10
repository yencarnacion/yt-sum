from env import OPENAI_API_KEY
from llama_index import StorageContext, load_index_from_storage
from bs4 import BeautifulSoup
import os
import openai

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise Exception('OPENAI_API_KEY environment variable not set')
    sys.exit(1)
    
def append_to_output(question, answer):
    # Open the HTML file and turn it into a BeautifulSoup object
    with open("./output/output.html", 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    # Find the body tag in the HTML
    body = soup.find('body')

    # Create the new h2 tag and p tag
    new_h2 = soup.new_tag('h2')
    new_h2.string = question
    new_p = soup.new_tag('p')
    new_p.string = answer

    # Append these tags to the body
    body.append(new_h2)
    body.append(new_p)

    # Write the changes back to the file
    with open("./output/output.html", "w") as f:
        f.write(str(soup))


def process_input(user_input):
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)


    query_engine = index.as_query_engine()

    question_01 = user_input
    response_01 = query_engine.query(question_01)

    response = [ {question_01: response_01.response} ]
    
    return response

while True:  # Start an infinite loop
    try:
        # Read the input
        user_input = input('Ask something: ')

        # Process the input
        response = process_input(user_input)

        answer = list(response[0].values())[0]

        # Print the output
        print(f">>>{answer}")
        print("<<<\n")
        append_to_output(user_input,answer)
    except KeyboardInterrupt:
        print("REPL terminated by user.")
        break
