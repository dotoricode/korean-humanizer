[README.md](README.md)를 해요체와 Nimbus 명칭에 맞춰 개선했어요. 준비 사항, 실행 위치, 명령, 예상 출력 순서로 안내하고 오프라인 지원은 향후 계획으로 유지했어요.

프로젝트 루트에서 `npm run preview`를 실행해 `Nimbus preview` 출력과 정상 종료를 확인했어요. README.md만 수정했어요.

| 구분 | 수정·보충한 사실 | 근거 |
| --- | --- | --- |
| 수정 | `npm run start` → `npm run preview` | [package.json](package.json:4)의 `scripts.preview` |
| 보충 | 의존성 설치 불필요, 프로젝트 루트에서 실행 | [사용 안내](docs/usage.md:3) |
| 보충 | 예상 출력과 실행 후 종료 | [preview.cjs](preview.cjs:1), 실제 실행 결과 |