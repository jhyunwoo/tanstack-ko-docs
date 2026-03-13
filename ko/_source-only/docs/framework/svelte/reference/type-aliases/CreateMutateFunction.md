---
id: CreateMutateFunction
title: CreateMutateFunction
---




# 타입 별칭: CreateMutateFunction()\<TData, TError, TVariables, TOnMutateResult\>

```ts
type CreateMutateFunction<TData, TError, TVariables, TOnMutateResult> = (...args) => void;
```
정의 위치: [packages/svelte-query/src/types.ts:96](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L96)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### T변수

`TVariables` = `void`

### TOnMutateResult

`TOnMutateResult` = `unknown`

## 매개변수

### 인수

...`Parameters`\<`MutateFunction`\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>\>

## 반환값

`void`