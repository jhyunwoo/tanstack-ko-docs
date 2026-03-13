---
id: UnusedSkipTokenOptions
title: UnusedSkipTokenOptions
---




# 타입 별칭: UnusedSkipTokenOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type UnusedSkipTokenOptions<TQueryFnData, TError, TData, TQueryKey> = OmitKeyof<UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object;
```
정의 위치: [preact-query/src/queryOptions.ts:25](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L25)

## 유형 선언

### queryFn?

```ts
optional queryFn: Exclude<UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>["queryFn"], SkipToken | undefined>;
```
## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`