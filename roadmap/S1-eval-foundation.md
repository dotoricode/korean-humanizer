# Sprint 1 — v0.6 Eval Foundation

> 자동 검증 layer 를 *형식* 에서 *내용* 으로 확장. 휴리스틱 기반, LLM 호출 없음, CI 무료.

| 항목 | 값 |
|---|---|
| 버전 | v0.5 → v0.6 |
| 기간 | 2 주 (10 working days) |
| 의존 | 없음 (시작 sprint) |
| 외부 의존 | 없음 |
| 위험도 | 낮음 |
| 다음 sprint | S2 도메인 추가가 이 eval-harness 를 통과해야 함 |

---

## Goal

`examples/*.md` 의 raw ↔ humanized 쌍이 SKILL.md 의 정량 룰 (20% cap, 단락 3 곳, 종결어미 톤 보존, 길이 압축률) 을 실제로 지키는지 자동 검증한다.

현재 lint 3 종 (`patterns` / `cross-file` / `examples`) 은 *형식* 만 본다. 이번 sprint 는 *내용 룰* 검증을 4 번째 layer 로 추가한다.

---

## Why

- **회귀 방지**: 누가 examples 에 6 번째 변경을 슬쩍 끼우거나, 발화체에 ~다체를 섞어도 사람 review 만으로는 놓칠 수 있다.
- **신뢰 신호**: contributor 가 PR 올리기 전 로컬에서 metric 점수를 보고 자기 검증할 수 있다.
- **v1.0 안정화 약속의 기반**: "20 % cap 을 지킨다" 는 우리 약속을 매 머지마다 자동으로 증명.

---

## Deliverables

