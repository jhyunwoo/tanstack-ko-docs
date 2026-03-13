---
id: testing
title: 테스트
---




React Query는 후크(우리가 제공하는 후크 또는 이를 감싸는 사용자 정의 후크)를 통해 작동합니다.

React 17 이하에서는 [React Hooks 테스트 라이브러리](https://react-hooks-testing-library.com/) 라이브러리를 사용하여 이러한 사용자 정의 후크에 대한 단위 테스트 작성을 수행할 수 있습니다.

다음을 실행하여 설치하세요.

```sh
npm install @testing-library/react-hooks react-test-renderer --save-dev
```
(`react-test-renderer` 라이브러리는 `@testing-library/react-hooks`의 Peer 종속성으로 필요하며, 사용 중인 React 버전과 일치해야 합니다.)

_참고_: React 18 이상을 사용하는 경우 `renderHook`는 `@testing-library/react` 패키지를 통해 직접 사용할 수 있으며 `@testing-library/react-hooks`는 더 이상 필요하지 않습니다.

## 첫 번째 테스트

일단 설치되면 간단한 테스트를 작성할 수 있습니다. 다음과 같은 사용자 정의 후크가 제공됩니다.

```tsx
export function useCustomHook() {
  return useQuery({ queryKey: ['customHook'], queryFn: () => 'Hello' })
}
```
이에 대한 테스트를 다음과 같이 작성할 수 있습니다.

```tsx
import { renderHook, waitFor } from '@testing-library/react'

const queryClient = new QueryClient()
const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
)

const { result } = renderHook(() => useCustomHook(), { wrapper })

await waitFor(() => expect(result.current.isSuccess).toBe(true))

expect(result.current.data).toEqual('Hello')
```
`QueryClient` 및 `QueryClientProvider`를 빌드하는 사용자 정의 래퍼를 제공합니다. 이는 우리 테스트가 다른 테스트와 완전히 격리되도록 하는 데 도움이 됩니다.

이 래퍼를 한 번만 작성할 수 있지만, 그렇다면 모든 테스트 전에 `QueryClient`가 지워지고 테스트가 병렬로 실행되지 않도록 해야 합니다. 그렇지 않으면 하나의 테스트가 다른 테스트의 결과에 영향을 미치게 됩니다.

## 재시도 끄기

라이브러리는 기본적으로 지수 백오프를 사용하여 3번의 재시도를 수행합니다. 이는 잘못된 query를 테스트하려는 경우 테스트가 시간 초과될 가능성이 있음을 의미합니다. 재시도를 끄는 가장 쉬운 방법은 QueryClientProvider를 사용하는 것입니다. 위의 예를 확장해 보겠습니다.

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // ✅ 재시도 기능을 끕니다
      retry: false,
    },
  },
})
const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
)
```
이렇게 하면 구성 요소 트리의 모든 queries에 대한 기본값이 "재시도 없음"으로 설정됩니다. 이는 실제 useQuery에 명시적인 재시도 설정이 없는 경우에만 작동한다는 점을 아는 것이 중요합니다. 5번의 재시도를 원하는 query가 있는 경우 기본값은 대체용으로만 사용되기 때문에 이는 여전히 우선순위를 갖습니다.

## Jest를 사용하여 gcTime를 무한대로 설정

Jest를 사용하는 경우 `gcTime`를 `Infinity`로 설정하여 "Jest가 테스트 실행이 완료된 후 1초 동안 종료되지 않았습니다." 오류 메시지를 방지할 수 있습니다. 이는 서버의 기본 동작이며 `gcTime`를 명시적으로 설정하는 경우에만 설정해야 합니다.

## 네트워크 호출 테스트

React Query의 주요 용도는 네트워크 요청을 캐시하는 것이므로 먼저 코드가 올바른 네트워크 요청을 하는지 테스트할 수 있는 것이 중요합니다.

이를 테스트할 수 있는 방법은 많지만 이 예에서는 [nock](https://www.npmjs.com/package/nock)을 사용하겠습니다.

다음과 같은 사용자 정의 후크가 제공됩니다.

```tsx
function useFetchData() {
  return useQuery({
    queryKey: ['fetchData'],
    queryFn: () => request('/api/data'),
  })
}
```
이에 대한 테스트를 다음과 같이 작성할 수 있습니다.

```tsx
const queryClient = new QueryClient()
const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
)

const expectation = nock('http://example.com').get('/api/data').reply(200, {
  answer: 42,
})

const { result } = renderHook(() => useFetchData(), { wrapper })

await waitFor(() => expect(result.current.isSuccess).toBe(true))

expect(result.current.data).toEqual({ answer: 42 })
```
여기서는 `waitFor`를 사용하고 query 상태가 요청이 성공했음을 나타낼 때까지 기다리고 있습니다. 이렇게 하면 후크가 완료되었으며 올바른 데이터가 있어야 함을 알 수 있습니다. _참고_: React 18을 사용할 때 `waitFor`의 의미는 위에서 언급한 대로 변경되었습니다.

## 추가 로드/무한 스크롤 테스트

먼저 API 응답을 모의해야 합니다.

```tsx
function generateMockedResponse(page) {
  return {
    page: page,
    items: [...]
  }
}
```
그런 다음 `nock` 구성은 페이지를 기반으로 응답을 차별화해야 하며 이를 위해 `uri`를 사용합니다.
여기서 `uri`의 값은 `"/?page=1` 또는 `/?page=2`와 같습니다.

```tsx
const expectation = nock('http://example.com')
  .persist()
  .query(true)
  .get('/api/data')
  .reply(200, (uri) => {
    const url = new URL(`http://example.com${uri}`)
    const { page } = Object.fromEntries(url.searchParams)
    return generateMockedResponse(page)
  })
```
(이 끝점에서 여러 번 호출하므로 `.persist()`에 유의하세요.)

이제 안전하게 테스트를 실행할 수 있습니다. 여기서 중요한 점은 데이터 어설션이 통과될 때까지 기다리는 것입니다.

```tsx
const { result } = renderHook(() => useInfiniteQueryCustomHook(), {
  wrapper,
})

await waitFor(() => expect(result.current.isSuccess).toBe(true))

expect(result.current.data.pages).toStrictEqual(generateMockedResponse(1))

result.current.fetchNextPage()

await waitFor(() =>
  expect(result.current.data.pages).toStrictEqual([
    ...generateMockedResponse(1),
    ...generateMockedResponse(2),
  ]),
)

expectation.done()
```
_참고_: React 18을 사용할 때 `waitFor`의 의미는 위에서 언급한 대로 변경되었습니다.

## 추가 자료

`mock-service-worker`를 사용한 추가 팁과 대체 설정에 대해서는 [React Query 테스트에 대한 TkDodo의 이 기사](https://tkdodo.eu/blog/testing-react-query)를 참조하세요.