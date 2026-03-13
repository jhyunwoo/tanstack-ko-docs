---
id: injectMutation
title: injectMutation
---




# 함수: injectMutation()

```ts
function injectMutation<TData, TError, TVariables, TOnMutateResult>(injectMutationFn, options?): CreateMutationResult<TData, TError, TVariables, TOnMutateResult>;
```
정의 위치: [inject-mutation.ts:45](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-mutation.ts#L45)

mutation를 삽입합니다. 이는 일반적으로 서버 부작용을 수행하는 호출할 수 있는 명령형 함수입니다.

queries와 달리 mutations는 ​​자동으로 실행되지 않습니다.

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

### injectMutationFn

() => [CreateMutationOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>

mutation 옵션을 반환하는 함수입니다.

### 옵션?

[InjectMutationOptions](../../../../_source-only/docs/framework/angular/reference/interfaces/InjectMutationOptions.md)

추가 구성

## 반환값

[CreateMutationResult](../../../../_source-only/docs/framework/angular/reference/type-aliases/CreateMutationResult.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>

mutation.