#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import LatestAiNews

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Silicon Valley',
        'current_year': str(datetime.now().year),
        "date": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    }
    
    try:
        LatestAiNews().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()