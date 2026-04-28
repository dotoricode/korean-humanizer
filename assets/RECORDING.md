# 데모 GIF 녹화 가이드 (30초)

`assets/demo.gif` 를 만들어 푸시하면 README hero 에 자동으로 노출된다. 두 가지 방법 — 본인 환경에 맞춰 고른다.

## 결과물 사양

- 위치: `assets/demo.gif`
- 길이: 20 ~ 30 초 권장 (60 초 넘으면 GitHub 에서 표시가 늦어짐)
- 가로 폭: 800 ~ 1200 px (모바일 + 데스크톱 모두 OK)
- 용량: 5 MB 이하 권장 (GitHub raw 표시 한도 100 MB 이지만 README 미리보기 속도 위해)
- 내용: Claude Code 또는 Cursor 등에서 raw 한국어 텍스트를 붙여넣고 humanize 결과가 나오는 모습. 가장 강력한 한 컷은 "안녕하세요! 오늘은 매우 중요한..." 류 입력 → 자연스러운 한 줄 변환.

녹화 후 README 상단의 다음 줄을 주석 해제한다 (`<!--` `-->` 제거):

```markdown
<!-- ![korean-humanizer 데모: raw → humanized 변환 (30초)](assets/demo.gif) -->
```

## 방법 A. macOS — 화면 녹화 → ffmpeg gif 변환 (가장 빠름)

1. **녹화**: `Cmd + Shift + 5` → "선택 영역 기록" → 터미널 / 에디터 영역만 잡기 → 녹화 → 저장 (`~/Desktop/recording.mov`).
2. **gif 변환** (Homebrew 의 ffmpeg 필요):

   ```bash
   ffmpeg -i ~/Desktop/recording.mov \
     -vf "fps=12,scale=1000:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
     -loop 0 \
     assets/demo.gif
   ```

3. **용량 확인** — `du -h assets/demo.gif`. 5 MB 넘으면 `fps=10` 또는 `scale=900:-1` 로 다시 변환.

ffmpeg 설치: `brew install ffmpeg`.

## 방법 B. asciinema → svg-term-cli (텍스트 기반, 가볍고 선명)

CLI 만 보여줄 거라면 SVG 가 GIF 보다 가볍고 검색 친화적이다. 단 GitHub README 는 SVG 애니메이션을 일부 차단하므로 결과를 GIF 로 한 번 더 변환하는 게 안전하다.

```bash
# 설치
brew install asciinema
npm i -g svg-term-cli

# 녹화 (Ctrl+D 로 종료)
asciinema rec demo.cast --idle-time-limit 1 --max-time 35

# SVG 로 변환
svg-term --in demo.cast --out demo.svg --window --width 100 --height 24

# (선택) SVG → GIF 변환 (cairosvg + ffmpeg 등 필요)
# 또는 단순히 demo.svg 를 그대로 README 에 ![](demo.svg) 로 박아도 됨 (정적 SVG 표시)
```

## 방법 C. Claude Code 에서 바로 녹화 (간단함)

1. 터미널 폰트 키우기 (`Cmd + +` 두세 번) — 작은 화면에서도 가독성 확보.
2. Claude Code 실행 후 `/korean-humanizer` 입력하고 raw 텍스트 한 단락 붙여넣기.
3. 응답이 나올 때까지 한 컷, "주요 변경" 까지 한 컷 — 두 컷 정도가 효과적.
4. `Cmd + Shift + 5` 로 위 방법 A 와 동일하게 녹화 → ffmpeg 변환.

## 콘텐츠 팁

- 시작 화면에 `/korean-humanizer` 명령이 보이면 호기심 자극.
- 입력 텍스트는 12 카테고리 패턴이 잘 보이는 short 한 단락 (`예: examples/before-after.md` 의 첫 사례).
- 결과 화면에서 "주요 변경 (최대 5개)" 가 보이면 skill 의 가치 제안이 한눈에 들어온다.
- 마지막 1 ~ 2 초는 humanized 결과가 화면에 머무르게 정지 (다음 입력 안 함).

## 푸시

```bash
git add assets/demo.gif
git commit -m "feat: README 데모 GIF 추가"
git push origin main
```

푸시 후 README 상단의 placeholder 주석을 해제하는 PR 1 줄 추가까지 하면 끝.

## 트러블슈팅

- **GIF 가 GitHub README 에서 안 움직임**: 파일 크기가 너무 커서 GitHub 가 정적 첫 프레임만 보여주는 경우. 5 MB 이하로 압축.
- **선명도가 흐림**: ffmpeg 의 `scale` 너비를 1200 으로 올리거나 `palettegen` 옵션을 위 명령처럼 정확히 사용.
- **모바일에서 잘림**: 가로 폭을 1000 px 이하로.
