# Trip Planner AI Agent

A conversational AI agent that helps you plan a complete trip — accommodations, activities, transport, and budget breakdown — through a simple back-and-forth terminal chat. Powered by [Groq](https://groq.com) LLMs via the OpenAI-compatible SDK.

---

## What it does

Rather than generating a one-shot itinerary, the agent guides you through your requirements one at a time — destination, number of travellers, trip duration, budget, and personal interests — before producing a detailed plan. If your budget is too low for what you're asking, the agent tells you plainly and suggests adjustments instead of hallucinating a plan that won't work.

---

## Features

- **Multi-turn conversation memory** — the full chat history is maintained in-session so the agent remembers everything you've told it
- **Dynamic model selection** — lists every model available on your Groq account and lets you pick at runtime
- **Budget validation** — the agent flags underfunded trips and offers concrete alternatives (reduce days, reduce party size)
- **Off-topic guardrail** — non-travel input is redirected back to trip planning
- **Sequential requirement gathering** — never assumes; asks for any missing information before planning
- **Groq via OpenAI SDK** — uses the OpenAI-compatible endpoint so swapping providers later requires changing one URL

---

## Requirements

- Python 3.9 or higher
- A [Groq API key](https://console.groq.com) (free tier available)

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Awaiskhan1187/Planning-a-trip-to-paris.git
cd Planning-a-trip-to-paris

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
echo "GROQ_API=your_groq_api_key_here" > .env
```

---

## Usage

```bash
python agent.py
```

1. The agent lists all available Groq models — enter the number of the one you want to use.
2. Start describing your trip. The agent will ask for anything that's missing.
3. Type `quit` or `exit` to end the session.

### Example session

```
Select through model number : 1

PROMPT : I want to plan a trip to Barcelona for 3 people, 7 days, $3000 budget.
RESPONSE :
Great! A 7-day trip to Barcelona for 3 people with a $3000 budget is very workable.
Before I build the full itinerary, do you have any specific interests — beaches,
architecture, food tours, nightlife, day trips?

PROMPT : Architecture and food, no nightlife.
RESPONSE :
Perfect. Here is your day-by-day itinerary ...
```

---

## Project structure

```
Planning-a-trip-to-paris/
├── agent.py            # Main agent — all logic lives here
├── .env                # Your Groq API key (never commit this)
├── .gitignore          # Excludes .env and __pycache__
├── requirements.txt    # Python dependencies with version pins
├── pyproject.toml      # Package metadata and tooling config
└── README.md           # This file
```

---

## How the conversation memory works

Every user and assistant message is stored in a Python list (`input_history`) and sent to the API on every call. This is the standard pattern for stateful LLM conversations — the model has no memory between API calls on its own; you provide the full context each time.

```python
input_history.append({"role": "user", "content": prompt})
response = client.chat.completions.create(model=model, messages=input_history)
input_history.append({"role": "assistant", "content": response.choices[0].message.content})
```

---

## Configuration

| Variable   | Description                        | Required |
|------------|------------------------------------|----------|
| `GROQ_API` | Your Groq API key from console.groq.com | Yes |

The `.env` file is loaded automatically at startup. Never commit it — add `.env` to your `.gitignore`.

---

## Known limitations

- Conversation history is in-memory only — it resets when the process exits.
- No structured output — itineraries are free-form text.
- The few-shot primer in `input_history` references Paris; this does not restrict the agent to Paris — it is only used to prime the model's response style.

---

## Roadmap

- [ ] Add `requirements.txt` and `pyproject.toml` ✅
- [ ] Export itinerary to a text or PDF file
- [ ] Add a `--model` CLI flag to skip the interactive selection step
- [ ] Persist conversation history to a JSON file between sessions
- [ ] Support multiple destinations in a single trip

---

## License

MIT — see [LICENSE](LICENSE) for details.
