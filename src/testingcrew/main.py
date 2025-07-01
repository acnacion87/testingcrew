#!/usr/bin/env python
import os
import sys
import warnings

from crewai_tools import MCPServerAdapter
from testingcrew.crew import Testingcrew
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

server_params={
    "url": "http://localhost:8931/sse", 
    "transport": "sse"
}

def run():
    """
    Run the crew.
    """
    inputs = {
        'url': os.getenv('URL'),
    }
    
    mcp_adpater = MCPServerAdapter(server_params)
    try:
        with mcp_adpater as mcp_tools:
            Testingcrew(tools=mcp_tools).crew().kickoff(inputs=inputs)
    except Exception as e:
        mcp_adpater.stop()
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'url': 'http://uitestingplayground.com/ajax',
    }
    try:
        Testingcrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Testingcrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
       'url': 'http://uitestingplayground.com/ajax',
    }
    
    try:
        Testingcrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
