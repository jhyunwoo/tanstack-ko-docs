---
id: useMutation
title: useMutation
---




# 함수: useMutation()

```ts
function useMutation<TData, TError, TVariables, TOnMutateResult>(options, queryClient?): UseMutationResult<TData, TError, TVariables, TOnMutateResult>;
```
정의 위치: [preact-query/src/useMutation.ts:19](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useMutation.ts#L19)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `Error`

### T변수

`TVariables` = `void`

### TOnMutateResult

`TOnMutateResult` = `unknown`

## 매개변수

### 옵션

[UseMutationOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>

### queryClient?

`QueryClient`

## 반환값

[UseMutationResult](../../../../_source-only/docs/framework/preact/reference/type-aliases/UseMutationResult.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>