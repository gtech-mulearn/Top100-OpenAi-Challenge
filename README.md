# AutoExcel

AutoExcel is a project that takes unstructured message data and converts it into structured messages in JSON format. It utilizes the Google Sheets API to store the structured messages in an Excel file.

The project consists of three repositories:

## Frontend
The frontend is built with React and Vite. It provides a user-friendly interface to interact with the application.
[Frontend Repository Link](https://github.com/riptide-rv/Top100-OpenAi-Challenge)

## API
The API is built with FastAPI. It handles the conversion of unstructured data to JSON and interacts with the Google Sheets API to store the data.
[API Repository Link](https://github.com/riptide-rv/AutoExcel-API)

## Discord
This part of the project handles Discord integration. It fetches the unstructured message data from Discord.
[Discord Repository Link](https://github.com/riptide-rv/AutoExcel-DiscordBot)

## Installation

### Frontend

1. Clone the frontend repository: `git clone https://github.com/riptide-rv/Top100-OpenAi-Challenge.git`
2. checkout to branch test
3. Navigate into the cloned repository: `cd Top100-OpenAi-Challenge/AutoExcel`
4. Install the dependencies: `npm install`
5. Start the development server: `npm run dev`

### API

1. Clone the API repository: `git clone https://github.com/riptide-rv/AutoExcel-API.git`
2. Navigate into the cloned repository: `cd AutoExcel-API`
3. Create a Python virtual environment: `python3 -m venv env`
4. Activate the virtual environment: `source env/bin/activate` (on Windows, use `env\Scripts\activate`)
5. Install the dependencies: `pip install fastapi uvicorn python-dotenv openai gspread`
6. Create a .env file and store OPENAI_API_KEY=your key in root folder
6. Start the development server: `uvicorn main:app --reload`

### Discord Bot

1. Clone the Discord bot repository: `git clone https://github.com/riptide-rv/AutoExcel-DiscordBot.git`
2. Navigate into the cloned repository: `cd AutoExcel-DiscordBot`
3. Create a Python virtual environment: `python3 -m venv env`
4. Activate the virtual environment: `source env/bin/activate` (on Windows, use `env\Scripts\activate`)
5. Install the dependencies: `pip install discord.py`
6. Start the bot: `python main.py`
   
   > for discord work properly , create a new bot with all message related permission by visiting discord developer portal and update the code to use the token of created bot.

 
