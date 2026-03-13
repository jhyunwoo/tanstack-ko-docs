---
id: DefinedInitialDataInfiniteOptions
title: DefinedInitialDataInfiniteOptions
---




# 타입 별칭: DefinedInitialDataInfiniteOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

```ts
type DefinedInitialDataInfiniteOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> = UseInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object;
```
정의 위치: [preact-query/src/infiniteQueryOptions.ts:56](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/infiniteQueryOptions.ts#L56)

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