import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = GROQ_API_KEY  # chat_routes.py 호환용 별칭

MODEL = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────
# Python이 직접 관리하는 다음 질문 (LLM에 의존 안 함)
# ─────────────────────────────────────────────
COUNTRY_KEYWORDS = [
    "일본", "베트남", "태국", "필리핀", "싱가포르", "홍콩", "대만",
    "중국", "유럽", "미국", "호주", "인도네시아", "말레이시아", "캄보디아",
    "스페인", "프랑스", "이탈리아", "영국", "독일", "터키", "그리스",
]

def get_next_question(slots: dict, last_user_msg: str = "") -> str | None:
    """슬롯 상태를 보고 다음에 물어볼 질문을 Python이 직접 결정"""
    dest = slots.get("destination")

    # 1단계: 목적지 (국가명만 있으면 세부 도시 재확인)
    if not dest:
        for kw in COUNTRY_KEYWORDS:
            if kw in last_user_msg:
                return f"{kw} 중에서도 어느 도시나 지역을 생각하고 계신가요?"
        return "이번 여행은 어디로 떠나고 싶으신가요? 📍"

    # 2단계: 기간
    if not slots.get("duration"):
        return "여행 기간은 어떻게 되시나요?"

    # 3단계: 동반자
    if not slots.get("companion"):
        return "이번 여행은 누구와 함께 가시나요?"

    # 4단계: 예산
    if not slots.get("budget"):
        return "이번 여행 총 예산은 어느 정도 생각하시나요?"

    # 5단계: 스타일
    if not slots.get("style"):
        return "어떤 여행 스타일을 원하시나요? 예를 들어 맛집 탐방, 쇼핑, 힐링 등이 있어요."

    # 6단계: 음식 취향
    if not slots.get("food_preference"):
        return "혹시 못 드시는 음식이나 알레르기가 있으신가요? 예를 들어 해산물, 유제품 등이요."

    return None  # 모든 슬롯 채워짐


# ─────────────────────────────────────────────
# LLM 슬롯 추출 전용 프롬프트 (질문 생성 없음)
# ─────────────────────────────────────────────
EXTRACTION_PROMPT = """당신은 여행 정보 추출 전문가입니다.
사용자의 대화 기록에서 아래 6가지 슬롯 정보를 추출하세요.

[슬롯 정의]
- destination: 구체적인 도시/지역명만 (예: "오사카", "나트랑", "도쿄"). 국가명만 언급된 경우(예: "일본", "베트남") null 유지.
- duration: 여행 기간 (예: "2박 3일", "4박 5일")
- companion: 동반자 (예: "혼자", "친구 1명", "친구 2명", "가족")
- budget: 예산 (예: "100만원", "총 150만원")
- style: 여행 스타일 (예: "맛집 탐방", "쇼핑", "힐링", "액티비티")
- food_preference: 음식 취향/선호/불호/알레르기 (예: "해산물 불호", "라멘 좋아함", "유제품 알레르기")

[추출 규칙]
- 대화 기록 전체를 분석하여 이미 언급된 슬롯을 모두 채우세요.
- 한 문장에서 여러 슬롯이 동시에 언급된 경우 모두 추출하세요.
- 명시되지 않은 슬롯은 반드시 null로 유지하세요.
- 국가명(일본, 베트남 등)은 destination에 넣지 마세요. 세부 도시/지역명만 허용.

[응답 형식 — 절대 규칙]
- <think> 태그, 마크다운 코드블록 없이 { 로 시작하는 순수 JSON만 반환하세요.
{
  "destination": string 또는 null,
  "duration": string 또는 null,
  "companion": string 또는 null,
  "budget": string 또는 null,
  "style": string 또는 null,
  "food_preference": string 또는 null
}"""


