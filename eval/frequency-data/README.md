# Frequency Data — 카탈로그 빈도 재라벨링용 LLM 출력 샘플

> v0.8 카탈로그 v2 의 **빈도** 컬럼을 데이터 기반으로 재라벨링하기 위한 raw LLM 출력 보관소.
>
> 이 디렉토리의 데이터는 빈도 라벨 (high / med / low) 의 근거가 된다. 재현·재라벨링 시 이 스키마를 그대로 사용한다.

## 현재 상태

- v0.8 (S3 첫 패스): **샘플 수집 미완료**. 카탈로그의 빈도 라벨은 **휴리스틱 기반 v1** 유지.
- 후속 sub-PR (v0.8.1 또는 v0.9 후보): 90 샘플 수집 → 137 패턴 빈도 카운팅 → 라벨 재산정 → 카탈로그 PR.

이 디렉토리는 **스키마와 방법론을 먼저 고정** 하고 데이터 수집만 후속 PR 로 분리하기 위한 자리.

## 방법론 (S3 spec 의 task 2D)

### 1. 데이터 수집 (목표 90 샘플)

| 차원 | 값 |
|---|---|
| 모델 | Claude Sonnet 4.6 / GPT-5 / Gemini 2.5 Pro (또는 그 시점의 동급 모델 3 종) |
| 프롬프트 도메인 | blog / marketing / email / linkedin / newsletter / b2b-message (6 도메인) |
| 도메인당 프롬프트 | 5 개 (총 30 프롬프트) |
| 샘플 = 모델 × 프롬프트 | 3 × 30 = **90 샘플** |
| 출력 길이 | 도메인 자연 길이 (블로그 500 자 / 이메일 200 자 / LinkedIn 300 자 등) |

**프롬프트 작성 룰** (humanizer 의식 없이 평소 한국어 출력 유도):

- 한국어 자연어로 task 만 명시 ("X 주제로 블로그 글 한 편 써줘")
- "AI 티 없이" / "자연스럽게" 같은 humanizer 지시어 **금지** — 평소 출력이 baseline
- 같은 도메인 내 5 프롬프트는 주제 다양화 (시간관리 / 기술 / 마케팅 / 라이프스타일 / 비즈니스 등)

**파일 구조**:

```
eval/frequency-data/
├── prompts.md              # 30 프롬프트 전문
├── claude-sonnet-4-6/
│   ├── blog-01.md          # raw output (수정 없음)
│   ├── blog-02.md
│   ├── ...
│   └── b2b-05.md
├── gpt-5/
│   └── (동일)
└── gemini-2-5-pro/
    └── (동일)
```

### 2. 빈도 측정

`scripts/count-frequencies.py` (v0.8.1 sub-PR 에서 작성 예정):

- 카탈로그의 137 패턴 각각에 대해 90 샘플에서 출현 횟수 카운트
- 각 패턴은 정규식 또는 fixed-string match
- 출현률 = 출현 sample 수 / 90 (0.0 ~ 1.0)

**빈도 라벨 기준** (data-driven cutoff):

| 라벨 | 출현률 | 의미 |
|---|---|---|
| `high` | ≥ 0.30 | 90 샘플 중 27 개 이상 |
| `med` | 0.05 ~ 0.30 | 90 샘플 중 5-27 개 |
| `low` | < 0.05 | 90 샘플 중 5 개 미만 |

### 3. 재라벨링

- 현재 카탈로그의 빈도 라벨과 데이터 기반 라벨 비교
- 차이가 있으면 데이터 라벨로 갱신
- 일부 휴리스틱 한 라벨은 **보수적으로** 유지 (예: 전문가 관찰로 high 였지만 90 샘플에서 med 으로 측정된 경우, 도메인 / 모델 편향 가능성 고려)
- 변동 사유는 카탈로그 PR 본문에 명시 — 모든 라벨 변동에 데이터 출처 (sample count) 표기

## 무엇이 이 디렉토리에 들어가는가

- `prompts.md` — 30 프롬프트 (도메인 × 5 개)
- `<model>/<domain>-<NN>.md` — 90 raw output (frontmatter 메타데이터: model, domain, prompt_id, generated_at)
- `frequency-counts.json` — 137 패턴 × 90 샘플 매트릭스 (count-frequencies.py 산출)
- `relabel-diff.md` — 카탈로그 빈도 변동 (이전 라벨 vs 데이터 라벨, 사유)

## 무엇이 안 들어가는가

- humanize 적용된 출력 → `eval/fixtures/` 가 그 자리
- 평가 메트릭 (M1-M4) → `scripts/eval-harness.py` + `scorecard.md`
- 137 패턴 표 자체 → `references/ko-ai-signals.md`

## 윤리·라이선스

- 90 샘플은 **공개 LLM API 의 자연 출력** — 사용자 데이터 / PII 없음
- 모델 ToS 가 학술·연구 목적 사용을 허용한다는 가정 (Claude / GPT / Gemini 모두 ToS 검토 후 사용)
- 샘플은 git 에 commit (gitignore 안 함) — 재현성 확보
- 외부 PR 로 데이터를 추가하려면 **공개 API 출력 + 같은 프롬프트 형식** 으로만. 사용자 글 sampling 금지.

## v0.8.1+ 로드맵

이 디렉토리에서 후속 sub-PR 로 풀어낼 작업:

- [ ] 30 프롬프트 작성 (`prompts.md`)
- [ ] 90 샘플 수집 (수동 또는 batch API)
- [ ] `count-frequencies.py` 작성
- [ ] 137 패턴 빈도 측정 + JSON 산출
- [ ] 카탈로그 빈도 컬럼 재라벨링 PR
- [ ] (선택) 빈도 변동 추세 분석 — 모델 / 도메인 / 시간에 따른 변화

이 작업은 v0.8 의 카탈로그 v2 4 컬럼 구조 위에 얹히는 형태이므로 **v0.8 다음 minor sub-PR** 로 분리. v1.0 freeze 약속 (S4) 에는 영향 없음.
