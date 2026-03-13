---
id: useQuery
title: useQuery
---




# 함수: useQuery()

## 호출 시그니처

```ts
function useQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): DefinedUseQueryResult<NoInfer<TData>, TError>;
```
정의 위치: [preact-query/src/useQuery.ts:19](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQuery.ts#L19)

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

#### queryClient?

`QueryClient`

### 반환값

[DefinedUseQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/DefinedUseQueryResult.md)\<`NoInfer`\<`TData`\>, `TError`\>

## 호출 시그니처

```ts
function useQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): UseQueryResult<NoInfer<TData>, TError>;
```
정의 위치: [preact-query/src/useQuery.ts:29](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQuery.ts#L29)

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

#### queryClient?

`QueryClient`

### 반환값

[UseQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseQueryResult.md)\<`NoInfer`\<`TData`\>, `TError`\>

## 호출 시그니처

```ts
function useQuery<TQueryFnData, TError, TData, TQueryKey>(options, queryClient?): UseQueryResult<NoInfer<TData>, TError>;
```
정의 위치: [preact-query/src/useQuery.ts:39](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQuery.ts#L39)

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

[UseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

#### queryClient?

`QueryClient`

### 반환값

[UseQueryResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseQueryResult.md)\<`NoInfer`\<`TData`\>, `TError`\>
