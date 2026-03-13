---
id: ssr
title: SSR
---




Vue Query는 서버에서 여러 queries를 프리패치한 다음 해당 queries를 queryClient에 _dehydrating_하는 것을 지원합니다. 즉, 서버는 페이지 로드 시 즉시 사용할 수 있는 마크업을 사전 렌더링할 수 있으며 JS를 사용할 수 있게 되자마자 Vue Query는 라이브러리의 전체 기능으로 해당 queries를 업그레이드하거나 _수화_할 수 있습니다. 여기에는 서버에서 렌더링된 이후로 오래된 queries를 클라이언트에서 다시 가져오는 작업이 포함됩니다.

## Nuxt.js 사용

### 누스트 3

먼저 다음 내용으로 `plugins` 디렉터리에 `vue-query.ts` 파일을 만듭니다.

```ts
import type {
  DehydratedState,
  VueQueryPluginOptions,
} from '@tanstack/vue-query'
import {
  VueQueryPlugin,
  QueryClient,
  hydrate,
  dehydrate,
} from '@tanstack/vue-query'
// Nuxt 3 앱 별칭
import { defineNuxtPlugin, useState } from '#imports'

export default defineNuxtPlugin((nuxt) => {
  const vueQueryState = useState<DehydratedState | null>('vue-query')

  // 여기에서 Vue Query 전역 설정을 수정하세요.
  const queryClient = new QueryClient({
    defaultOptions: { queries: { staleTime: 5000 } },
  })
  const options: VueQueryPluginOptions = { queryClient }

  nuxt.vueApp.use(VueQueryPlugin, options)

  if (import.meta.server) {
    nuxt.hooks.hook('app:rendered', () => {
      vueQueryState.value = dehydrate(queryClient)
    })
  }

  if (import.meta.client) {
    hydrate(queryClient, vueQueryState.value)
  }
})
```
이제 `onServerPrefetch`를 사용하여 페이지의 일부 데이터를 미리 가져올 준비가 되었습니다.

- `queryClient.prefetchQuery` 또는 `suspense`와 함께 필요한 모든 queries를 미리 가져옵니다.

```ts
export default defineComponent({
  setup() {
    const { data, suspense } = useQuery({
      queryKey: ['test'],
      queryFn: fetcher,
    })

    onServerPrefetch(async () => {
      await suspense()
    })

    return { data }
  },
})
```
### 누스트 2

먼저 다음 내용으로 `plugins` 디렉터리에 `vue-query.js` 파일을 만듭니다.

```js
import Vue from 'vue'
import { VueQueryPlugin, QueryClient, hydrate } from '@tanstack/vue-query'

export default (context) => {
  // 여기에서 Vue Query 전역 설정을 수정하세요.
  const queryClient = new QueryClient({
    defaultOptions: { queries: { staleTime: 5000 } },
  })

  if (process.server) {
    context.ssrContext.VueQuery = queryClient
  }

  if (process.client) {
    Vue.use(VueQueryPlugin, { queryClient })

    if (context.nuxtState && context.nuxtState.vueQueryState) {
      hydrate(queryClient, context.nuxtState.vueQueryState)
    }
  }
}
```
이 플러그인을 `nuxt.config.js`에 추가하세요

```js
module.exports = {
  ...
  plugins: ['~/plugins/vue-query.js'],
}
```
이제 `onServerPrefetch`를 사용하여 페이지의 일부 데이터를 미리 가져올 준비가 되었습니다.

- `useContext`를 사용하여 nuxt 컨텍스트를 얻습니다.
- `useQueryClient`를 사용하여 `queryClient`의 서버측 인스턴스를 가져옵니다.
- `queryClient.prefetchQuery` 또는 `suspense`와 함께 필요한 모든 queries를 미리 가져옵니다.
- `queryClient`를 `nuxtContext`로 탈수시킵니다.

```vue
// 페이지/todos.vue
<template>
  <div>
    <button @click="refetch">Refetch</button>
    <p>{{ data }}</p>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  onServerPrefetch,
  useContext,
} from '@nuxtjs/composition-api'
import { useQuery, useQueryClient, dehydrate } from '@tanstack/vue-query'

export default defineComponent({
  setup() {
    // SSR 컨텍스트 또는 Vue 컨텍스트에서 QueryClient 가져오기
    const { ssrContext } = useContext()
    // `useQuery` 호출에 대한 두 번째 매개변수로 `queryClient`를 제공해야 합니다.
    const queryClient =
      (ssrContext != null && ssrContext.VueQuery) || useQueryClient()

    // 이는 서버에서 프리패치되어 전송됩니다.
    const { data, refetch, suspense } = useQuery(
      {
        queryKey: ['todos'],
        queryFn: getTodos,
      },
      queryClient,
    )
    // 이는 미리 가져오지 않고 클라이언트 측에서 가져오기를 시작합니다.
    const { data2 } = useQuery(
      {
        queryKey: 'todos2',
        queryFn: getTodos,
      },
      queryClient,
    )

    onServerPrefetch(async () => {
      await suspense()
      ssrContext.nuxt.vueQueryState = dehydrate(queryClient)
    })

    return {
      refetch,
      data,
    }
  },
})
</script>
```
설명된 것처럼 일부 queries를 프리패치하고 다른 queries를 queryClient에서 페치하도록 하는 것은 괜찮습니다. 즉, 특정 query에 대해 `prefetchQuery` 또는 `suspense`를 추가하거나 제거하여 콘텐츠 서버가 렌더링하는 내용을 제어할 수 있습니다.

