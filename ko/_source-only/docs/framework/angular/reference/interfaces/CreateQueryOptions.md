---
id: CreateQueryOptions
title: CreateQueryOptions
---




# 인터페이스: CreateQueryOptions\<TQueryFnData, TError, TData, TQueryKey\>

정의 위치: [types.ts:35](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L35)

## 확장

- `OmitKeyof`\<[CreateBaseQueryOptions](CreateBaseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryFnData`, `TQueryKey`\>, `"suspense"`\>

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`