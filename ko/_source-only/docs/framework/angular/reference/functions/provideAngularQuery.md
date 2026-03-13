---
id: provideAngularQuery
title: provideAngularQuery
---




# ~~함수: provideAngularQuery()~~

```ts
function provideAngularQuery(queryClient): Provider[];
```
정의 위치: [providers.ts:124](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/providers.ts#L124)

Angular 애플리케이션에 대해 TanStack Query 기능을 활성화하는 데 필요한 공급자를 설정합니다.

`QueryClient`를 구성할 수 있습니다.

## 매개변수

### queryClient

`QueryClient`

`QueryClient` 인스턴스.

## 반환값

`Provider`[]

TanStack Query를 설정하는 공급자 집합입니다.

## 참고
https://tanstack.com/query/v5/docs/framework/angular/quick-start

## 더 이상 사용되지 않음

대신 `provideTanStackQuery`를 사용하세요.