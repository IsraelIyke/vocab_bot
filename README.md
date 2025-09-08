# 📚 Vocab Bot

<p align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmFqOWF3OHJuZ3hiZ3FrY2N0bXI1ZmY4YTBwZDYyamk3dXMyanViaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/M7XQJbvAQEGicYnHrv/giphy.gif" alt="Vocab Bot Demo" width="400" height="180"/>
</p>


<p align="center">
  <b>A simple telegram bot for learning Italian verbs with English translations 🇮🇹➡️🇬🇧</b>
</p>

---

## ✨ Features
- 📖 Provides Italian verbs with their English meanings
- ⚡ Lightweight Node.js API (ideal for serverless platforms like Vercel)
- ☁️ Database integration ready for persistence/expansion

---

```
## 📂 Project Structure
vocab_bot-main/
├── api/
│ └── webhook.js # API endpoint serving vocab
├── package.json # Dependencies (@supabase/supabase-js)
├── package-lock.json
└── .gitignore
```
---

## ⚙️ Installation
# Clone the repo
```
git clone https://github.com/IsraelIyke/vocab_bot.git
cd vocab_bot
```

# Install dependencies
npm install

---

## 🚀 Usage
Run locally with Node.js:
```node api/webhook.js```

Or deploy to Vercel:
- Push repo to GitHub
- Import into Vercel
- API will be available at: https://your-app.vercel.app/api/webhook

---

## 🤝 Contributing

Pull requests are welcome!
