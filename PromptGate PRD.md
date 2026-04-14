# **PromptGate PRD (Product Requirements Document)**

## **Intelligent Prompt Gateway (v1.0)**

## **1\. 개요**

**PromptGate**는 사용자의 단순하고 모호한 요구사항을 AI와의 '스무고개'식 대화를 통해 전문가 수준의 프롬프트로 자동 변환해 주는 지능형 미들웨어 서비스입니다. **Antigravity** 프레임워크 기반의 견고한 백엔드와 React 프론트엔드를 결합하여, 일반인도 최상급의 LLM 결과물을 얻게 함과 동시에 API 토큰 호출 비용을 획기적으로 최적화합니다.

### **핵심 가치 제안**

* **직관성 (No Prompting Required):** 사용자는 프롬프트 작성법을 몰라도 챗봇의 1\~2가지 질문에만 답하면 최적의 결과를 얻습니다.  
* **비용 최적화 (Token Routing):** 사전 대화는 가벼운 모델로 처리하고, 완성된 완벽한 프롬프트만 고성능 모델에 한 번에 전송하여 전체 API 비용을 최대 50% 절감합니다.  
* **데이터 보안 (PII Masking):** 사용자가 실수로 입력한 개인정보나 사내 기밀을 게이트웨이 단에서 감지하고 자동 마스킹 처리하여 정보 유출을 막습니다.  
* **전문성 (Expert Framework):** Chain-of-Thought, Few-shot 등 고급 프롬프트 엔지니어링 기법을 백그라운드에서 자동 적용합니다.

## **2\. 타겟 사용자**

### **주 사용자**

* **AI 활용이 서툰 일반 직장인/학생:** ChatGPT를 띄워놓고 어떻게 질문해야 할지 막막함을 느끼는 사용자.  
* **비용에 민감한 1인 개발자 및 스타트업:** 잦은 프롬프트 시행착오로 인해 발생하는 LLM API 과금(Token 비용)을 줄이고 싶은 개발자.  
* **보안이 중요한 기업 실무자:** 사내 문서를 요약하거나 번역할 때 민감 정보 유출이 걱정되는 사용자.

### **페인포인트**

* "원하는 대답이 안 나와서 계속 질문을 고치다 보니 시간도 낭비되고 토큰 비용만 계속 나간다."  
* "전문가들은 '페르소나를 부여해라, 출력 형식을 지정해라' 하는데 그게 너무 복잡하고 귀찮다."  
* "회사 고객 데이터를 요약하고 싶은데 LLM에 그대로 올리기엔 보안 규정에 걸린다."

## **3\. 핵심 기능 (Features)**

### **P0 \- 필수 기능 (MVP 범위)**

|

| **기능** | **설명** | **기술적 포인트** | **구현 난이도** |

| **Agentic Interviewer** | 사용자 입력 분석 후 누락된 핵심 정보(의도, 형식 등) 역질문 챗봇 | LangGraph (Stateful Workflow) | ⭐⭐⭐⭐ |

| **Prompt Assembler** | 대화 내용을 바탕으로 전문 프롬프트 템플릿에 맞춰 문장 자동 조립 | Antigravity, 템플릿 매핑 로직 | ⭐⭐⭐ |

| **Token Cost Simulator** | "직접 질문 시 예상 비용" vs "PromptGate 사용 시 절감 비용" 실시간 비교 대시보드 | Tokenizer API 연동, 비용 계산식 | ⭐⭐ |

### **P1 \- 고도화 기능 (차별화 포인트)**

| **기능** | **설명** | **기술적 포인트** | **구현 난이도** |

| **Smart LLM Routing** | 조립된 프롬프트의 난이도를 분석하여 적절한 모델(Llama3 vs GPT-4o)로 자동 라우팅 | 분류 알고리즘, 다중 API 통신 | ⭐⭐⭐⭐ |

| **PII Auto-Masking** | 주민번호, 이메일, 전화번호 등 민감 정보를 감지하고

![][image1]처리 | 정규표현식, Named Entity Recognition | ⭐⭐⭐ |

| **Prompt Archive** | 성공적으로 생성된 프롬프트를 사용자 계정에 저장하고 재사용 기능 제공 | PostgreSQL, CRUD API | ⭐⭐ |

## **4\. 기술 스택 (Tech Stack)**

### **백엔드 프레임워크 (Core)**

* **Antigravity:** 메인 서버 API 구축, 데이터 라우팅, 미들웨어 로직 처리 (빠른 비동기 처리 및 파이썬 생태계와의 완벽한 호환성 활용).  
* **LangChain / LangGraph:** 에이전트 워크플로우 제어, 프롬프트 체이닝, 대화 상태(Memory) 관리.

### **프론트엔드 프레임워크**

* **React (Vite):** 컴포넌트 기반 UI 개발 (Split View 레이아웃 적용).  
* **Tailwind CSS:** 빠르고 일관된 디자인 시스템 및 반응형 UI 구현.  
* **Zustand / Context API:** 채팅 상태 및 토큰 절감 데이터 전역 상태 관리.

### **외부 API & 인프라**

* **OpenAI API / Anthropic API:** 대화 처리용(Mini 모델) 및 최종 결과 도출용(Pro 모델) 분리 호출.  
* **PostgreSQL:** 사용자 정보 및 프롬프트 히스토리 저장.

## **5\. 프로젝트 구조 (Architecture)**

