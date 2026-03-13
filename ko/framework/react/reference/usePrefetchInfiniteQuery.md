---
id: usePrefetchInfiniteQuery
title: usePrefetchInfiniteQuery
---





```tsx
usePrefetchInfiniteQuery(options)
```
**옵션**

[QueryClient](../../../reference/QueryClient.md#queryclientprefetchinfinitequery)에 전달할 수 있는 모든 것을 `usePrefetchInfiniteQuery`에 전달할 수 있습니다. 그 중 일부는 아래와 같이 필요하다는 점을 기억하세요.

- `queryKey: QueryKey`
  - **필수**
  - 렌더링 중에 프리페치할 query 키

- `queryFn: (context: QueryFunctionContext) => Promise<TData>`
  - **필수이지만 기본 query 함수가 정의되지 않은 경우에만** 자세한 내용은 [기본 Query 함수](../guides/default-query-function.md)를 참조하세요.

- `initialPageParam: TPageParam`
  - **필수**
  - 첫 번째 페이지를 가져올 때 사용할 기본 페이지 매개변수입니다.

- `getNextPageParam: (lastPage, allPages, lastPageParam, allPageParams) => TPageParam | undefined | null`
  - **필수**
  - 이 query에 대한 새로운 데이터가 수신되면 이 함수는 무한한 데이터 목록의 마지막 페이지와 모든 페이지의 전체 배열 및 pageParam 정보를 모두 수신합니다.
  - query 함수에 마지막 선택적 매개변수로 전달될 **단일 변수**를 반환해야 합니다.
  - 사용 가능한 다음 페이지가 없음을 나타내려면 `undefined` 또는 `null`를 반환합니다.

- **반환값**

`usePrefetchInfiniteQuery`는 아무 것도 반환하지 않습니다. [useSuspenseInfiniteQuery](useSuspenseInfiniteQuery.md)를 사용하는 구성 요소를 래핑하는 suspense 경계 전에 렌더링 중에 프리페치를 실행하는 데만 사용해야 합니다.