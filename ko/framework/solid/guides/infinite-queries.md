---
id: infinite-queries
title: 인피니트 Queries
---




기존 데이터 집합에 추가로 "더 많은 데이터를 로드"하거나 "무한 스크롤"할 수 있는 렌더링 목록도 매우 일반적인 UI 패턴입니다. TanStack Query는 이러한 유형의 목록을 쿼리하기 위해 `useInfiniteQuery`라는 유용한 `useQuery` 버전을 지원합니다.

`useInfiniteQuery`를 사용하면 몇 가지 다른 점을 알 수 있습니다.

- `data`는 이제 무한한 query 데이터를 포함하는 객체입니다.
- 가져온 페이지를 포함하는 `data.pages` 배열
- 페이지를 가져오는 데 사용되는 페이지 매개변수를 포함하는 `data.pageParams` 배열
- 이제 `fetchNextPage` 및 `fetchPreviousPage` 기능을 사용할 수 있습니다(`fetchNextPage` 필요)
- 이제 `initialPageParam` 옵션을 사용하여 초기 페이지 매개변수를 지정할 수 있습니다(필수).
- 로드할 데이터가 더 있는지 여부와 이를 가져올 정보가 있는지 확인하는 데 `getNextPageParam` 및 `getPreviousPageParam` 옵션을 사용할 수 있습니다. 이 정보는 query 함수의 추가 매개변수로 제공됩니다.
- 이제 `hasNextPage` boolean을 사용할 수 있으며 `getNextPageParam`가 `null` 또는 `undefined` 이외의 값을 반환하는 경우 `true`입니다.
- 이제 `hasPreviousPage` boolean을 사용할 수 있으며 `getPreviousPageParam`가 `null` 또는 `undefined` 이외의 값을 반환하는 경우 `true`입니다.
- 이제 `isFetchingNextPage` 및 `isFetchingPreviousPage` boolean을 사용하여 백그라운드 새로 고침 상태와 추가 로드 상태를 구분할 수 있습니다.

> 참고: `initialData` 또는 `placeholderData` 옵션은 `data.pages` 및 `data.pageParams` 속성을 가진 개체의 동일한 구조를 따라야 합니다.

## 예

다음 프로젝트 그룹을 가져오는 데 사용할 수 있는 커서와 함께 `cursor` 인덱스를 기반으로 한 번에 `projects` 3개의 페이지를 반환하는 API가 있다고 가정해 보겠습니다.

```tsx
fetch('/api/projects?cursor=0')
// { 데이터: [...], nextCursor: 3}
fetch('/api/projects?cursor=3')
// { 데이터: [...], nextCursor: 6}
fetch('/api/projects?cursor=6')
// { 데이터: [...], nextCursor: 9}
fetch('/api/projects?cursor=9')
// { 데이터: [...] }
```
이 정보를 사용하여 다음과 같은 방법으로 "추가 로드" UI를 만들 수 있습니다.

- 기본적으로 `useInfiniteQuery`가 첫 번째 데이터 그룹을 요청하기를 기다리는 중입니다.
- `getNextPageParam`에서 다음 query에 대한 정보를 반환합니다.
- `fetchNextPage` 함수 호출



```tsx
import { Switch, Match, For, Show } from 'solid-js'
import { useInfiniteQuery } from '@tanstack/solid-query'

function Projects() {
  const fetchProjects = async ({ pageParam }) => {
    const res = await fetch('/api/projects?cursor=' + pageParam)
    return res.json()
  }

  const projectsQuery = useInfiniteQuery(() => ({
    queryKey: ['projects'],
    queryFn: fetchProjects,
    initialPageParam: 0,
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
  }))

  return (
    <Switch>
      <Match when={projectsQuery.isPending}>
        <p>Loading...</p>
      </Match>
      <Match when={projectsQuery.isError}>
        <p>Error: {projectsQuery.error.message}</p>
      </Match>
      <Match when={projectsQuery.isSuccess}>
        <For each={projectsQuery.data.pages}>
          {(group) => (
            <For each={group.data}>{(project) => <p>{project.name}</p>}</For>
          )}
        </For>
        <div>
          <button
            onClick={() => projectsQuery.fetchNextPage()}
            disabled={!projectsQuery.hasNextPage || projectsQuery.isFetching}
          >
            {projectsQuery.isFetchingNextPage
              ? 'Loading more...'
              : projectsQuery.hasNextPage
                ? 'Load More'
                : 'Nothing more to load'}
          </button>
        </div>
        <Show
          when={projectsQuery.isFetching && !projectsQuery.isFetchingNextPage}
        >
          <div>Fetching...</div>
        </Show>
      </Match>
    </Switch>
  )
}
```



진행 중인 가져오기가 진행 중인 동안 `fetchNextPage`를 호출하면 백그라운드에서 발생하는 데이터 새로 고침을 덮어쓸 위험이 있다는 점을 이해하는 것이 중요합니다. 이 상황은 목록을 렌더링하고 `fetchNextPage`를 동시에 트리거할 때 특히 중요합니다.

InfiniteQuery에 대해 진행 중인 가져오기는 단 한 번만 가능하다는 점을 기억하세요. 단일 캐시 항목이 모든 페이지에 공유되므로 동시에 두 번 가져오려고 하면 데이터 덮어쓰기가 발생할 수 있습니다.

