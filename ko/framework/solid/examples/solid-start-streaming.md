# SolidStart

[`solid-start`](https://start.solidjs.com)를 기반으로 Solid 프로젝트를 구축하는 데 필요한 모든 것;

## 프로젝트 생성

```bash
# 현재 디렉터리에 새 프로젝트를 만듭니다.
npm init solid@latest

# 내 앱에서 새 프로젝트 만들기
npm init solid@latest my-app
```
## 개발 중

프로젝트를 생성하고 `npm install`(또는 `pnpm install` 또는 `yarn`)를 사용하여 종속성을 설치한 후 개발 서버를 시작합니다.

```bash
npm run dev

# 또는 서버를 시작하고 새 브라우저 탭에서 앱을 엽니다.
npm run dev -- --open
```
## 건물

견고한 앱은 다양한 환경에 배포하기 위해 프로젝트를 최적화하는 _presets_로 구축되었습니다.

기본적으로 `npm run build`는 `npm start`로 실행할 수 있는 노드 앱을 생성합니다. 다른 사전 설정을 사용하려면 `package.json`의 `devDependencies`에 추가하고 `app.config.js`에 지정하세요.

## 이 프로젝트는 [Solid CLI](https://solid-cli.netlify.app)를 사용하여 생성되었습니다.