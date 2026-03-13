---
id: testing
title: 테스트
---




TanStack Query를 사용하는 대부분의 Angular 테스트에는 `injectQuery`/`injectMutation`를 호출하는 서비스 또는 구성 요소가 포함됩니다.

TanStack Query의 `inject*` 기능은 [`PendingTasks`](https://angular.dev/api/core/PendingTasks)와 통합되어 프레임워크가 진행 중인 queries 및 mutations를 인식하도록 합니다.

이는 테스트와 SSR이 mutations 및 queries가 해결될 때까지 기다릴 수 있음을 의미합니다. 단위 테스트에서는 `ApplicationRef.whenStable()` 또는 `fixture.whenStable()`를 사용하여 query 완료를 기다릴 수 있습니다. 이는 Zone.js 및 Zoneless 설정 모두에서 작동합니다.

> 이 통합에는 Angular 19 이상이 필요합니다. 이전 버전의 Angular는 `PendingTasks`를 지원하지 않습니다.

## 테스트베드 설정

모든 사양에 대해 새로운 `QueryClient`를 생성하고 `provideTanStackQuery` 또는 `provideQueryClient`와 함께 제공하세요. 이렇게 하면 캐시를 격리된 상태로 유지하고 테스트별로 기본 옵션을 변경할 수 있습니다.

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false, // ✅ 더 빠른 실패 테스트
    },
  },
})

TestBed.configureTestingModule({
  providers: [provideTanStackQuery(queryClient)],
})
```
> 애플리케이션의 실제 TanStack Query 구성이 단위 테스트에 사용되는 경우 `withDevtools`가 실수로 테스트 공급자에 포함되지 않았는지 확인하세요. 이로 인해 테스트 속도가 느려질 수 있습니다. 테스트 구성과 프로덕션 구성을 별도로 유지하는 것이 가장 좋습니다.

도우미를 공유하는 경우 `afterEach`에서 `queryClient.clear()`를 호출(또는 새 인스턴스 구축)하여 한 테스트의 데이터가 다른 테스트로 흘러가지 않도록 해야 합니다.

## 첫 번째 query 테스트

Query 테스트는 일반적으로 `TestBed.runInInjectionContext` 내부에서 실행된 후 안정성을 기다립니다.

```ts
const appRef = TestBed.inject(ApplicationRef)
const query = TestBed.runInInjectionContext(() =>
  injectQuery(() => ({
    queryKey: ['greeting'],
    queryFn: () => 'Hello',
  })),
)

TestBed.tick() // 트리거 효과

// queries가 유휴 상태일 때 애플리케이션이 안정적입니다.
await appRef.whenStable()

expect(query.status()).toBe('success')
expect(query.data()).toBe('Hello')
```
PendingTasks에서는 query가 해결된 후 `whenStable()`가 해결됩니다. 가짜 타이머(Vitest)를 사용하는 경우 안정성을 기다리기 전에 시계와 마이크로태스크를 앞당깁니다.

```ts
await vi.advanceTimersByTimeAsync(0)
await Promise.resolve()
await appRef.whenStable()
```
## 테스트 구성 요소

구성 요소의 경우 `TestBed.createComponent`를 통해 부트스트랩한 다음 `fixture.whenStable()`를 기다립니다.

```ts
const fixture = TestBed.createComponent(ExampleComponent)

await fixture.whenStable()
expect(fixture.componentInstance.query.data()).toEqual({ value: 42 })
```
## 재시도 처리

기본 백오프가 세 번 실행되므로 느리게 실패한 테스트를 다시 시도합니다. 테스트를 빠르게 유지하려면 `defaultOptions`를 통해 또는 query에 따라 `retry: false`(또는 특정 번호)를 설정하세요. query가 의도적으로 재시도하는 경우 중간 카운트가 아닌 최종 상태를 어설션합니다.

## HttpClient 및 네트워크 스텁

Angular의 `HttpClientTestingModule`는 PendingTasks와 잘 작동합니다. Query 공급자와 함께 등록하고 `HttpTestingController`를 통해 응답을 플러시합니다.

```ts
TestBed.configureTestingModule({
  imports: [HttpClientTestingModule],
  providers: [provideTanStackQuery(queryClient)],
})

const httpCtrl = TestBed.inject(HttpTestingController)
const query = TestBed.runInInjectionContext(() =>
  injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: () => lastValueFrom(TestBed.inject(HttpClient).get('/api/todos')),
  })),
)

const fixturePromise = TestBed.inject(ApplicationRef).whenStable()
httpCtrl.expectOne('/api/todos').flush([{ id: 1 }])
await fixturePromise

expect(query.data()).toEqual([{ id: 1 }])
httpCtrl.verify()
```
## 무한 queries 및 페이지 매김

무한 queries에 대해 동일한 패턴을 사용합니다. `fetchNextPage()`를 호출하고, 시간을 속이는 경우 타이머를 앞당긴 다음, 안정성을 기다리고 `data().pages`에서 어설션합니다.

```ts
const infinite = TestBed.runInInjectionContext(() =>
  injectInfiniteQuery(() => ({
    queryKey: ['pages'],
    queryFn: ({ pageParam = 1 }) => fetchPage(pageParam),
    getNextPageParam: (last, all) => all.length + 1,
  })),
)

await appRef.whenStable()
expect(infinite.data().pages).toHaveLength(1)

await infinite.fetchNextPage()
await vi.advanceTimersByTimeAsync(0)
await appRef.whenStable()

expect(infinite.data().pages).toHaveLength(2)
```
## Mutations 및 낙관적인 업데이트

```ts
const mutation = TestBed.runInInjectionContext(() =>
  injectMutation(() => ({
    mutationFn: async (input: string) => input.toUpperCase(),
  })),
)

mutation.mutate('test')

// 트리거 효과
TestBed.tick()

await appRef.whenStable()

expect(mutation.isSuccess()).toBe(true)
expect(mutation.data()).toBe('TEST')
```
## 빠른 체크리스트

- 테스트당 신선한 `QueryClient`(나중에 지우기)
- 시간 초과를 방지하기 위해 재시도를 비활성화하거나 제어합니다.
- 가짜 타이머를 사용할 때 `whenStable()` 이전의 고급 타이머 + 마이크로태스크
- `HttpClientTestingModule` 또는 선호하는 모의를 사용하여 네트워크 호출을 주장하십시오.
- 모든 `refetch`, `fetchNextPage` 또는 mutation 후에 `whenStable()`를 기다립니다.
- 서비스 테스트에는 `TestBed.runInInjectionContext`를 선호하고 구성 요소 테스트에는 `fixture.whenStable()`를 선호합니다.