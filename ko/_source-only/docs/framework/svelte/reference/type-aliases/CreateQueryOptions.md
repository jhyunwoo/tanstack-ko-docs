---
id: CreateQueryOptions
title: CreateQueryOptions
---




# 타입 별칭: CreateQueryOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> = CreateBaseQueryOptions<TQueryFnData, TError, TData, TQueryFnData, TQueryKey>;
```
정의 위치: [packages/svelte-query/src/types.ts:39](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L39)

createQuery 옵션

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`