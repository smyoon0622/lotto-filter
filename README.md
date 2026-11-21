# 로또 베이스 필터 생성기 (웹 배포판 1.0.0)

브라우저에서 동작하는 정적 웹앱입니다. 서버 프로그램이 필요 없고, 이 폴더를 그대로 웹 호스팅에 올리면 됩니다.

## 폴더 구성
- `index.html` : 앱 본체
- `lib/` : QR코드·숫자인식 모듈 — 큰 파일(jsQR, tesseract)은 저장소에 없고 배포할 때 GitHub Actions가 받아서 넣음 (오프라인 동작)
- `data/draws.json` : 회차별 당첨번호 (매주 갱신)
- `version.json` : 현재 배포 버전 — 바꾸면 사용자에게 "새 버전" 알림
- `sw.js`, `manifest.webmanifest`, `icons/` : 설치형 앱(PWA)·오프라인용
- `.github/workflows/deploy.yml` : 올릴 때마다 GitHub Pages로 자동 배포 + 매주 토/일 `scripts/update_draws.py`로 당첨번호 자동 추가 후 재배포

## 새 버전 올리는 법
1. 파일을 새 것으로 교체
2. `version.json`의 version과 `sw.js`의 VERSION, `index.html`의 APP_VERSION을 같은 새 값으로 변경 (빌드 스크립트가 자동으로 맞춤)
3. 업로드하면 사용자가 다음에 열 때 "업데이트" 알림이 뜸

## 사용자 데이터
입력값·설정은 각 사용자 브라우저에 저장됩니다. 1단계의 "설정 백업 / 설정 불러오기"로 옮길 수 있습니다.
