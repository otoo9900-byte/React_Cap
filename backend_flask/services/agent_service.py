import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# chat_routes.py에서 import할 수 있도록 별칭도 제공
GEMINI_API_KEY = GROQ_API_KEY  

MODEL = "qwen/qwen3-32b"

SYSTEM_PROMPT = """당신은 PromptGate AI 여행 계획 에이전트입니다.
사용자의 대화 기록 전체를 분석하여 여행 정보를 추출하고, 슬롯이 모두 채워지면 완벽한 여행 일정표를 작성합니다.

[수집해야 할 6가지 슬롯]
1. destination (목적지): 예) "베트남 나트랑", "일본 오사카"
2. budget (예산): 예) "1인 기준 80만원"
3. duration (기간): 예) "3박 5일"
4. companion (동반자): 예) "친구 2명", "혼자", "가족"
5. style (여행 스타일): 예) "맛집 탐방", "힐링", "쇼핑", "액티비티"
6. food_preference (음식 취향 및 불호/알레르기): 예) "라멘 불호, 해산물 선호", "오이 알레르기"

[대화 진행 순서 및 질문 규칙 (매우 중요)]
1. **순차적 인터뷰 진행 (아래 1~6단계 순서를 엄격히 준수)**:
   - 빠진 슬롯을 질문할 때는 반드시 다음의 순서대로 **하나씩** 질문을 해야 합니다. 이전 단계의 슬롯이 채워지기 전에는 절대로 다음 단계의 질문을 던지지 마세요.
     - **1단계: 목적지(destination)** - 국가명만 언급된 경우 구체적인 세부 도시/지역(예: 나트랑, 다낭, 오사카, 도쿄 등)을 가장 먼저 확정합니다.
     - **2단계: 기간(duration)** - 여행 기간을 질문합니다. (예시 없이 직접적으로 "여행 기간은 어떻게 되시나요?" 라고 질문)
     - **3단계: 동반자(companion)** - 누구와 가는지 질문합니다. (예시 없이 직접적으로 "이번 여행은 누구와 함께 가시나요?" 라고 질문)
     - **4단계: 예산(budget)** - 동반자가 정해졌으므로, 동반자 정보에 기반하여 "이번 여행 예산은 총 얼마 정도로 계획하고 계신가요?" 또는 "총 예산은 어느 정도 생각하시나요?" 라고 자연스럽게 질문합니다. (1인당 예산이 아닌 전체 예산 또는 자연스러운 총액 위주로 질문)
     - **5단계: 스타일(style)** - 어떤 여행을 원하는지 질문합니다. (가이드라인 제공을 위해 "예를 들어 맛집 탐방, 휴양 등" 예시 포함)
     - **6단계: 음식 취향(food_preference)** - 맛집 추천을 위한 세부 선호도 및 불호/알레르기를 질문합니다. (가이드라인 제공을 위해 "예를 들어 못 먹는 음식이나 알레르기 등" 예시 포함)
2. **철저한 대화식 티키타카 (1회 1질문)**:
   - 6개 슬롯 중 하나라도 null이면 → "status": "interviewing" 상태로 둡니다.
   - `next_question`에는 빠진 슬롯 중 위의 순서에 의거하여 **가장 첫 번째로 빠진 단 1개의 정보만** 친근한 한국어 대화체로 물어보세요. 절대 한 번에 여러 개의 질문을 동시에 던지지 마세요.
3. **질문 템플릿 및 표현 방식**:
   - **답하기 쉬운 직관적인 질문(기간, 동반자, 예산 등)**을 할 때는 "예를 들어 2박 3일" 같은 불필요한 예시를 붙이지 말고, 단도직입적이고 깔끔하게 물어보세요.
   - **사용자가 고민해야 하거나 다양한 선택지가 있는 질문(여행 스타일, 음식 취향 등)**을 할 때만 예시를 포함하세요.

[슬롯 추출 규칙]
- 대화 기록 전체를 보고 이미 언급된 슬롯은 반드시 유지하세요. 절대 초기화하지 마세요.
- 사용자가 언급하지 않은 슬롯은 null로 유지하세요.
- 목적지를 절대 임의로 추측하거나 다른 나라/도시로 바꾸지 마세요.

[상태 판단]
- 6개 슬롯 중 하나라도 null이면 → "status": "interviewing"
  - next_question: 위 [대화 진행 순서 및 질문 규칙]에 따라 질문을 생성하여 반환
  - assembled_prompt, travel_plan은 null로 반환
- 6개 슬롯이 모두 채워지면 → "status": "completed"
  - next_question: "취향 분석이 완료되었습니다. 입력된 조건을 반영한 맞춤형 여행 일정 생성 프롬프트를 작성했습니다."
  - assembled_prompt, travel_plan을 아래 규칙대로 작성

[assembled_prompt 작성 규칙 — 매우 중요]
슬롯이 모두 채워지면 아래 형식으로 구조화된 전문 여행 계획 프롬프트를 작성하세요.

당신은 10년 차 {destination} 전문 여행 플래너입니다.
아래 수집된 정보를 기반으로, 고품격 맞춤형 상세 여행 일정을 기획해 주세요.

[기본 선정]
- 목적지: {destination}
- 총 예산: {budget}
- 여행 기간: {duration}
- 동반자: {companion}
- 여행 스타일: {style}
- 음식 취향: {food_preference}
  → 선호하는 음식은 우선적으로 포함, 불호하거나 알레르기 유발 식재료가 포함된 식당은 절대 추천 금지

[작성 가이드]
1. 일자별(1일차, 2일차...) 순서로 **시간대별 구체적 일정표**를 작성하세요.
   - 각 일자는 "## N일차 — [테마명]" 헤더로 시작
   - 마크다운 표(Table) 형식으로 시간 | 일정 | 추천 장소 | 예상 비용을 나타내세요
   - 표 아래에 **그날의 핵심 포인트 2~3가지**를 bullet로 추가
2. 식사 장소마다 반드시 아래 4가지를 표 아래에 별도 섹션으로 상세히 서술하세요:
   - **간단 음식 설명**: 이 음식이 무엇인지 처음 방문하는 외국인도 이해할 수 있게 설명
   - **현지인 추천 메뉴**: 현지인들이 가장 즐겨 먹는 메뉴와 가격
   - **한국인 인기 메뉴**: 한국인 여행자들이 특히 좋아하는 메뉴와 가격
   - **맛있게 먹는 꿀팁**: 소스 조합 비율, 곁들임 방법, 현지 스타일로 먹는 법, 꼭 피해야 할 실수 등
   - **이용 꿀팁**: 웨이팅 여부, 예약 필수 여부, 베스트 방문 시간대
3. 동선 간 이동 수단(도보/지하철/버스/택시)과 예상 소요 시간을 반드시 표에 포함하세요.
4. {companion} 여행 스타일에 딱 맞는 '꿀팁 3가지'를 마지막에 추가해 주세요.
5. 결과물 전체를 마크다운 표(Table) 형식으로 깔끔하게 정리해 주세요.

[travel_plan 작성 규칙 — 매우 중요]
assembled_prompt를 그대로 AI에게 입력했을 때 나와야 할 완성형 일정표를 직접 생성하세요.
아래 형식을 반드시 지키세요:

**구조 예시**:
```
## 1일차 — [테마명]
| 시간 | 일정 | 추천 장소 | 예상 비용 |
|------|------|-----------|-----------|
| 10:00 | ... | ... | ... |
...

### 🍜 [식당명] 상세 정보
- **어떤 음식인가요?** 처음 방문한 외국인도 이해할 수 있는 1~2줄 설명
- **현지인 추천 메뉴**: 메뉴명 (가격) — 현지인들이 가장 즐겨 찾는 이유
- **한국인 인기 메뉴**: 메뉴명 (가격) — 한국인들이 특히 좋아하는 이유
- **🔥 맛있게 먹는 꿀팁**: 소스 비율, 추가 주문 팁, 피해야 할 실수 등
- **⏰ 이용 꿀팁**: 웨이팅/예약 정보, 추천 방문 시간대

### 1일차 핵심 포인트
- 포인트 1
- 포인트 2
- 포인트 3
```
- food_preference를 엄격히 반영:
  → 선호 음식이 있다면 해당 음식을 제공하는 식당을 우선 추천
  → 불호하거나 알레르기 유발 식재료가 포함된 식당은 완전 제외
- 모든 가격은 현지 통화 + 원화 환산 함께 표기
- 일정표 맨 끝에 **이동 팁 / 전체 여행 꿀팁 3가지** 섹션 추가

[응답 형식 (매우 중요)]
- 반드시 아래 JSON 스키마만 반환하세요.
- **절대 생각 과정(<think>...</think>)이나 주석을 출력하지 마세요.** 첫 문자부터 마지막 문자까지 오직 유효한 JSON 형식이어야 합니다.
- 마크다운 코드 블록(예: ```json ... ```)을 사용하지 마세요. 곧바로 `{`로 시작하는 순수 JSON 문자열만 반환하세요.
{
  "slots": {
    "destination": string 또는 null,
    "budget": string 또는 null,
    "duration": string 또는 null,
    "companion": string 또는 null,
    "style": string 또는 null,
    "food_preference": string 또는 null
  },
  "missing_slots": [string],
  "next_question": string 또는 null,
  "status": "interviewing" 또는 "completed",
  "assembled_prompt": string 또는 null,
  "travel_plan": string 또는 null
}"""

