from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.thinking import ThinkingTools
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY_temp_1")  # or use os.getenv("GROQ_API_KEY") if from .env

class SelfCritiquingWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.initial_draft_agent = Agent(
            model=Groq(id="deepseek-r1-distill-llama-70b", api_key=self.api_key),
            tools=[ThinkingTools(add_instructions=True)],
            instructions="You are a blog post writer. Your task is to write a short, engaging introduction for a blog post on a given topic. The introduction should be concise and capture the reader's attention.",
            show_tool_calls=False,
            markdown=True,
        )

        self.critique_agent = Agent(
            model=Groq(id="deepseek-r1-distill-llama-70b", api_key=self.api_key),
            tools=[ThinkingTools(add_instructions=True)],
            instructions=dedent("""
                You are a critical editor. Your task is to review a blog post introduction and provide constructive feedback on its clarity, tone, and conciseness.
                Focus on identifying areas for improvement to make the introduction more engaging and easier to understand for a general audience.
                Your feedback should be actionable and specific. Do not rewrite the introduction, just provide critique.
            """),
            show_tool_calls=False,
            markdown=True,
        )

        self.revision_agent = Agent(
            model=Groq(id="deepseek-r1-distill-llama-70b", api_key=self.api_key),
            tools=[ThinkingTools(add_instructions=True)],
            instructions=dedent("""
                You are a meticulous reviser. Your task is to take an initial blog post introduction and a critique, and then rewrite the introduction based on the feedback.
                The revised introduction should be clear, engaging, concise, and easy to read for a general audience.
                Ensure the final output is no more than 200 words. Do not include any critique or additional commentary in your final output, only the revised introduction.
            """),
            show_tool_calls=False,
            markdown=True,
        )

    def write_and_critique(self, topic: str) -> str:
        print(f"\n--- Generating initial draft for: {topic} ---")
        initial_draft_generator = self.initial_draft_agent.run(
            f"Write a blog post introduction about {topic}.", stream=True
        )
        initial_draft = "".join([chunk.content for chunk in initial_draft_generator if chunk and chunk.content])
        print(f"Initial Draft:\n{initial_draft}")

        print("\n--- Critiquing initial draft ---")
        critique_generator = self.critique_agent.run(
            f"Critique the following blog post introduction:\n\n{initial_draft}", stream=True
        )
        critique = "".join([chunk.content for chunk in critique_generator if chunk and chunk.content])
        print(f"Critique:\n{critique}")

        print("\n--- Revising draft based on critique ---")
        final_version_generator = self.revision_agent.run(
            f"Revise the following blog post introduction based on the critique. Ensure it is under 200 words and easy to read:\n\nInitial Draft:\n{initial_draft}\n\nCritique:\n{critique}",
            stream=True
        )
        final_version = "".join([chunk.content for chunk in final_version_generator if chunk and chunk.content])
        print(f"Final Version:\n{final_version}")

        return final_version

if __name__ == "__main__":
    writer = SelfCritiquingWriter(api_key=GROQ_API_KEY)
    final_post = writer.write_and_critique("the benefits of remote work")
    print(f"\n--- Final Polished Blog Post Introduction ---")
    print(final_post)