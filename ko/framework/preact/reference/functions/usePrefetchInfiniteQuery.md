---
id: usePrefetchInfiniteQuery
title: usePrefetchInfiniteQuery
---




# 함수: usePrefetchInfiniteQuery()

```ts
function usePrefetchInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): void;
```
정의 위치: [preact-query/src/usePrefetchInfiniteQuery.tsx:9](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/usePrefetchInfiniteQuery.tsx#L9)

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `Error`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### TPageParam

`TPageParam` = `unknown`

## 매개변수

### 옵션

`FetchInfiniteQueryOptions`\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

### queryClient?

`QueryClient`

## 반환값

`void`