---
id: injectIsRestoring
title: injectIsRestoring
---




# 함수: injectIsRestoring()

```ts
function injectIsRestoring(options?): Signal<boolean>;
```
정의 위치: [inject-is-restoring.ts:32](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-restoring.ts#L32)

복원이 현재 진행 중인지 여부를 추적하는 신호를 삽입합니다. [injectQuery](../../../../../../framework/angular/reference/functions/injectQuery.md) 및 친구들도 복원과 queries 초기화 사이의 경쟁 조건을 피하기 위해 내부적으로 이를 확인합니다.

## 매개변수

### 옵션?

`InjectIsRestoringOptions`

injectIsRestoring 옵션.

## 반환값

`Signal`\<`boolean`\>

복원이 진행 중인지 여부를 나타내는 boolean이 포함된 readonly 신호입니다.