---
id: devtools
title: 개발자 도구
---




Vue Query에는 전용 개발 도구가 함께 제공되므로 공중에 손을 흔들고 만세를 외쳐보세요! 🥳

Vue Query 여정을 시작할 때 이러한 개발 도구를 곁에 두고 싶을 것입니다. 이는 Vue Query의 모든 내부 작동을 시각화하는 데 도움이 되며 위기에 처했을 때 디버깅 시간을 절약해 줄 것입니다!

> Chrome, Firefox 및 Edge 사용자의 경우: 브라우저 DevTools에서 TanStack Query를 직접 디버깅하기 위해 타사 브라우저 확장 프로그램을 사용할 수 있습니다. 이는 프레임워크별 devtools 패키지와 동일한 기능을 제공합니다.
>
> - <img alt="Chrome 로고" src="https://www.google.com/chrome/static/images/chrome-logo.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 크롬](https://chromewebstore.google.com/detail/tanstack-query-devtools/annajfchloimdhceglpgglpeepfghfai)
> - <img alt="Firefox 로고" src="https://upload.wikimedia.org/wikipedia/commons/a/a0/Firefox_logo%2C_2019.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for Firefox](https://addons.mozilla.org/en-US/firefox/addon/tanstack-query-devtools/)
> - <img alt="Edge logo" src="https://upload.wikimedia.org/wikipedia/commons/9/98/Microsoft_Edge_logo_%282019%29.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 엣지](https://microsoftedge.microsoft.com/addons/detail/tanstack-query-devtools/edmdpkgkacmjopodhfolmphdenmddobj)

## 구성요소 기반 Devtool(Vue 3)

전용 패키지를 사용하여 devtools 구성 요소를 페이지에 직접 통합할 수 있습니다.
구성 요소 기반 개발 도구는 프레임워크에 구애받지 않는 구현을 사용하며 항상 최신 상태입니다.

devtools 구성요소는 설치해야 하는 별도의 패키지입니다.

```bash
npm i @tanstack/vue-query-devtools
```
또는

```bash
pnpm add @tanstack/vue-query-devtools
```
또는

```bash
yarn add @tanstack/vue-query-devtools
```
또는

```bash
bun add @tanstack/vue-query-devtools
```
기본적으로 Vue Query Devtools는 `process.env.NODE_ENV === 'development'`인 경우에만 번들에 포함되므로 프로덕션 빌드 중에 제외하는 것에 대해 걱정할 필요가 없습니다.

## 플로팅 모드

Devtools는 앱에 고정된 부동 요소로 마운트되며 화면 모서리에 devtool을 표시하고 숨길 수 있는 토글을 제공합니다. 이 토글 상태는 다시 로드할 때마다 localStorage에 저장되고 기억됩니다.

Vue 앱에서 가능한 한 높은 위치에 다음 코드를 배치하세요. 페이지의 루트에 가까울수록 더 잘 작동합니다!

```vue
<script setup>
import { VueQueryDevtools } from '@tanstack/vue-query-devtools'
</script>

<template>
  <h1>The app!</h1>
  <VueQueryDevtools />
</template>
```
### Options

- `initialIsOpen: boolean`
  - 개발 도구가 기본적으로 열려 있도록 하려면 이 `true`를 설정하십시오.
- `buttonPosition?: "top-left" | "top-right" | "bottom-left" | "bottom-right"`
  - 기본값은 `bottom-right`입니다.
  - devtools 패널을 열고 닫는 React Query 로고의 위치입니다.
- `position?: "top" | "bottom" | "left" | "right"`
  - 기본값은 `bottom`입니다.
  - React Query devtools 패널의 위치.
- `client?: QueryClient`
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.
- `errorTypes?: { name: string; initializer: (query: Query) => TError}`
  - 이를 사용하여 queries에서 발생할 수 있는 일부 오류를 미리 정의합니다. 해당 오류가 UI에서 전환되면 초기화 프로그램이 호출됩니다(특정 query 포함). 오류를 반환해야 합니다.
- `styleNonce?: string`
  - 문서 헤드에 추가된 스타일 태그에 nonce를 전달하는 데 사용합니다. 이는 인라인 스타일을 허용하기 위해 CSP(콘텐츠 보안 정책) nonce를 사용하는 경우 유용합니다.
- `shadowDOMTarget?: ShadowRoot`
  - 기본 동작은 devtool의 스타일을 DOM 내의 head 태그에 적용합니다.
  - 스타일이 light DOM의 head 태그 내에서 대신 Shadow DOM 내에서 적용되도록 Shadow DOM 대상을 devtools에 전달하는 데 사용합니다.

## 임베디드 모드

임베디드 모드에서는 개발 도구가 애플리케이션의 고정 요소로 표시되므로 자체 개발 도구에서 패널을 사용할 수 있습니다.

다음 코드를 React 앱의 가능한 한 높은 위치에 배치하세요. 페이지의 루트에 가까울수록 더 잘 작동합니다!

```vue
<script setup>
import { VueQueryDevtoolsPanel } from '@tanstack/vue-query-devtools'
const isDevtoolsOpen = ref(false)
function toggleDevtools() {
  isDevtoolsOpen.value = !isDevtoolsOpen.value
}
</script>

<template>
  <h1>The app!</h1>
  <button @click="toggleDevtools">Open Devtools</button>
  <VueQueryDevtoolsPanel v-if="isDevtoolsOpen" :onClose="toggleDevtools" />
</template>
```
### Options

- `style?: React.CSSProperties`
  - devtools 패널의 사용자 정의 스타일
  - 기본값 : `{ height: '500px' }`
  - 예: `{ height: '100%' }`
  - 예: `{ height: '100%', width: '100%' }`
- `onClose?: () => unknown`
  - devtools 패널이 닫힐 때 호출되는 콜백 함수
-`client?: QueryClient`,
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.
- `errorTypes?: { name: string; initializer: (query: Query) => TError}[]`
  - 이를 사용하여 queries에서 발생할 수 있는 일부 오류를 미리 정의합니다. UI에서 해당 오류가 전환되면 초기화 프로그램이 특정 query와 함께 호출됩니다. 오류를 반환해야 합니다.
- `styleNonce?: string`
  - 문서 헤드에 추가된 스타일 태그에 nonce를 전달하는 데 사용합니다. 이는 인라인 스타일을 허용하기 위해 CSP(콘텐츠 보안 정책) nonce를 사용하는 경우 유용합니다.
- `shadowDOMTarget?: ShadowRoot`
  - 기본 동작은 devtool의 스타일을 DOM 내의 head 태그에 적용합니다.
  - 스타일이 light DOM의 head 태그 내에서 대신 Shadow DOM 내에서 적용되도록 Shadow DOM 대상을 devtools에 전달하는 데 사용합니다.

## 기존 개발 도구

Vue Query는 [공식 Vue devtools](https://github.com/vuejs/devtools-next)와 원활하게 통합되어 사용자 정의 검사기와 타임라인 이벤트를 추가합니다.
Devtool 코드는 기본적으로 프로덕션 번들에서 트리쉐이킹됩니다.

작동하게 하려면 플러그인 옵션에서만 활성화하면 됩니다.

```ts
app.use(VueQueryPlugin, {
  enableDevtoolsV6Plugin: true,
})
```
devtools의 v6 및 v7 버전이 모두 지원됩니다.