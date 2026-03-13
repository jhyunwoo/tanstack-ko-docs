---
id: CreateBaseQueryOptions
title: CreateBaseQueryOptions
---




# 타입 별칭: CreateBaseQueryOptions\<TQueryFnData, TError, TData, TQueryData, TQueryKey\>

```ts
type CreateBaseQueryOptions<TQueryFnData, TError, TData, TQueryData, TQueryKey> = QueryObserverOptions<TQueryFnData, TError, TData, TQueryData, TQueryKey>;
```
정의 위치: [packages/svelte-query/src/types.ts:24](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L24)

createBaseQuery 옵션

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryData

`TQueryData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`