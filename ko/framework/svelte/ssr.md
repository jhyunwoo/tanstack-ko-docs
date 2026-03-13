---
id: overview
title: SSR 및 SvelteKit
---




## 설정

SvelteKit은 기본적으로 SSR을 사용하여 경로를 렌더링합니다. 이 때문에 서버에서 query를 비활성화해야 합니다. 그렇지 않으면 HTML이 클라이언트에 전송된 후에도 query가 서버에서 비동기식으로 계속 실행됩니다.

이를 달성하기 위해 권장되는 방법은 `QueryClient` 개체에서 SvelteKit의 `browser` 모듈을 사용하는 것입니다. 아래 솔루션 중 하나에 사용되는 `queryClient.prefetchQuery()`는 비활성화되지 않습니다.

**src/routes/+layout.svelte**

```svelte
<script lang="ts">
  import { browser } from '$app/environment'
  import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query'

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        enabled: browser,
      },
    },
  })
</script>

<QueryClientProvider client={queryClient}>
  <slot />
</QueryClientProvider>
```
## 데이터 프리패칭

Svelte Query는 서버에서 데이터를 미리 가져오고 SvelteKit을 사용하여 이를 클라이언트에 전달하는 두 가지 방법을 지원합니다.

이상적인 SSR 설정을 보려면 [create-svelte](examples/ssr.md)를 살펴보세요.

### `initialData` 사용하기

SvelteKit의 [`load`](https://kit.svelte.dev/docs/load)와 ​​함께 서버 측에 로드된 데이터를 `createQuery`의 `initialData` 옵션으로 전달할 수 있습니다.

**src/routes/+page.ts**

```ts
export async function load() {
  const posts = await getPosts()
  return { posts }
}
```
**src/routes/+page.svelte**

```svelte
<script>
  import { createQuery } from '@tanstack/svelte-query'
  import type { PageData } from './$types'

  export let data: PageData

  const query = createQuery(() => ({
    queryKey: ['posts'],
    queryFn: getPosts,
    initialData: data.posts,
  }))
</script>
```
장점:

- 이 설정은 최소한이며 어떤 경우에는 빠른 해결 방법이 될 수 있습니다.
- `+page.ts`/`+layout.ts` 및 `+page.server.ts`/`+layout.server.ts` 로드 기능 모두와 함께 작동합니다.

단점:

- 트리의 더 깊은 하위 구성 요소에서 `createQuery`를 호출하는 경우 해당 지점까지 `initialData`를 전달해야 합니다.
- 여러 위치에서 동일한 query를 사용하여 `createQuery`를 호출하는 경우 모든 위치에 `initialData`를 전달해야 합니다.
- 서버에서 query를 가져온 시간을 알 수 있는 방법이 없으므로 `dataUpdatedAt` 및 query를 다시 가져와야 하는지 결정하는 것은 대신 페이지가 로드된 시간을 기준으로 합니다.

### `prefetchQuery` 사용하기

Svelte Query는 서버에서 queries 프리패치를 지원합니다. 아래 설정을 사용하면 데이터를 가져와서 사용자 브라우저로 보내기 전에 QueryClientProvider에 전달할 수 있습니다. 따라서 이 데이터는 캐시에서 이미 사용 가능하며 클라이언트 측에서는 초기 가져오기가 발생하지 않습니다.

**src/routes/+layout.ts**

```ts
import { browser } from '$app/environment'
import { QueryClient } from '@tanstack/svelte-query'

export async function load() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        enabled: browser,
      },
    },
  })

  return { queryClient }
}
```
**src/routes/+layout.svelte**

```svelte
<script lang="ts">
  import { QueryClientProvider } from '@tanstack/svelte-query'
  import type { LayoutData } from './$types'

  export let data: LayoutData
</script>

<QueryClientProvider client={data.queryClient}>
  <slot />
</QueryClientProvider>
```
**src/routes/+page.ts**

```ts
export async function load({ parent, fetch }) {
  const { queryClient } = await parent()

  // 여기서 SvelteKit 가져오기 기능을 사용해야 합니다.
  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: async () => (await fetch('/api/posts')).json(),
  })
}
```
**src/routes/+page.svelte**

```svelte
<script lang="ts">
  import { createQuery } from '@tanstack/svelte-query'

  // 이 데이터는 +page.ts의 prefetchQuery에 의해 캐시되므로 여기서는 실제로 가져오기가 발생하지 않습니다.
  const query = createQuery(() => ({
    queryKey: ['posts'],
    queryFn: async () => (await fetch('/api/posts')).json(),
  }))
</script>
```
장점:

- 서버에 로드된 데이터는 소품 드릴링 없이 어디서나 액세스 가능
- query 캐시는 `dataUpdatedAt`를 포함하여 작성된 query에 대한 모든 정보를 유지하므로 페이지가 렌더링되면 클라이언트 측에서 초기 가져오기가 발생하지 않습니다.

단점:

- 초기 설정에 더 많은 파일이 필요합니다.
- `+page.server.ts`/`+layout.server.ts` 로드 기능에서는 작동하지 않습니다. (단, TanStack Query와 함께 사용되는 API는 어쨌든 브라우저에 완전히 노출되어야 합니다.)