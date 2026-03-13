---
id: infiniteQueryOptions
title: infiniteQueryOptions
---




# 함수: infiniteQueryOptions()

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>;
```
정의 위치: [packages/svelte-query/src/infiniteQueryOptions.ts:4](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/infiniteQueryOptions.ts#L4)

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

[CreateInfiniteQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

## 반환값

[CreateInfiniteQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>