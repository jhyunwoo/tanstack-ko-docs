---
id: UsePrefetchQueryOptions
title: UsePrefetchQueryOptions
---




# 인터페이스: UsePrefetchQueryOptions\<TQueryFnData, TError, TData, TQueryKey\>

정의 위치: [preact-query/src/types.ts:49](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L49)

## 확장

- `OmitKeyof`\<`FetchQueryOptions`\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>, `"queryFn"`\>

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`

## 속성

### queryFn?

```ts
optional queryFn: QueryFunction<TQueryFnData, TQueryKey, never>;
```
정의 위치: [preact-query/src/types.ts:58](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L58)