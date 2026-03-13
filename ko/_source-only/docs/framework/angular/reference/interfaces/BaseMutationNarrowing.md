---
id: BaseMutationNarrowing
title: BaseMutationNarrowing
---




# 인터페이스: BaseMutationNarrowing\<TData, TError, TVariables, TOnMutateResult\>

정의 위치: [types.ts:190](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L190)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### T변수

`TVariables` = `unknown`

### TOnMutateResult

`TOnMutateResult` = `unknown`

## 속성

### isError

```ts
isError: SignalFunction<(this) => this is CreateMutationResult<TData, TError, TVariables, TOnMutateResult, Override<MutationObserverErrorResult<TData, TError, TVariables, TOnMutateResult>, { mutate: CreateMutateFunction<TData, TError, TVariables, TOnMutateResult> }> & { mutateAsync: CreateMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult> }>>;
```
정의 위치: [types.ts:213](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L213)

***

### isIdle

```ts
isIdle: SignalFunction<(this) => this is CreateMutationResult<TData, TError, TVariables, TOnMutateResult, Override<MutationObserverIdleResult<TData, TError, TVariables, TOnMutateResult>, { mutate: CreateMutateFunction<TData, TError, TVariables, TOnMutateResult> }> & { mutateAsync: CreateMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult> }>>;
```
정의 위치: [types.ts:247](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L247)

***

### isPending

```ts
isPending: SignalFunction<(this) => this is CreateMutationResult<TData, TError, TVariables, TOnMutateResult, Override<MutationObserverLoadingResult<TData, TError, TVariables, TOnMutateResult>, { mutate: CreateMutateFunction<TData, TError, TVariables, TOnMutateResult> }> & { mutateAsync: CreateMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult> }>>;
```
정의 위치: [types.ts:230](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L230)

***

### isSuccess

```ts
isSuccess: SignalFunction<(this) => this is CreateMutationResult<TData, TError, TVariables, TOnMutateResult, Override<MutationObserverSuccessResult<TData, TError, TVariables, TOnMutateResult>, { mutate: CreateMutateFunction<TData, TError, TVariables, TOnMutateResult> }> & { mutateAsync: CreateMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult> }>>;
```
정의 위치: [types.ts:196](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L196)