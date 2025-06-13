import { Router } from "express";
const router = Router();
import { getResponse } from "../services/responseService.js";

router.post("/", async (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: "Message is required" });
  }

  try {
    const response = await getResponse(message);
    res.status(200).json({ response });
  } catch (error) {
    console.error("Error in chat route:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// mood api
router.post('/mood', (req, res) => {
  const { mood } = req.body;
  if (!mood) return res.status(400).json({ error: 'Mood required' });

  const result = responseService.recordMood(mood);
  res.json(result);
});

// GET /api/suggestions
router.get('/suggestions', (req, res) => {
  const suggestions = responseService.getSuggestions();
  res.json({ suggestions });
});

// Handle 404 errors for this route
router.use((req, res) => {  
  res.status(404).json({ error: "Not Found" });
});
export default router;