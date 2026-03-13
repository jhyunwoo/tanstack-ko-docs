---
id: injectIsFetching
title: injectIsFetching
---




# 함수: injectIsFetching()

```ts
function injectIsFetching(filters?, options?): Signal<number>;
```
정의 위치: [inject-is-fetching.ts:31](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-is-fetching.ts#L31)

애플리케이션이 로드 중인 queries 수를 추적하는 신호를 주입합니다.
백그라운드에서 가져오는 중입니다.

앱 전체 로딩 표시기에 사용할 수 있습니다.

## 매개변수

### 필터?

`QueryFilters`\<readonly `unknown`[]\>

query에 적용할 필터입니다.

### 옵션?

[InjectIsFetchingOptions](../interfaces/InjectIsFetchingOptions.md)

추가 구성

## 반환값

`Signal`\<`number`\>

queries를 로드하거나 가져오는 횟수가 포함된 신호.