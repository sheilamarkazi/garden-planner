from .crew import create_crew

def run_crew(plants_text: str, beds_text: str):
    """
    TEMP: ignore raw text for now—just run the Crew with default prompts.
    Later we’ll parse plants_text & beds_text and feed them in.
    """
    crew = create_crew()
    result = crew.kickoff()
    # TODO: extract real report & diagram paths from `result`
    return "output/report.md", "output/garden_plan.png"