| 산출물 | 경로 | 설명 |
|---|---|---|
| Eval harness 스크립트 | `scripts/eval-harness.sh` | 4 metric 자동 측정, fixture 단위로 pass/fail |
| Fixture 디렉토리 | `eval/fixtures/` | raw/humanized 쌍 20 개, JSON 또는 markdown |
| Fixture 추출기 | `scripts/extract-fixtures.sh` | examples/*.md 에서 fixture 자동 추출 |
| Scorecard | `eval/scorecard.md` | CI 가 매 머지마다 갱신, fixture 별 metric 점수 표 |
| 새 CI job | `.github/workflows/lint.yml` | `eval-harness` (hard-fail) 5 번째 job |

---

## Tasks

### 1. Fixture 형식 결정 + 입력 추출기 (1.5d)

- **결정**: fixture 는 markdown (raw + humanized 두 블록 포함). JSON 보다 사람이 읽기 쉽고, examples/ 와 호환.
- 형식 (`eval/fixtures/<domain>-<num>.md`):
  ```markdown
  ---
  domain: blog | marketing | email | linkedin | youtube | newsletter | wiki | academic | news | chat | review | b2b-message
  cap: 20  # 최대 수정 % (기본 20)
  paragraph_cap: 3  # 단락당 최대 변경 (기본 3)
  ---
  ## Raw
  [원문]
  ## Humanized
  [다듬어진 텍스트]
  ```
- 추출기: `scripts/extract-fixtures.sh examples/before-after.md` → `eval/fixtures/blog-1.md` 등.
- 기존 4 개 examples 의 형식 통일 (Before/After ↔ Raw/Humanized 정규화).

### 2. Metric 1 — 20 % cap 검증 (1d)

- 알고리즘:
  1. raw / humanized 각각 `[.!?。]` 기준 sentence-split (한국어 `.` `!` `?` 모두).
  2. 양쪽 sentence 를 line-by-line 으로 align (LCS 기반 Myers diff).
  3. modified sentence = 양쪽 sentence pair 의 normalized edit distance > 0.15.
  4. modified count / total raw sentence count → 0.20 이하면 pass.
- 출력: `pass / fail`, modified ratio 수치.

### 3. Metric 2 — 단락 3 곳 룰 (1d)

- 알고리즘:
  1. raw 의 단락(빈 줄 기준) 정렬.
  2. humanized 의 단락도 같은 수로 정렬 (단락 수 불일치면 warning).
  3. 단락별 modified sentence 수 카운트.
  4. 어느 단락이라도 > 3 이면 fail.
- 출력: 단락별 변경 수, max paragraph changes.

### 4. Metric 3 — 길이 압축률 (0.5d)

- 알고리즘: humanized char count / raw char count.
- pass: 0.5 ≤ ratio ≤ 1.05.
- warning: ratio > 1.05 (팽창 의심) 또는 ratio < 0.5 (over-correction 의심).
- fail: ratio > 1.20 또는 ratio < 0.30 (명백 룰 위반).

### 5. Metric 4 — 종결어미 톤 보존 (1.5d, 가장 어려움)

- 알고리즘:
  1. fixture frontmatter `domain` 읽기.
  2. 발화체 도메인 (`youtube` / `podcast` / `live` / `lecture`) 인 경우만 실행.
  3. humanized 텍스트에서 ~다체 글말체 종결 검출.
     - 패턴: 문장 끝 `~다.` `~ㄴ다.` `~한다.` `~된다.` `~였다.` `~겠다.`
     - 단, 발화체 raw 에서 이미 그 종결어미가 있었던 경우는 OK (raw 에서 해당 패턴이 1+ 출현 시 패스).
  4. 발화체에서 새로 ~다체 도입 시 fail.
- 휴리스틱 한계: 문장이 모호하면 false positive 가능 — 처음에는 warning 으로 두고 추후 fail 로 격상.

### 6. Fixture 큐레이션 (2d)

- 기존 examples 에서 추출 ~10 개:
  - before-after.md: 3 (블로그·마케팅·이메일)
  - agent-vs-skill.md: 6 (블로그·LinkedIn·이메일·마케팅·YouTube·뉴스레터)
  - long-form.md: 1 (장문 블로그)
- 신규 작성 ~10 개 (S2 의 도메인 일부 미리 cover):
  - 학술 초록 1, 뉴스 기사 1, 채팅·DM 2, 제품 리뷰 1, 카톡 비즈니스 1
  - 짧은 길이 edge case 2 (1-2 문장)
  - 장문 edge case 1 (장문에서 단락 3 곳 룰 boundary)
  - 발화체 톤 위반 trap 1 (일부러 ~다체 섞은 humanized — fail 시나리오)
- 합계 20 개.

### 7. Scorecard 생성기 (1d)

- `eval/scorecard.md` 자동 생성:
  ```markdown
  # Eval Scorecard (auto-generated)
  > Generated: <timestamp>
  ## Summary
  - Total fixtures: 20
  - All metrics pass: 19 (95.0 %)
  - Any metric fail: 1
  ## Per-fixture results
  | Fixture | Domain | M1 (20%) | M2 (3곳) | M3 (length) | M4 (tone) | Overall |
  ...
  ```
- CI artifact 로 업로드.

### 8. CI 통합 (0.5d)

- `.github/workflows/lint.yml` 에 5 번째 job 추가:
  ```yaml
  eval-harness:
    name: eval harness (must pass)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run eval harness
        run: bash scripts/eval-harness.sh
      - name: Upload scorecard
        uses: actions/upload-artifact@v4
        with:
          name: eval-scorecard
          path: eval/scorecard.md
  ```
- README CI 섹션 갱신 (5 jobs 명시).

### 9. 회귀 테스트 (0.5d)

- 4 시나리오 시연:
  1. fixture 일부러 21 % 변경으로 수정 → M1 fail
  2. 한 단락에 4 곳 변경 → M2 fail
  3. humanized 를 raw 보다 30 % 길게 → M3 fail
  4. YouTube fixture 에 ~다체 추가 → M4 fail
- 모두 자동 catch 되는지 확인 후 fixture 원복.

### 10. 문서·핸드오프 (0.5d)

- `CONTRIBUTING.md` PR 체크리스트에 "eval-harness 로컬 통과" 추가.
- `README.md` File Structure 에 `eval/`, `scripts/eval-harness.sh` 추가.
- ROADMAP.md S1 섹션 status 갱신.

---

## Acceptance criteria

- [ ] 20 개 fixture 모두 4 metric 통과 (or 의도적 trap 1 개는 metric fail 검증)
- [ ] 새 CI job `eval-harness` 가 hard-fail 로 동작
- [ ] `scripts/eval-harness.sh` 로컬 실행 시 scorecard 생성
- [ ] 회귀 시나리오 4 종 모두 잡힘
- [ ] 기존 lint 3 종 + 신규 1 종 = 총 4 hard-fail + 1 warning (markdownlint) job
- [ ] CONTRIBUTING.md / README.md 갱신
- [ ] v0.6 GitHub release tag

---

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| 한국어 sentence-tokenize 휴리스틱이 약함 (인용문·생략·`다음과 같다:` 등) | M1·M2 의 sentence-split 은 보수적 — 명백 종결만 분리. 인용문 안은 한 sentence 로 묶음. |
| 종결어미 분류 false positive | M4 는 처음에 warning, 1-2 sprint 사용 후 fail 격상 |
| Edit distance threshold (0.15) 가 부적절 | fixture 큐레이션 후 threshold 튜닝, 변경 사항은 PR 으로 명시 |
| Fixture 큐레이션 시간 over-run | 신규 10 개 중 어려운 4-5 개는 S2 로 미루기 OK |

---

## Out of scope (이번 sprint 안 함)

- LLM-as-judge 정성 평가 (다음 라운드 후보)
- 의미 보존 자동 검증 (사람 review 만)
- BLEU / ROUGE / BERTScore 같은 NLP metric (한국어 부적합)
- Brand voice 일관성 metric (S3 에서 재고)
- 도메인 weight 적용 metric (S3 catalog v2 후)

---

## Effort breakdown

| Task | 시간 |
|---|---|
| 1. Fixture 형식 + 추출기 | 1.5d |
| 2. M1 20% cap | 1d |
| 3. M2 3곳 룰 | 1d |
| 4. M3 길이 압축 | 0.5d |
| 5. M4 종결어미 톤 | 1.5d |
| 6. Fixture 큐레이션 (20 개) | 2d |
| 7. Scorecard 생성기 | 1d |
| 8. CI 통합 | 0.5d |
| 9. 회귀 테스트 | 0.5d |
| 10. 문서·핸드오프 | 0.5d |
| **합계** | **10d (2 주)** |

Buffer 0.5-1d 권장.
