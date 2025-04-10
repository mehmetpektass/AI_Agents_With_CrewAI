#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, start, listen
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks
import assemblyai as aai
from crews.meeting_assistant.meeting_assistant import MeetingAssistantCrew

load_dotenv()

client = OpenAI()

aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
transcriber = aai.Transcriber()


class MeetingAssistantState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class MeetingAssistantFlow(Flow[MeetingAssistantState]):

    @start()
    def transcribe_meeting (self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        audio_file = Path(SCRIPT_DIR) / "Indian_podcast.wav"
        filename_without_ext = audio_file.stem

        audio = AudioSegment.from_file(audio_file, format="wav")

        chunk_length = 60000
        chunks = make_chunks(audio, chunk_length)

        full_transcription = ""
        for i,chunk in enumerate(chunks):
            print(f"Transcribing chunk {i +1}/{len(chunks)}")
            chunk_path = f"{filename_without_ext}_chunk_{i +1}.wav"
            chunk.export(chunk_path, format="wav")

            
            with open(chunk_path, "rb") as audio:
                transcription = transcriber.transcribe(audio)

                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")

    
    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating Meeting Minutes")

        crew = MeetingAssistantCrew()

        inputs = {
            "transcript": self.state.transcript
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = meeting_minutes


    
def kickoff():
    poem_flow = MeetingAssistantFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
