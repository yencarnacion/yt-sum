from youtube_transcript_api import YouTubeTranscriptApi
import argparse
from urllib.parse import urlparse, parse_qs
from env import OPENAI_API_KEY
import os
from llama_index import download_loader, GPTVectorStoreIndex
from pathlib import Path
import tempfile
from llama_index import ServiceContext
from llama_index import StorageContext, load_index_from_storage
import sys
import openai

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise Exception('OPENAI_API_KEY environment variable not set')
    sys.exit(1)

def extract_video_id(url):
    # Parse the URL
    query = urlparse(url)

    # Extract the video ID from the query parameters
    video_id = parse_qs(query.query).get('v')

    if video_id:
        return video_id[0]
    else:
        return None

def get_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    return transcript

def index_persist(transcript):
    UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)
    loader = UnstructuredReader()

    # Create a temporary file and write the string data to it
    with tempfile.NamedTemporaryFile(delete=False,  mode='w') as temp:
        for item in transcript:
            text = item['text']
            temp.write(text +'\n')
        temp_file_path = Path(temp.name)
    
    # Load the data from the temporary file
    data = loader.load_data(file=temp_file_path, split_documents=False)

    service_context = ServiceContext.from_defaults(chunk_size_limit=512)

    cur_index = GPTVectorStoreIndex.from_documents(data, service_context=service_context)

    cur_index.storage_context.persist()


def get_summary():
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()

    
    question_01 = "what is this video about?"
    response_01 = query_engine.query(question_01)

    question_02 = "can you give me a very clear explanation of the core assertions, implications, and mechanics elucidated in this video?"
    response_02 = query_engine.query(question_02)

    question_03 = "can you explain the value of this in basic terms? Like you're talking to a ceo. so what? what's the bottom line here?"
    response_03 = query_engine.query(question_03)

    question_04 = "can you give me an analogy or metaphor that will help explain this to a broad audience"
    response_04 = query_engine.query(question_04)

    response = [ {question_01: response_01.response},
                 {question_02: response_02.response},
                 {question_03: response_03.response},
                 {question_04: response_04.response}
                ]

    return response

def write_response_to_file(video_id, response):
    # Starting the HTML string
    html_string = f"""<!DOCTYPE html>
    <html>
    <head>
    <title>{video_id}</title>
    <style>
    body {{
    font-family: Arial, sans-serif;
    }}
    h1 {{
    font-weight: bold;
    }}
    h2 {{
    font-weight: bold;
    }}
    </style>
    </head>
    <body>
    """
    html_string += f'<h1>Embedded YouTube Video</h1>\n<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>\n'

    # Appending each question and response
    for r in response:
        for question, answer in r.items():
            html_string += f"<h2>{question}</h2>\n<p>{answer}</p>\n"
            
    # Closing the HTML string
    html_string += """
    </body>
    </html>
    """

    # Make directory if it doesn't exist
    if not os.path.exists('./output'):
        os.makedirs('./output')
        
    # Writing the HTML string to a file
    with open(os.path.expanduser("./output/output.html"), "w") as file:
        file.write(html_string)

def main():
    # Initialize the ArgumentParser object
    parser = argparse.ArgumentParser(description='Summarize a YouTube video from URL.')

    # Add an argument for the YouTube URL
    parser.add_argument('url', type=str, help='The YouTube video URL.')

    # Parse the arguments
    args = parser.parse_args()

    # Extract the video ID
    video_id = extract_video_id(args.url)

    # Print the video ID
    if video_id:
        print(f'Video ID: {video_id}')
    else:
        print('Invalid URL or no video ID found.')
        sys.exit(1)

    # check if something already stored in ./storage
    # if not persist index
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        del storage_context
    except FileNotFoundError as e:
        transcript = get_video_transcript(video_id)
        if not transcript:
            print('Invalid transcript or transcript found.')
            sys.exit(1)
        
        index_persist(transcript)

    response = get_summary()

    write_response_to_file(video_id, response)
    
if __name__ == "__main__":
    main()
