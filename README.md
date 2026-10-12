# 🤖 LLM-Based Assistant (Chatbot)

Ek simple lekin powerful **AI Assistant** jo Google Gemini (LLM) ki madad se sawalon ke jawab deta hai, conversation yaad rakhta hai, **chats save karta hai**, aur Streamlit ke zariye black-gradient web interface par chalta hai.

> NLP (Natural Language Processing) ka ek beginner-friendly project: text samajhna aur text generate karna.

---

## ✨ Features

- 💬 Multi-turn conversation (history yaad rakhta hai)
- 💾 **Chat history storage**: har chat `chats/` folder mein JSON file ke taur par save hoti hai, app restart ke baad bhi wapas khul sakti hai
- 🗂 Sidebar mein saved chats ki list, **New chat** aur delete button
- 🚀 Grok-style **starter suggestions** (naye chat par ek click se sawal shuru)
- 🖤 Black gradient dark theme
- 🧠 Custom **system prompt** (assistant ki personality)
- ⚡ Streaming response (jawab word-by-word)
- 🔄 Automatic retry jab Gemini busy ho (503)
- 🔐 API key `.env` file mein safe

---

## 🛠 Tech Stack

| Cheez | Use |
|---|---|
| Python 3.9+ | Main language |
| `google-genai` | LLM API (Gemini) |
| `streamlit` | Web interface |
| `python-dotenv` | API key safe rakhna |

---

## 📁 Project Structure

```
llm-assistant/
├── app.py                # Streamlit web version (UI, starters, sidebar chats)
├── chatbot_cli.py        # Terminal version
├── assistant.py          # Gemini config, client, streaming + retry
├── chat_store.py         # Chats ko JSON files mein save/load/delete
├── requirements.txt      # Libraries ki list
├── .env.example          # API key setup template
├── .env                  # Local API key (GitHub par upload NAHI karna)
├── .gitignore            # .env aur chats/ ko ignore karta hai
├── chats/                # Saved chats (auto-create hota hai)
└── README.md
```

---

## 🚀 Setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

1. [aistudio.google.com/apikey](https://aistudio.google.com/apikey) se Gemini API key banao
2. `.env.example` ko copy karke `.env` banao aur key daalo:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-flash-latest
```
> ⚠️ Asli key kabhi `.env.example` ya GitHub par mat daalo. `.env.example` mein sirf placeholder rakho.

---

## ▶️ Run Kaise Karein

**Web version:**
```bash
streamlit run app.py
```
Browser khud khul jayega (`http://localhost:8501`).

**Terminal version:**
```bash
python chatbot_cli.py
```

---

## 💾 Chats Kaise Save Hoti Hain

- Har jawab ke baad chat `chats/<id>.json` mein save hoti hai
- Title pehle sawal se ban jata hai
- Sidebar se purani chat par click karo to wapas load ho jati hai
- 🗑 button se chat delete hoti hai
- Terminal aur web dono ki chats same folder mein save hoti hain
- `chats/` `.gitignore` mein hai, is liye aapki private baatein GitHub par nahi jayengi

---

## 🧩 Kaise Kaam Karta Hai

```
User ka sawal
     │
     ▼
messages list mein add hota hai (history)
     │
     ▼
System prompt + poori history  ──►  Gemini API
     │
     ▼
Jawab stream hota hai (word by word)
     │
     ▼
Jawab history mein add hota hai + chats/ mein save
```

---

## 🔧 Troubleshooting

| Problem | Hal |
|---|---|
| `GEMINI_API_KEY is not set` | `.env` file banao aur key daalo |
| `ModuleNotFoundError` | `pip install -r requirements.txt` dobara chalao |
| 503 / high demand | Thodi der baad try karo, app khud retry karta hai |
| Model error | `.env` mein `GEMINI_MODEL` check karo |
| `streamlit` command nahi chal rahi | `python -m streamlit run app.py` |
| Jawab beech mein kat jata hai | `assistant.py` mein `MAX_TOKENS` barhao |

---

## 🔮 Future Improvements

- 📄 RAG: apne PDFs/notes par sawal
- 🎤 Voice input/output
- ☁️ Streamlit Community Cloud par deploy
- 🔧 Tool use (calculator, web search)

---

## 📤 GitHub par Upload

```bash
git init
git add .
git commit -m "Add LLM-based assistant project"
git branch -M main
git remote add origin https://github.com/<your-username>/llm-assistant.git
git push -u origin main
```

**Topics:** `nlp`, `llm`, `chatbot`, `python`, `streamlit`, `gemini`, `generative-ai`

> ✅ Upload se pehle check karo ki `.env` `.gitignore` mein hai aur `.env.example` mein asli key nahi hai.

---

## 📝 License

MIT License

⭐ Agar project pasand aaye to repo ko star zaroor karein!
