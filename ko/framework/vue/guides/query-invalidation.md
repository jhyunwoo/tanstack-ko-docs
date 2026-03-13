---
id: query-invalidation
title: Query 무효화
---




queries가 다시 가져오기 전에 오래될 때까지 기다리는 것이 항상 작동하는 것은 아닙니다. 특히 사용자가 수행한 작업으로 인해 query의 데이터가 오래되었다는 사실을 알고 있는 경우에는 더욱 그렇습니다. 이러한 목적을 위해 `QueryClient`에는 queries를 오래된 것으로 지능적으로 표시하고 잠재적으로 다시 가져올 수 있는 `invalidateQueries` 방법이 있습니다!



```tsx
// 캐시의 모든 query를 무효화합니다.
queryClient.invalidateQueries()
// `todos`로 시작하는 키를 사용하여 모든 query를 무효화합니다.
queryClient.invalidateQueries({ queryKey: ['todos'] })
```



> 참고: 정규화된 캐시를 사용하는 다른 라이브러리가 명령적으로 또는 스키마 추론을 통해 로컬 queries를 새 데이터로 업데이트하려고 시도하는 경우 TanStack Query는 정규화된 캐시를 유지 관리하는 데 수반되는 수동 작업을 방지하고 대신 **대상 무효화, 백그라운드 다시 가져오기 및 궁극적으로 원자성 업데이트**를 규정하는 도구를 제공합니다.

query가 `invalidateQueries`로 무효화되면 두 가지 일이 발생합니다.

- 오래된 것으로 표시됩니다. 이 오래된 상태는 `useQuery` 또는 관련 후크에서 사용되는 모든 `staleTime` 구성을 재정의합니다.
- query가 현재 `useQuery` 또는 관련 후크를 통해 렌더링되고 있는 경우 백그라운드에서도 다시 가져옵니다.

## Query `invalidateQueries`와 일치

`invalidateQueries` 및 `removeQueries`(및 부분 query 일치를 지원하는 다른 API)와 같은 API를 사용하는 경우 접두사로 여러 queries를 일치시키거나 매우 구체적으로 일치시켜 정확한 query와 일치시킬 수 있습니다. 사용할 수 있는 필터 유형에 대한 자세한 내용은 [Query 필터](../../react/guides/filters.md#query-filters)를 참조하세요.

이 예에서는 `todos` 접두사를 사용하여 query 키에서 `todos`로 시작하는 모든 queries를 무효화할 수 있습니다.



```tsx
import { useQuery, useQueryClient } from '@tanstack/vue-query'

// 컨텍스트에서 QueryClient 가져오기
const queryClient = useQueryClient()

queryClient.invalidateQueries({ queryKey: ['todos'] })

// 아래 queries는 모두 무효화됩니다.
const todoListQuery = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodoList,
})
const todoListQuery = useQuery({
  queryKey: ['todos', { page: 1 }],
  queryFn: fetchTodoList,
})
```



보다 구체적인 query 키를 `invalidateQueries` 메서드에 전달하여 특정 변수로 queries를 무효화할 수도 있습니다.



```tsx
queryClient.invalidateQueries({
  queryKey: ['todos', { type: 'done' }],
})

// 아래 query는 무효화됩니다.
const todoListQuery = useQuery({
  queryKey: ['todos', { type: 'done' }],
  queryFn: fetchTodoList,
})

// 그러나 아래의 query는 무효화되지 않습니다.
const todoListQuery = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodoList,
})
```



`invalidateQueries` API는 매우 유연하므로 더 이상 변수나 하위 키가 없는 `todos` queries를 **만** 무효화하려는 경우에도 `exact: true` 옵션을 `invalidateQueries` 메서드에 전달할 수 있습니다.



```tsx
queryClient.invalidateQueries({
  queryKey: ['todos'],
  exact: true,
})

// 아래 query는 무효화됩니다.
const todoListQuery = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodoList,
})

// 그러나 아래의 query는 무효화되지 않습니다.
const todoListQuery = useQuery({
  queryKey: ['todos', { type: 'done' }],
  queryFn: fetchTodoList,
})
```



**더욱** 세분성을 원하는 경우 `invalidateQueries` 메서드에 조건자 함수를 전달할 수 있습니다. 이 함수는 query 캐시에서 각 `Query` 인스턴스를 수신하고 해당 query를 무효화할지 여부에 대해 `true` 또는 `false`를 반환할 수 있습니다.



```tsx
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' && query.queryKey[1]?.version >= 10,
})

// 아래 query는 무효화됩니다.
const todoListQuery = useQuery({
  queryKey: ['todos', { version: 20 }],
  queryFn: fetchTodoList,
})

// 아래 query는 무효화됩니다.
const todoListQuery = useQuery({
  queryKey: ['todos', { version: 10 }],
  queryFn: fetchTodoList,
})

// 그러나 아래의 query는 무효화되지 않습니다.
const todoListQuery = useQuery({
  queryKey: ['todos', { version: 5 }],
  queryFn: fetchTodoList,
})
```


