import { create } from 'zustand';

const usePromptGateStore = create((set) => ({
  // Chat State
  messages: [
    {
      id: 'system-start',
      role: 'assistant',
      content: '안녕하세요! 저는 PromptGate 에이전트입니다. 어떤 종류의 프롬프트를 만들고 싶으신가요? (예: "로고 만들어줘", "블로그 글 써줘")',
    },
  ],
  isTyping: false,

  // Assembler State
  assembledPrompt: null,
  intents: null,

  // Token Metrics State
  tokenMetrics: {
    directCostUsd: 0,
    optimizedCostUsd: 0,
    savedTokens: 0,
  },

  // Actions
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  setIsTyping: (isTyping) => set({ isTyping }),

  setAssembledResult: (result) =>
    set({
      assembledPrompt: result.assembledPrompt,
      intents: result.extractedIntents,
      tokenMetrics: result.tokenMetrics,
    }),

  resetSession: () =>
    set({
      messages: [
        {
          id: 'system-start',
          role: 'assistant',
          content: '안녕하세요! 저는 PromptGate 에이전트입니다. 어떤 종류의 프롬프트를 만들고 싶으신가요?',
        },
      ],
      assembledPrompt: null,
      intents: null,
      tokenMetrics: { directCostUsd: 0, optimizedCostUsd: 0, savedTokens: 0 },
    }),

  // Real API Call
  sendMessage: async (userText) => {
    set((state) => ({
      messages: [...state.messages, { id: Date.now().toString(), role: 'user', content: userText }],
      isTyping: true,
    }));

    try {
      const { sendChatMessage } = await import('../api/chatClient.js');
      const result = await sendChatMessage(userText);
      
      set((state) => ({
        messages: [
          ...state.messages,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: result.response || "서버 응답이 없습니다.",
          },
        ],
        isTyping: false,
      }));

      // Update token metrics if provided
      if (result.token_metrics) {
        set({ tokenMetrics: result.token_metrics });
      }

    } catch (error) {
      console.error(error);
      set((state) => ({
        messages: [
          ...state.messages,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: "서버와 통신하는 중 오류가 발생했습니다. Flask 백엔드가 실행 중인지 확인해주세요.",
          },
        ],
        isTyping: false,
      }));
    }
  },
}));

export default usePromptGateStore;
