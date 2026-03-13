---
id: DefinedInitialDataOptions
title: DefinedInitialDataOptions
---




# 타입 별칭: DefinedInitialDataOptions\<TQueryFnData, TError, TData, TQueryKey\>

```ts
type DefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey> = Omit<UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object;
```
정의 위치: [preact-query/src/queryOptions.ts:40](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L40)

## 유형 선언

### initialData

```ts
initialData: 
  | NonUndefinedGuard<TQueryFnData>
| () => NonUndefinedGuard<TQueryFnData>;
```
### queryFn?

```ts
optional queryFn: QueryFunction<TQueryFnData, TQueryKey>;
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