import express, { json } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { connectDB } from "./config/db.js";
import chatRoutes from "./routes/chat.js";

// Load environment variables
dotenv.config();

const app = express();
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(json());

app.use("/chat", chatRoutes);
app.get('/', (req, res) => {
  res.json({ message: 'chatbot-api is running' });
});

const PORT = process.env.PORT || 3000;

// Initialize DB connection and start server
connectDB()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Chatbot API running on port ${PORT}`);
    });
  })
  .catch((error) => {
    console.error('Failed to start server:', error);
    process.exit(1);
  });

// Handle 404 errors
app.use((req, res) => {
  res.status(404).json({ error: "Not Found" });
});