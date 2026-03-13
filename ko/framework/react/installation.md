---
id: installation
title: 설치
---

[NPM](https://npmjs.com/)을 통해 React Query를 설치할 수 있습니다.
아니면 좋은 `<script>`를 통해
[ESM.sh](https://esm.sh/).

### NPM

```bash
npm i @tanstack/react-query
```
또는

```bash
pnpm add @tanstack/react-query
```
또는

```bash
yarn add @tanstack/react-query
```
또는

```bash
bun add @tanstack/react-query
```
[//]: # 'Compatibility'

React Query는 React v18+와 호환되며 ReactDOM 및 React Native와 함께 작동합니다.

> 다운로드하기 전에 한번 사용해 보고 싶으신가요? [간단](examples/simple.md) 또는 [기본](examples/basic.md) 예시를 사용해 보세요!

[//]: # 'Compatibility'

### CDN

모듈 번들러나 패키지 관리자를 사용하지 않는 경우 [ESM.sh](https://esm.sh/)와 같은 ESM 호환 CDN을 통해 이 라이브러리를 사용할 수도 있습니다. HTML 파일 하단에 `<script type="module">` 태그를 추가하기만 하면 됩니다.

[//]: # 'CDNExample'

```html
<script type="module">
  import React from 'https://esm.sh/react@18.2.0'
  import ReactDOM from 'https://esm.sh/react-dom@18.2.0'
  import { QueryClient } from 'https://esm.sh/@tanstack/react-query'
</script>
```
> JSX 없이 React를 사용하는 방법은 [여기](https://react.dev/reference/react/createElement#creating-an-element-without-jsx)에서 확인할 수 있습니다.

[//]: # 'CDNExample'

### 요구사항

React Query는 최신 브라우저에 최적화되어 있습니다. 다음 브라우저 구성과 호환됩니다.

```
Chrome >= 91
Firefox >= 90
Edge >= 91
Safari >= 15
iOS >= 15
Opera >= 77
```
> 환경에 따라 폴리필을 추가해야 할 수도 있습니다. 이전 브라우저를 지원하려면 `node_modules`에서 라이브러리를 직접 트랜스파일해야 합니다.

### 권장 사항

코딩하는 동안 버그와 불일치를 잡는 데 도움이 되도록 [ESLint 플러그인 Query](../../eslint/eslint-plugin-query.md)을 사용하는 것이 좋습니다. 다음을 통해 설치할 수 있습니다.

```bash
npm i -D @tanstack/eslint-plugin-query
```
또는

```bash
pnpm add -D @tanstack/eslint-plugin-query
```
또는

```bash
yarn add -D @tanstack/eslint-plugin-query
```
또는

```bash
bun add -D @tanstack/eslint-plugin-query
```
