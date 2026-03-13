---
id: UseMutateFunction
title: UseMutateFunction
---




# 타입 별칭: UseMutateFunction()\<TData, TError, TVariables, TOnMutateResult\>

```ts
type UseMutateFunction<TData, TError, TVariables, TOnMutateResult> = (...args) => void;
```
정의 위치: [preact-query/src/types.ts:202](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L202)

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