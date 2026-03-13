---
id: queryOptions
title: queryOptions
---




# 함수: queryOptions()

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): Omit<UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object & object;
```
정의 위치: [preact-query/src/queryOptions.ts:52](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L52)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData` = `unknown`

#### TError

`TError` = `Error`

#### TData

`TData` = `TQueryFnData`

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### 매개변수

#### 옵션

[DefinedInitialDataOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/DefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### 반환값

`Omit`\<[UseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>, `"queryFn"`\> & `object` & `object`

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): OmitKeyof<UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object & object;
```
정의 위치: [preact-query/src/queryOptions.ts:63](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L63)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData` = `unknown`

#### TError

`TError` = `Error`

#### TData

`TData` = `TQueryFnData`

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### 매개변수

#### 옵션

[UnusedSkipTokenOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/UnusedSkipTokenOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### 반환값

`OmitKeyof`\<[UseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>, `"queryFn"`\> & `object` & `object`

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): UseQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object & object;
```
정의 위치: [preact-query/src/queryOptions.ts:74](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/queryOptions.ts#L74)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData` = `unknown`

#### TError

`TError` = `Error`

#### TData

`TData` = `TQueryFnData`

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### 매개변수

#### 옵션

[UndefinedInitialDataOptions](../../../../_source-only/docs/framework/preact/reference/type-aliases/UndefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### 반환값

[UseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\> & `object` & `object`
