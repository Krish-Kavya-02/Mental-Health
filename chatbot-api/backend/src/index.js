import express, { json } from "express";
import cors from "cors";
import dotenv from "dotenv";
dotenv.config();

import chatRoutes from "./routes/chat.js";

const app = express();
app.use(cors()); // Enable CORS for all routes
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded requests
app.use(json()); // Parse JSON requests

app.use("/chat", chatRoutes); // Use /chat routes






const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Chatbot API running on port ${PORT}`);
});

// Handle 404 errors
app.use((req, res) => {
  res.status(404).json({ error: "Not Found" });
});