# Summary Feeds (http://www.summaryfeeds.com)
Read AI-Focused Videos like a Daily News Feed


## About
This is an open-source project that uses the YouTube Transcript API and OpenAI's GPT3.5-turbo-16k to fetch and summarize video transcripts. The project is built with a tech stack that includes HTML, CSS, Jinja2, Python (Flask), PostgreSQL, and is deployed on AWS Elastic Beanstalk.

## Features
* Fetches transcripts of AI-focused YouTube videos, using the YouTube Transcript API by pypi.org ([link](https://pypi.org/project/youtube-transcript-api/)).
* Uses OpenAI's GPT-3.5-turbo-16k to summarize video transcripts.
* Presents summaries in an easily readable format.
* Organized interface to browse video summaries by date.

## Getting Started to Run Your Own Summary Feeds

### Prerequisites
* Python 3.8 or higher
* An OpenAI API key
* PostgreSQL
* An AWS account (for Elastic Beanstalk deployment)

### Installation Steps (work in progres...)
1. Clone the repository:
```
  git clone https://github.com/bingdai/summaryfeeds
  cd summaryfeeds
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Set up your PostgreSQL database and note your database credentials.
4. Get an OpenAI API key.
5. Get a Google Developer API key for the YouTube Data API
6. Create a .env file in the project root directory with your configurations:
```
  OPENAI_API_KEY='your_openai_api_key_here'
  YT_API_KEY='your_youtube_api_key_here'
  DB_NAME='your_database_name_here'
  DB_HOST='your_database_host_here'
  DB_USER ='your_database_user_here'
  DB_PASSWORD='your_database_password_here'
```
(to be continued...)

## License (MIT)

You are welcome to use, modify, and distribute the code, for both private and commercial use, provided that the license is included with the software ([LICENSE](https://github.com/bingdai/summaryfeeds/blob/main/LICENSE)).


## Acknowledgement
* YouTube Transcript API by pypi.org ([link](https://pypi.org/project/youtube-transcript-api/))
* Google Cloud's YouTube Data API ([link](https://developers.google.com/youtube/v3))
* OpenAI's GPT3.5-turbo-16k ([link](https://platform.openai.com/docs/models/gpt-3-5-turbo)
* Python Community's amazing backend stack (mainly [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [SQLAlchemy](https://www.sqlalchemy.org/))
* PostgreSQL Database ([link](https://www.postgresql.org/))


## Get in Touch with Bing
1. Email me at bingdai9 at gmail dot com
2. Grab coffee in Vancouver, Canada
