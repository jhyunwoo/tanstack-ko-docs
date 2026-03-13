---
id: Angular-HttpClient-and-other-data-fetching-clients
title: Angular HttpClient 및 기타 데이터 가져오기 클라이언트
---




TanStack Query의 가져오기 메커니즘은 Promise를 기반으로 구축되었으므로 브라우저 기본 `fetch` API, `graphql-request` 등을 포함하여 문자 그대로 모든 비동기 데이터 가져오기 클라이언트를 사용할 수 있습니다.

## 데이터 가져오기를 위해 Angular의 `HttpClient` 사용

`HttpClient`는 Angular의 강력하고 통합된 부분으로 다음과 같은 이점을 제공합니다.

- [provideHttpClientTesting](https://angular.dev/guide/http/testing)을 사용한 단위 테스트의 모의 응답.
- [인터셉터](https://angular.dev/guide/http/interceptors)는 인증 헤더 추가, 로깅 수행 등을 포함한 광범위한 기능에 사용될 수 있습니다. 일부 데이터 가져오기 라이브러리에는 자체 인터셉터 시스템이 있지만 `HttpClient` 인터셉터는 Angular의 종속성 주입 시스템과 통합됩니다.
- `HttpClient`는 [`PendingTasks`](https://angular.dev/api/core/PendingTasks#)에 자동으로 이를 알리므로 Angular가 보류 중인 요청을 인식할 수 있습니다. 단위 테스트와 SSR은 결과 애플리케이션 _stableness_ 정보를 사용하여 보류 중인 요청이 완료될 때까지 기다릴 수 있습니다. 이를 통해 [Zoneless](https://angular.dev/guide/zoneless) 애플리케이션에 대한 단위 테스트가 훨씬 쉬워집니다.
- SSR을 사용하는 경우 `HttpClient`는 서버에서 수행되는 [캐시 요청](https://angular.dev/guide/ssr#caching-data-when-using-HttpClient)을 수행합니다. 이렇게 하면 클라이언트에서 불필요한 요청을 방지할 수 있습니다. `HttpClient` SSR 캐싱은 기본적으로 작동합니다. TanStack Query에는 더 강력할 수 있지만 일부 설정이 필요한 자체 hydration 기능이 있습니다. 귀하의 요구 사항에 가장 적합한 것은 사용 사례에 따라 다릅니다.

### `queryFn`에서 Observable 사용하기

TanStack Query는 Promise 기반 라이브러리이므로 `HttpClient`의 관찰 가능 항목을 Promise으로 변환해야 합니다. 이는 `rxjs`의 `lastValueFrom` 또는 `firstValueFrom` 기능을 사용하여 수행할 수 있습니다.

```ts
@Component({
  // ...
})
class ExampleComponent {
  private readonly http = inject(HttpClient)

  readonly query = injectQuery(() => ({
    queryKey: ['repoData'],
    queryFn: () =>
      lastValueFrom(
        this.http.get('https://api.github.com/repos/tanstack/query'),
      ),
  }))
}
```
> Angular는 RxJS를 선택적 종속성으로 전환하고 있으므로 `HttpClient`도 향후 Promise를 지원할 것으로 예상됩니다.
>
> Angular용 TanStack Query에서 Observable에 대한 지원이 계획되어 있습니다.

## 비교표

|데이터 가져오기 클라이언트|장점|단점|
| --------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- |
|**Angular HttpClient**|기능이 뛰어나며 Angular와 매우 잘 통합됩니다.|Observable을 Promise로 변환해야 합니다.|
|**술책**|브라우저 기본 API이므로 번들 크기에 아무것도 추가되지 않습니다.|많은 기능이 부족한 Barebones API입니다.|
|**`graphql-request`와 같은 전문 라이브러리**|특정 사용 사례에 특화된 기능입니다.|Angular 라이브러리가 아니면 프레임워크와 잘 통합되지 않습니다.|
