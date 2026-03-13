---
id: overview
title: 개요
---




`@tanstack/svelte-query` 패키지는 Svelte를 통해 TanStack Query를 사용하기 위한 1급 API를 제공합니다.

> 상점에서 룬 구문으로 마이그레이션하시나요? [마이그레이션 가이드](migrate-from-v5-to-v6.md)를 참조하세요.

## 예

프로젝트 루트 근처에 QueryClientProvider를 포함합니다.

```svelte
<script lang="ts">
  import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query'
  import Example from './lib/Example.svelte'

  const queryClient = new QueryClient()
</script>

<QueryClientProvider client={queryClient}>
  <Example />
</QueryClientProvider>
```
그런 다음 모든 구성 요소에서 함수(예: createQuery)를 호출합니다.

```svelte
<script lang="ts">
  import { createQuery } from '@tanstack/svelte-query'

  const query = createQuery(() => ({
    queryKey: ['todos'],
    queryFn: () => fetchTodos(),
  }))
</script>

<div>
  {#if query.isLoading}
    <p>Loading...</p>
  {:else if query.isError}
    <p>Error: {query.error.message}</p>
  {:else if query.isSuccess}
    {#each query.data as todo}
      <p>{todo.title}</p>
    {/each}
  {/if}
</div>
```
## SvelteKit

SvelteKit을 사용하고 계시다면 [SSR & SvelteKit](ssr.md)를 살펴보시기 바랍니다.

## 사용 가능한 기능

Svelte Query는 Svelte 앱에서 서버 상태를 더 쉽게 관리할 수 있는 유용한 기능과 구성 요소를 제공합니다.

- `createQuery`
- `createQueries`
- `createInfiniteQuery`
- `createMutation`
- `useQueryClient`
- `useIsFetching`
- `useIsMutating`
- `useMutationState`
- `useIsRestoring`
- `useHydrate`
- `<QueryClientProvider>`
- `<HydrationBoundary>`

## Svelte Query와 React Query의 중요한 차이점

Svelte Query는 React Query와 유사한 API를 제공하지만 염두에 두어야 할 몇 가지 주요 차이점이 있습니다.

- 반응성을 유지하려면 `create*` 함수에 대한 인수를 함수로 래핑해야 합니다.
