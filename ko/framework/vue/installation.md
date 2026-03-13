---
id: installation
title: 설치
---




[NPM](https://npmjs.com)을 통해 Vue Query를 설치할 수 있습니다.

### NPM

```bash
npm i @tanstack/vue-query
```
또는

```bash
pnpm add @tanstack/vue-query
```
또는

```bash
yarn add @tanstack/vue-query
```
또는

```bash
bun add @tanstack/vue-query
```
> 다운로드하기 전에 한번 사용해 보고 싶으신가요? [기본](examples/basic.md) 예제를 사용해 보세요!

Vue Query는 Vue 2.x 및 3.x와 호환됩니다.

> Vue 2.6을 사용하는 경우 [@vue/composition-api](https://github.com/vuejs/composition-api)도 설정해야 합니다.

### Vue Query 초기화

Vue Query를 사용하기 전에 `VueQueryPlugin`를 사용하여 초기화해야 합니다.

```tsx
import { VueQueryPlugin } from '@tanstack/vue-query'

app.use(VueQueryPlugin)
```
### `<script setup>`와 함께 Composition API 사용

문서의 모든 예시에서는 [`<script setup>`](https://staging.vuejs.org/api/sfc-script-setup.html) 구문을 사용합니다.

Vue 2 사용자는 [이 플러그인](https://github.com/antfu/unplugin-vue2-script-setup)을 사용하여 해당 구문을 사용할 수도 있습니다. 설치 세부 사항은 플러그인 설명서를 확인하세요.

`<script setup>` 구문을 좋아하지 않는다면 `setup()` 함수 아래의 코드를 이동하고 템플릿에 사용된 값을 반환하여 모든 예제를 일반 Composition API 구문으로 쉽게 변환할 수 있습니다.

```vue
<script setup>
import { useQuery } from '@tanstack/vue-query'

const { isPending, isFetching, isError, data, error } = useQuery({
  queryKey: ['todos'],
  queryFn: getTodos,
})
</script>

<template>...</template>
```
