---
id: injectQuery
title: injectQuery
---




# 함수: injectQuery()

고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성인 query를 삽입합니다.

**기본 예**```ts
class ServiceOrComponent {
  query = injectQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      this.#http.get<Response>('https://api.github.com/repos/tanstack/query'),
  }))
}
```
Angular의 `computed`와 유사하게 `injectQuery`에 전달된 함수는 반응형 컨텍스트에서 실행됩니다.
아래 예에서는 필터 신호가 변경되면 query가 자동으로 활성화되고 실행됩니다.
진실한 가치로. 필터 신호가 잘못된 값으로 다시 변경되면 query가 비활성화됩니다.

**반응적 예**```ts
class ServiceOrComponent {
  filter = signal('')

  todosQuery = injectQuery(() => ({
    queryKey: ['todos', this.filter()],
    queryFn: () => fetchTodos(this.filter()),
    // 신호는 표현식과 결합될 수 있습니다.
    enabled: !!this.filter(),
  }))
}
```
## 매개변수

query 옵션을 반환하는 함수입니다.

## 매개변수

추가 구성

## 참고
https://tanstack.com/query/latest/docs/framework/angular/guides/queries

## 호출 시그니처

```ts
function injectQuery<TQueryFnData, TError, TData, TQueryKey>(injectQueryFn, options?): DefinedCreateQueryResult<TData, TError>;
```
정의 위치: [inject-query.ts:65](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query.ts#L65)

고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성인 query를 삽입합니다.

**기본 예**```ts
class ServiceOrComponent {
  query = injectQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      this.#http.get<Response>('https://api.github.com/repos/tanstack/query'),
  }))
}
```
Angular의 `computed`와 유사하게 `injectQuery`에 전달된 함수는 반응형 컨텍스트에서 실행됩니다.
아래 예에서는 필터 신호가 변경되면 query가 자동으로 활성화되고 실행됩니다.
진실한 가치로. 필터 신호가 잘못된 값으로 다시 변경되면 query가 비활성화됩니다.

**반응적 예**```ts
class ServiceOrComponent {
  filter = signal('')

  todosQuery = injectQuery(() => ({
    queryKey: ['todos', this.filter()],
    queryFn: () => fetchTodos(this.filter()),
    // 신호는 표현식과 결합될 수 있습니다.
    enabled: !!this.filter(),
  }))
}
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

#### injectQueryFn

() => [DefinedInitialDataOptions](../../../../_source-only/docs/framework/angular/reference/type-aliases/DefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectQueryOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/InjectQueryOptions.md)

추가 구성

### 반환값

[DefinedCreateQueryResult](../../../../_source-only/docs/framework/angular/reference/type-aliases/DefinedCreateQueryResult.md)\<`TData`, `TError`\>

query 결과입니다.

### 참고
https://tanstack.com/query/latest/docs/framework/angular/guides/queries

## 호출 시그니처

```ts
function injectQuery<TQueryFnData, TError, TData, TQueryKey>(injectQueryFn, options?): CreateQueryResult<TData, TError>;
```
정의 위치: [inject-query.ts:116](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query.ts#L116)

고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성인 query를 삽입합니다.

**기본 예**```ts
class ServiceOrComponent {
  query = injectQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      this.#http.get<Response>('https://api.github.com/repos/tanstack/query'),
  }))
}
```
Angular의 `computed`와 유사하게 `injectQuery`에 전달된 함수는 반응형 컨텍스트에서 실행됩니다.
아래 예에서는 필터 신호가 변경되면 query가 자동으로 활성화되고 실행됩니다.
진실한 가치로. 필터 신호가 잘못된 값으로 다시 변경되면 query가 비활성화됩니다.

**반응적 예**```ts
class ServiceOrComponent {
  filter = signal('')

  todosQuery = injectQuery(() => ({
    queryKey: ['todos', this.filter()],
    queryFn: () => fetchTodos(this.filter()),
    // 신호는 표현식과 결합될 수 있습니다.
    enabled: !!this.filter(),
  }))
}
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

#### injectQueryFn

() => [UndefinedInitialDataOptions](../../../../_source-only/docs/framework/angular/reference/type-aliases/UndefinedInitialDataOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectQueryOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/InjectQueryOptions.md)

추가 구성

### 반환값

[CreateQueryResult](../../../../_source-only/docs/framework/angular/reference/type-aliases/CreateQueryResult.md)\<`TData`, `TError`\>

query 결과입니다.

### 참고
https://tanstack.com/query/latest/docs/framework/angular/guides/queries

## 호출 시그니처

```ts
function injectQuery<TQueryFnData, TError, TData, TQueryKey>(injectQueryFn, options?): CreateQueryResult<TData, TError>;
```
정의 위치: [inject-query.ts:167](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query.ts#L167)

고유 키에 연결된 비동기 데이터 소스에 대한 선언적 종속성인 query를 삽입합니다.

**기본 예**```ts
class ServiceOrComponent {
  query = injectQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      this.#http.get<Response>('https://api.github.com/repos/tanstack/query'),
  }))
}
```
Angular의 `computed`와 유사하게 `injectQuery`에 전달된 함수는 반응형 컨텍스트에서 실행됩니다.
아래 예에서는 필터 신호가 변경되면 query가 자동으로 활성화되고 실행됩니다.
진실한 가치로. 필터 신호가 잘못된 값으로 다시 변경되면 query가 비활성화됩니다.

**반응적 예**```ts
class ServiceOrComponent {
  filter = signal('')

  todosQuery = injectQuery(() => ({
    queryKey: ['todos', this.filter()],
    queryFn: () => fetchTodos(this.filter()),
    // 신호는 표현식과 결합될 수 있습니다.
    enabled: !!this.filter(),
  }))
}
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

#### injectQueryFn

() => [CreateQueryOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/CreateQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>

query 옵션을 반환하는 함수입니다.

#### 옵션?

[InjectQueryOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/InjectQueryOptions.md)

추가 구성

### 반환값

[CreateQueryResult](../../../../_source-only/docs/framework/angular/reference/type-aliases/CreateQueryResult.md)\<`TData`, `TError`\>

query 결과입니다.

### 참고
https://tanstack.com/query/latest/docs/framework/angular/guides/queries
