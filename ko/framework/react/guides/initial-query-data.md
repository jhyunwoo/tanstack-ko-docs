---
id: initial-query-data
title: 초기 Query 데이터
---




query에 대한 초기 데이터가 필요하기 전에 캐시에 제공하는 방법에는 여러 가지가 있습니다.

- 선언적으로:
  - query에 `initialData`를 제공하여 비어 있는 경우 캐시를 미리 채웁니다.
- 반드시:
  - [`queryClient.prefetchQuery`를 사용하여 데이터 프리페치](prefetching.md)
  - [`queryClient.setQueryData`를 사용하여 수동으로 데이터를 캐시에 배치](prefetching.md)

## `initialData`를 사용하여 query 미리 채우기

앱에서 사용할 수 있는 query에 대한 초기 데이터가 이미 있고 이를 query에 직접 제공할 수 있는 경우가 있을 수 있습니다. 이런 경우에는 `config.initialData` 옵션을 사용하여 query에 대한 초기 데이터를 설정하고 초기 로딩 상태를 건너뛸 수 있습니다!

> 중요: `initialData`는 캐시에 유지되므로 이 옵션에 자리 표시자, 부분 또는 불완전한 데이터를 제공하지 않고 대신 `placeholderData`를 사용하는 것이 좋습니다.

