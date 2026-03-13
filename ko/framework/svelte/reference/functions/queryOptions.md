---
id: queryOptions
title: queryOptions
---




# 함수: queryOptions()

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object & object;
```
정의 위치: [packages/svelte-query/src/queryOptions.ts:30](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/queryOptions.ts#L30)

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

[DefinedInitialDataOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/DefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### 반환값

[CreateQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\> & `object` & `object`

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object & object;
```
정의 위치: [packages/svelte-query/src/queryOptions.ts:41](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/queryOptions.ts#L41)

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

[UndefinedInitialDataOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/UndefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

### 반환값

[CreateQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\> & `object` & `object`