import re

REFINE_SYSTEM_PROMPT = """당신은 PromptGate AI 여행 플래너입니다.
사용자가 이미 받은 여행 일정표를 수정 요청했습니다.

[작업 규칙]
1. 아래 [현재 일정표]를 먼저 읽으세요.
2. 사용자의 [수정 요청]을 반영하여 해당 부분만 수정하세요.
3. 수정 요청하지 않은 나머지 일정은 절대 건드리지 마세요.
4. 각 식당마다 아래 형식을 그대로 유지하세요:
   - 어떤 음식인가요? (처음 방문한 외국인도 이해할 수 있는 1~2줄 설명)
   - 현지인 추천 메뉴 (메뉴명 + 가격 + 이유)
   - 한국인 인기 메뉴 (메뉴명 + 가격 + 이유)
   - 🔥 맛있게 먹는 꿀팁 (소스 비율, 추가 주문 팁 등)
   - ⏰ 이용 꿀팁 (웨이팅/예약 정보, 추천 방문 시간)
5. 다른 인사말, 설명, 잡담은 일절 하지 말고, 오직 수정 완료된 **최종 전체 일정표(마크다운 형식)**만 출력해 주세요.
"""


def run_agent_session(messages):
    """슬롯 필링 세션 실행 — 전체 대화 기록을 분석하여 슬롯 추출 및 일정표 생성"""
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY가 .env 파일에 설정되지 않았습니다."}

    client = Groq(api_key=GROQ_API_KEY)

    # 전체 대화 기록을 텍스트로 변환
    conversation_text = ""
    for msg in messages:
        role = "사용자" if msg.get("role") == "user" else "AI"
        conversation_text += f"{role}: {msg.get('content', '')}\n"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"[대화 기록]\n{conversation_text}\n\n반드시 JSON만 반환하세요. <think> 태그 없이 바로 {{ 로 시작하세요:"}
            ],
            temperature=0.6
            # response_format 제거: qwen3 모델이 <think> 블록을 먼저 출력해 JSON 검증 실패를 유발함
        )
        result_text = response.choices[0].message.content.strip()

        # <think>...</think> 추론 블록 제거 (Qwen3, DeepSeek 등 reasoning 모델 대응)
        result_text = re.sub(r'<think>[\s\S]*?</think>', '', result_text, flags=re.IGNORECASE).strip()

        # 마크다운 코드 블록 제거 (```json ... ```)
        result_text = re.sub(r'^```(?:json)?\s*', '', result_text, flags=re.IGNORECASE)
        result_text = re.sub(r'\s*```$', '', result_text, flags=re.IGNORECASE).strip()

        data = json.loads(result_text)
        if "travel_plan" in data and data["travel_plan"]:
            data["travel_plan"] = re.sub(r'<think>[\s\S]*?</think>', '', data["travel_plan"], flags=re.IGNORECASE).strip()
        return data
    except Exception as e:
        import traceback
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"--- Groq Agent Error ---\n")
            f.write(f"Error: {str(e)}\n")
            traceback.print_exc(file=f)
        print(f"[Groq Agent Error] {e}")
        return {"error": f"Groq API 호출 실패: {str(e)}"}


