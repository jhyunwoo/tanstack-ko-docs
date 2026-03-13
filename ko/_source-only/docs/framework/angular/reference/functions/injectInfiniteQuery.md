---
id: injectInfiniteQuery
title: injectInfiniteQuery
---




# 함수: injectInfiniteQuery()

무한한 query를 삽입합니다. 고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성입니다.
Infinite queries는 기존 데이터 세트에 추가로 "더 많은 데이터를 로드"하거나 "무한 스크롤"할 수 있습니다.

## 매개변수

무한한 query 옵션을 반환하는 함수입니다.

## 매개변수

추가 구성.

## 호출 시그니처

```ts
function injectInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(injectInfiniteQueryFn, options?): DefinedCreateInfiniteQueryResult<TData, TError>;
```
정의 위치: [inject-infinite-query.ts:41](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-infinite-query.ts#L41)

무한한 query를 삽입합니다. 고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성입니다.
Infinite queries는 기존 데이터 세트에 추가로 "더 많은 데이터를 로드"하거나 "무한 스크롤"할 수 있습니다.

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

#### injectInfiniteQueryFn

() => [DefinedInitialDataInfiniteOptions](../type-aliases/DefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

무한한 query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectInfiniteQueryOptions](../interfaces/InjectInfiniteQueryOptions.md)

추가 구성.

### 반환값

[DefinedCreateInfiniteQueryResult](../type-aliases/DefinedCreateInfiniteQueryResult.md)\<`TData`, `TError`\>

무한한 query 결과입니다.

## 호출 시그니처

```ts
function injectInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(injectInfiniteQueryFn, options?): CreateInfiniteQueryResult<TData, TError>;
```
정의 위치: [inject-infinite-query.ts:65](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-infinite-query.ts#L65)

무한한 query를 삽입합니다. 고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성입니다.
Infinite queries는 기존 데이터 세트에 추가로 "더 많은 데이터를 로드"하거나 "무한 스크롤"할 수 있습니다.

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

#### injectInfiniteQueryFn

() => [UndefinedInitialDataInfiniteOptions](../type-aliases/UndefinedInitialDataInfiniteOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

무한한 query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectInfiniteQueryOptions](../interfaces/InjectInfiniteQueryOptions.md)

추가 구성.

### 반환값

[CreateInfiniteQueryResult](../type-aliases/CreateInfiniteQueryResult.md)\<`TData`, `TError`\>

무한한 query 결과입니다.

## 호출 시그니처

```ts
function injectInfiniteQuery<TQueryFnData, TError, TData, TQueryKey, TPageParam>(injectInfiniteQueryFn, options?): CreateInfiniteQueryResult<TData, TError>;
```
정의 위치: [inject-infinite-query.ts:89](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-infinite-query.ts#L89)

무한한 query를 삽입합니다. 고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성입니다.
Infinite queries는 기존 데이터 세트에 추가로 "더 많은 데이터를 로드"하거나 "무한 스크롤"할 수 있습니다.

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

#### injectInfiniteQueryFn

() => [CreateInfiniteQueryOptions](../interfaces/CreateInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>

무한한 query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectInfiniteQueryOptions](../interfaces/InjectInfiniteQueryOptions.md)

추가 구성.

### 반환값

[CreateInfiniteQueryResult](../type-aliases/CreateInfiniteQueryResult.md)\<`TData`, `TError`\>

무한한 query 결과입니다.
