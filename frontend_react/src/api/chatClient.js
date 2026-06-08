const API_BASE_URL = 'http://localhost:5000/api';

export const sendChatMessage = async (message, messages = [], conversationId = "", currentPlan = null, currentAssembledPrompt = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, messages, conversationId, currentPlan, currentAssembledPrompt }),
    });

    if (!response.ok) {
      throw new Error(`API error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error sending message to backend:", error);
    throw error;
  }
};

export const executeAssembledPrompt = async (prompt) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      throw new Error(`API error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error executing prompt:", error);
    throw error;
  }
};