# ─────────────────────────────────────────────
# 완료 시 일정(travel_plan) 생성 프롬프트 및 조립 함수
# ─────────────────────────────────────────────
PLAN_GENERATION_PROMPT = """당신은 10년 경력의 전문 여행 플래너입니다.
제공된 여행 정보를 바탕으로 마크다운 형식의 상세 일정을 기획해 주세요.

[작성 규칙]
1. 일자별(1일차, 2일차...) 순서로 시간대별 구체적 일정표를 작성하세요.
   - 각 일자는 "## N일차 — [테마명]" 헤더로 시작
   - 마크다운 표(Table) 형식으로 시간 | 일정 | 추천 장소 | 예상 비용
   - 표 아래에 그날의 핵심 포인트 2~3가지 bullet 추가
2. 식사 장소마다 표 아래에 별도 섹션으로 상세 서술:
   - 어떤 음식인가요? (처음 방문한 외국인도 이해할 수 있는 1~2줄 설명)
   - 현지인 추천 메뉴 (메뉴명 + 가격 + 이유)
   - 한국인 인기 메뉴 (메뉴명 + 가격 + 이유)
   - 맛있게 먹는 꿀팁 (소스 비율, 추가 주문 팁 등)
   - ⏰ 이용 꿀팁 (웨이팅/예약 정보, 추천 방문 시간)
3. 동선 간 이동 수단과 소요 시간 포함
4. 마지막에 동반자 스타일 맞춤 꿀팁 3가지 추가
5. 음식 취향(food_preference)을 엄격히 반영:
   - 선호하는 음식은 우선적으로 추천 목록에 포함
   - 싫어하거나 알레르기가 있는 재료는 추천 식당에서 완전히 배제
6. 모든 가격은 현지 통화와 원화 환산 가격을 함께 표기하세요.

다른 인사말이나 설명, 잡담은 일절 하지 말고, 곧바로 '## 1일차 — ...'부터 출력해 주세요."""


