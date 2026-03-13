---
id: UndefinedInitialDataOptions
title: UndefinedInitialDataOptions
---




# 타입 별칭: UndefinedInitialDataOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type UndefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey> = CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object;
```
정의 위치: [packages/svelte-query/src/queryOptions.ts:10](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/queryOptions.ts#L10)

## 유형 선언

### initialData?

```ts
optional initialData: InitialDataFunction<NonUndefinedGuard<TQueryFnData>>;
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