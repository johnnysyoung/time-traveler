# Imports

# Import modules
import os
import datetime

# Import packages
from dotenv import load_dotenv
import billboard
from boxoffice_api import BoxOffice
import google.generativeai as genai

load_dotenv() # Load environment variables from .env

year = int(input("Enter a year: ")) # Get the year from the user

# One of Billboard's Top Song of the Year

start_date = datetime.date(year, 12, 31) # Start from the last day of the year due weeks attribute limitation

# Initialize variables to track the top song and its duration
top_song = None
top_song_weeks = 0

# Loop through each week of the year
while start_date.year == year:
    chart = billboard.ChartData('hot-100', date=start_date.strftime('%Y-%m-%d'))

    # Get the top song of the week and its duration on the Hot 100 chart
    current_song = chart[0]
    current_song_weeks = current_song.weeks

    # Update the top song if new song has been on the chart for longer
    if current_song_weeks > top_song_weeks:
        top_song = current_song
        top_song_weeks = current_song_weeks

    # Move to the previous week based on the current song's duration on the charts
    start_date -= datetime.timedelta(weeks=current_song_weeks)


# Top Box Office Movie

box_office = BoxOffice()
yearly_data = box_office.get_yearly(year) # Retrieves the box office figures for that year
top_movie = yearly_data[0] # Stores the top movie of that year


# Gemini Diary Entry

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
  system_instruction="The model will receive a chat message containing the year, top song, artist, weeks on the charts, and top movie. Using this information, the model will generate a diary entry dated December 31st of the given year. The entry should be written in a positive, lighthearted, and nostalgic tone, reflecting the language and cultural references of that time. It should include mentions of the top movie and song, one popular activity reminiscent of that era, and one iconic consumer technology product from that time - these latter two will be chosen by the model itself. The writing style should be authentic to the period, incorporating slang, catchphrases, and humor. The diary entry should evoke a sense of fond memories and optimism, capturing the essence of the year while remaining relatable to a modern audience. The diary entry should be under 300 words in length. Avoid any mention of anything, like clothing or activites, that is stereotypically male or female. Do not include a placeholder for name signage at the end of the diary entry.",

)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message(f"Year = {year}; Top Song of {year} = {top_song.title}; Artist of Top Song = {top_song.artist}; Top Song Weeks on Billboards Hot-100 Chart = {top_song_weeks}; Top Movie of {year}: {top_movie}")

print(response.text)