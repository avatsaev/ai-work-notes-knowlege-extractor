from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import os
import fnmatch
import datetime
from embedder import openai_embed
import tiktoken

tokenizer = tiktoken.get_encoding('p50k_base')


def tiktoken_len(text):
    return len(tokenizer.encode(text, disallowed_special=()))


def format_date(date_str):
    # Use strptime to convert the date string to a datetime object
    date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')

    # Use strftime to format the datetime object as an ISO8601 date string
    iso_date_str = date_obj.strftime('%Y-%m-%dT%H:%M:%S')

    return iso_date_str


def split_flight_record_contents(contents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=10,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ']
    )
    chunks = splitter.split_text(contents)
    return chunks


# extract hashtags into an array from the string
def extract_hashtags(text):
    # find the header and hashtags line
    match = re.search(r'^#{4}\s+.*\n+(#[^\s#]+(?:\s+#[^\s#]+)*)', text, flags=re.MULTILINE)
    if match:
        # extract hashtags from the line and return them as a list
        hashtags = match.group(1).split()
        return [hashtag[1:] for hashtag in hashtags]  # remove the '#' character from each hashtag
    else:
        return []  # no hashtags found


# extract the date from the string (string format: .*-date_dd-mm-yyyy)
def extract_date(string):
    match = re.match(r".*-date_(.*).md", string)
    if match:
        return format_date(match.group(1))
    return None


# read the flight rect body test (format: everything that follows after the line that starts #### )
def extract_flight_record_body(string):
    # find the header and return all text after it
    match = re.search(r'^#{4}\s+.*\n((?:.|\n)*)', string, flags=re.MULTILINE)
    if match:
        return match.group(1)
    else:
        return ''  # no header found


# call read_dataset_files() and iterate through each record
# extract the date, the hashtags, and the contents
# return an arrays of hashes of recrods
def extract_dataset_records(dataset_path):
    file_contents = read_dataset_files(dataset_path)

    records = []
    for filename, contents in file_contents.items():
        date = extract_date(filename)
        hashtags = extract_hashtags(contents)
        body_contents = extract_flight_record_body(contents)
        texts = split_flight_record_contents(body_contents)
        records.extend([{
                           "date": date,
                           "hashtags": hashtags,
                           "contents": f"Date: {date}\nHashtags: {hashtags}\nNote: {texts[i]}"
                       } for i in range(len(texts))])
    return records


# Read the contents of every file in the directory and return a list of records
def read_dataset_files(directory_path):
    dir_path = directory_path

    # Initialize a dictionary to store the file names and contents
    file_contents = {}

    # Iterate through each file in the directory
    for filename in os.listdir(dir_path):
        # Create the full file path by joining the directory path and the filename
        file_path = os.path.join(dir_path, filename)

        # Check if the current path is a file, not a directory, and matches the pattern (e.g., .md files)
        if os.path.isfile(file_path) and fnmatch.fnmatch(filename, "*.md"):
            # Read the contents of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()

            # Store the filename and contents in the dictionary
            file_contents[filename] = contents

    return file_contents


def create_flight_record_collection_item(data):
    hashtags = ','.join(data['hashtags'])
    embed_vector = openai_embed(data['contents'])
    record = {'flight_record_tags':  hashtags,
              'flight_record_date': data['date'],
              'flight_record_contents': data['contents'],
              'flight_record_contents_embed': embed_vector}
    print(f"creating record and embedding {data['date']}")
    return record
