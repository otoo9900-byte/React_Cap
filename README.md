# PromptGate

**PromptGate**는 단순하고 모호한 요구사항을 AI와의 역질문 대화를 통해 전문가 수준의 프롬프트로 자동 변환해 주는 지능형 커뮤니케이션 서비스입니다. (Antigravity + Vite React 기반)

## 📌 주요 링크
- [제품 요구사항 문서 (PRD)](./PromptGate%20PRD.md)

## 🚀 프로젝트 구조
```text
promptgate-project/
├── backend_antigravity/    # (예정) Antigravity 기반 Python API 서버
├── frontend_react/         # React 프론트엔드 (Vite + Tailwind CSS + Zustand)
│   ├── src/
│   │   ├── components/     # UI 모듈 (Chat, Dashboard, ResultView)
│   │   ├── pages/          # 라우팅 페이지
│   │   └── store/          # 전역 상태 관리
└── ...
```

## 💻 팀원 로컬 실행 방법 (Getting Started)

### 1. Repository Clone
```bash
git clone https://github.com/otoo9900-byte/React_Cap.git
cd React_Cap
```

### 2. Frontend 실행
프론트엔드 디렉토리로 이동하여 패키지를 설치하고 개발 서버를 실행합니다.
```bash
cd frontend_react
npm install
npm run dev
```
브라우저에서 `http://localhost:5173` 으로 접속하여 UI를 확인합니다.

### 3. Backend 실행 (개발 예정)
*(Phase 3 백엔드 구축 이후 작성될 공간입니다.)*

## 🤝 협업 가이드 (Collaboration Guide)
1. **Branching**: 새로운 기능 개발 전 항상 새 브랜치를 생성하고 작업해주세요.
   - `feature/기능이름` (예: `feature/chat-ui`)
   - `fix/버그이름`
2. **Pull Request (PR)**: 작업 완료 후 `main` 브랜치로 바로 푸시하지 않고, PR을 생성하여 팀원의 리뷰를 거친 뒤 Merge 합니다.
3. **환경 변수**: 보안이 필요한 키(API Key 등)는 절대로 커밋하지 않고 각자의 `.env` 로컬 파일에서 관리합니다.
