---
id: usePrefetchQuery
title: usePrefetchQuery
---




# 함수: usePrefetchQuery()

```ts
function usePrefetchQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): void;
```
정의 위치: [preact-query/src/usePrefetchQuery.tsx:5](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/usePrefetchQuery.tsx#L5)

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `Error`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

## 매개변수

### 옵션

[UsePrefetchQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UsePrefetchQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### queryClient?

`QueryClient`

## 반환값

`void`