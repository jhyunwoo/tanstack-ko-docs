---
id: useInfiniteQuery
title: useInfiniteQuery
---





```tsx
const {
  fetchNextPage,
  fetchPreviousPage,
  hasNextPage,
  hasPreviousPage,
  isFetchingNextPage,
  isFetchingPreviousPage,
  promise,
  ...result
} = useInfiniteQuery({
  queryKey,
  queryFn: ({ pageParam }) => fetchPage(pageParam),
  initialPageParam: 1,
  ...options,
  getNextPageParam: (lastPage, allPages, lastPageParam, allPageParams) =>
    lastPage.nextCursor,
  getPreviousPageParam: (firstPage, allPages, firstPageParam, allPageParams) =>
    firstPage.prevCursor,
})
```
**옵션**

`useInfiniteQuery`에 대한 옵션은 다음을 추가하면 [useQuery](useQuery.md)와 동일합니다.

- `queryFn: (context: QueryFunctionContext) => Promise<TData>`
  - **필수이지만 기본 query 기능이 정의되지 않은 경우에만** [`defaultQueryFn`](../guides/default-query-function.md)
  - query가 데이터를 요청하는 데 사용할 기능입니다.
  - [QueryFunctionContext](../guides/query-functions.md#queryfunctioncontext)를 수신합니다.
  - 데이터를 해결하거나 오류를 발생시키는 Promise를 반환해야 합니다.
- `initialPageParam: TPageParam`
  - **필수**
  - 첫 번째 페이지를 가져올 때 사용할 기본 페이지 매개변수입니다.
- `getNextPageParam: (lastPage, allPages, lastPageParam, allPageParams) => TPageParam | undefined | null`
  - **필수**
  - 이 query에 대한 새로운 데이터가 수신되면 이 함수는 무한한 데이터 목록의 마지막 페이지와 모든 페이지의 전체 배열 및 pageParam 정보를 모두 수신합니다.
  - query 함수에 마지막 선택적 매개변수로 전달될 **단일 변수**를 반환해야 합니다.
  - 사용 가능한 다음 페이지가 없음을 나타내려면 `undefined` 또는 `null`를 반환합니다.
- `getPreviousPageParam: (firstPage, allPages, firstPageParam, allPageParams) => TPageParam | undefined | null`
  - 이 query에 대한 새로운 데이터가 수신되면 이 함수는 무한 데이터 목록의 첫 번째 페이지와 모든 페이지의 전체 배열 및 pageParam 정보를 모두 수신합니다.
  - query 함수에 마지막 선택적 매개변수로 전달될 **단일 변수**를 반환해야 합니다.
  - `undefined` 또는 `null`를 반환하여 사용 가능한 이전 페이지가 없음을 나타냅니다.
- `maxPages: number | undefined`
  - 무한 query 데이터에 저장할 수 있는 최대 페이지 수입니다.
  - 최대 페이지 수에 도달한 경우 새 페이지를 가져오면 지정된 방향에 따라 페이지 배열에서 첫 번째 또는 마지막 페이지가 제거됩니다.
  - `undefined` 또는 `0`와 같으면 페이지 수는 무제한입니다.
  - 기본값은 `undefined`입니다.
  - 필요할 때 양방향으로 페이지를 가져올 수 있도록 `maxPages` 값이 `0`보다 큰 경우 `getNextPageParam` 및 `getPreviousPageParam`를 올바르게 정의해야 합니다.

**보고**

`useInfiniteQuery`에 대해 반환된 속성은 [useQuery](useQuery.md)와 동일하지만 다음 속성이 추가되고 `isRefetching` 및 `isRefetchError`에 약간의 차이가 있습니다.

- `data.pages: TData[]`
  - 모든 페이지를 포함하는 배열입니다.
- `data.pageParams: unknown[]`
  - 모든 페이지 매개변수를 포함하는 배열입니다.
- `isFetchingNextPage: boolean`
  - `fetchNextPage`로 다음 페이지를 가져오는 동안 `true`가 됩니다.
- `isFetchingPreviousPage: boolean`
  - `fetchPreviousPage`로 이전 페이지를 가져오는 동안 `true`가 됩니다.
- `fetchNextPage: (options?: FetchNextPageOptions) => Promise<UseInfiniteQueryResult>`
  - 이 기능을 사용하면 결과의 다음 "페이지"를 가져올 수 있습니다.
  - `options.cancelRefetch: boolean`를 `true`로 설정하면 `fetchNextPage`를 반복적으로 호출하면 이전 호출 여부에 관계없이 매번 `queryFn`가 호출됩니다.
    호출이 해결되었는지 여부. 또한 이전 호출의 결과는 무시됩니다. `false`로 설정된 경우 `fetchNextPage` 호출
    첫 번째 호출이 해결될 때까지 반복적으로 아무런 효과가 없습니다. 기본값은 `true`입니다.
- `fetchPreviousPage: (options?: FetchPreviousPageOptions) => Promise<UseInfiniteQueryResult>`
  - 이 기능을 사용하면 이전 결과 "페이지"를 가져올 수 있습니다.
  - `options.cancelRefetch: boolean` `fetchNextPage`와 동일합니다.
- `hasNextPage: boolean`
  - 가져올 다음 페이지가 있는 경우 `true`가 됩니다(`getNextPageParam` 옵션을 통해 알 수 있음).
- `hasPreviousPage: boolean`
  - 가져올 이전 페이지가 있는 경우 `true`가 됩니다(`getPreviousPageParam` 옵션을 통해 알려짐).
- `isFetchNextPageError: boolean`
  - 다음 페이지를 가져오는 동안 query가 실패한 경우 `true`가 됩니다.
- `isFetchPreviousPageError: boolean`
  - 이전 페이지를 가져오는 동안 query가 실패한 경우 `true`가 됩니다.
- `isRefetching: boolean`
  - 백그라운드 다시 가져오기가 진행 중일 때마다 `true`가 됩니다. 여기에는 초기 `pending`나 다음 또는 이전 페이지 가져오기가 포함되지 _않습니다_
  - `isFetching && !isPending && !isFetchingNextPage && !isFetchingPreviousPage`와 동일합니다.
- `isRefetchError: boolean`
  - 페이지를 다시 가져오는 동안 query가 실패한 경우 `true`가 됩니다.
- `promise: Promise<TData>`
  - query 결과로 해결되는 안정적인 Promise입니다.
  - `React.use()`와 함께 사용하여 데이터를 가져올 수 있습니다.
  - `QueryClient`에서 활성화하려면 `experimental_prefetchInRender` 기능 플래그가 필요합니다.

`fetchNextPage`와 같은 명령형 가져오기 호출은 기본 다시 가져오기 동작을 방해하여 오래된 데이터를 초래할 수 있다는 점에 유의하세요. 사용자 작업에 대한 응답으로만 이러한 함수를 호출하거나 `hasNextPage && !isFetching`와 같은 조건을 추가하세요.