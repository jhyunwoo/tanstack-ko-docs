---
id: DefinedInitialDataInfiniteOptions
title: DefinedInitialDataInfiniteOptions
---




# 타입 별칭: DefinedInitialDataInfiniteOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

```ts
type DefinedInitialDataInfiniteOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> = CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object;
```
정의 위치: [infinite-query-options.ts:62](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L62)

## 유형 선언

### initialData

```ts
initialData: 
  | NonUndefinedGuard<InfiniteData<TQueryFnData, TPageParam>>
  | () => NonUndefinedGuard<InfiniteData<TQueryFnData, TPageParam>>
  | undefined;
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