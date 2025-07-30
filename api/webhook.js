// Italian Verbs Telegram Bot - Vercel webhook style

// Store verbs in memory
const verbs = [
  { id: 1, italian: "andare", english: "to go" },
  { id: 2, italian: "avere", english: "to have" },
  { id: 500, italian: "promettere", english: "to promise" },
];

// Store user progress in memory
const userProgress = new Map();

// Main webhook handler
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(200).send("Bot running");
  }

  const { message } = req.body;
  const chatId = message?.chat?.id;
  const text = message?.text?.trim();

  if (!chatId || !text) return res.status(200).end();

  // START command
  if (text === "/start" || text === "/restart") {
    userProgress.set(chatId, 0);
    await askQuestion(chatId);
    return res.status(200).end();
  }

  // ANSWER handling
  let currentIndex = userProgress.get(chatId) ?? 0;

  if (currentIndex < verbs.length) {
    const verb = verbs[currentIndex];
    const correctAnswer = verb.english.toLowerCase();
    const userAnswer = text.toLowerCase();

    if (userAnswer === correctAnswer) {
      await sendMessage(
        chatId,
        `✅ Correct! **${verb.italian}** means **${verb.english}**.`
      );
    } else {
      await sendMessage(
        chatId,
        `❌ Not quite. **${verb.italian}** means **${verb.english}**.`
      );
    }

    // Move to next question
    userProgress.set(chatId, currentIndex + 1);
    await askQuestion(chatId);
  } else {
    await sendMessage(
      chatId,
      "🎉 Congratulations! You've completed all 500 verbs!"
    );
    userProgress.set(chatId, 0);
  }

  res.status(200).end();
}

// Ask next question
async function askQuestion(chatId) {
  const index = userProgress.get(chatId) ?? 0;
  if (index < verbs.length) {
    const verb = verbs[index];
    await sendMessage(
      chatId,
      `(${verb.id}/${verbs.length}) What does **${verb.italian}** mean?`
    );
  }
}

// Send message to Telegram
async function sendMessage(chatId, text) {
  await fetch(
    `https://api.telegram.org/bot${process.env.BOT_TOKEN}/sendMessage`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: "Markdown",
      }),
    }
  );
}
