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

  // Mock API Call
  sendMessageMock: async (userText) => {
    set((state) => ({
      messages: [...state.messages, { id: Date.now().toString(), role: 'user', content: userText }],
      isTyping: true,
    }));

    // Simulate network delay
    setTimeout(() => {
      // Mock basic intent analysis and follow-up
      if (userText.includes('블로그') || userText.includes('글')) {
        set((state) => ({
          messages: [
            ...state.messages,
            {
              id: Date.now().toString(),
              role: 'assistant',
              content: '블로그 글 작성이군요! 글의 타겟 독자(예: 20대 직장인)와 주요 톤앤매너(예: 전문적인, 친근한)를 알려주시면 더 완벽한 프롬프트를 만들어드릴게요.',
            },
          ],
          isTyping: false,
        }));
      } else {
        // Mock Final Assembly
        set((state) => ({
          messages: [
            ...state.messages,
            {
              id: Date.now().toString(),
              role: 'assistant',
              content: '필요한 정보가 모두 수집되었습니다. 우측 창에서 최적화된 프롬프트를 확인해주세요!',
            },
          ],
          isTyping: false,
          assembledPrompt: `당신은 10년 차 전문가입니다. 다음 요구사항을 바탕으로 작업을 수행해 주세요.\n\n[주제]: ${userText}\n[포맷]: 구조화된 마크다운\n[제약사항]: 간결하고 명확하게 작성할 것`,
          intents: { topic: userText, format: "Markdown" },
          tokenMetrics: {
            directCostUsd: 0.15,
            optimizedCostUsd: 0.03,
            savedTokens: 850,
          }
        }));
      }
    }, 1500);
  },
}));

export default usePromptGateStore;
