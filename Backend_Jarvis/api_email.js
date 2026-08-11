const express = require("express");
const multer = require("multer");
const temp_memory = multer.memoryStorage();
const app = express();
const port = 8000;

/** NOTE: to start this application, follow these steps:
 * create Brevo account and register
 * create API-Key
 * copy paste it in .env file into API_KEYS
 * put it your Email used in signing in, and Email you want to receive images
 * */

// speichert Bild in RAM, nicht in storage
const upload = new multer({
  storage: temp_memory,
});

/** Hört auf POST /api/pic
 * upload.single("image") -> image ist name aus dem multipart-Block mit der "Bild"-Datei (in Bytecode)
 * durch req.file.buffer aufrufbar
 * speichert "image" in RAM -> wird in base64String konvertiert -> damit als JSON-Datei sendbar wird
 * String wird als Mail an Brevo Server gesandt -> leitet an gewünschte Email weiter
 * */
app.post("/api/pic", upload.single("image"), (req, res) => {
  console.log("API POST pic angekommen");
  const base64String = req.file.buffer.toString("base64");
  sendMail(base64String);
  res.json({
    message: "HAT FUNKTIONIERT",
  });
  console.log(req.file.originalname);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

/**
 * Hier findet der E-Mail Prozess statt
 */
const apiKey = process.env.BREVO_API_KEY;

async function sendMail(base64String) {
  const response = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",

    headers: {
      accept: "application/json",
      "content-type": "application/json",
      "api-key": apiKey,
    },

    body: JSON.stringify({
      sender: {
        name: "Jarvis",
        email: process.env.SENDER_EMAIL,
      },

      to: [
        {
          email: process.env.RECEIVER_EMAIL,
        },
      ],

      subject: "Jarvis Cam Detection",

      textContent: "Someone in your house got detected",

      attachment: [
        {
          content: base64String,
          name: "jarvis.jpg",
        },
      ],
    }),
  });

  const data = await response.json();

  console.log(`BREVO ANTWORTET: ${data} und api key ist ${apiKey}`);
}
