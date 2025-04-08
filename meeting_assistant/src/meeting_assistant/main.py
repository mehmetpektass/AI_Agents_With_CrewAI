#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from meeting_assistant.crews.poem_crew.poem_crew import PoemCrew
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment

load_dotenv()

client = OpenAI()


class MeetingAssistantState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class MeetingAssistantFlow(Flow[MeetingAssistantState]):

    @start()
    def transcribe_meeting (self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        audio_path = str(SCRIPT_DIR/"EarningsCall.wav")

        audio = AudioSegment.from_file(audio_path, format="wav")
        audio_file= open("/path/to/file/audio.mp3", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        print(transcription.text)

    
def kickoff():
    poem_flow = MeetingAssistantFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
