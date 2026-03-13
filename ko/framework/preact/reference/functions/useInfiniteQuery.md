---
id: useInfiniteQuery
title: useInfiniteQuery
---




# 함수: useInfiniteQuery()

## 호출 시그니처

```ts
function useInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): DefinedUseInfiniteQueryResult<TData, TError>;
```
정의 위치: [preact-query/src/useInfiniteQuery.ts:20](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useInfiniteQuery.ts#L20)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData`

#### TError

`TError` = `Error`

#### TData

`TData` = `InfiniteData`\<`TQueryFnData`, `unknown`\>

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

#### TPageParam

`TPageParam` = `unknown`

### 매개변수

#### 옵션

[DefinedInitialDataInfiniteOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/DefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

#### queryClient?

`QueryClient`

### 반환값

[DefinedUseInfiniteQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/DefinedUseInfiniteQueryResult.md)\<`TData`, `TError`\>

## 호출 시그니처

```ts
function useInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): UseInfiniteQueryResult<TData, TError>;
```
정의 위치: [preact-query/src/useInfiniteQuery.ts:37](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useInfiniteQuery.ts#L37)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData`

#### TError

`TError` = `Error`

#### TData

`TData` = `InfiniteData`\<`TQueryFnData`, `unknown`\>

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

#### TPageParam

`TPageParam` = `unknown`

### 매개변수

#### 옵션

[UndefinedInitialDataInfiniteOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/UndefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

#### queryClient?

`QueryClient`

### 반환값

[UseInfiniteQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseInfiniteQueryResult.md)\<`TData`, `TError`\>

## 호출 시그니처

```ts
function useInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options, queryClient?): UseInfiniteQueryResult<TData, TError>;
```
정의 위치: [preact-query/src/useInfiniteQuery.ts:54](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useInfiniteQuery.ts#L54)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData`

#### TError

`TError` = `Error`

#### TData

`TData` = `InfiniteData`\<`TQueryFnData`, `unknown`\>

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

#### TPageParam

`TPageParam` = `unknown`

### 매개변수

#### 옵션

[UseInfiniteQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

#### queryClient?

`QueryClient`

### 반환값

[UseInfiniteQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseInfiniteQueryResult.md)\<`TData`, `TError`\>
