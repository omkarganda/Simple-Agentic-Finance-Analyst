from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from phi.playground import Playground, serve_playground_app

load_dotenv()

BASE_FORMATTING = [
    "Use clear Markdown formatting",
    "Headings: # Main, ## Section, ### Subsection",
    "Lists: Use bullet points for multiple items",
    "Tables: | Column 1 | Column 2 |",
    "Links: [Display Text](URL)",
    "Code: ```python code blocks ```",
    "Separate major sections with ---"
]

web_agent = Agent(
    name="Web Agent",
    model = OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGo()],
    instructions=[
        *BASE_FORMATTING,
        "Present sources as:",
        "• [Source Name](URL) - Brief summary",
        "Use > for quoted content",
        "Group related findings under ### subheadings"
    ],
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role = "Get financial data of listed companies.",
    model = OpenAIChat(id = "gpt-4o-mini"),
    tools=[YFinanceTools(stock_price = True, analyst_recommendations = True, company_info = True, historical_prices = True)],
    instructions=[
        *BASE_FORMATTING,
        "Display the data in tabular format."
    ],
    markdown=True
)

agent_team = Agent(
    name="Agent Team",
    team=[web_agent, finance_agent],
    model = OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        *BASE_FORMATTING,
        "Report structure:",
        "# Summary (2-3 sentences)",
        "## Financial Data (tables)",
        "## Market Insights (bullets)",
        "## Sources ([links](URL))",
        "Keep lines under 80 characters",
        "Bold **key takeaways**"
    ],
    markdown=True
)

app = Playground(agents=[finance_agent, web_agent, agent_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)