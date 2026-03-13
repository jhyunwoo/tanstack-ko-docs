---
id: UndefinedInitialDataInfiniteOptions
title: UndefinedInitialDataInfiniteOptions
---




# 타입 별칭: UndefinedInitialDataInfiniteOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

```ts
type UndefinedInitialDataInfiniteOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> = CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object;
```
정의 위치: [infinite-query-options.ts:13](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L13)

## 유형 선언

### initialData?

```ts
optional initialData: 
  | NonUndefinedGuard<InfiniteData<TQueryFnData, TPageParam>>
| InitialDataFunction<NonUndefinedGuard<InfiniteData<TQueryFnData, TPageParam>>>;
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