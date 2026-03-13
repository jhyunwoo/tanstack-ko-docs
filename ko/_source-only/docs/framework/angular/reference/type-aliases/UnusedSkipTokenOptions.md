---
id: UnusedSkipTokenOptions
title: UnusedSkipTokenOptions
---




# 타입 별칭: UnusedSkipTokenOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type UnusedSkipTokenOptions<TQueryFnData, TError, TData, TQueryKey> = OmitKeyof<CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object;
```
정의 위치: [query-options.ts:25](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/query-options.ts#L25)

## 유형 선언

### queryFn?

```ts
optional queryFn: Exclude<CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey>["queryFn"], SkipToken | undefined>;
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