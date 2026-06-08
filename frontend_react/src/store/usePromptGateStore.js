import { create } from 'zustand';

const usePromptGateStore = create((set, get) => ({
  // Chat State
  messages: [
    {
      id: 'system-start',
      role: 'assistant',
      content: '안녕하세요! ✈️ **PromptGate AI 여행 플래너**입니다. 사용자님의 선호도와 맛집 취향에 맞는 완벽한 일정을 디자인해 드릴게요. 먼저, **이번 여행은 어디로 떠나고 싶으신가요? 📍**',
    },
  ],
  isTyping: false,
  conversationId: null,

  // Assembler State
  assembledPrompt: null,
  travelPlan: null,
  intents: null,
  finalResult: null,
  isExecuting: false,

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
          content: '안녕하세요! ✈️ **PromptGate AI 여행 플래너**입니다. 사용자님의 선호도와 맛집 취향에 맞는 완벽한 일정을 디자인해 드릴게요. 먼저, **이번 여행은 어디로 떠나고 싶으신가요? 📍**',
        },
      ],
      assembledPrompt: null,
      travelPlan: null,
      intents: null,
      finalResult: null,
      isExecuting: false,
      tokenMetrics: { directCostUsd: 0, optimizedCostUsd: 0, savedTokens: 0 },
      conversationId: null,
    }),

  // Real API Call
  sendMessage: async (userText) => {
    set((state) => ({
      messages: [...state.messages, { id: Date.now().toString(), role: 'user', content: userText }],
      isTyping: true,
    }));

    try {
      const { sendChatMessage } = await import('../api/chatClient.js');
      const currentConversationId = get().conversationId || "";
      const allMessages = get().messages;
      const currentPlan = get().travelPlan || null;
      const currentAssembledPrompt = get().assembledPrompt || null;
      const result = await sendChatMessage(userText, allMessages, currentConversationId, currentPlan, currentAssembledPrompt);

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
        conversationId: result.conversation_id || state.conversationId,
      }));

      // Update assembled prompt, travel plan & intents if provided
      if (result.assembledPrompt || result.travel_plan) {
        set({
          assembledPrompt: result.assembledPrompt || get().assembledPrompt,
          travelPlan: result.travel_plan || get().travelPlan,
          intents: result.extractedIntents || get().intents,
        });
      }

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

  // Execute Prompt Action
  runAssembledPrompt: async () => {
    const { assembledPrompt } = get();
    if (!assembledPrompt) return;

    set({ isExecuting: true, finalResult: null });

    try {
      const { executeAssembledPrompt } = await import('../api/chatClient.js');
      const result = await executeAssembledPrompt(assembledPrompt);

      if (result.status === 'success') {
        set({ finalResult: result.result, isExecuting: false });
      } else {
        set({ finalResult: "오류가 발생했습니다: " + result.error, isExecuting: false });
      }
    } catch (error) {
      console.error(error);
      set({ 
        finalResult: "결과를 생성하는 중 오류가 발생했습니다. 백엔드 연결 또는 API 키를 확인해주세요.", 
        isExecuting: false 
      });
    }
  },
}));

export default usePromptGateStore;