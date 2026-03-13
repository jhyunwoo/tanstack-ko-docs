---
id: UseBaseMutationResult
title: UseBaseMutationResult
---




# 타입 별칭: UseBaseMutationResult\<TData, TError, TVariables, TOnMutateResult\>

```ts
type UseBaseMutationResult<TData, TError, TVariables, TOnMutateResult> = Override<MutationObserverResult<TData, TError, TVariables, TOnMutateResult>, {
  mutate: UseMutateFunction<TData, TError, TVariables, TOnMutateResult>;
}> & object;
```
정의 위치: [preact-query/src/types.ts:220](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L220)

## 유형 선언

### mutateAsync

```ts
mutateAsync: UseMutateAsyncFunction<TData, TError, TVariables, TOnMutateResult>;
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