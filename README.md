# PromptGate (v2.0)

**PromptGate**는 사용자의 단순하고 모호한 요구사항을 AI와의 역질문 대화를 통해 전문가 수준의 프롬프트로 자동 변환해 주는 지능형 커뮤니케이션 서비스입니다. (Flask 백엔드 + Vite React 프론트엔드 + Dify 워크플로우 기반)

## 📌 주요 문서
- [제품 요구사항 문서 (PRD v2)](./PromptGate%20PRD%20v2.md)
- [기존 PRD (v1)](./PromptGate%20PRD.md)

## 🚀 프로젝트 구조
전체 프로젝트는 유지보수성과 협업을 위해 백엔드, 프론트엔드, AI 워크플로우 3가지 영역으로 분리되어 있습니다.

```text
promptgate-project/
├── backend_flask/          # Flask 기반 API 서버 (프론트엔드 - Dify 중계)
│   ├── api/                # REST API 엔드포인트 라우터 (chat_routes 등)
│   ├── app.py              # Flask 애플리케이션 진입점
│   └── requirements.txt
├── frontend_react/         # React 프론트엔드 (Vite + Tailwind CSS + Zustand)
│   ├── src/
│   │   ├── api/            # 백엔드 API 호출 모듈
│   │   ├── components/     # UI 모듈 (Chat, Dashboard, ResultView)
│   │   ├── pages/          # 라우팅 페이지
│   │   └── store/          # Zustand 전역 상태 관리
│   └── ...
└── dify_workflows/         # (예정) Dify Chatflow 설정 파일 (Export)
```

## 📈 현재 개발 진행 상태 (Current Status)
현재 프로젝트는 **초기 UI 프로토타입 및 백엔드 구조 스캐폴딩 단계**입니다.
- **Frontend (`frontend_react/`)**: 
  - 화면 분할 구조(Split View) 구성: 좌측 대화형 챗봇 화면, 우측 최종 프롬프트 출력 화면(ResultView).
  - Zustand를 활용한 통합 상태 관리.
  - 상단 Dashboard 영역에 토큰 비용 시뮬레이터(CostSimulator) 팝업 UI 구현.
  - Axios를 통해 로컬 Flask 백엔드의 Mock API와 통신 연동.
- **Backend (`backend_flask/`)**:
  - Flask 애플리케이션 및 CORS 초기 세팅 (`app.py`).
  - `/api/chat/` 라우트를 통해 프론트엔드의 메시지를 받고 Mock 데이터 응답을 내려주도록 구성 (`chat_routes.py`).

## 💻 팀원 로컬 실행 방법 (Getting Started)

### 1. Repository Clone
```bash
git clone https://github.com/otoo9900-byte/React_Cap.git
cd React_Cap
```

### 2. Backend 실행 (Flask)
Python 가상 환경을 생성하고 백엔드 서버를 실행합니다.
```bash
cd backend_flask

# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# (Mac/Linux)
# python3 -m venv venv
# source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행 (기본 포트: 5000)
python app.py
```
서버가 켜지면 브라우저에서 `http://localhost:5000/` 접속 시 상태 확인 메시지가 표시됩니다.

### 3. Frontend 실행 (React)
새 터미널을 열고 프론트엔드 디렉토리로 이동하여 개발 서버를 실행합니다.
```bash
cd frontend_react

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```
브라우저에서 `http://localhost:5173` 으로 접속하여 UI와 백엔드 통신(채팅)을 테스트합니다.

## 🤝 협업 가이드 (Collaboration Guide)
1. **Branching**: 새로운 기능 개발 전 항상 새 브랜치를 생성하고 작업해주세요.
   - `feature/기능이름` (예: `feature/chat-ui`, `feature/dify-integration`)
   - `fix/버그이름`
2. **Pull Request (PR)**: 작업 완료 후 `main` 브랜치로 바로 푸시하지 않고, PR을 생성하여 팀원의 리뷰를 거친 뒤 Merge 합니다.
3. **환경 변수**: 향후 Dify API Key 등 보안이 필요한 키는 절대 커밋하지 않고 각자의 `.env` 로컬 파일에서 관리합니다.
