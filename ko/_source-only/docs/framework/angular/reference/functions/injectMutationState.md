---
id: injectMutationState
title: injectMutationState
---




# 함수: injectMutationState()

```ts
function injectMutationState<TResult>(injectMutationStateFn, options?): Signal<TResult[]>;
```
정의 위치: [inject-mutation-state.ts:60](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-mutation-state.ts#L60)

모든 mutations의 상태를 추적하는 신호를 주입합니다.

## 타입 매개변수

### TResult

`TResult` = `MutationState`\<`unknown`, `Error`, `unknown`, `unknown`\>

## 매개변수

### injectMutationStateFn

() => `MutationStateOptions`\<`TResult`\>

mutation 상태 옵션을 반환하는 함수입니다.

### 옵션?

[InjectMutationStateOptions](../interfaces/InjectMutationStateOptions.md)

사용할 Angular 인젝터입니다.

## 반환값

`Signal`\<`TResult`[]\>

모든 mutations의 상태를 추적하는 신호입니다.