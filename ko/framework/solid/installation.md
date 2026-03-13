---
id: installation
title: 설치
---




[NPM](https://npmjs.com/)을 통해 Solid Query를 설치할 수 있습니다.
아니면 좋은 `<script>`를 통해
[ESM.sh](https://esm.sh/).

### NPM

```bash
npm i @tanstack/solid-query
```
또는

```bash
pnpm add @tanstack/solid-query
```
또는

```bash
yarn add @tanstack/solid-query
```
또는

```bash
bun add @tanstack/solid-query
```
> 다운로드하기 전에 한번 사용해 보고 싶으신가요? [단순](examples/simple.md) 또는 [기본](examples/basic.md) 예제를 사용해 보세요!

### CDN

모듈 번들러나 패키지 관리자를 사용하지 않는 경우 [ESM.sh](https://esm.sh/)와 같은 ESM 호환 CDN을 통해 이 라이브러리를 사용할 수도 있습니다. HTML 파일 하단에 `<script type="module">` 태그를 추가하기만 하면 됩니다.

```html
<script type="module">
  import { QueryClient } from 'https://esm.sh/@tanstack/solid-query'
</script>
```
### 요구사항

Solid Query는 최신 브라우저에 최적화되어 있습니다. 다음 브라우저 구성과 호환됩니다.

```
Chrome >= 91
Firefox >= 90
Edge >= 91
Safari >= 15
iOS >= 15
Opera >= 77
```
> 환경에 따라 폴리필을 추가해야 할 수도 있습니다. 이전 브라우저를 지원하려면 `node_modules`에서 라이브러리를 직접 트랜스파일해야 합니다.