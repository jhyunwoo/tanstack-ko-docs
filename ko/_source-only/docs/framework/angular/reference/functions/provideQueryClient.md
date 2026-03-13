---
id: provideQueryClient
title: provideQueryClient
---




# 함수: provideQueryClient()

```ts
function provideQueryClient(queryClient): Provider;
```
정의 위치: [providers.ts:14](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/providers.ts#L14)

일반적으로 [provideTanStackQuery](provideTanStackQuery.md)는 TanStack Query를 설정하는 데 한 번 사용되며
[https://tanstack.com/query/latest/docs/reference/QueryClient\|QueryClient](https://tanstack.com/query/latest/docs/reference/QueryClient|QueryClient)
전체 응용 프로그램에 대해. 내부적으로는 `provideQueryClient`를 호출합니다.
`provideQueryClient`를 사용하여 부품에 대해 다른 `QueryClient` 인스턴스를 제공할 수 있습니다.
응용 프로그램 또는 단위 테스트 목적으로.

## 매개변수

### queryClient

`QueryClient` 인스턴스 또는 `QueryClient`를 제공하는 `InjectionToken`입니다.

`QueryClient` | `InjectionToken`\<`QueryClient`\>

## 반환값

`Provider`

`QueryClient` 인스턴스를 제공하는 데 사용할 수 있는 공급자 개체입니다.