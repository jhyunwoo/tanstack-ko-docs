---
id: createQuery
title: createQuery
---




# 함수: createQuery()

## 호출 시그니처

```ts
function createQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): CreateQueryResult<TData, TError>;
```
정의 위치: [packages/svelte-query/src/createQuery.ts:15](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createQuery.ts#L15)

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

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<[UndefinedInitialDataOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/UndefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>\>

#### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

### 반환값

[CreateQueryResult](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateQueryResult.md)\<`TData`, `TError`\>

## 호출 시그니처

```ts
function createQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): DefinedCreateQueryResult<TData, TError>;
```
정의 위치: [packages/svelte-query/src/createQuery.ts:27](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createQuery.ts#L27)

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

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<[DefinedInitialDataOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/DefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>\>

#### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

### 반환값

[DefinedCreateQueryResult](../../../../_source-only/docs/framework/svelte/reference/type-aliases/DefinedCreateQueryResult.md)\<`TData`, `TError`\>

## 호출 시그니처

```ts
function createQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): CreateQueryResult<TData, TError>;
```
정의 위치: [packages/svelte-query/src/createQuery.ts:39](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createQuery.ts#L39)

### 타입 매개변수

#### TQueryFnData

`TQueryFnData`

#### TError

`TError` = `Error`

#### TData

`TData` = `TQueryFnData`

#### TQueryKey

`TQueryKey` *extends* readonly `unknown`[] = readonly `unknown`[]

### 매개변수

#### 옵션

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<[CreateQueryOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>\>

#### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

### 반환값

[CreateQueryResult](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateQueryResult.md)\<`TData`, `TError`\>
