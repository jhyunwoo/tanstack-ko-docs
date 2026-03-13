---
id: devtools
title: 개발자 도구
---




> Chrome, Firefox 및 Edge 사용자의 경우: 브라우저 DevTools에서 TanStack Query를 직접 디버깅하기 위해 타사 브라우저 확장 프로그램을 사용할 수 있습니다. 이는 프레임워크별 devtools 패키지와 동일한 기능을 제공합니다.
>
> - <img alt="Chrome 로고" src="https://www.google.com/chrome/static/images/chrome-logo.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 크롬](https://chromewebstore.google.com/detail/tanstack-query-devtools/annajfchloimdhceglpgglpeepfghfai)
> - <img alt="Firefox 로고" src="https://upload.wikimedia.org/wikipedia/commons/a/a0/Firefox_logo%2C_2019.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for Firefox](https://addons.mozilla.org/en-US/firefox/addon/tanstack-query-devtools/)
> - <img alt="Edge logo" src="https://upload.wikimedia.org/wikipedia/commons/9/98/Microsoft_Edge_logo_%282019%29.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 엣지](https://microsoftedge.microsoft.com/addons/detail/tanstack-query-devtools/edmdpkgkacmjopodhfolmphdenmddobj)

## Devtools 설치 및 가져오기

devtools는 설치해야 하는 별도의 패키지입니다.

```bash
npm i @tanstack/svelte-query-devtools
```
또는

```bash
pnpm add @tanstack/svelte-query-devtools
```
또는

```bash
yarn add @tanstack/svelte-query-devtools
```
또는

```bash
bun add @tanstack/svelte-query-devtools
```
다음과 같이 devtools를 가져올 수 있습니다.

```ts
import { SvelteQueryDevtools } from '@tanstack/svelte-query-devtools'
```
## 플로팅 모드

플로팅 모드는 개발자 도구를 앱에 고정된 플로팅 요소로 마운트하고 화면 모서리에 개발자 도구를 표시하고 숨길 수 있는 토글을 제공합니다. 이 토글 상태는 다시 로드할 때마다 localStorage에 저장되고 기억됩니다.

Svelte 앱에서 가능한 한 높은 위치에 다음 코드를 배치하세요. 페이지의 루트에 가까울수록 더 잘 작동합니다!

```ts
<script>
  import { QueryClientProvider } from '@tanstack/svelte-query'
  import { SvelteQueryDevtools } from '@tanstack/svelte-query-devtools'
</script>

<QueryClientProvider client={queryClient}>
  {/* 신청서의 나머지 부분 */}
  <SvelteQueryDevtools />
</QueryClientProvider>
```
### Options

- `initialIsOpen: boolean`
  - 개발 도구가 기본적으로 열려 있도록 하려면 이 `true`를 설정하십시오.
- `buttonPosition?: "top-left" | "top-right" | "bottom-left" | "bottom-right" | "relative"`
  - 기본값은 `bottom-right`입니다.
  - devtools 패널을 열고 닫는 TanStack 로고의 위치
  - `relative`인 경우 버튼은 개발자 도구를 렌더링하는 위치에 배치됩니다.
- `position?: "top" | "bottom" | "left" | "right"`
  - 기본값은 `bottom`입니다.
  - Svelte Query devtools 패널의 위치
- `client?: QueryClient`,
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.
- `errorTypes?: { name: string; initializer: (query: Query) => TError}`
  - 이를 사용하여 queries에서 발생할 수 있는 일부 오류를 미리 정의합니다. UI에서 해당 오류가 전환되면 초기화 프로그램이 특정 query와 함께 호출됩니다. 오류를 반환해야 합니다.
- `styleNonce?: string`
  - 문서 헤드에 추가된 스타일 태그에 nonce를 전달하는 데 사용합니다. 이는 인라인 스타일을 허용하기 위해 CSP(콘텐츠 보안 정책) nonce를 사용하는 경우 유용합니다.
- `shadowDOMTarget?: ShadowRoot`
  - 기본 동작은 devtool의 스타일을 DOM 내의 head 태그에 적용합니다.
  - 스타일이 light DOM의 head 태그 내에서 대신 Shadow DOM 내에서 적용되도록 Shadow DOM 대상을 devtools에 전달하는 데 사용합니다.