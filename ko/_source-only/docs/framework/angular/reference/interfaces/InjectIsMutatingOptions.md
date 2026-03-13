---
id: InjectIsMutatingOptions
title: InjectIsMutatingOptions
---




# 인터페이스: InjectIsMutatingOptions

정의 위치: [inject-is-mutating.ts:13](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-mutating.ts#L13)

## 속성

### 인젝터?

```ts
optional injector: Injector;
```
정의 위치: [inject-is-mutating.ts:19](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-mutating.ts#L19)

isMutating 신호를 생성할 `Injector`입니다.

이것이 제공되지 않으면 현재 주입 컨텍스트가 대신 사용됩니다(`inject`를 통해).