[//]: # 'Example'

```tsx
const result = useQuery({
  queryKey: ['todos'],
  queryFn: () => fetch('/todos'),
  initialData: initialTodos,
})
```
[//]: # 'Example'

### `staleTime` 및 `initialDataUpdatedAt`

기본적으로 `initialData`는 마치 방금 가져온 것처럼 완전히 새로운 것으로 처리됩니다. 이는 또한 `staleTime` 옵션에 의해 해석되는 방식에 영향을 미친다는 것을 의미합니다.

- `initialData`로 query 관찰자를 구성하고 `staleTime`(기본 `staleTime: 0`)는 구성하지 않은 경우 query는 마운트 시 즉시 다시 가져옵니다.

[//]: # '예제2'

'``tsx
  // Will show initialTodos immediately, but also immediately refetch todos after mount
  const result = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/todos'),
    initialData: initialTodos,
  })
  ``'

[//]: # '예제2'

- `initialData` 및 `1000` ms의 `staleTime`로 query 관찰자를 구성하면 데이터는 마치 query 함수에서 방금 가져온 것처럼 동일한 시간 동안 최신 상태로 간주됩니다.

[//]: # '예제3'

'``tsx
  // Show initialTodos immediately, but won't refetch until another interaction event is encountered after 1000 ms
  const result = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/todos'),
    initialData: initialTodos,
    staleTime: 1000,
  })
  ``'

[//]: # '예제3'

- `initialData`가 완전히 신선하지 않다면 어떻게 될까요? 그러면 실제로 가장 정확하고 `initialDataUpdatedAt`라는 옵션을 사용하는 마지막 구성이 남게 됩니다. 이 옵션을 사용하면 initialData 자체가 마지막으로 업데이트된 시점의 숫자 JS 타임스탬프를 밀리초 단위로 전달할 수 있습니다. `Date.now()`가 제공하는 것. Unix 타임스탬프가 있는 경우 `1000`를 곱하여 JS 타임스탬프로 변환해야 합니다.

[//]: # '예제4'

'``tsx
  // Show initialTodos immediately, but won't refetch until another interaction event is encountered after 1000 ms
  const result = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/todos'),
    initialData: initialTodos,
    staleTime: 60 * 1000, // 1 minute
    // This could be 10 seconds ago or 10 minutes ago
    initialDataUpdatedAt: initialTodosUpdatedTimestamp, // eg. 1608412420052
  })
  ``'

[//]: # '예제4'

이 옵션을 사용하면 staleTime를 원래 목적으로 사용하여 데이터의 최신 상태를 결정하는 동시에 `initialData`가 `staleTime`보다 오래된 경우 마운트 시 데이터를 다시 가져올 수 있습니다. 위의 예에서 데이터는 1분 이내에 최신 상태여야 하며 initialData가 마지막으로 업데이트되었을 때 query에 힌트를 주어 query가 데이터를 다시 가져와야 하는지 여부를 스스로 결정할 수 있습니다.

> 데이터를 **프리페치된 데이터**로 처리하려면 `prefetchQuery` 또는 `fetchQuery` API를 사용하여 캐시를 미리 채우고 initialData와 독립적으로 `staleTime`를 구성할 수 있도록 하는 것이 좋습니다.

### 초기 데이터 기능

query의 초기 데이터에 액세스하는 프로세스가 집중적이거나 모든 렌더링에서 수행하고 싶은 작업이 아닌 경우 함수를 `initialData` 값으로 전달할 수 있습니다. 이 기능은 query가 초기화될 때 한 번만 실행되어 귀중한 메모리 및/또는 CPU를 절약합니다.

[//]: # 'Example5'

```tsx
const result = useQuery({
  queryKey: ['todos'],
  queryFn: () => fetch('/todos'),
  initialData: () => getExpensiveTodos(),
})
```
[//]: # 'Example5'

### 캐시의 초기 데이터

어떤 상황에서는 캐시된 다른 결과에서 query에 대한 초기 데이터를 제공할 수 있습니다. 이에 대한 좋은 예는 개별 할일 항목에 대해 할일 목록 query에서 캐시된 데이터를 검색한 다음 이를 개별 할일 query의 초기 데이터로 사용하는 것입니다.

[//]: # 'Example6'

```tsx
const result = useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetch('/todos'),
  initialData: () => {
    // 이 할일 query의 초기 데이터로 'todos' query의 할일을 사용하세요.
    return queryClient.getQueryData(['todos'])?.find((d) => d.id === todoId)
  },
})
```
[//]: # 'Example6'

### `initialDataUpdatedAt`를 사용한 캐시의 초기 데이터

캐시에서 초기 데이터를 얻는다는 것은 초기 데이터를 조회하는 데 사용하는 소스 query가 오래되었을 가능성이 있음을 의미합니다. query가 즉시 다시 가져오는 것을 방지하기 위해 인공적인 `staleTime`를 사용하는 대신 소스 query의 `dataUpdatedAt`를 `initialDataUpdatedAt`에 전달하는 것이 좋습니다. 이는 제공되는 초기 데이터에 관계없이 query를 다시 가져와야 하는지 여부와 시기를 결정하는 데 필요한 모든 정보를 query 인스턴스에 제공합니다.

[//]: # 'Example7'

```tsx
const result = useQuery({
  queryKey: ['todos', todoId],
  queryFn: () => fetch(`/todos/${todoId}`),
  initialData: () =>
    queryClient.getQueryData(['todos'])?.find((d) => d.id === todoId),
  initialDataUpdatedAt: () =>
    queryClient.getQueryState(['todos'])?.dataUpdatedAt,
})
```
[//]: # 'Example7'

### 캐시의 조건부 초기 데이터

초기 데이터를 조회하는 데 사용하는 소스 query가 오래된 경우 캐시된 데이터를 전혀 사용하지 않고 서버에서 가져오는 것이 좋습니다. 이 결정을 더 쉽게 내리려면 대신 `queryClient.getQueryState` 메서드를 사용하여 query가 요구 사항에 충분히 "신선"한지 결정하는 데 사용할 수 있는 `state.dataUpdatedAt` 타임스탬프를 포함하여 소스 query에 대한 자세한 정보를 얻을 수 있습니다.

[//]: # 'Example8'

```tsx
const result = useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetch(`/todos/${todoId}`),
  initialData: () => {
    // query 상태 가져오기
    const state = queryClient.getQueryState(['todos'])

    // query가 존재하고 10초 이내의 데이터가 있는 경우...
    if (state && Date.now() - state.dataUpdatedAt <= 10 * 1000) {
      // 개별 할일 반환
      return state.data.find((d) => d.id === todoId)
    }

    // 그렇지 않으면 정의되지 않은 값을 반환하고 하드 로딩 상태에서 가져오도록 하세요!
  },
})
```
[//]: # 'Example8'
[//]: # 'Materials'

## 추가 자료

`Initial Data`와 `Placeholder Data`의 비교는 [TkDodo 글](https://tkdodo.eu/blog/placeholder-and-initial-data-in-react-query)을 참조하세요.

[//]: # 'Materials'
