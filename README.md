# Simple-Agentic-Finance-Analyst

This repository implements an intelligent financial analysis system using the Phidata framework and OpenAI's advanced language models. The solution demonstrates how to build specialized AI agents that can analyze stocks, retrieve real-time market data, and generate comprehensive investment insights.

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

2. To access the Phidata's chat playground, set up an account with Phidata, get the api key and export the api key to your windows environment.

```commandline
    setx PHI_API_KEY phi-***
```

3. To test the agents in the chat playground of  Phidata's, run the following command, a locally hosted URL is generated, test the agents in the chat playground.

```commandline
    python playground.py
```

**Chat Playground Display**

![img.png](imgs/playground.png)
