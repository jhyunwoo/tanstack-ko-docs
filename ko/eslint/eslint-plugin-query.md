---
id: eslint-plugin-query
title: ESLint 플러그인 Query
---




TanStack Query에는 자체 ESLint 플러그인이 함께 제공됩니다. 이 플러그인은 모범 사례를 적용하고 일반적인 실수를 방지하는 데 사용됩니다.

## 설치

플러그인은 설치해야 하는 별도의 패키지입니다.

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
## 플랫 구성(`eslint.config.js`)

### 권장 설정

플러그인에 권장되는 모든 규칙을 활성화하려면 다음 구성을 추가하세요.

```js
import pluginQuery from '@tanstack/eslint-plugin-query'

export default [
  ...pluginQuery.configs['flat/recommended'],
  // 다른 구성은...
]
```
### 맞춤 설정

또는 플러그인을 로드하고 사용하려는 규칙만 구성할 수 있습니다.

```js
import pluginQuery from '@tanstack/eslint-plugin-query'

export default [
  {
    plugins: {
      '@tanstack/query': pluginQuery,
    },
    rules: {
      '@tanstack/query/exhaustive-deps': 'error',
    },
  },
  // 다른 구성은...
]
```
## 레거시 구성(`.eslintrc`)

### 권장 설정

플러그인에 권장되는 모든 규칙을 활성화하려면 확장에 `plugin:@tanstack/query/recommended`를 추가하세요.

```json
{
  "extends": ["plugin:@tanstack/query/recommended"]
}
```
### 맞춤 설정

또는 플러그인 섹션에 `@tanstack/query`를 추가하고 사용하려는 규칙을 구성합니다.

```json
{
  "plugins": ["@tanstack/query"],
  "rules": {
    "@tanstack/query/exhaustive-deps": "error"
  }
}
```
## 규칙

- [@tanstack/query/exhaustive-deps](exhaustive-deps.md)
- [@tanstack/query/no-rest-destructuring](no-rest-destructuring.md)
- [@tanstack/query/stable-query-클라이언트](stable-query-client.md)
- [@tanstack/query/no-unstable-deps](no-unstable-deps.md)
- [@tanstack/query/infinite-query-속성-순서](infinite-query-property-order.md)
- [@tanstack/query/no-void-query-fn](no-void-query-fn.md)
- [Ensure correct order of inference-sensitive properties in useMutation()](mutation-property-order.md)