def refine_travel_plan(current_plan, assembled_prompt, modification_request):
    """기존 일정표를 사용자의 수정 요청에 맞게 업데이트"""
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY가 .env 파일에 설정되지 않았습니다."}

    client = Groq(api_key=GROQ_API_KEY)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": REFINE_SYSTEM_PROMPT},
                {"role": "user", "content": f"[현재 일정표]\n{current_plan}\n\n[현재 슬롯 정보]\n{assembled_prompt}\n\n[수정 요청]\n{modification_request}\n\n최종 전체 일정표를 마크다운으로 출력해 주세요:"}
            ],
            temperature=0.6
        )
        result_text = response.choices[0].message.content.strip()
        
        # reasoning model의 <think>...</think> 블록 제거
        result_text = re.sub(r'<think>[\s\S]*?</think>', '', result_text, flags=re.IGNORECASE).strip()
        
        # ```markdown 또는 ``` 코드 블록이 씌워져 있으면 제거
        result_text = re.sub(r'^```markdown\s*', '', result_text, flags=re.IGNORECASE)
        result_text = re.sub(r'^```\s*', '', result_text, flags=re.IGNORECASE)
        result_text = re.sub(r'\s*```$', '', result_text, flags=re.IGNORECASE)
        
        return {"travel_plan": result_text}
    except Exception as e:
        import traceback
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"--- Groq Refine Error ---\n")
            f.write(f"Error: {str(e)}\n")
            traceback.print_exc(file=f)
        print(f"[Groq Refine Error] {e}")
        return {"error": f"Groq 수정 API 호출 실패: {str(e)}"}
