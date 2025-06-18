import { connectDB } from '../config/db.js';
/**
 * responseService.js
 * This service handles chat responses, mood recording, and suggestions.
 */
export function getResponse(message) {
  const msg = message.toLowerCase();

  if (msg.includes('hello') || msg.includes('hi')) {
    return 'Hello! How can I help you today?';
  }
  if (msg.includes('how are you')) {
    return 'I’m doing great, thanks for asking! How about you?';
  }
  if (msg.includes('bye')) {
    return 'Goodbye! Have a great day!';
  }
  return 'I’m not sure how to respond to that. Try saying "hello" or "how are you".';
}
export async function recordMood(mood) {
  try {
    const db = await connectDB();
    const collection = db.collection('moods');
    const timestamp = new Date();
    const result = await collection.insertOne({ mood, timestamp });
    return { status: 'Mood recorded', mood, id: result.insertedId };
  } catch (error) {
    console.error('Error recording mood:', error);
    throw new Error('Failed to record mood');
  }
}
export function getSuggestions() {
  return ['Try a calming activity', 'Listen to music'];
}