---
id: CreateMutationResult
title: CreateMutationResult
---




# 타입 별칭: CreateMutationResult\<TData, TError, TVariables, TOnMutateResult, TState\>

```ts
type CreateMutationResult<TData, TError, TVariables, TOnMutateResult, TState> = BaseMutationNarrowing<TData, TError, TVariables, TOnMutateResult> & MapToSignals<OmitKeyof<TState, keyof BaseMutationNarrowing, "safely">>;
```
정의 위치: [types.ts:266](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L266)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### T변수

`TVariables` = `unknown`

### TOnMutateResult

`TOnMutateResult` = `unknown`

### TState

`TState` = `CreateStatusBasedMutationResult`\<[CreateBaseMutationResult](CreateBaseMutationResult.md)\[`"status"`\], `TData`, `TError`, `TVariables`, `TOnMutateResult`\>