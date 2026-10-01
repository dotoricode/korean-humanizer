# 문서 안내

처음 사용한다면 [한국어 README](../README.ko.md)를 읽으세요. 아래 안내는 미출시 2.0 준비 변경 기준입니다. 마지막 출시 버전 v1.0.1의 규칙은 해당 태그와 [1.x 호환성 약속](STABILITY-PROMISE.md)에 남아 있습니다.

## 사용에 필요한 문서

| 목적 | 파일 |
|---|---|
| 스킬 지침 | [SKILL.md](../SKILL.md) |
| 설치 없이 사용 | [짧은 프롬프트](../PROMPT.short.md), [전체 프롬프트](../PROMPT.md) |
| 표현별 후보 | [패턴 카탈로그](../references/ko-ai-signals.md), [빠른 참고표](../CHEATSHEET.md) |
| 첫 편집 예시 | [실제 모델 출력 비교](../eval/emoji-and-flow-2026-10-01.md), [과거 수동 편집 3쌍](../examples/before-after.md) |
| 개인 설정 | [개인 목록 양식](../examples/personal-list.md) |
| 브랜드 설정 | [Brand voice 양식](../examples/brand-voice-template.md), [격식 낮은 제품 안내](../examples/brand-voice-toss-style.md), [에세이](../examples/brand-voice-essayist.md) |
| 도메인 참고 | [학술](../examples/domain-academic.md), [뉴스](../examples/domain-news.md), [채팅](../examples/domain-chat.md), [리뷰](../examples/domain-review.md), [B2B](../examples/domain-b2b-message.md), [GitHub Issue](../examples/domain-github-issue.md) |

도메인 예시는 과거 과교정 사례와 한계 설명을 포함합니다. 현재 규칙을 모두 통과하는 정답집으로 사용하지 마세요. 적용 기준은 `SKILL.md`와 카탈로그를 따릅니다.

## 개발·검증 자료

| 목적 | 파일 |
|---|---|
| 기여 규칙 | [CONTRIBUTING](../CONTRIBUTING.md), [에이전트 지침](../AGENTS.md) |
| 회귀 검사 | [평가 안내](../eval/README.md), [평가표](../eval/scorecard.md), `eval/fixtures/` |
| 실제 모델 비교 | [README 예시: Opus 5.5·Astra](../eval/emoji-and-flow-2026-10-01.md) |
| 이번 QA 근거 | [2026-10-01 QA 기록](reviews/2026-10-01-qa.md) |
| 버전과 호환성 | [CHANGELOG](../CHANGELOG.md), [1.x 약속](STABILITY-PROMISE.md), [2.0 마이그레이션 준비](MIGRATION-1.x-to-2.x.md) |
| 남은 출시 작업 | [ROADMAP](../ROADMAP.md) |
| 보안·라이선스 | [SECURITY](../SECURITY.md), [LICENSE](../LICENSE) |

고정 평가 사례의 통과 수는 실제 모델의 출력 품질 성공률이 아닙니다. 수동 예시와 작은 실행 검사도 대규모 품질 평가와 구분합니다.

## 선택 자료와 과거 기록

- [연구 배경 초안](research/background.md): 출처 검토가 필요한 배경 자료이며 스킬 품질의 검증 결과가 아닙니다.
- [빈도 측정 계획](plans/frequency-evaluation.md): 샘플 수집 전 계획입니다. 현재 빈도 라벨은 휴리스틱입니다.
- [홍보 문구 기록](marketing/LAUNCH.md): 재사용 가능한 과거 출시 문구입니다. 현재 버전·효과는 따로 확인해야 합니다.
- [보관 문서](archive/README.md): 완료된 개발 계획·베타 안내·과거 비교 예시입니다.

배포 ZIP에는 `SKILL.md`, `LICENSE`, 간단한 사용법과 스킬이 참조하는 `references/`, `examples/`만 포함하는 방향으로 준비합니다. 보관 문서·연구 배경·개발 지침은 실행에 필요하지 않습니다. ZIP 제작과 새 설치 검증은 아직 남아 있습니다.
