---
id: CreateMutationOptions
title: CreateMutationOptions
---




# 타입 별칭: CreateMutationOptions\<TData, TError, TVariables, TOnMutateResult\>

```ts
type CreateMutationOptions<TData, TError, TVariables, TOnMutateResult> = OmitKeyof<MutationObserverOptions<TData, TError, TVariables, TOnMutateResult>, "_defaulted">;
```
정의 위치: [packages/svelte-query/src/types.ts:86](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L86)

createMutation에 대한 옵션

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### T변수

`TVariables` = `void`

### TOnMutateResult

`TOnMutateResult` = `unknown`