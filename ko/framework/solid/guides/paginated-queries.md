---
id: paginated-queries
title: 페이지 매김/지연됨 Queries
---




페이지가 매겨진 데이터 렌더링은 매우 일반적인 UI 패턴이며 TanStack Query에서는 query 키에 페이지 정보를 포함하여 "작동"합니다.



```tsx
const projectsQuery = useQuery(() => ({
  queryKey: ['projects', page()],
  queryFn: () => fetchProjects(page()),
}))
```



그러나 이 간단한 예제를 실행하면 이상한 점을 발견할 수 있습니다.

**각 새 페이지가 새로운 query처럼 처리되기 때문에 UI가 `success` 및 `pending` 상태에 들어오고 나갑니다.**

이 경험은 최적이 아니며 불행히도 오늘날 얼마나 많은 도구가 작동을 요구하는지입니다. 하지만 TanStack Query는 아닙니다! 짐작하셨겠지만, TanStack Query에는 이 문제를 해결할 수 있는 `placeholderData`라는 놀라운 기능이 포함되어 있습니다.

## `placeholderData`를 사용하여 더 나은 페이지 매기기 Queries

query에 대한 pageIndex(또는 커서)를 이상적으로 증가시키려는 다음 예를 고려하십시오. `useQuery`를 사용한다면 **기술적으로는 여전히 잘 작동하겠지만** 각 페이지 또는 커서에 대해 서로 다른 queries가 생성되고 삭제됨에 따라 UI가 `success` 및 `pending` 상태에 들어오고 나갈 것입니다. `placeholderData`를 `(previousData) => previousData` 또는 TanStack Query에서 내보낸 `keepPreviousData` 함수로 설정하면 몇 가지 새로운 기능을 얻을 수 있습니다.

- **query 키가 변경되었더라도 새 데이터를 요청하는 동안 마지막으로 성공한 가져오기의 데이터를 사용할 수 있습니다**.
- 새 데이터가 도착하면 이전 `data`가 원활하게 교체되어 새 데이터를 표시합니다.
- `isPlaceholderData`는 query가 현재 어떤 데이터를 제공하고 있는지 알 수 있도록 제공됩니다.



```tsx
import { createSignal, Switch, Match, Show, For } from 'solid-js'
import { keepPreviousData, useQuery } from '@tanstack/solid-query'

function Todos() {
  const [page, setPage] = createSignal(0)

  const fetchProjects = (page = 0) =>
    fetch('/api/projects?page=' + page).then((res) => res.json())

  const projectsQuery = useQuery(() => ({
    queryKey: ['projects', page()],
    queryFn: () => fetchProjects(page()),
    placeholderData: keepPreviousData,
  }))

  return (
    <div>
      <Switch>
        <Match when={projectsQuery.isPending}>
          <div>Loading...</div>
        </Match>
        <Match when={projectsQuery.isError}>
          <div>Error: {projectsQuery.error.message}</div>
        </Match>
        <Match when={projectsQuery.isSuccess}>
          <div>
            <For each={projectsQuery.data.projects}>
              {(project) => <p>{project.name}</p>}
            </For>
          </div>
        </Match>
      </Switch>
      <span>Current Page: {page() + 1}</span>
      <button
        onClick={() => setPage((old) => Math.max(old - 1, 0))}
        disabled={page() === 0}
      >
        Previous Page
      </button>
      <button
        onClick={() => {
          if (!projectsQuery.isPlaceholderData && projectsQuery.data?.hasMore) {
            setPage((old) => old + 1)
          }
        }}
        // 다음 페이지를 사용할 수 있을 때까지 다음 페이지 버튼을 비활성화합니다.
        disabled={
          projectsQuery.isPlaceholderData || !projectsQuery.data?.hasMore
        }
      >
        Next Page
      </button>
      <Show when={projectsQuery.isFetching}>
        <span> Loading...</span>
      </Show>
    </div>
  )
}
```



## `placeholderData`를 사용하면 무한 Query 결과가 지연됩니다.

흔하지는 않지만 `placeholderData` 옵션은 `useInfiniteQuery` 기능과 완벽하게 작동하므로 시간이 지남에 따라 무한한 query 키가 변경되는 동안 사용자가 캐시된 데이터를 계속해서 볼 수 있도록 원활하게 허용할 수 있습니다.