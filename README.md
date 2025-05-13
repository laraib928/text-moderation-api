#  Text Moderation API using FastAPI and Toxic-BERT

This project is a text moderation system built using **FastAPI** and a pre-trained model from Hugging Face: [`unitary/toxic-bert`](https://huggingface.co/unitary/toxic-bert). It detects toxic, harmful, or inappropriate content and classifies it as `approved`, `flagged`, or `rejected` based on confidence scores. All moderation actions are logged into an SQLite database.

---

## Features

- Real-time toxic text detection
- Uses powerful NLP model (`toxic-bert`)
- Logs user input, result, and metadata into SQLite
- Interactive API docs at `/docs` (Swagger UI)
- Built using FastAPI for speed and simplicity

---

## Technologies Used

- Python 3.x
- FastAPI
- SQLite (via `sqlite3`)
- Hugging Face Transformers
- Uvicorn (ASGI server)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text-moderation-api.git
cd text-moderation-api
2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt, install manually:

bash
Copy
Edit
pip install fastapi uvicorn transformers
4. Run the application
bash
Copy
Edit
uvicorn main:app --reload

Access API Docs
Once the server is running, go to:

🔗 http://127.0.0.1:8000/docs

This opens Swagger UI where you can interactively test the /moderate endpoint.

API Endpoints
POST /moderate
Request:

json
Copy
Edit
{
  "user_id": "user123",
  "text": "your text here"
}
Response:

json
Copy
Edit
{
  "decision": "approved | flagged | rejected",
  "confidence": 0.78,
  "reason": "Potential Toxicity"
}
GET /
Returns a welcome message and API usage guide.

View Logs in SQLite
To check if moderation data is being stored:

Run:

python check_db.py
Output will display all records from the moderation_logs table.

Notes
The moderation.db file is created automatically when the app starts.

Use the view_logs.py script to see stored moderation logs.

The AI model may take a few seconds to load the first time.

Author
Developed by Laraib