# Simple-Agentic-Finance-Analyst

This repository implements an intelligent financial analysis system using the Phidata framework and OpenAI's advanced language models with a custom FastAPI web interface. The solution demonstrates how to build specialized AI agents that can analyze stocks, retrieve real-time market data, and generate comprehensive investment insights through a modern, responsive web application.

## Key Features

### Specialized Agents

**Web Research Agent**
- Performs web searches using DuckDuckGo to gather relevant market news and references
- Provides source-attributed information with proper citations

**Financial Data Agent**
- Accesses real-time market data through Yahoo Finance (YFinance) integration
- Retrieves stock prices, historical trends, and fundamental company data

### Collaborative Team

**Agent Team**
- Combines capabilities of both Web and Finance agents
- Generates comprehensive reports combining quantitative data with qualitative insights
- Provides investment recommendations based on both technical and fundamental analysis

## System Architecture

![img.png](imgs/architecture_flow.png)

## Getting Started

### Prerequisites

- Python 3.8+
- Phidata API key
- OpenAI API key

### Installation

1. Install required dependencies:

```commandline
pip install -r requirements.txt
```

2. Set up your environment variables by creating a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
PHI_API_KEY=your_phidata_api_key_here  # Optional, for Phidata features
```

3. Launch the custom web interface:

```commandline
    python playground.py
```

The application will start on `http://localhost:8000` with a modern web interface featuring:
- **Agent Selection**: Choose between Finance Agent, Web Agent, or Agent Team
- **Interactive UI**: Clean, responsive design with real-time analysis
- **API Endpoints**: RESTful API for programmatic access

**Custom Web Interface Features**

- 🎨 Modern gradient design with responsive layout
- 📊 Agent-specific information cards  
- 🔄 Real-time query processing with loading indicators
- 📱 Mobile-friendly responsive design
- 🛡️ Error handling and validation