동시 가져오기를 활성화하려는 경우 `fetchNextPage` 내에서 `{ cancelRefetch: false }` 옵션(기본값: true)을 활용할 수 있습니다.

충돌 없이 원활한 쿼리 프로세스를 보장하려면 특히 사용자가 해당 통화를 직접 제어하지 않는 경우 query가 `isFetching` 상태가 아닌지 확인하는 것이 좋습니다.



```jsx
<List
  onEndReached={() =>
    projectsQuery.hasNextPage &&
    !projectsQuery.isFetching &&
    projectsQuery.fetchNextPage()
  }
/>
```



## 무한 query를 다시 가져와야 하는 경우 어떻게 되나요?

무한 query가 `stale`가 되어 다시 가져와야 하는 경우 각 그룹은 첫 번째 그룹부터 시작하여 `sequentially`를 가져옵니다. 이렇게 하면 기본 데이터가 변경되더라도 오래된 커서를 사용하지 않고 잠재적으로 중복되거나 레코드를 건너뛰는 일이 발생하지 않습니다. 무한 query의 결과가 queryCache에서 제거되면 초기 그룹만 요청된 상태로 초기 상태에서 페이지 매김이 다시 시작됩니다.

## 양방향 무한 목록을 구현하고 싶다면 어떻게 해야 하나요?

`getPreviousPageParam`, `fetchPreviousPage`, `hasPreviousPage` 및 `isFetchingPreviousPage` 속성과 함수를 사용하여 양방향 목록을 구현할 수 있습니다.



```tsx
useInfiniteQuery(() => ({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  initialPageParam: 0,
  getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
  getPreviousPageParam: (firstPage, pages) => firstPage.prevCursor,
}))
```



## 페이지를 역순으로 표시하고 싶다면 어떻게 해야 하나요?

때로는 페이지를 역순으로 표시하고 싶을 수도 있습니다. 이 경우 `select` 옵션을 사용할 수 있습니다.



```tsx
useInfiniteQuery(() => ({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  select: (data) => ({
    pages: [...data.pages].reverse(),
    pageParams: [...data.pageParams].reverse(),
  }),
}))
```



## 무한 query를 수동으로 업데이트하고 싶다면 어떻게 해야 하나요?

### 첫 번째 페이지를 수동으로 제거:



```tsx
queryClient.setQueryData(['projects'], (data) => ({
  pages: data.pages.slice(1),
  pageParams: data.pageParams.slice(1),
}))
```



### 개별 페이지에서 단일 값을 수동으로 제거하려면 다음 단계를 따르세요.



```tsx
const newPagesArray =
  oldPagesArray?.pages.map((page) =>
    page.filter((val) => val.id !== updatedId),
  ) ?? []

queryClient.setQueryData(['projects'], (data) => ({
  pages: newPagesArray,
  pageParams: data.pageParams,
}))
```



### 첫 번째 페이지만 유지:



```tsx
queryClient.setQueryData(['projects'], (data) => ({
  pages: data.pages.slice(0, 1),
  pageParams: data.pageParams.slice(0, 1),
}))
```



페이지와 pageParams의 데이터 구조를 항상 동일하게 유지하세요!

## 페이지 수를 제한하고 싶으면 어떻게 하나요?

일부 사용 사례에서는 성능과 UX를 개선하기 위해 query 데이터에 저장되는 페이지 수를 제한할 수 있습니다.

- 사용자가 많은 수의 페이지를 로드할 수 있는 경우(메모리 사용량)
- 수십 개의 페이지가 포함된 무한한 query를 다시 가져와야 하는 경우 (네트워크 사용량: 모든 페이지를 순차적으로 가져옴)

해결책은 "Limited Infinite Query"를 사용하는 것입니다. 이는 `getNextPageParam` 및 `getPreviousPageParam`와 함께 `maxPages` 옵션을 사용하여 필요할 때 양방향으로 페이지를 가져올 수 있도록 함으로써 가능해졌습니다.

다음 예에서는 query 데이터 페이지 배열에 3개의 페이지만 보관됩니다. 다시 가져오기가 필요한 경우 3페이지만 순차적으로 다시 가져옵니다.



```tsx
useInfiniteQuery(() => ({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  initialPageParam: 0,
  getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
  getPreviousPageParam: (firstPage, pages) => firstPage.prevCursor,
  maxPages: 3,
}))
```



## 내 API가 커서를 반환하지 않으면 어떻게 되나요?

API가 커서를 반환하지 않으면 `pageParam`를 커서로 사용할 수 있습니다. `getNextPageParam` 및 `getPreviousPageParam`도 현재 페이지의 `pageParam`를 가져오므로 이를 사용하여 다음/이전 페이지 매개변수를 계산할 수 있습니다.



```tsx
return useInfiniteQuery(() => ({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  initialPageParam: 0,
  getNextPageParam: (lastPage, allPages, lastPageParam) => {
    if (lastPage.length === 0) {
      return undefined
    }
    return lastPageParam + 1
  },
  getPreviousPageParam: (firstPage, allPages, firstPageParam) => {
    if (firstPageParam <= 1) {
      return undefined
    }
    return firstPageParam - 1
  },
}))
```




## 추가 자료

Infinite Queries가 내부적으로 작동하는 방식을 더 잘 이해하려면 [Infinite Queries 작동 방식](https://tkdodo.eu/blog/how-infinite-queries-work) 문서를 참조하세요.


