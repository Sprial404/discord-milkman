# Discord Milkman Bot

A personal Discord bot I made for my Discord server with my mates! This Python bot functionalities are subject to change without notice, but I have listed some of its functionality below.

## Features
- **Temporary Channels:** Easily create and manage temporary voice or text channels.
- **Moderation Tools:** Kick, ban, mute, and other moderation commands to help manage your server.
- **Fun Commands:** A collection of entertaining commands for you and your friends.

## Getting Started

### Prerequisites
- Python 3.8+
- Discord Bot Token ([How to get one](https://discord.com/developers/applications))
- Docker & docker-compose (optional, for containerized deployment)

### Local Setup
1. Clone the repository:
   ```bash
   git clone <this-repo-url>
   cd discord-milkman
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token:
   ```env
   DISCORD_TOKEN=your-bot-token-here
   BOT_PREFIX=!
   ```
4. Run the bot:
   ```bash
   python -m milkman.bot
   ```

### Docker Setup
1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Or build and run manually:
   ```bash
   docker build -t discord-milkman .
   docker run --env-file .env discord-milkman
   ```

## Usage
Invite the bot to your server and use the available commands. Type `!help` or `/help` in Discord to see the full list of commands.

## Contributing
This is a personal project, but feel free to fork and modify for your own use!

## License
MIT License
