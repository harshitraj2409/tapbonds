# Tap Bonds AI Assistant

An AI-powered assistant for bond discovery and research, built for the Tap Bonds Hackathon.

![Tap Bonds AI Assistant](https://img.shields.io/badge/Tap%20Bonds-AI%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)

## Overview

Tap Bonds AI Assistant is an intelligent chatbot that helps users with bond discovery, financial analysis, and yield calculations. The system uses a multi-agent architecture to route queries to specialized agents based on the context of the prompt.

## Features

- **Bond Directory Agent**: Provides information on various bonds, including ISIN-level details, credit ratings, maturity dates, and security types.
- **Bond Finder Agent**: Helps users compare bonds across multiple platforms and find the best available yields.
- **Cash Flow & Maturity Agent**: Handles queries related to bond cash flows, maturity schedules, and payment timelines.
- **Bond Screener Agent**: Performs company-level financial analysis of bond-issuing firms.
- **Yield Calculator Agent**: Calculates bond yields, prices, and considerations.

## Architecture

The system consists of:

1. **Orchestrator Agent**: Routes user queries to the appropriate specialized agent based on the context of the prompt.
2. **Specialized Agents**: Each feature has a dedicated agent responsible for handling queries related to its functionality.
3. **Web Interface**: A simple web interface with a search bar where users can enter prompts and receive responses.

## Demo

You can watch the live demo at: [Video Tutorial](https://www.youtube.com/watch?v=s28IJWocJGk&t=275s)


## Setup

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/harshitraj2409/tapbonds.git
   cd tapbonds
   ```

2. Create and activate a virtual environment (optional):
   ```
   python -m venv tapbonds_env
   source tapbonds_env/bin/activate  # On Windows: tapbonds_env\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Add your OpenAI API key and other configuration:
     ```
     OPENAI_API_KEY=your_api_key_here
     MODEL_NAME=gpt-4o-mini
     ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Deployment

### Deploying to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: tapbonds-ai-assistant
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Add Environment Variables**: Add all variables from your `.env` file

### Deploying to Heroku

1. Install the Heroku CLI and log in
2. Create a new Heroku app:
   ```
   heroku create tapbonds-ai-assistant
   ```
3. Add environment variables:
   ```
   heroku config:set OPENAI_API_KEY=your_api_key_here
   heroku config:set MODEL_NAME=gpt-4o-mini
   ```
4. Deploy the app:
   ```
   git push heroku main
   ```

## Usage

1. Enter your query in the search bar.
2. The system will automatically route your query to the appropriate agent.
3. View the response in the chat interface.

## Example Queries

- "Show me details for ISIN INE08XP07258"
- "What is the rating of Tata Capital?"
- "Calculate the yield for a bond with price 98.5, ISIN INE08XP07258, investment date 2023-01-01, and 10 units"
- "Show me the cash flow schedule for ISIN INE08XP07258"
- "Compare the debt/equity ratio of Tata Capital and Reliance"
- "What will be the consideration for ISIN INE08XP07258 for 20 units at 2025-03-03?"

## Data Sources

The system uses the following data files:
- `bonds_details_202503011115.csv`: Contains bond details
- `cashflows_202503011113.csv`: Contains cash flow information
- `company_insights_202503011114.csv`: Contains company financial data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Tap Bonds for providing the hackathon opportunity and data
- OpenAI for the GPT models used in the agents 
