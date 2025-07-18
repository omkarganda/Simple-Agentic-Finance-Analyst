from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import asyncio
import os

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

# Custom FastAPI Web Interface
app = FastAPI(title="Finance Analyst AI", description="Agentic Finance Analysis System")

class QueryRequest(BaseModel):
    message: str
    agent_type: str = "team"  # Options: "finance", "web", "team"

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    """Serve the main web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Finance Analyst AI</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #4A90E2;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #555;
            }
            select, textarea, button {
                width: 100%;
                padding: 12px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            select:focus, textarea:focus {
                outline: none;
                border-color: #4A90E2;
            }
            textarea {
                min-height: 120px;
                resize: vertical;
            }
            button {
                background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
                color: white;
                border: none;
                cursor: pointer;
                font-weight: 600;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            .response {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #4A90E2;
                min-height: 100px;
                white-space: pre-wrap;
            }
            .loading {
                text-align: center;
                color: #4A90E2;
                font-style: italic;
            }
            .agent-info {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .agent-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #4A90E2;
            }
            .agent-card h3 {
                margin-top: 0;
                color: #4A90E2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Finance Analyst AI</h1>
            <p class="subtitle">Intelligent Financial Analysis with AI Agents</p>
            
            <div class="agent-info">
                <div class="agent-card">
                    <h3>💹 Finance Agent</h3>
                    <p>Real-time market data, stock prices, analyst recommendations, and company fundamentals via Yahoo Finance.</p>
                </div>
                <div class="agent-card">
                    <h3>🔍 Web Agent</h3>
                    <p>Market news, trends, and insights from web research using DuckDuckGo search.</p>
                </div>
                <div class="agent-card">
                    <h3>👥 Agent Team</h3>
                    <p>Combined analysis leveraging both financial data and web research for comprehensive insights.</p>
                </div>
            </div>

            <form id="queryForm">
                <div class="form-group">
                    <label for="agent">Select Agent:</label>
                    <select id="agent" name="agent">
                        <option value="team">Agent Team (Recommended)</option>
                        <option value="finance">Finance Agent</option>
                        <option value="web">Web Agent</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="query">Your Financial Query:</label>
                    <textarea id="query" name="query" placeholder="e.g., Analyze AAPL stock performance and provide investment recommendations" required></textarea>
                </div>
                
                <button type="submit" id="submitBtn">Analyze</button>
            </form>
            
            <div id="response" class="response" style="display: none;"></div>
        </div>

        <script>
            document.getElementById('queryForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const responseDiv = document.getElementById('response');
                const query = document.getElementById('query').value;
                const agent = document.getElementById('agent').value;
                
                if (!query.trim()) return;
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Analyzing...';
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = '<div class="loading">🤖 AI agents are analyzing your request...</div>';
                
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: query,
                            agent_type: agent
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        responseDiv.innerHTML = data.response;
                    } else {
                        responseDiv.innerHTML = `<div style="color: red;">Error: ${data.detail || 'Unknown error occurred'}</div>`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `<div style="color: red;">Network error: ${error.message}</div>`;
                }
                
                submitBtn.disabled = false;
                submitBtn.textContent = 'Analyze';
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process user query with selected agent"""
    try:
        # Select the appropriate agent
        if request.agent_type == "finance":
            agent = finance_agent
        elif request.agent_type == "web":
            agent = web_agent
        else:  # default to team
            agent = agent_team
        
        # Run the agent asynchronously
        response = agent.run(request.message)
        
        return {"response": response.content}
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Finance Analyst AI"}

if __name__ == "__main__":
    print("🚀 Starting Finance Analyst AI Web Interface...")
    print("📊 Available at: http://localhost:8000")
    uvicorn.run("playground:app", host="0.0.0.0", port=8000, reload=True)