# create-svelte

[`create-svelte`](https://github.com/sveltejs/kit/tree/master/packages/create-svelte)를 기반으로 Svelte 프로젝트를 빌드하는 데 필요한 모든 것입니다.

## 프로젝트 생성

이 내용이 표시된다면 아마도 이미 이 단계를 완료했을 것입니다. 축하해요!

```bash
# 현재 디렉터리에 새 프로젝트를 만듭니다.
npm create svelte@latest

# 내 앱에서 새 프로젝트 만들기
npm create svelte@latest my-app
```
## 개발 중

프로젝트를 생성하고 `npm install`(또는 `pnpm install`, `yarn` 또는 `bun install`)를 사용하여 종속성을 설치한 후 개발 서버를 시작합니다.

```bash
npm run dev

# 또는 서버를 시작하고 새 브라우저 탭에서 앱을 엽니다.
npm run dev -- --open
```
## 건물

앱의 프로덕션 버전을 만들려면 다음 안내를 따르세요.

```bash
npm run build
```
`npm run preview`를 사용하여 프로덕션 빌드를 미리 볼 수 있습니다.

> 앱을 배포하려면 대상 환경에 맞는 [어댑터](https://kit.svelte.dev/docs/adapters)를 설치해야 할 수도 있습니다.