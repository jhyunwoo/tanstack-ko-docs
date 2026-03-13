---
id: infiniteQueryOptions
title: infiniteQueryOptions
---




# 함수: infiniteQueryOptions()

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): UseInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object & object;
```
정의 위치: [preact-query/src/infiniteQueryOptions.ts:75](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/infiniteQueryOptions.ts#L75)

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

### 반환값

[UseInfiniteQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\> & `object` & `object`

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): OmitKeyof<UseInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>, "queryFn"> & object & object;
```
정의 위치: [preact-query/src/infiniteQueryOptions.ts:99](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/infiniteQueryOptions.ts#L99)

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

[UnusedSkipTokenInfiniteOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/UnusedSkipTokenInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

### 반환값

`OmitKeyof`\<[UseInfiniteQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>, `"queryFn"`\> & `object` & `object`

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): UseInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object & object;
```
정의 위치: [preact-query/src/infiniteQueryOptions.ts:123](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/infiniteQueryOptions.ts#L123)

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

### 반환값

[UseInfiniteQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\> & `object` & `object`
