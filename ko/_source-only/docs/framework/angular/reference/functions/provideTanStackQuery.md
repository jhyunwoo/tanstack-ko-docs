---
id: provideTanStackQuery
title: provideTanStackQuery
---




# 함수: provideTanStackQuery()

```ts
function provideTanStackQuery(queryClient, ...features): Provider[];
```
정의 위치: [providers.ts:105](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/providers.ts#L105)

Angular 애플리케이션에 대해 TanStack Query 기능을 활성화하는 데 필요한 공급자를 설정합니다.

`QueryClient` 및 개발자 도구와 같은 선택적 기능을 구성할 수 있습니다.

**예 - 독립형**

```ts
import {
  provideTanStackQuery,
  QueryClient,
} from '@tanstack/angular-query-experimental'

bootstrapApplication(AppComponent, {
  providers: [provideTanStackQuery(new QueryClient())],
})
```
**예 - NgModule 기반**

```ts
import {
  provideTanStackQuery,
  QueryClient,
} from '@tanstack/angular-query-experimental'

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule],
  providers: [provideTanStackQuery(new QueryClient())],
  bootstrap: [AppComponent],
})
export class AppModule {}
```
`withDevtools`를 추가하여 선택적 개발자 도구를 활성화할 수도 있습니다. 작성자:
기본적으로 앱이 개발 모드에 있을 때 도구가 로드됩니다.```ts
import {
  provideTanStackQuery,
  withDevtools
  QueryClient,
} from '@tanstack/angular-query-experimental'

bootstrapApplication(AppComponent,
  {
    providers: [
      provideTanStackQuery(new QueryClient(), withDevtools())
    ]
  }
)
```
**예: InjectionToken 사용**

```ts
export const MY_QUERY_CLIENT = new InjectionToken('', {
  factory: () => new QueryClient(),
})

// 지연 로드 경로 또는 지연 로드 구성 요소의 공급자 배열에서:
providers: [provideTanStackQuery(MY_QUERY_CLIENT)]
```
QueryClient에 대해 주입 토큰을 사용하는 것은 TanStack Query가 기본 애플리케이션 번들에 없을 수 있도록 하는 고급 최적화입니다.
이는 `QueryClient`를 계속 공유하면서 지연 로드 경로에만 TanStack Query를 포함하려는 경우에 유용할 수 있습니다.

이는 작은 최적화이며 대부분의 애플리케이션에서는 기본 애플리케이션 구성에 `QueryClient`를 제공하는 것이 바람직합니다.

## 매개변수

### queryClient

`QueryClient` 인스턴스 또는 `QueryClient`를 제공하는 `InjectionToken`입니다.

`QueryClient` | `InjectionToken`\<`QueryClient`\>

### 특징

...[QueryFeatures](../type-aliases/QueryFeatures.md)[]

추가 Query 기능을 구성하는 선택적 기능입니다.

## 반환값

`Provider`[]

TanStack Query를 설정하는 공급자 집합입니다.

## 참고
- https://tanstack.com/query/v5/docs/framework/angular/quick-start
 - Devtools를 사용하여