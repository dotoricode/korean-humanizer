# Beta Feedback — v1.0 안정화 응답 누적

> Google Form 응답 raw 데이터 → 익명화 후 이 문서에 누적. v1.0 RC → GA 의 룰 미세 조정 데이터 베이스.
>
> **현재 상태**: 베타 운영 시작 전. 스캐폴딩만. 베타 시작 후 메인테이너가 매일 갱신.

---

## 익명화 룰

| 영역 | 처리 |
|---|---|
| 베타 사용자 식별자 | GitHub username / 한국어 닉네임 → `[user-N]` 같이 익명 ID. 폼 Q10 동의자만 release notes 에 실명 표기. |
| 사용 텍스트 | 폼 Q9 의 "동의" 응답자 텍스트만 인용. 회사명 → `[회사 X]`, 인물명 → `[인물 Y]`, 내부 도메인 → `[domain]`. |
| 환경 / 도메인 / mode (Q1-Q3) | 그대로 — 통계 의미 있음. |
| 1-5 척도 (Q4-Q6) | 그대로. |
| 자유 응답 (Q7-Q8) | 사용자 식별 가능 표현 (이름 / 회사 / 특정 프로젝트) 마스킹. 의도는 그대로. |

---

## 통계 누적 (Week 별)

### Week 1 (yyyy-mm-dd ~ yyyy-mm-dd)

베타 사용자: **N 명 confirmed / N 응답**

| 지표 | 값 |
|---|---|
| 총 응답 수 | N |
| Q4 만족도 평균 | -.- / 5 |
| Q5 의미 보존 평균 | -.- / 5 |
| Q6 톤 일치 평균 | -.- / 5 |
| Q5 ≤ 2 응답 (critical) | N (응답 ID: ...) |

### Week 2 (yyyy-mm-dd ~ yyyy-mm-dd)

(베타 운영 시작 후 채움)

### Week 3 (있을 시)

(필요 시 채움)

---

## 응답 raw 누적 (익명화 후)

각 응답을 다음 형식으로 추가:

```markdown
### [user-1] / 2026-mm-dd / blog / Mode A

- 만족도: 4 / 5
- 의미 보존: 5 / 5
- 톤 일치: 4 / 5
- 부족: "X 표현을 Y 로 바꿨는데 어색"
- 좋음: "Z 패턴 빼는 거 정확함"
- 사용 텍스트 공유: 부분 동의 — 첫 단락만
```

(베타 시작 후 누적)

---

## 발견 패턴 — 룰 미세 조정 후보

응답을 4 카테고리로 분류:

### 1. 누락 패턴

> 카탈로그에 없지만 자주 출현하는 AI 티 → 카탈로그 행 추가 (12 카테고리 freeze 안에서)

(누적)

### 2. 과교정

> 카탈로그가 잡지 말았어야 할 것을 잡음 → 빈도 high → med 조정 또는 자연스러움 컬럼 개선

(누적)

### 3. 도메인 톤 위반

> 도메인 디폴트가 raw 톤과 맞지 않음 → 부록 E 우선순위 조정 또는 카테고리 #9-A 보강

(누적)

### 4. Brand voice 한계

> Brand voice frontmatter / 톤 가이드의 부족함 → 4 번째 mode 보강 또는 보조 필드 추가

(누적)

---

## 룰 미세 조정 PR 계획

각 카테고리에서 우선순위 매겨 PR:

| Priority | 카테고리 | 변경 | freeze 영역 안? | 예상 PR |
|---|---|---|---|---|
| (Week 3 종료 시점에 채움) | | | | |

> **freeze 영역 (`docs/STABILITY-PROMISE.md`) 깨야 하는 변경**: v1.1 / v2 트랙으로 미루기. v1.0 은 *현재 룰* 의 안정화.

---

## v1.0 GA 후

이 문서는 v1.0 GA release 후:

- 응답 raw → archive (`docs/beta-feedback-archive-v1.0.md` 로 rename)
- 누적 통계 → README 또는 release notes 에 요약 인용 (베타 사용자 동의자만)
- v1.0 부터 30 일 폼 유지 — 자연 사용자 응답도 받음. 30 일 후 폼 닫고 v1.0.x / v1.1 의 데이터 베이스로 사용.

---

## 메인테이너용 — 응답 모니터링 일정

| 시점 | 작업 | 시간 |
|---|---|---|
| 매일 (베타 운영 동안) | 폼 응답 새 응답 체크 + Q5 ≤ 2 = critical 즉시 컨택 | 10 분 |
| Week 1 종료 | 익명화 후 이 문서 raw 섹션 누적 + 통계 갱신 | 30 분 |
| Week 2 종료 | 동일 + 발견 패턴 4 카테고리 분류 시작 | 1 시간 |
| Week 3 종료 (있을 시) | 룰 미세 조정 PR 계획표 채움 + 본인 review | 1.5 시간 |
| RC publish 직후 | 베타 사용자에게 RC 알림 + 1 주 confirmation 요청 | 30 분 |
| GA publish 직후 | README contributor 섹션 추가 + 감사 메시지 | 30 분 |

---

## 참고

- 폼 spec: [`docs/beta-feedback-form-spec.md`](beta-feedback-form-spec.md)
- 모집 글: [`docs/beta-recruit.md`](beta-recruit.md)
- 사용 가이드: [`docs/beta-guide.md`](beta-guide.md)
- 핸드오프 체크리스트: [`docs/v1.0-handoff.md`](v1.0-handoff.md)
- Freeze 영역: [`docs/STABILITY-PROMISE.md`](STABILITY-PROMISE.md)
