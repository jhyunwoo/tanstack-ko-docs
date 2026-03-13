---
id: UnusedSkipTokenInfiniteOptions
title: UnusedSkipTokenInfiniteOptions
---




# 타입 별칭: UnusedSkipTokenInfiniteOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

```ts
type UnusedSkipTokenInfiniteOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> = OmitKeyof<CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>, "queryFn"> & object;
```
정의 위치: [infinite-query-options.ts:34](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L34)

## 유형 선언

### queryFn?

```ts
optional queryFn: Exclude<CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>["queryFn"], SkipToken | undefined>;
```
## 타입 매개변수

### TQueryFnData

`TQueryFnData`

### TError

`TError` = `DefaultError`

### TData

`TData` = `InfiniteData`\<`TQueryFnData`\>

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`

### TPageParam

`TPageParam` = `unknown`