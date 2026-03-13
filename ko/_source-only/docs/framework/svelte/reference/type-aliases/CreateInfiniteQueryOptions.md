---
id: CreateInfiniteQueryOptions
title: CreateInfiniteQueryOptions
---




# 타입 별칭: CreateInfiniteQueryOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

```ts
type CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> = InfiniteQueryObserverOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>;
```
정의 위치: [packages/svelte-query/src/types.ts:53](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L53)

createInfiniteQuery 옵션

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`

### TPageParam

`TPageParam` = `unknown`