## Vite SSR 사용하기

VueQuery 클라이언트 상태를 [vite-ssr](https://github.com/frandiox/vite-ssr)과 동기화하여 DOM에서 직렬화합니다.

```js
// main.js(진입점)
import App from './App.vue'
import viteSSR from 'vite-ssr/vue'
import {
  QueryClient,
  VueQueryPlugin,
  hydrate,
  dehydrate,
} from '@tanstack/vue-query'

export default viteSSR(App, { routes: [] }, ({ app, initialState }) => {
  // -- 요청당 한 번 호출되는 Vite SSR 메인 후크입니다.

  // 새로운 VueQuery 클라이언트 생성
  const queryClient = new QueryClient()

  // initialState를 클라이언트 상태와 동기화
  if (import.meta.env.SSR) {
    // SSR 중에 VueQuery 상태에 액세스하고 직렬화하는 방법을 나타냅니다.
    initialState.vueQueryState = { toJSON: () => dehydrate(queryClient) }
  } else {
    // 브라우저에서 기존 상태를 재사용합니다.
    hydrate(queryClient, initialState.vueQueryState)
  }

  // 클라이언트를 앱 구성 요소에 마운트하고 제공합니다.
  app.use(VueQueryPlugin, { queryClient })
})
```
그런 다음 Vue의 `onServerPrefetch`를 사용하여 모든 구성 요소에서 VueQuery를 호출합니다.

```html
<!-- MyComponent.vue -->
<template>
  <div>
    <button @click="refetch">Refetch</button>
    <p>{{ data }}</p>
  </div>
</template>

<script setup>
  import { useQuery } from '@tanstack/vue-query'
  import { onServerPrefetch } from 'vue'

  // This will be prefetched and sent from the server
  const { refetch, data, suspense } = useQuery({
    queryKey: ['todos'],
    queryFn: getTodos,
  })

  onServerPrefetch(suspense)
</script>
```
## 팁, 요령 및 주의 사항

### 성공한 queries만 탈수에 포함됩니다.

오류가 있는 query는 탈수에서 자동으로 제외됩니다. 즉, 기본 동작은 이러한 queries가 서버에 로드되지 않은 척하고 일반적으로 로드 상태를 대신 표시하고 queryClient에서 queries를 다시 시도하는 것입니다. 이는 오류와 관계없이 발생합니다.

때로는 이 동작이 바람직하지 않을 수도 있습니다. 특정 오류 또는 queries 대신 올바른 상태 코드로 오류 페이지를 렌더링하려고 할 수도 있습니다. 이러한 경우에는 `fetchQuery`를 사용하고 오류를 잡아 수동으로 처리하세요.

### 오래된 상태는 서버에서 query를 가져온 시점부터 측정됩니다.

query는 `dataUpdatedAt`였던 시기에 따라 오래된 것으로 간주됩니다. 여기서 주의할 점은 이것이 제대로 작동하려면 서버의 정확한 시간이 필요하지만 UTC 시간이 사용되므로 시간대는 이를 고려하지 않는다는 것입니다.

`staleTime`의 기본값은 `0`이므로 queries는 기본적으로 페이지 로드 시 백그라운드에서 다시 가져옵니다. 특히 마크업을 캐시하지 않는 경우 이러한 이중 가져오기를 방지하려면 더 높은 `staleTime`를 사용하는 것이 좋습니다.

오래된 queries를 다시 가져오는 것은 CDN에서 마크업을 캐싱할 때 완벽하게 일치합니다! 서버에서 페이지를 다시 렌더링할 필요가 없도록 페이지 자체의 캐시 시간을 상당히 높게 설정할 수 있지만, 사용자가 페이지를 방문하자마자 백그라운드에서 데이터를 다시 가져오도록 queries의 `staleTime`를 더 낮게 구성할 수 있습니다. 일주일 동안 페이지를 캐시하고 싶지만 하루보다 오래된 경우 페이지 로드 시 자동으로 데이터를 다시 가져오고 싶을 수도 있습니다.

### 서버의 높은 메모리 소비

모든 요청에 ​​대해 `QueryClient`를 생성하는 경우 Vue Query는 이 클라이언트에 대해 격리된 캐시를 생성하며 이는 `gcTime` 기간 동안 메모리에 보존됩니다. 해당 기간 동안 요청 수가 많은 경우 서버의 메모리 소비가 높아질 수 있습니다.

서버에서 `gcTime`는 수동 가비지 수집을 비활성화하고 요청이 완료되면 자동으로 메모리를 지우는 `Infinity`로 기본 설정됩니다. Infinity가 아닌 `gcTime`를 명시적으로 설정하는 경우 캐시를 조기에 지워야 합니다.

필요하지 않은 캐시를 지우고 메모리 소비를 줄이려면 요청이 처리되고 탈수 상태가 클라이언트에 전송된 후 [QueryClient](../../../reference/QueryClient.md#queryclientclear)에 대한 호출을 추가할 수 있습니다.

또는 더 작은 `gcTime`를 설정할 수 있습니다.