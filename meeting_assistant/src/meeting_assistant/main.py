#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, start
from crews.poem_crew.poem_crew import PoemCrew
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks

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

        chunk_length = 60000
        chunks = make_chunks(audio, chunk_length)

        full_transcription = ""
        for i,chunk in enumerate(chunks):
            print(f"Transcribing chunk {i +1}/{len(chunks)}")
            chunk_path = f"chunk_{i +1}.wav"
            chunk.export(chunk_path, format="wav")

            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")
    
def kickoff():
    poem_flow = MeetingAssistantFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
