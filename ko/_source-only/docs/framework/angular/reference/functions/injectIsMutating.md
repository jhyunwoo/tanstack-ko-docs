---
id: injectIsMutating
title: injectIsMutating
---




# 함수: injectIsMutating()

```ts
function injectIsMutating(filters?, options?): Signal<number>;
```
정의 위치: [inject-is-mutating.ts:30](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-mutating.ts#L30)

애플리케이션이 가져오는 mutations 수를 추적하는 신호를 주입합니다.

앱 전체 로딩 표시기에 사용할 수 있습니다.

## 매개변수

### 필터?

`MutationFilters`\<`unknown`, `Error`, `unknown`, `unknown`\>

query에 적용할 필터입니다.

### 옵션?

[InjectIsMutatingOptions](../interfaces/InjectIsMutatingOptions.md)

추가 구성

## 반환값

`Signal`\<`number`\>

mutations를 가져오는 횟수가 포함된 readonly 신호입니다.