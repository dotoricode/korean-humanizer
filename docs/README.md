# 문서 안내

처음 사용한다면 [한국어 README](../README.ko.md)를 읽으세요. 아래 안내는 main의 개선 사항 기준이며 다음 버전 번호는 미정입니다. 마지막 출시 버전 v1.0.1의 규칙은 해당 태그와 [버전 정책과 과거 기록](STABILITY-PROMISE.md)에 남아 있습니다.

## 사용에 필요한 문서

| 목적 | 파일 |
|---|---|
| 스킬 지침 | [SKILL.md](../SKILL.md) |
| 설치 없이 사용 | [짧은 프롬프트](../PROMPT.short.md), [전체 프롬프트](../PROMPT.md) |
| 표현별 후보 | [패턴 카탈로그](../references/ko-ai-signals.md), [빠른 참고표](../CHEATSHEET.md) |
| 첫 편집 예시 | [실제 스킬 호출 비교](../eval/native-skill-2026-10-01.md), [첫 응답 3쌍](../examples/before-after.md) |
| 개인 설정 | [개인 목록 양식](../examples/personal-list.md) |
| 브랜드 설정 | [Brand voice 양식](../examples/brand-voice-template.md), [격식 낮은 제품 안내](../examples/brand-voice-toss-style.md), [에세이](../examples/brand-voice-essayist.md) |
| 도메인 참고 | [학술](../examples/domain-academic.md), [뉴스](../examples/domain-news.md), [채팅](../examples/domain-chat.md), [리뷰](../examples/domain-review.md), [B2B](../examples/domain-b2b-message.md), [GitHub Issue](../examples/domain-github-issue.md) |

도메인 예시는 과거 과교정 사례와 한계 설명을 포함합니다. 현재 규칙을 모두 통과하는 정답집으로 사용하지 마세요. 적용 기준은 `SKILL.md`와 카탈로그를 따릅니다.

## 개발·검증 자료

| 목적 | 파일 |
|---|---|
| 기여 규칙 | [CONTRIBUTING](../CONTRIBUTING.md), [에이전트 지침](../AGENTS.md) |
| 회귀 검사 | [평가 안내](../eval/README.md), [평가표](../eval/scorecard.md), `eval/fixtures/` |
| 실제 모델 비교 | [실제 스킬 호출: Opus 5.5·Astra](../eval/native-skill-2026-10-01.md) |
| 이번 QA 근거 | [2026-10-01 QA 기록](reviews/2026-10-01-qa.md) |
| 버전과 호환성 | [CHANGELOG](../CHANGELOG.md), [버전 정책](STABILITY-PROMISE.md), [변경 안내](UPGRADE-NOTES.md) |
| 남은 출시 작업 | [ROADMAP](../ROADMAP.md) |
| 보안·라이선스 | [SECURITY](../SECURITY.md), [LICENSE](../LICENSE) |

고정 평가 사례의 통과 수는 실제 모델의 출력 품질 성공률이 아닙니다. 수동 예시와 작은 실행 검사도 대규모 품질 평가와 구분합니다.

## 선택 자료와 과거 기록

- [연구 배경 초안](research/background.md): 출처 검토가 필요한 배경 자료이며 스킬 품질의 검증 결과가 아닙니다.
- [빈도 측정 계획](plans/frequency-evaluation.md): 샘플 수집 전 계획입니다. 현재 빈도 라벨은 휴리스틱입니다.
- [홍보 문구 기록](marketing/LAUNCH.md): 재사용 가능한 과거 출시 문구입니다. 현재 버전·효과는 따로 확인해야 합니다.
- [보관 문서](archive/README.md): 완료된 개발 계획·베타 안내·과거 비교 예시입니다.

배포 ZIP은 `python3 scripts/package-skill.py --output-dir <저장할 폴더>`로 생성합니다. `SKILL.md`, `LICENSE`, 구매자용 사용법, 프롬프트와 실행에 필요한 `references/`, `examples/`를 포함합니다. 보관 문서·연구 배경·개발 지침은 포함하지 않습니다. ZIP 설치와 첫 실행, 최신 9응답의 출력 형식을 확인했으며 작은 표본의 원본 기록은 `eval/model-runs/package-skill-2026-10-02.json`에 있습니다.
