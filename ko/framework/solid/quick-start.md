---
id: quick-start
title: 빠른 시작
---




`@tanstack/solid-query` 패키지는 SolidJS와 함께 TanStack Query를 사용하기 위한 1급 API를 제공합니다.

## 예

```tsx
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/solid-query'
import { Switch, Match, For } from 'solid-js'

const queryClient = new QueryClient()

function Example() {
  const query = useQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  }))

  return (
    <div>
      <Switch>
        <Match when={query.isPending}>
          <p>Loading...</p>
        </Match>
        <Match when={query.isError}>
          <p>Error: {query.error.message}</p>
        </Match>
        <Match when={query.isSuccess}>
          <For each={query.data}>{(todo) => <p>{todo.title}</p>}</For>
        </Match>
      </Switch>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  )
}
```
## Solid Query와 React Query의 중요한 차이점

Solid Query는 React Query와 유사한 API를 제공하지만 염두에 두어야 할 몇 가지 주요 차이점이 있습니다.

- `solid-query` 기본 요소(예: `useQuery`, `useMutation`, `useIsFetching`)에 대한 인수는 함수이므로 반응 범위에서 추적할 수 있습니다.

```tsx
// ❌ 반응 버전
useQuery({
  queryKey: ['todos', todo],
  queryFn: fetchTodos,
})

// ✅ 솔리드 버전
useQuery(() => ({
  queryKey: ['todos', todo],
  queryFn: fetchTodos,
}))
```
- Suspense는 `<Suspense>` 경계 내부의 query 데이터에 액세스하는 경우 기본적으로 queries에 대해 작동합니다.

```tsx
import { For, Suspense } from 'solid-js'

function Example() {
  const query = useQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  }))
  return (
    <div>
      {/* ✅ suspense 경계에서 액세스되는 데이터인 폴백 로드를 트리거합니다. */}
      <Suspense fallback={'Loading...'}>
        <For each={query.data}>{(todo) => <div>{todo.title}</div>}</For>
      </Suspense>
      {/* ❌ suspense 경계에서 데이터에 액세스되지 않아 대체 로드를 트리거하지 않습니다. */}
      <For each={query.data}>{(todo) => <div>{todo.title}</div>}</For>
    </div>
  )
}
```
- Solid Query 기본 요소는 구조 분해를 지원하지 않습니다. 이러한 함수의 반환 값은 저장소이며 해당 속성은 반응형 컨텍스트에서만 추적됩니다.

```tsx
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/solid-query'
import { Match, Switch } from 'solid-js'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  )
}

function Example() {
  // ❌ 반응 버전 - 외부 반응 컨텍스트 파괴를 지원합니다.
  // const { isPending, 오류, 데이터 } = useQuery({
  //   queryKey: ['repoData'],
  //   queryFn: () =>
  //     fetch('https://api.github.com/repos/tannerlinsley/react-query').then(
  //       (res) => res.json()
  //     ),
  // })

  // ✅ 솔리드 버전 - 반응 컨텍스트 외부의 구조 분해를 지원하지 않습니다.
  const query = useQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      fetch('https://api.github.com/repos/tannerlinsley/react-query').then(
        (res) => res.json(),
      ),
  }))

  // ✅ JSX 반응 컨텍스트에서 query 속성에 액세스
  return (
    <Switch>
      <Match when={query.isPending}>Loading...</Match>
      <Match when={query.isError}>Error: {query.error.message}</Match>
      <Match when={query.isSuccess}>
        <div>
          <h1>{query.data.name}</h1>
          <p>{query.data.description}</p>
          <strong>👀 {query.data.subscribers_count}</strong>{' '}
          <strong>✨ {query.data.stargazers_count}</strong>{' '}
          <strong>🍴 {query.data.forks_count}</strong>
        </div>
      </Match>
    </Switch>
  )
}
```
- 신호 및 저장 값을 함수 인수에 직접 전달할 수 있습니다. Solid Query는 query `store`를 자동으로 업데이트합니다.

```tsx
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/solid-query'
import { createSignal, For } from 'solid-js'

const queryClient = new QueryClient()

function Example() {
  const [enabled, setEnabled] = createSignal(false)
  const [todo, setTodo] = createSignal(0)

  // ✅ 신호를 직접 전달하는 것은 안전하며 관찰자는 업데이트합니다.
  // 신호 값이 변경되면 자동으로
  const todosQuery = useQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    enabled: enabled(),
  }))

  const todoDetailsQuery = useQuery(() => ({
    queryKey: ['todo', todo()],
    queryFn: fetchTodo,
    enabled: todo() > 0,
  }))

  return (
    <div>
      <Switch>
        <Match when={todosQuery.isPending}>
          <p>Loading...</p>
        </Match>
        <Match when={todosQuery.isError}>
          <p>Error: {todosQuery.error.message}</p>
        </Match>
        <Match when={todosQuery.isSuccess}>
          <For each={todosQuery.data}>
            {(todo) => (
              <button onClick={() => setTodo(todo.id)}>{todo.title}</button>
            )}
          </For>
        </Match>
      </Switch>
      <button onClick={() => setEnabled(!enabled())}>Toggle enabled</button>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  )
}
```
- SolidJS의 기본 `ErrorBoundary` 구성 요소를 사용하여 오류를 포착하고 재설정할 수 있습니다.
  `throwOnError` 또는 `suspense` 옵션을 `true`로 설정하여 `ErrorBoundary`에 오류가 발생하는지 확인하세요.

- 속성 추적은 Solid의 미세한 반응성을 통해 처리되므로 `notifyOnChangeProps`와 같은 옵션이 필요하지 않습니다.