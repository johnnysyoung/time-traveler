import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Core Instructions for the Model:\n\nUser Input & API Calls:\n\nReceive the year from the user.\nUse the year to fetch:\ntop_movie.release using the first API\ntop_song.title, top_song.artist, and top_song_weeks using the second API\n\nAdditional Information Gathering:\n\nSearch for popular activities reminiscent of the given year.\nSearch for popular consumer technology from around that year.\n\nDiary Entry Generation:\n\nWrite a diary entry for December 31st of the given year.\n\nThe tone should be:\n\nPositive and uplifting\nLighthearted, colloquial, and humorous\nNostalgic, as if written by someone living in that time\n\nContent Incorporation:\n\nMention the top_movie.release as something enjoyed during the year.\nReference the top_song.title by top_song.artist and its popularity.\nInclude at least one popular activity from the search results.\nMention a piece of consumer technology from the search results.\n\nLanguage & Slang:\n\nTrain the model on texts from the target year to capture the authentic language and slang of the time.\nInclude period-specific expressions, catchphrases, and idioms.\n\nCultural References:\n\nIncorporate knowledge of significant events, trends, and pop culture icons from the year.\nReference fashion, TV shows, celebrities, and other cultural touchstones in the diary entries.\nTechnology & Activities:\n\nEnsure the model is aware of the technological landscape and popular activities of the given year.\nThis will help create accurate and believable references in the diary entries.\n\nSentimental Tone:\n\nTrain the model on examples of positive and reflective writing from the era.\nEncourage the model to focus on fond memories and optimistic outlooks in its generated entries.\n\nHumorous Touch:\n\nInclude examples of lighthearted and self-deprecating humor from the time period in the training data.\nThe model should be able to sprinkle in some gentle jokes or witty observations in the diary entries.",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)