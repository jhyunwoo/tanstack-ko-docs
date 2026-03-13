---
id: infiniteQueryOptions
title: infiniteQueryOptions
---





```tsx
infiniteQueryOptions({
  queryKey,
  ...options,
})
```
**옵션**

일반적으로 [useInfiniteQuery](../../react/reference/useInfiniteQuery.md)에도 전달할 수 있는 모든 것을 `infiniteQueryOptions`에 전달할 수 있습니다. 일부 옵션은 `queryClient.prefetchInfiniteQuery`와 같은 함수로 전달될 때 아무런 효과가 없지만 TypeScript는 이러한 초과 속성에도 여전히 문제가 없습니다.

- `queryKey: QueryKey`
  - **필수**
  - 옵션을 생성할 query 키입니다.

자세한 내용은 [useInfiniteQuery](../../react/reference/useInfiniteQuery.md)를 참조하세요.