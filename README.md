# ai-work-notes-knowlege-extractor
Usage of Langcahin and OpenAI to do multi stage knowledge extraction with Milvus vector database of flight records from work

# Usage

- Start Milvus in docker
 
```bash
docker compose up milvus/docker-compose.yml -d
```

- rename `.env.example` to `.env` and add your OPENAI Key

- populate the milvus database from a .md file that contains all your notes, each note must be in the following format, separated by at least 3 dashes, example:

```md

#### {date}

#tag1 #tag2

{notes}

-----

#### {date}

#tag3 #tag4

{notes}

```

- put the file in project root at and name it `fl.md`

- run `inject_data_into_milvus()` from `dataset_milvus_injector.py`

- Once milvus is populated run `main.py`