def build_assembled_prompt(slots: dict) -> str:
    dest = slots.get("destination") or "선택된 목적지"
    budget = slots.get("budget") or "적정 예산"
    duration = slots.get("duration") or "지정 기간"
    companion = slots.get("companion") or "동반자"
    style = slots.get("style") or "추천 스타일"
    food = slots.get("food_preference") or "없음"
    
    return f"""당신은 10년 차 {dest} 전문 여행 플래너입니다.
아래 수집된 정보를 기반으로, 고품격 맞춤형 상세 여행 일정을 기획해 주세요.

[기본 설정]
- 목적지: {dest}
- 총 예산: {budget}
- 여행 기간: {duration}
- 동반자: {companion}
- 여행 스타일: {style}
- 음식 취향: {food}
  → 선호하는 음식은 우선적으로 포함, 불호하거나 알레르기 유발 식재료가 포함된 식당은 절대 추천 금지

[작성 가이드]
1. 일자별(1일차, 2일차...) 순서로 시간대별 구체적 일정표를 작성하세요.
   - 각 일자는 "## N일차 — [테마명]" 헤더로 시작
   - 마크다운 표(Table) 형식으로 시간 | 일정 | 추천 장소 | 예상 비용
   - 표 아래에 그날의 핵심 포인트 2~3가지 bullet 추가
2. 식사 장소마다 표 아래에 별도 섹션으로 상세 서술:
   - 어떤 음식인가요? (외국인도 이해할 수 있는 설명)
   - 현지인 추천 메뉴 (메뉴명 + 가격 + 이유)
   - 한국인 인기 메뉴 (메뉴명 + 가격 + 이유)
   - 맛있게 먹는 꿀팁 (소스 조합, 현지 스타일)
   - 이용 꿀팁 (웨이팅/예약 정보)
3. 동선 간 이동 수단과 소요 시간 포함
4. 마지막에 동반자 스타일 맞춤 꿀팁 3가지 추가"""



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
5. 다른 인사말, 설명, 잡담은 일절 하지 말고, 오직 수정 완료된 최종 전체 일정표(마크다운 형식)만 출력해 주세요.
"""


# ─────────────────────────────────────────────
# 공통 JSON 파싱 유틸
# ─────────────────────────────────────────────
def _parse_json(text: str) -> dict:
    """<think> 제거, 코드블록 제거, {…} 추출 후 JSON 파싱"""
    text = re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text, flags=re.IGNORECASE).strip()
    start, end = text.find('{'), text.rfind('}')
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return json.loads(text)


def _call_groq(system: str, user: str, temperature: float = 0.6, max_tokens: int = None) -> str:
    """Groq API 호출 공통 함수"""
    client = Groq(api_key=GROQ_API_KEY)
    kwargs = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        "temperature": temperature,
    }
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
        
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()



# ─────────────────────────────────────────────
# 메인 에이전트 세션
# ─────────────────────────────────────────────
def run_agent_session(messages: list) -> dict:
    """슬롯 추출은 LLM, 다음 질문은 Python이 직접 결정"""
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY가 .env 파일에 설정되지 않았습니다."}

    # 대화 기록 텍스트 변환
    conversation_text = ""
    last_user_msg = ""
    for msg in messages:
        role = "사용자" if msg.get("role") == "user" else "AI"
        content = msg.get("content", "")
        conversation_text += f"{role}: {content}\n"
        if msg.get("role") == "user":
            last_user_msg = content

    try:
        # ① LLM으로 슬롯만 추출 (rate limit 대비 1회 재시도)
        import time
        for attempt in range(2):
            try:
                raw = _call_groq(
                    system=EXTRACTION_PROMPT,
                    user=f"[대화 기록]\n{conversation_text}\n\n슬롯을 추출하여 JSON으로만 반환하세요:",
                    temperature=0.3,
                )
                break
            except Exception as api_err:
                if attempt == 0 and ("429" in str(api_err) or "rate" in str(api_err).lower()):
                    time.sleep(3)
                    continue
                raise api_err

        parsed = _parse_json(raw)

        # 모델이 {"slots": {...}} 로 감싸서 반환하는 경우 처리
        if "slots" in parsed and isinstance(parsed.get("slots"), dict):
            slots = parsed["slots"]
        else:
            slots = parsed

        # 슬롯 키 정규화 (누락된 키 → null)
        for key in ["destination", "duration", "companion", "budget", "style", "food_preference"]:
            if key not in slots or slots[key] == "":
                slots[key] = None

        # ② Python이 다음 질문 결정
        next_q = get_next_question(slots, last_user_msg)

        if next_q is not None:
            # 아직 인터뷰 중
            return {
                "status": "interviewing",
                "slots": slots,
                "missing_slots": [k for k, v in slots.items() if not v],
                "next_question": next_q,
                "assembled_prompt": None,
                "travel_plan": None,
            }

        # ③ 모든 슬롯 채워짐 → Python으로 assembled_prompt 생성, LLM으로 travel_plan 생성
        assembled = build_assembled_prompt(slots)

        travel_plan = _call_groq(
            system=PLAN_GENERATION_PROMPT,
            user=(
                f"[수집된 여행 정보]\n"
                f"목적지: {slots['destination']}\n"
                f"기간: {slots['duration']}\n"
                f"동반자: {slots['companion']}\n"
                f"예산: {slots['budget']}\n"
                f"스타일: {slots['style']}\n"
                f"음식 취향: {slots['food_preference']}\n\n"
                f"이 조건에 맞춘 최고의 마크다운 여행 일정을 생성해 주세요:"
            ),
            temperature=0.7,
            max_tokens=4000,
        )

        # <think>...</think> 추론 블록 제거 및 코드블록 마크다운 기호 제거
        travel_plan = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', travel_plan, flags=re.IGNORECASE).strip()
        travel_plan = re.sub(r'^```(?:markdown)?\s*', '', travel_plan, flags=re.IGNORECASE)
        travel_plan = re.sub(r'\s*```$', '', travel_plan, flags=re.IGNORECASE).strip()

        return {
            "status": "completed",
            "slots": slots,
            "missing_slots": [],
            "next_question": "취향 분석이 완료되었습니다. 입력된 조건을 반영한 맞춤형 여행 일정 생성 프롬프트를 작성했습니다.",
            "assembled_prompt": assembled,
            "travel_plan": travel_plan,
        }


    except Exception as e:
        import traceback
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("--- Groq Agent Error ---\n")
            f.write(f"Error: {str(e)}\n")
            traceback.print_exc(file=f)
        print(f"[Groq Agent Error] {e}")
        return {"error": f"Groq API 호출 실패: {str(e)}"}


# ─────────────────────────────────────────────
# 일정 수정 (Refine)
# ─────────────────────────────────────────────
def refine_travel_plan(current_plan: str, assembled_prompt: str, modification_request: str) -> dict:
    """기존 일정표를 사용자의 수정 요청에 맞게 업데이트"""
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY가 .env 파일에 설정되지 않았습니다."}

    try:
        result_text = _call_groq(
            system=REFINE_SYSTEM_PROMPT,
            user=(
                f"[현재 일정표]\n{current_plan}\n\n"
                f"[현재 슬롯 정보]\n{assembled_prompt}\n\n"
                f"[수정 요청]\n{modification_request}\n\n"
                f"최종 전체 일정표를 마크다운으로 출력해 주세요:"
            ),
            temperature=0.6,
        )
        result_text = re.sub(r'<think>[\s\S]*?</think>', '', result_text, flags=re.IGNORECASE).strip()
        result_text = re.sub(r'^```(?:markdown)?\s*', '', result_text, flags=re.IGNORECASE)
        result_text = re.sub(r'\s*```$', '', result_text, flags=re.IGNORECASE).strip()
        return {"travel_plan": result_text}

    except Exception as e:
        import traceback
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("--- Groq Refine Error ---\n")
            f.write(f"Error: {str(e)}\n")
            traceback.print_exc(file=f)
        print(f"[Groq Refine Error] {e}")
        return {"error": f"Groq 수정 API 호출 실패: {str(e)}"}
