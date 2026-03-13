---
id: CreateBaseMutationResult
title: CreateBaseMutationResult
---




# 타입 별칭: CreateBaseMutationResult\<TData, TError, TVariables, TOnMutateResult\>

```ts
type CreateBaseMutationResult<TData, TError, TVariables, TOnMutateResult> = Override<MutationObserverResult<TData, TError, TVariables, TOnMutateResult>, {
  mutate: CreateMutateFunction<TData, TError, TVariables, TOnMutateResult>;
}> & object;
```
정의 위치: [types.ts:160](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L160)

## 유형 선언

### mutateAsync

```ts
mutateAsync: CreateMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult>;
```
## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### T변수

`TVariables` = `unknown`

### TOnMutateResult

`TOnMutateResult` = `unknown`