async function getResponse(message) {
  // Dummy logic – NLP integration in future
  if (message.toLowerCase().includes("sad")) {
    return "I'm here for you. Want to log how you're feeling?";
  } else if (message.toLowerCase().includes("happy")) {
    return "That's great to hear! Would you like to track your mood today?";
  }
  return "Tell me more about what's on your mind.";
}

const responseService = {
  getResponse,
  getChatResponse: (message) => {
    // Placeholder for chatbot logic (to be integrated with nlp-engine on Days 8-9)
    return `Echo: ${message}`;
  },

  recordMood: (mood) => {
    // Placeholder for mood-tracker integration (to be connected on Days 10-11)
    return { status: 'Mood recorded', mood };
  },

  getSuggestions: () => {
    // Placeholder for suggestions (to be enhanced on Days 10-11)
    return ['Try a calming activity', 'Listen to music'];
  }
};

export { getResponse, responseService };
// chatbot-api/src/services/responseService.js