---
id: usePrefetchQuery
title: usePrefetchQuery
---





```tsx
usePrefetchQuery(options)
```
**옵션**

[QueryClient](../../../reference/QueryClient.md#queryclientprefetchquery)에 전달할 수 있는 모든 것을 `usePrefetchQuery`에 전달할 수 있습니다. 그 중 일부는 아래와 같이 필요하다는 점을 기억하세요.

- `queryKey: QueryKey`
  - **필수**
  - 렌더링 중에 프리페치할 query 키

- `queryFn: (context: QueryFunctionContext) => Promise<TData>`
  - **필수이지만 기본 query 함수가 정의되지 않은 경우에만** 자세한 내용은 [기본 Query 함수](../guides/default-query-function.md)를 참조하세요.

**보고**

`usePrefetchQuery`는 아무 것도 반환하지 않습니다. [useSuspenseQuery](useSuspenseQuery.md)를 사용하는 구성 요소를 래핑하는 suspense 경계 이전에 렌더링 중에 프리페치를 실행하는 데만 사용해야 합니다.