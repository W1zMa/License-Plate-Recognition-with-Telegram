# License Plate Recognition Bot

This Telegram bot is designed to **detect license plate numbers from images** and **store them in a SQLite database**.  
It uses the [Ultralytics](https://github.com/ultralytics/ultralytics) library for detection, and [Aiogram](https://aiogram.dev/) library for interact with telegram. 
The pre-trained license plate recognition model is taken from [RamatovInomjon/license_plate_recognition](https://github.com/RamatovInomjon/license_plate_recognition).

---


## Project Structure
```markdown
licens_recogn/
│
├── data/
│ ├── db.sqlite3 # SQLite database
│ └── photos/ # Folder to save uploaded photos
│
├── keyboard/
│ ├── inlinekey.py # Inline buttons
│ └── replykey.py # Reply buttons
│
├── recognition/
│ ├── detector.py # Script to detect license plates (adapted)
│ └── weights/ # Pre-trained models
│  ├── detection.pt
│  └── recognition.pt
│
├── services/
│ └── db.py # Handles database operations
│
├── .env # Bot token and user_id
├── .gitignore
├── handlers.py # Main bot handlers
├── main.py # Bot initialization
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
└── states.py # State management
```

---

## Requirements

- Python **3.8 – 3.10** (tested on **3.10.5**) 
> Note: Ultralytics may not be compatible with newer versions.

---

## Setup Instructions(With Docker 🐳)
- Using Docker allows you to run the project without installing Python or dependencies locally.
## Requirements

- [Docker](https://www.docker.com/)
- Docker Compose

1. **Prepare environment variables**
- Edit .env and set:
   ```bash
   BOT_TOKEN=<YOUR_BOT_TOKEN>
   ADMIN_ID=<YOUR_TELEGRAM_USER_ID>

2. **Build and run the container**
   ```bash
   docker compose up --build
> ⚠️ The first build may take several minutes due to ML dependencies (PyTorch, Ultralytics).

3. **Subsequent runs**
   ```bash
   docker compose up

4. **How to stop?**
   ```bash
   docker compose down

- or CTRL + C in terminal

## Setup Instructions(Without Docker 🐳)

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Configure .env file:**
   ```bash
   BOT_TOKEN=<YOUR_BOT_TOKEN>
   ADMIN_ID=<YOUR_USER_ID>

4. **Run the bot:**
   ```bash
   python main.py

How It Works

1. The bot receives an image or video from a user.

2. The recognition/detector.py script uses Ultralytics models to detect license plate numbers.

3. Detected numbers are saved in data/db.sqlite3.

4. Users interact with the bot via inline and reply buttons defined in keyboard/.
