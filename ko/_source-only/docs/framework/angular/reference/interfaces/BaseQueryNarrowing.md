---
id: BaseQueryNarrowing
title: BaseQueryNarrowing
---




# 인터페이스: BaseQueryNarrowing\<TData, TError\>

정의 위치: [types.ts:57](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L57)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

## 속성

### isError()

```ts
isError: (this) => this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"error", TData, TError>>;
```
정의 위치: [types.ts:65](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L65)

#### 매개변수

##### 이것

[CreateBaseQueryResult](../type-aliases/CreateBaseQueryResult.md)\<`TData`, `TError`\>

#### 반환값

`this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"error", TData, TError>>`

***

### isPending()

```ts
isPending: (this) => this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"pending", TData, TError>>;
```
정의 위치: [types.ts:72](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L72)

#### 매개변수

##### 이것

[CreateBaseQueryResult](../type-aliases/CreateBaseQueryResult.md)\<`TData`, `TError`\>

#### 반환값

`this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"pending", TData, TError>>`

***

### isSuccess()

```ts
isSuccess: (this) => this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"success", TData, TError>>;
```
정의 위치: [types.ts:58](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L58)

#### 매개변수

##### 이것

[CreateBaseQueryResult](../type-aliases/CreateBaseQueryResult.md)\<`TData`, `TError`\>

#### 반환값

`this is CreateBaseQueryResult<TData, TError, CreateStatusBasedQueryResult<"success", TData, TError>>`