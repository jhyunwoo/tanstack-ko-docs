---
id: injectQueryClient
title: injectQueryClient
---




# ~~함수: injectQueryClient()~~

```ts
function injectQueryClient(injectOptions): QueryClient;
```
정의 위치: [inject-query-client.ts:18](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/inject-query-client.ts#L18)

`QueryClient` 인스턴스를 주입하고 사용자 지정 인젝터 전달을 허용합니다.

## 매개변수

### injectOptions

`InjectOptions` & `object` = `{}`

주입할 옵션 인수의 유형과 선택적으로 사용자 정의 인젝터.

## 반환값

`QueryClient`

`QueryClient` 인스턴스.

## 더 이상 사용되지 않음

대신 `inject(QueryClient)`를 사용하세요.
맞춤형 인젝터에서 `QueryClient`를 가져와야 하는 경우 `injector.get(QueryClient)`를 사용하세요.

**예**```ts
const queryClient = injectQueryClient();
```
