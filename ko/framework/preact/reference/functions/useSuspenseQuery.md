---
id: useSuspenseQuery
title: useSuspenseQuery
---




# 함수: useSuspenseQuery()

```ts
function useSuspenseQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): UseSuspenseQueryResult<TData, TError>;
```
정의 위치: [preact-query/src/useSuspenseQuery.ts:7](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseQuery.ts#L7)

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

[UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### queryClient?

`QueryClient`

## 반환값

[UseSuspenseQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseSuspenseQueryResult.md)\<`TData`, `TError`\>