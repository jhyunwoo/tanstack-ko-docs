# Astro 스타터 키트: 최소

```sh
npm create astro@latest -- --template minimal
```
[![StackBlitz에서 열기](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/withastro/astro/tree/latest/examples/minimal)
[![CodeSandbox로 열기](https://assets.codesandbox.io/github/button-edit-lime.svg)](https://codesandbox.io/p/sandbox/github/withastro/astro/tree/latest/examples/minimal)
[![GitHub Codespaces에서 열기](https://github.com/codespaces/badge.svg)](https://codespaces.new/withastro/astro?devcontainer_path=.devcontainer/minimal/devcontainer.json)

> 🧑‍🚀 **노련한 우주비행사?** 이 파일을 삭제하세요. 재미있게 보내세요!

## 🚀 프로젝트 구조

Astro 프로젝트 내부에는 다음 폴더와 파일이 표시됩니다.

```text
/
├── public/
├── src/
│   └── pages/
│       └── index.astro
└── package.json
```
Astro는 `src/pages/` 디렉터리에서 `.astro` 또는 `.md` 파일을 찾습니다. 각 페이지는 파일 이름을 기반으로 경로로 노출됩니다.

`src/components/`에는 특별한 것이 없지만 Astro/React/Vue/Svelte/Preact 구성 요소를 여기에 배치하고 싶습니다.

이미지와 같은 모든 정적 자산은 `public/` 디렉터리에 배치될 수 있습니다.

## 🧞 명령

모든 명령은 프로젝트 루트, 터미널에서 실행됩니다.

|명령|행동|
| :------------------------ | :----------------------------------------------- |
|`npm install`|종속성을 설치합니다.|
|`npm run dev`|`localhost:4321`에서 로컬 개발 서버를 시작합니다.|
|`npm run build`|생산 사이트를 `./dist/`로 구축하세요|
|`npm run preview`|배포하기 전에 로컬에서 빌드 미리보기|
|`npm run astro ...`|`astro add`, `astro check`와 같은 CLI 명령을 실행합니다.|
|`npm run astro -- --help`|Astro CLI를 사용하여 도움 받기|

## 🙌 더 자세히 알고 싶으세요?

[문서](https://docs.astro.build)를 확인하거나 [Discord 서버](https://astro.build/chat)로 이동하세요.