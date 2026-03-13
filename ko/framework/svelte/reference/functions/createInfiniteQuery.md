---
id: createInfiniteQuery
title: createInfiniteQuery
---




# 함수: createInfiniteQuery()

```ts
function createInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): CreateInfiniteQueryResult<TData, TError>;
```
정의 위치: [packages/svelte-query/src/createInfiniteQuery.ts:16](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createInfiniteQuery.ts#L16)

## 타입 매개변수

### TQueryFnData

`TQueryFnData`

### TError

`TError` = `Error`

### TData

`TData` = `InfiniteData`\<`TQueryFnData`, `unknown`\>

### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### TPageParam

`TPageParam` = `unknown`

## 매개변수

### 옵션

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<[CreateInfiniteQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>\>

### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

## 반환값

[CreateInfiniteQueryResult](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateInfiniteQueryResult.md)\<`TData`, `TError`\>