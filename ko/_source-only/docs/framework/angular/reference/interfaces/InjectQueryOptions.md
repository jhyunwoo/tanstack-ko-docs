---
id: InjectQueryOptions
title: InjectQueryOptions
---




# 인터페이스: InjectQueryOptions

정의 위치: [inject-query.ts:20](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query.ts#L20)

## 속성

### 인젝터?

```ts
optional injector: Injector;
```
정의 위치: [inject-query.ts:26](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query.ts#L26)

query를 생성할 `Injector`입니다.

이것이 제공되지 않으면 현재 주입 컨텍스트가 대신 사용됩니다(`inject`를 통해).