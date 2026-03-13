---
id: infiniteQueryOptions
title: infiniteQueryOptions
---




# 함수: infiniteQueryOptions()

유형이 안전한 방식으로 무한한 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

## 매개변수

`queryFn` 유형으로 태그를 지정하는 무한 query 옵션입니다.

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object & object;
```
정의 위치: [infinite-query-options.ts:88](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L88)

유형이 안전한 방식으로 무한한 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

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

[DefinedInitialDataInfiniteOptions](../type-aliases/DefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

`queryFn` 유형으로 태그를 지정하는 무한 query 옵션입니다.

### 반환값

[CreateInfiniteQueryOptions](../interfaces/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\> & `object` & `object`

태그가 붙은 무한 query 옵션.

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): OmitKeyof<CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>, "queryFn"> & object & object;
```
정의 위치: [infinite-query-options.ts:119](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L119)

유형이 안전한 방식으로 무한한 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

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

[UnusedSkipTokenInfiniteOptions](../type-aliases/UnusedSkipTokenInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

`queryFn` 유형으로 태그를 지정하는 무한 query 옵션입니다.

### 반환값

`OmitKeyof`\<[CreateInfiniteQueryOptions](../interfaces/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>, `"queryFn"`\> & `object` & `object`

태그가 붙은 무한 query 옵션.

## 호출 시그니처

```ts
function infiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam>(options): CreateInfiniteQueryOptions<TQueryFnData, TError, TData, TQueryKey, TPageParam> & object & object;
```
정의 위치: [infinite-query-options.ts:150](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/infinite-query-options.ts#L150)

유형이 안전한 방식으로 무한한 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

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

[UndefinedInitialDataInfiniteOptions](../type-aliases/UndefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

`queryFn` 유형으로 태그를 지정하는 무한 query 옵션입니다.

### 반환값

[CreateInfiniteQueryOptions](../interfaces/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\> & `object` & `object`

태그가 붙은 무한 query 옵션.
