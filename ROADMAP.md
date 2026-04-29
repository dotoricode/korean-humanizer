# Roadmap — korean-humanizer

> v0.5 (현재) → **v1.0.0** 까지 4 sprint 로 가는 길.
>
> 한국어 전용. [다국어 확장은 영구 out-of-scope](roadmap/S3-brand-voice-catalog-v2.md#out-of-scope).

---

## 한눈에 보기

| Sprint | Version | 기간 | 테마 | 상세 |
|---|---|---|---|---|
| **S1** | v0.5 → v0.6 | 2 주 | Eval foundation — 휴리스틱 자동 검증 | [S1-eval-foundation.md](roadmap/S1-eval-foundation.md) |
| **S2** | v0.6 → v0.7 | 2 주 | Domain v2 — 5 신규 도메인 | [S2-domain-coverage-v2.md](roadmap/S2-domain-coverage-v2.md) |
| **S3** | v0.7 → v0.8 | 3 주 | Brand voice + Catalog v2 | [S3-brand-voice-catalog-v2.md](roadmap/S3-brand-voice-catalog-v2.md) |
| **S4** | v0.8 → **v1.0.0** | 3 주 | Stabilization + 베타 + Polish | [S4-v1.0.0-stabilization.md](roadmap/S4-v1.0.0-stabilization.md) |

**총 10 주** (공격적) / **14 주** (현실적, +1 주 buffer per sprint).

---

## 각 sprint 가 풀어내는 문제

### S1 — Eval Foundation

> **문제**: 현재 lint 3 종은 *형식* 만 본다. examples 가 실제로 20 % cap·3 곳 룰을 지키는지 자동 검증이 없다.
>
> **해결**: 휴리스틱 4 metric (20 % cap / 단락 3 곳 / 길이 압축률 / 종결어미 톤) + 20 fixture + scorecard + CI 5 번째 job.

### S2 — Domain Coverage v2

> **문제**: 7 도메인 (블로그·마케팅·이메일·LinkedIn·YouTube·뉴스레터·위키) 만 cover. 한국 사용자가 자주 쓰는 학술·뉴스·채팅·리뷰·B2B 메시지 사례 없음.
>
> **해결**: 5 신규 도메인 사례 + 카탈로그 부록 E (도메인별 카테고리 우선순위).

### S3 — Brand Voice + Catalog v2

> **문제 1**: humanize 결과가 평범한 한국어 톤만. 사용자 *브랜드 톤* (Toss 풍·작가 X 톤) 으로 다듬을 길 없음.
>
> **문제 2**: "활용" 같은 패턴이 마케팅·학술에서 다른 가중치인데 카탈로그가 동일 처리.
>
> **해결**: Personal list 4 번째 mode (brand voice profile) + 카탈로그 4 컬럼 확장 (`나쁨 / 자연스러움 / 빈도 / 적용 도메인`) + 빈도 데이터 기반 재라벨링.

### S4 — v1.0.0 Stabilization

> **문제**: v0.x 는 "변할 수 있다" 신호. 사용자·contributor 가 의존하기 어렵다.
>
> **해결**: SemVer 약속 (12 카테고리 / SKILL 출력 포맷 / 정량 규칙 / PROMPT.md API freeze) + 베타 3-5 명 1-2 주 검증 + CHANGELOG / SECURITY / MIGRATION / README v1.0 hero.

---

## 의존성 그래프

```
S1 (eval) ──┬──> S2 (도메인) ──> S3 (brand + catalog v2) ──> S4 (v1.0)
            └─────────────────────────────────────────────────^
                       (S1 의 fixture 가 S4 까지 계속 grow)
```

- S1 의 eval-harness 는 S2-S4 모든 신규 examples 가 통과해야 함.
- S2 의 도메인 셋은 S3 카탈로그 v2 의 도메인 컬럼 값을 결정.
- S3 의 카탈로그 v2 / brand voice 는 S4 의 freeze 약속 대상.

---

## 외부 의존도

| Sprint | 외부 의존 | Blocker 위험 |
|---|---|---|
| S1 | 없음 | 낮음 |
| S2 | 없음 | 낮음 |
| S3 | 없음 (가상 brand 케이스) | 중간 (137 행 재라벨링 시간) |
| S4 | **베타 사용자 3-5 명 모집** | **높음** |

S4 가 가장 큰 변수. 모집 더디면 **v1.0.0-rc** 분리 출시 후 1.0.1 에서 베타 피드백 반영.

---

## 의도적으로 안 함 (영구 out-of-scope)

- **다국어 확장** (일본어·중국어 등). 한국어 전용 유지.
- 다른 언어용 humanizer 가 필요하면 별도 레포로.
- 카탈로그 / 디렉토리 구조의 다언어 일반화도 안 함.

## v1.0 이후 후속 후보 (1.x 마이너)

이번 로드맵 스프린트에서 *의도적으로 뺀* 항목 — v1.0 release 후 별도 트랙으로 검토:

- **LLM-as-judge eval** — 정성 자연스러움 / 의미 보존 자동 평가
- **Batch / API mode** — 다수 텍스트 일괄 humanize
- **Brand voice 자동 추출** — 사용자 글 샘플에서 brand voice profile 자동 생성
- **사용자 만족도 정량 측정** — A/B test, NPS 등
- **X·Threads / 강의 소개 도메인** — S2 에서 미룬 도메인
- **카테고리 #13+ 후보** — 실 사용 데이터로 새 패턴 군 발견 시 (major bump 동반)

---

## 진행 상태

| Sprint | Status | Date |
|---|---|---|
| v0.5 (이전 sprint) | ✓ 완료 | 2026-04-29 |
| **S1 v0.6** | 대기 | - |
| **S2 v0.7** | 대기 | - |
| **S3 v0.8** | 대기 | - |
| **S4 v1.0.0** | 대기 | - |

---

## 참고

- 각 sprint 상세는 [`roadmap/`](roadmap/) 디렉토리.
- v0.5 까지의 history: [README Version History](README.md#version-history).
- 현재 안정화 정책 (v1.0 부터 적용): [`docs/STABILITY-PROMISE.md`](docs/STABILITY-PROMISE.md) — S4 에서 작성.

---

## 이 ROADMAP 사용법

- **사용자**: 어느 sprint 에 어떤 기능이 들어오는지 미리 파악. v1.0 freeze 영역 확인.
- **Contributor**: 어느 sprint 에 자기 PR 이 적합한지 확인. PR 본문에 `Closes ROADMAP S2 task 4` 같이 link.
- **Maintainer**: 매 sprint 시작 시 해당 sprint 상세 문서 열고, task 별 in-progress / completed 표시. ROADMAP.md 의 status 표 갱신.
