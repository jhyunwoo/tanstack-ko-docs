---
id: provideIsRestoring
title: provideIsRestoring
---




# 함수: provideIsRestoring()

```ts
function provideIsRestoring(isRestoring): Provider;
```
정의 위치: [inject-is-restoring.ts:43](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-restoring.ts#L43)

복원 상태를 추적하는 신호를 제공하기 위해 TanStack Query Angular 지속 클라이언트 플러그인에서 사용됩니다.

## 매개변수

### isRestoring

`Signal`\<`boolean`\>

boolean을 반환하는 readonly 신호

## 반환값

`Provider`

`isRestoring` 신호 제공자