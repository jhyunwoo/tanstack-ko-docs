---
id: prefetching
title: 프리페칭
---




운이 좋다면 사용자가 필요한 데이터가 필요하기 전에 미리 가져올 수 있도록 무엇을 할 것인지 충분히 알 수 있을 것입니다! 이 경우 `prefetchQuery` 메서드를 사용하여 캐시에 배치할 query의 결과를 미리 가져올 수 있습니다.

[//]: # 'ExamplePrefetching'

```tsx
const prefetchTodos = async () => {
  // 이 query의 결과는 일반 query처럼 캐시됩니다.
  await queryClient.prefetchQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })
}
```
[//]: # 'ExamplePrefetching'

- 이 query에 대한 **신선한** 데이터가 이미 캐시에 있는 경우 데이터를 가져오지 않습니다.
- 예를 들어 `staleTime`가 전달된 경우. `prefetchQuery({ queryKey: ['todos'], queryFn: fn, staleTime: 5000 })`이고 데이터가 지정된 `staleTime`보다 오래되면 query를 가져옵니다.
- 프리페치된 query에 대해 `useQuery`의 인스턴스가 나타나지 않으면 `gcTime`에 지정된 시간 이후 삭제되고 가비지 수집됩니다.

## 무한 Queries 프리페칭

Infinite Queries는 일반 Queries처럼 프리패치할 수 있습니다. 기본적으로 Query의 첫 번째 페이지만 프리페치되어 지정된 QueryKey에 저장됩니다. 두 개 이상의 페이지를 프리페치하려는 경우 `pages` 옵션을 사용할 수 있으며, 이 경우 `getNextPageParam` 기능도 제공해야 합니다.

[//]: # 'ExampleInfiniteQuery'

```tsx
const prefetchProjects = async () => {
  // 이 query의 결과는 일반 query처럼 캐시됩니다.
  await queryClient.prefetchInfiniteQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
    initialPageParam: 0,
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    pages: 3, // 처음 3페이지 미리 가져오기
  })
}
```
[//]: # 'ExampleInfiniteQuery'

위의 코드는 3개의 페이지를 순서대로 프리페치하려고 시도하며, 각 페이지마다 `getNextPageParam`가 실행되어 프리페치할 다음 페이지를 결정합니다. `getNextPageParam`가 `undefined`를 반환하면 프리페치가 중지됩니다.