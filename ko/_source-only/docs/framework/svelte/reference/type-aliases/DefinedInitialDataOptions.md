---
id: DefinedInitialDataOptions
title: DefinedInitialDataOptions
---




# 타입 별칭: DefinedInitialDataOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type DefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey> = CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object;
```
정의 위치: [packages/svelte-query/src/queryOptions.ts:19](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/queryOptions.ts#L19)

## 유형 선언

### initialData

```ts
initialData: 
  | NonUndefinedGuard<TQueryFnData>
| () => NonUndefinedGuard<TQueryFnData>;
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