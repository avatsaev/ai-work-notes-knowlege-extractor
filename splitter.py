import re
import os
from dateutil.parser import parse


def read_markdown_file(file_path):
    with open(file_path, 'r') as md_file:
        contents = md_file.read()
    return contents

def split_contents(contents):
    chunks = re.split(r'-{3,}', contents)
    return chunks

def extract_and_format_date(chunk):

    match = re.match(r".*####\s*(.*)", chunk, re.MULTILINE | re.DOTALL)
    if match:
        date_string = match.group(1)[:11].strip()
        try:
            date = parse(date_string)

            print(date)
            return date.strftime('%d-%m-%Y')
        except ValueError:
            pass
    return None

def save_chunks(chunks, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)



    for index, chunk in enumerate(chunks):

        formatted_date = extract_and_format_date(chunk)
        if formatted_date:
            file_name = f"index_{index}-date_{formatted_date}.md"

            file_path = os.path.join(output_directory, file_name)
            with open(file_path, 'w') as chunk_file:
                chunk_file.write(chunk.strip())

def extract_flight_records(path):
    input_file_path = path
    output_directory = "./datasets/flight-records"
    contents = read_markdown_file(input_file_path)
    chunks = split_contents(contents)
    save_chunks(chunks, output_directory)
    print(f"Chunks saved in {output_directory}")


# extract_flight_records("fl.md")


