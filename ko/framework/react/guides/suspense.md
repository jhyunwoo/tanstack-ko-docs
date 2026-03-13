---
id: suspense
title: Suspense
---




React Query는 데이터 가져오기 API용 React의 Suspense와 함께 사용할 수도 있습니다. 이를 위해 전용 후크가 있습니다.

- [useSuspenseQuery](../reference/useSuspenseQuery.md)
- [useSuspenseInfiniteQuery](../reference/useSuspenseInfiniteQuery.md)
- [useSuspenseQueries](../reference/useSuspenseQueries.md)
- 추가로 `useQuery().promise` 및 `React.use()`(실험용)를 사용할 수 있습니다.

suspense 모드를 사용하는 경우 `status` 상태 및 `error` 객체는 필요하지 않으며 `React.Suspense` 구성 요소의 사용으로 대체됩니다(오류 잡기를 위한 `fallback` 소품 및 React 오류 경계 사용 포함). suspense 모드 설정 방법에 대한 자세한 내용은 [오류 경계 재설정](#resetting-error-boundaries)을 읽고 [Suspense 예](../examples/suspense.md)를 참조하세요.

mutations가 가장 가까운 오류 경계(queries와 유사)에 오류를 전파하도록 하려면 `throwOnError` 옵션을 `true`로 설정할 수도 있습니다.

query에 대해 suspense 모드 활성화:

```tsx
import { useSuspenseQuery } from '@tanstack/react-query'

const { data } = useSuspenseQuery({ queryKey, queryFn })
```
이는 `data`가 정의되도록 보장되기 때문에 TypeScript에서 잘 작동합니다(오류 및 로딩 상태는 Suspense 및 ErrorBoundaries에 의해 처리됨).

따라서 Query를 조건부로 활성화/비활성화할 수 없습니다. 일반적으로 종속 Queries에는 필요하지 않습니다. suspense를 사용하면 하나의 구성 요소 내부에 있는 모든 Queries가 직렬로 가져오기 때문입니다.

이 Query에는 `placeholderData`도 존재하지 않습니다. 업데이트 중에 UI가 대체되는 것을 방지하려면 QueryKey를 [startTransition](https://react.dev/reference/react/Suspense#preventing-unwanted-fallbacks)으로 변경하는 업데이트를 래핑하세요.

### throwOnError 기본값

기본적으로 모든 오류가 가장 가까운 오류 경계에 발생하는 것은 아닙니다. 표시할 다른 데이터가 없는 경우에만 오류가 발생합니다. 즉, Query가 캐시에서 데이터를 성공적으로 가져온 경우 데이터가 `stale`인 경우에도 구성 요소가 렌더링됩니다. 따라서 `throwOnError`의 기본값은 다음과 같습니다.

```
throwOnError: (error, query) => typeof query.state.data === 'undefined'
```
`throwOnError`를 변경할 수 없으므로(`data`가 잠재적으로 `undefined`가 될 수 있기 때문에) 모든 오류를 오류 경계로 처리하려면 수동으로 오류를 발생시켜야 합니다.

```tsx
import { useSuspenseQuery } from '@tanstack/react-query'

const { data, error, isFetching } = useSuspenseQuery({ queryKey, queryFn })

if (error && !isFetching) {
  throw error
}

// 계속해서 데이터 렌더링
```
## 오류 경계 재설정

queries에서 **suspense** 또는 **throwOnError**를 사용하는지 여부에 관계없이 오류가 발생한 후 다시 렌더링할 때 다시 시도하고 싶다는 것을 queries에 알리는 방법이 필요합니다.

Query 오류는 `QueryErrorResetBoundary` 구성 요소 또는 `useQueryErrorResetBoundary` 후크를 사용하여 재설정할 수 있습니다.

구성요소를 사용할 때 구성요소 경계 내의 모든 query 오류가 재설정됩니다.

```tsx
import { QueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

const App = () => (
  <QueryErrorResetBoundary>
    {({ reset }) => (
      <ErrorBoundary
        onReset={reset}
        fallbackRender={({ resetErrorBoundary }) => (
          <div>
            There was an error!
            <Button onClick={() => resetErrorBoundary()}>Try again</Button>
          </div>
        )}
      >
        <Page />
      </ErrorBoundary>
    )}
  </QueryErrorResetBoundary>
)
```
후크를 사용하면 가장 가까운 `QueryErrorResetBoundary` 내의 모든 query 오류가 재설정됩니다. 정의된 경계가 없으면 전역적으로 재설정됩니다.

```tsx
import { useQueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

const App = () => {
  const { reset } = useQueryErrorResetBoundary()
  return (
    <ErrorBoundary
      onReset={reset}
      fallbackRender={({ resetErrorBoundary }) => (
        <div>
          There was an error!
          <Button onClick={() => resetErrorBoundary()}>Try again</Button>
        </div>
      )}
    >
      <Page />
    </ErrorBoundary>
  )
}
```
## 렌더링할 때 가져오기 vs 가져올 때 렌더링

기본적으로 `suspense` 모드의 React Query는 추가 구성 없이 **Fetch-on-render** 솔루션으로 매우 잘 작동합니다. 이는 구성요소가 마운트를 시도할 때 query 가져오기 및 일시중단을 트리거하지만 해당 구성요소를 가져오고 마운트한 후에만 가능함을 의미합니다. 다음 단계로 나아가서 **가져오는 대로 렌더링** 모델을 구현하려면 라우팅 콜백 및/또는 사용자 상호 작용 이벤트에 [프리페칭](prefetching.md)을 구현하여 queries가 마운트되기 전, 상위 구성 요소 가져오기 또는 마운트를 시작하기 전에 로드를 시작하는 것이 좋습니다.

## 스트리밍을 사용하는 서버의 Suspense

`NextJs`를 사용하는 경우 서버: `@tanstack/react-query-next-experimental`에서 Suspense에 대한 **실험적** 통합을 사용할 수 있습니다. 이 패키지를 사용하면 구성 요소에서 `useSuspenseQuery`를 호출하기만 하면 서버(클라이언트 구성 요소)에서 데이터를 가져올 수 있습니다. 그런 다음 SuspenseBoundaries가 해결되면 결과가 서버에서 클라이언트로 스트리밍됩니다.

이를 달성하려면 `ReactQueryStreamedHydration` 구성 요소에 앱을 래핑하세요.

```tsx
// 앱/providers.tsx
'use client'

import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import * as React from 'react'
import { ReactQueryStreamedHydration } from '@tanstack/react-query-next-experimental'

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
        // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
        staleTime: 60 * 1000,
      },
    },
  })
}

let browserQueryClient: QueryClient | undefined = undefined

function getQueryClient() {
  if (isServer) {
    // 서버: 항상 새로운 query 클라이언트를 만드세요
    return makeQueryClient()
  } else {
    // 브라우저: 아직 없는 경우 새 query 클라이언트를 만듭니다.
    // 이는 매우 중요하므로 React가 다음과 같은 경우 새 클라이언트를 다시 만들지 않습니다.
    // 초기 렌더링 중에 일시 중지됩니다. 다음과 같은 경우에는 이것이 필요하지 않을 수도 있습니다.
    // query 클라이언트 생성 아래에 suspense 경계가 있습니다.
    if (!browserQueryClient) browserQueryClient = makeQueryClient()
    return browserQueryClient
  }
}

export function Providers(props: { children: React.ReactNode }) {
  // 참고: query 클라이언트를 초기화할 때 useState를 사용하지 마세요.
  //       이 코드와 코드 사이에 suspense 경계가 있습니다.
  //       React가 초기에 클라이언트를 버릴 것이기 때문에 일시 중지하세요.
  //       일시 중단되고 경계가 없는 경우 렌더링
  const queryClient = getQueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryStreamedHydration>
        {props.children}
      </ReactQueryStreamedHydration>
    </QueryClientProvider>
  )
}
```
자세한 내용은 [NextJs Suspense 스트리밍 예제](../examples/nextjs-suspense-streaming.md) 및 [고급 렌더링 및 Hydration](advanced-ssr.md) 가이드를 확인하세요.

## `useQuery().promise` 및 `React.use()` 사용(실험적)

> 이 기능을 활성화하려면 `QueryClient`를 생성할 때 `experimental_prefetchInRender` 옵션을 `true`로 설정해야 합니다.

**예제 코드:**

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      experimental_prefetchInRender: true,
    },
  },
})
```
**용법:**

```tsx
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { fetchTodos, type Todo } from './api'

function TodoList({ query }: { query: UseQueryResult<Todo[]> }) {
  const data = React.use(query.promise)

  return (
    <ul>
      {data.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  )
}

export function App() {
  const query = useQuery({ queryKey: ['todos'], queryFn: fetchTodos })

  return (
    <>
      <h1>Todos</h1>
      <React.Suspense fallback={<div>Loading...</div>}>
        <TodoList query={query} />
      </React.Suspense>
    </>
  )
}
```
더 완전한 예를 보려면 [GitHub의 suspense 예](https://github.com/TanStack/query/tree/489359a569fd865f3afd7aac8fa43dfc429309e3/examples/react/suspense)를 참조하세요.

Next.js 스트리밍 예제는 [nextjs-suspense-streaming example]을 참조하세요. GitHub](https://github.com/TanStack/query/tree/489359a569fd865f3afd7aac8fa43dfc429309e3/examples/react/nextjs-suspense-streaming).