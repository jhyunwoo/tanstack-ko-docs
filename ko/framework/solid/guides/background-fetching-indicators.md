---
id: background-fetching-indicators
title: 배경 가져오기 표시기
---




query의 `status === 'pending'` 상태는 query의 초기 하드 로딩 상태를 표시하기에 충분하지만 때로는 query가 백그라운드에서 다시 가져오고 있다는 추가 표시기를 표시할 수도 있습니다. 이를 위해 queries는 `status` 변수의 상태에 관계없이 가져오기 상태에 있음을 표시하는 데 사용할 수 있는 `isFetching` boolean도 제공합니다.



```tsx
import { Switch, Match, Show, For } from 'solid-js'

function Todos() {
  const todosQuery = useQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  }))

  return (
    <Switch>
      <Match when={todosQuery.isPending}>
        <span>Loading...</span>
      </Match>
      <Match when={todosQuery.isError}>
        <span>Error: {todosQuery.error.message}</span>
      </Match>
      <Match when={todosQuery.isSuccess}>
        <Show when={todosQuery.isFetching}>
          <div>Refreshing...</div>
        </Show>
        <div>
          <For each={todosQuery.data}>{(todo) => <Todo todo={todo} />}</For>
        </div>
      </Match>
    </Switch>
  )
}
```



## 전역 배경 가져오기 로드 상태 표시

개별 query 로딩 상태 외에도 **모든** queries를 가져올 때(백그라운드 포함) 전역 로딩 표시기를 표시하려면 `useIsFetching` 함수를 사용할 수 있습니다.



```tsx
import { useIsFetching } from '@tanstack/solid-query'

function GlobalLoadingIndicator() {
  const isFetching = useIsFetching()

  return (
    <Show when={isFetching()}>
      <div>Queries are fetching in the background...</div>
    </Show>
  )
}
```


