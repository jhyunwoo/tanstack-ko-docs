---
id: useSuspenseInfiniteQuery
title: useSuspenseInfiniteQuery
---




# 함수: useSuspenseInfiniteQuery()

```ts
function useSuspenseInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): UseSuspenseInfiniteQueryResult<TData, TError>;
```
정의 위치: [preact-query/src/useSuspenseInfiniteQuery.ts:17](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseInfiniteQuery.ts#L17)

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

[UseSuspenseInfiniteQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

### queryClient?

`QueryClient`

## 반환값

[UseSuspenseInfiniteQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseSuspenseInfiniteQueryResult.md)\<`TData`, `TError`\>