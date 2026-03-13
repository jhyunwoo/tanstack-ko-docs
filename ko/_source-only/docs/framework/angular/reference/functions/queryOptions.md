---
id: queryOptions
title: queryOptions
---




# 함수: queryOptions()

유형이 안전한 방식으로 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

**예**

```ts
 const { queryKey } = queryOptions({
    queryKey: ['key'],
    queryFn: () => Promise.resolve(5),
    //  ^?  Promise<번호>
  })

  const queryClient = new QueryClient()
  const data = queryClient.getQueryData(queryKey)
  //    ^?  번호 | 한정되지 않은
```
## 매개변수

`queryFn`의 유형으로 태그를 지정하는 query 옵션입니다.

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): Omit<CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object & object;
```
정의 위치: [query-options.ts:76](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/query-options.ts#L76)

유형이 안전한 방식으로 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

**예**

```ts
 const { queryKey } = queryOptions({
    queryKey: ['key'],
    queryFn: () => Promise.resolve(5),
    //  ^?  Promise<번호>
  })

  const queryClient = new QueryClient()
  const data = queryClient.getQueryData(queryKey)
  //    ^?  번호 | 한정되지 않은
```
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

[DefinedInitialDataOptions](../type-aliases/DefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

`queryFn`의 유형으로 태그를 지정하는 query 옵션입니다.

### 반환값

`Omit`\<[CreateQueryOptions](../interfaces/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>, `"queryFn"`\> & `object` & `object`

태그가 지정된 query 옵션.

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): OmitKeyof<CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey>, "queryFn"> & object & object;
```
정의 위치: [query-options.ts:108](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/query-options.ts#L108)

유형이 안전한 방식으로 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

**예**

```ts
 const { queryKey } = queryOptions({
    queryKey: ['key'],
    queryFn: () => Promise.resolve(5),
    //  ^?  Promise<번호>
  })

  const queryClient = new QueryClient()
  const data = queryClient.getQueryData(queryKey)
  //    ^?  번호 | 한정되지 않은
```
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

[UnusedSkipTokenOptions](../type-aliases/UnusedSkipTokenOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

`queryFn`의 유형으로 태그를 지정하는 query 옵션입니다.

### 반환값

`OmitKeyof`\<[CreateQueryOptions](../interfaces/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>, `"queryFn"`\> & `object` & `object`

태그가 지정된 query 옵션.

## 호출 시그니처

```ts
function queryOptions<TQueryFnData, TError, TData, TQueryKey>(options): CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey> & object & object;
```
정의 위치: [query-options.ts:140](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/query-options.ts#L140)

유형이 안전한 방식으로 query 옵션을 공유하고 재사용할 수 있습니다.

`queryKey`에는 `queryFn` 유형으로 태그가 지정됩니다.

**예**

```ts
 const { queryKey } = queryOptions({
    queryKey: ['key'],
    queryFn: () => Promise.resolve(5),
    //  ^?  Promise<번호>
  })

  const queryClient = new QueryClient()
  const data = queryClient.getQueryData(queryKey)
  //    ^?  번호 | 한정되지 않은
```
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

[UndefinedInitialDataOptions](../type-aliases/UndefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

`queryFn`의 유형으로 태그를 지정하는 query 옵션입니다.

### 반환값

[CreateQueryOptions](../interfaces/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\> & `object` & `object`

태그가 지정된 query 옵션.
