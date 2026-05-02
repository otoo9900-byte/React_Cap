const API_BASE_URL = 'http://localhost:5000/api';

export const sendChatMessage = async (message) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
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