promptgate-project/  
├── backend\_antigravity/        \# Antigravity 기반 백엔드 (Python)  
│   ├── app.py                  \# 메인 서버 엔트리포인트  
│   ├── api/                    \# RESTful API 라우터 (Chat, History, Auth)  
│   ├── core/  
│   │   ├── agent.py            \# LangGraph 인터뷰어 챗봇 로직  
│   │   ├── assembler.py        \# 프롬프트 자동 조립 및 최적화 엔진  
│   │   ├── router.py           \# LLM 비용 최적화 라우팅 로직  
│   │   └── security.py         \# PII 데이터 마스킹 정규식 모듈  
│   ├── db/                     \# DB 모델 및 쿼리  
│   └── utils/                  \# Tokenizer 비용 계산 유틸리티  
│  
├── frontend\_react/             \# React 프론트엔드  
│   ├── src/  
│   │   ├── components/  
│   │   │   ├── Chat/           \# 챗봇 인터페이스 (역질문 UI, 버튼형 옵션)  
│   │   │   ├── Dashboard/      \# 비용 절감 시각화 패널 (그래프, 게이지)  
│   │   │   └── ResultView/     \# 생성된 전문가 프롬프트 & 최종 답변 영역  
│   │   ├── pages/              \# Main(Workspace), History, Settings  
│   │   ├── store/              \# Zustand 상태 관리  
│   │   └── services/           \# Antigravity 서버와 통신하는 API 함수  
│   └── package.json

## **6\. API 통합 및 라우팅 전략**

1. **Phase 1 (Intent Analysis):** \* 사용자 첫 입력 수신 ![][image2] 저비용 모델(예: GPT-4o-mini)을 호출하여 의도 파악 및 1\~2개의 핵심 역질문 생성.  
2. **Phase 2 (Assembly & Masking):** \* 대화 완료 시 Antigravity 서버에서 정규식을 통해 PII 데이터 마스킹 수행 ![][image2] CoT 프레임워크 기반 프롬프트 조립.  
3. **Phase 3 (Smart Routing & Execution):** \* 작업 난이도가 낮으면(단순 번역/요약) ![][image2] 저비용 모델로 전송.  
   * 작업 난이도가 높으면(코드 생성, 기획서 작성) ![][image2] 고성능 모델(GPT-4o)로 전송하여 최종 결과 획득.

## **7\. 데이터 모델 (Data Flow)**

### **Optimized Request Object (서버 내부 처리 데이터)**

{  
  "session\_id": "pg-session-9012",  
  "original\_user\_input": "회사 제품 홍보하는 글 좀 써줘. 연락처는 010-1234-5678로 해주고.",  
  "masked\_input": "회사 제품 홍보하는 글 좀 써줘. 연락처는 \[PHONE\_NUMBER\_1\]로 해주고.",  
  "extracted\_intents": {  
    "topic": "신제품 홍보",  
    "tone": "전문적이고 신뢰감 있는",  
    "platform": "링크드인"  
  },  
  "assembled\_prompt": "당신은 10년 차 B2B 전문 카피라이터입니다. 다음 제약 조건과 정보를 바탕으로 링크드인에 적합한 신제품 홍보 게시글을 작성해 주세요. \\n\[조건 1\] 서론-본론-결론의 구조를 가질 것...\\n\[데이터\] 연락처: \[PHONE\_NUMBER\_1\]",  
  "token\_metrics": {  
    "saved\_tokens": 1250,  
    "cost\_reduced\_usd": 0.04  
  }  
}

## **8\. 사용자 스토리 (User Stories)**

### **US-001: 대화형 프롬프트 작성**

* **As a** AI 활용 초보자는  
* **I want to** "로고 만들어줘"처럼 대충 입력해도 챗봇이 "어떤 색상을 원하시나요?"라고 물어봐주기를 원한다.  
* **So that** 프롬프트 엔지니어링을 몰라도 내 의도에 딱 맞는 멋진 결과물을 얻을 수 있다.

### **US-002: 시각적 비용 절감 확인**

* **As a** 비용에 민감한 서비스 기획자는  
* **I want to** 내가 방금 이 시스템을 써서 기존 챗GPT에 직접 썼을 때보다 토큰을 얼마나 아꼈는지 화면에서 바로 확인하고  
* **So that** 시스템 사용의 경제적 효용감을 즉시 느끼고 싶다.

### **US-003: 자동 보안 마스킹**

* **As a** 기업의 HR 담당자는  
* **I want to** 이력서 요약을 요청할 때 실수로 지원자의 전화번호가 포함되더라도 시스템이 알아서 마스킹 처리를 해 주어  
* **So that** 사내 보안 규정을 어기지 않고 안전하게 LLM을 활용할 수 있다.

## **9\. 향후 로드맵 (Roadmap)**

* **1\~4주차:** Antigravity 서버 환경 세팅, React UI Split View 프로토타입 개발, 기초 LangChain 연결.  
* **5\~8주차:** 에이전트(Agentic Interviewer) 로직 구현 및 PII 마스킹 모듈 개발.  
* **9\~12주차:** 프롬프트 템플릿 조립기 완성 및 토큰 라우팅(비용 최적화) 로직 적용.  
* **13\~16주차:** 통합 연동 테스트, 토큰 절감량 대시보드 시각화 고도화, 캡스톤 최종 발표(데모) 준비.