import requests
import json

class SummaryGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/chat/completions"


    def generate_summary(self, video_id, transcript):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-3.5-turbo-16k",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts into one paragraph."},
                {"role": "user", "content": transcript}
            ]
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                response_json = response.json()
                summary = response_json['choices'][0]['message']['content']
                return summary
            else:
                print(f"Failed to generate summary, status code: {response.status_code}")
                print(f"Response: {response.json()}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {video_id}: {e}")
            return None