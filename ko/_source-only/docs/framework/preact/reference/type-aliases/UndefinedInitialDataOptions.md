---
id: UndefinedInitialDataOptions
title: UndefinedInitialDataOptions
---




# 타입 별칭: UndefinedInitialDataOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type UndefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey> = UseQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object;
```
정의 위치: [preact-query/src/queryOptions.ts:13](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L13)

## 유형 선언

### initialData?

```ts
optional initialData: 
  | InitialDataFunction<NonUndefinedGuard<TQueryFnData>>
| NonUndefinedGuard<TQueryFnData>;
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