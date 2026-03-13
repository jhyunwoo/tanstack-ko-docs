---
id: ssr
title: 서버 렌더링 및 Hydration
---




이 가이드에서는 서버 렌더링과 함께 React Query를 사용하는 방법을 배웁니다.

배경 지식은 [프리페칭 및 라우터 통합](prefetching.md) 가이드를 참조하세요. 그 전에 [성능 및 요청 폭포수 가이드](request-waterfalls.md)를 확인해 보는 것도 좋습니다.

hydration + 프리패치(코드 분할 포함)에 대한 더 자세한 예시는 [종속 Queries 및 코드 분할](prefetching.md#dependent-queries-code-splitting) 섹션을 참조하세요.

스트리밍, 서버 구성 요소 및 새로운 Next.js 앱 라우터와 같은 고급 서버 렌더링 패턴에 대해서는 [고급 서버 렌더링 가이드](advanced-ssr.md)를 참조하세요.

일부 코드만 보고 싶다면 아래의 [전체 Next.js 페이지 라우터 예시](#full-nextjs-pages-router-example) 또는 [전체 리믹스 예시](#full-remix-example)로 건너뛸 수 있습니다.

## 서버 렌더링 및 React Query

그렇다면 서버 렌더링이란 무엇일까요? 이 가이드의 나머지 부분에서는 귀하가 이 개념에 대해 잘 알고 있다고 가정하지만, 이 개념이 React Query와 어떻게 관련되는지 살펴보는 시간을 갖도록 하겠습니다. 서버 렌더링은 페이지가 로드되자마자 사용자가 볼 수 있는 일부 콘텐츠를 갖도록 서버에서 초기 HTML을 생성하는 작업입니다. 이는 페이지가 요청될 때(SSR) 요청 시 발생할 수 있습니다. 이전 요청이 캐시되었거나 빌드 시간(SSG)에 미리 발생할 수도 있습니다.

[성능 및 요청 폭포수 가이드](request-waterfalls.md)를 읽어보셨다면 다음 내용을 기억하실 것입니다.

```
1. |-> Markup (without content)
2.   |-> JS
3.     |-> Query
```
클라이언트 렌더링 애플리케이션을 사용하면 사용자를 위해 화면에 콘텐츠를 표시하기 전에 최소 3번의 서버 왕복이 필요합니다. 서버 렌더링을 보는 한 가지 방법은 위의 내용을 다음과 같이 바꾸는 것입니다.

```
1. |-> Markup (with content AND initial data)
2.   |-> JS
```
**1.**이 완료되자마자 사용자는 콘텐츠를 볼 수 있으며 **2.**가 완료되면 페이지가 대화형이며 클릭 가능합니다. 마크업에는 필요한 초기 데이터도 포함되어 있으므로 최소한 어떤 이유로 데이터의 유효성을 재검토하기 전까지는 **3.** 단계를 클라이언트에서 실행할 필요가 전혀 없습니다.

이것은 모두 고객의 관점에서 본 것입니다. 서버에서는 마크업을 생성/렌더링하기 전에 해당 데이터를 **프리페치**해야 하고, 해당 데이터를 마크업에 포함할 수 있는 직렬화 가능한 형식으로 **디하이드레이션**해야 하며, 클라이언트에서는 해당 데이터를 React Query 캐시로 **수화**해야 클라이언트에서 새 가져오기를 수행하는 것을 피할 수 있습니다.

React Query를 사용하여 이 세 단계를 구현하는 방법을 알아보려면 계속 읽어보세요.

## Suspense에 대한 간단한 참고 사항

이 가이드에서는 일반 `useQuery` API를 사용합니다. 반드시 권장되는 것은 아니지만 **항상 모든 queries**를 미리 가져오는 한 이를 `useSuspenseQuery`로 교체할 수 있습니다. 장점은 클라이언트에 상태를 로드하기 위해 `<Suspense>`를 사용할 수 있다는 것입니다.

`useSuspenseQuery`를 사용할 때 query를 프리페치하는 것을 잊어버린 경우 결과는 사용 중인 프레임워크에 따라 달라집니다. 어떤 경우에는 데이터가 일시 중지되어 서버에서 가져오지만 클라이언트로 수화되지 않아 다시 가져오게 됩니다. 이러한 경우 서버와 클라이언트가 서로 다른 것을 렌더링하려고 시도했기 때문에 마크업 hydration 불일치가 발생합니다.

## 초기 설정

React Query를 사용하는 첫 번째 단계는 항상 `queryClient`를 만들고 `<QueryClientProvider>`에 애플리케이션을 래핑하는 것입니다. 서버 렌더링을 수행할 때 React 상태에서 **앱 내부**에 `queryClient` 인스턴스를 생성하는 것이 중요합니다(인스턴스 참조도 잘 작동함). **이렇게 하면 서로 다른 사용자와 요청 간에 데이터가 공유되지 않으며** 구성 요소 수명 주기당 한 번만 `queryClient`를 생성할 수 있습니다.

Next.js 페이지 라우터:

```tsx
// _app.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

// 절대 이렇게 하지 마세요:
// const queryClient = 새로운 QueryClient()
//
// 파일 루트 수준에서 queryClient를 생성하면 캐시가 공유됩니다.
// 모든 요청과 수단 사이에서 _모든_ 데이터가 _모든_ 사용자에게 전달됩니다.
// 성능이 저하될 뿐만 아니라 민감한 데이터도 유출됩니다.

export default function MyApp({ Component, pageProps }) {
  // 대신 다음을 수행하여 각 요청에 자체 캐시가 있는지 확인하세요.
  const [queryClient] = React.useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
            // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
            staleTime: 60 * 1000,
          },
        },
      }),
  )

  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  )
}
```
리믹스:

```tsx
// 앱/root.tsx
import { Outlet } from '@remix-run/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export default function MyApp() {
  const [queryClient] = React.useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
            // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
            staleTime: 60 * 1000,
          },
        },
      }),
  )

  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  )
}
```
## `initialData`로 빠르게 시작하세요

시작하는 가장 빠른 방법은 프리패치 시 React Query를 전혀 사용하지 않고 `dehydrate`/`hydrate` API를 사용하지 않는 것입니다. 대신 수행할 작업은 원시 데이터를 `initialData` 옵션으로 `useQuery`에 전달하는 것입니다. `getServerSideProps`를 사용하여 Next.js 페이지 라우터를 사용하는 예를 살펴보겠습니다.

```tsx
export async function getServerSideProps() {
  const posts = await getPosts()
  return { props: { posts } }
}

function Posts(props) {
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
    initialData: props.posts,
  })

  // ...
}
```
이는 `getStaticProps` 또는 이전 `getInitialProps`에서도 작동하며 동일한 기능을 가진 다른 프레임워크에도 동일한 패턴을 적용할 수 있습니다. 다음은 Remix와 동일한 예입니다.

```tsx
export async function loader() {
  const posts = await getPosts()
  return json({ posts })
}

function Posts() {
  const { posts } = useLoaderData<typeof loader>()

  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
    initialData: posts,
  })

  // ...
}
```
설정은 최소화되어 어떤 경우에는 빠른 솔루션이 될 수 있지만 전체 접근 방식과 비교할 때 **고려해야 할 몇 가지 절충 사항**이 있습니다.

- 트리의 더 깊은 하위 구성 요소에서 `useQuery`를 호출하는 경우 해당 지점까지 `initialData`를 전달해야 합니다.
- 여러 위치에서 동일한 query를 사용하여 `useQuery`를 호출하는 경우 `initialData`를 그 중 하나만 전달하면 앱이 변경될 때 부서지기 쉽고 중단될 수 있습니다. `useQuery`와 `initialData`가 있는 구성 요소를 제거하거나 이동하면 더 깊게 중첩된 `useQuery`에 더 이상 데이터가 없을 수 있습니다. `initialData`를 필요한 **모든** queries에 전달하는 것도 번거로울 수 있습니다.
- 서버에서 query를 가져온 시간을 알 수 있는 방법이 없으므로 `dataUpdatedAt` 및 query를 다시 가져와야 하는지 결정하는 것은 대신 페이지가 로드된 시간을 기준으로 합니다.
- query에 대한 캐시에 이미 데이터가 있는 경우 `initialData`는 **새 데이터가 이전 데이터보다 최신인 경우에도** 이 데이터를 덮어쓰지 않습니다.
  - 이것이 특히 나쁜 이유를 이해하려면 위의 `getServerSideProps` 예를 고려하십시오. 페이지를 여러 번 앞뒤로 탐색하면 매번 `getServerSideProps`가 호출되어 새 데이터를 가져오지만 `initialData` 옵션을 사용하고 있기 때문에 클라이언트 캐시와 데이터는 절대 업데이트되지 않습니다.

전체 hydration 솔루션을 설정하는 것은 간단하며 이러한 단점이 없습니다. 나머지 문서에서는 이에 중점을 둘 것입니다.

## Hydration API 사용

조금만 더 설정하면 사전 로드 단계에서 `queryClient`를 사용하여 queries를 사전 가져오고 해당 `queryClient`의 직렬화된 버전을 앱의 렌더링 부분에 전달한 후 거기에서 재사용할 수 있습니다. 이렇게 하면 위의 단점을 피할 수 있습니다. 전체 Next.js 페이지 라우터 및 Remix 예제를 보려면 건너뛰어도 좋지만 일반적인 수준에서는 다음과 같은 추가 단계가 있습니다.

- 프레임워크 로더 기능에서 `const queryClient = new QueryClient(options)`를 생성합니다.
- 로더 기능에서 프리페치하려는 각 query에 대해 `await queryClient.prefetchQuery(...)`를 수행합니다.
  - 가능하면 `await Promise.all(...)`를 사용하여 queries를 병렬로 가져오고 싶습니다.
  - 프리페치되지 않은 queries가 있어도 괜찮습니다. 이는 서버에서 렌더링되지 않고 대신 애플리케이션이 대화형이 된 후 클라이언트에서 가져옵니다. 이는 사용자 상호 작용 후에만 표시되는 콘텐츠에 유용할 수 있으며, 더 중요한 콘텐츠를 차단하지 않기 위해 페이지 아래쪽에 표시되는 경우에도 유용합니다.
- 로더에서 `dehydrate(queryClient)`를 반환합니다. 이를 반환하는 정확한 구문은 프레임워크마다 다릅니다.
- `dehydratedState`가 프레임워크 로더에서 제공되는 `<HydrationBoundary state={dehydratedState}>`로 트리를 래핑합니다. `dehydratedState`를 얻는 방법도 프레임워크마다 다릅니다.
  - 각 경로에 대해 수행하거나 상용구를 피하기 위해 애플리케이션 상단에서 수행할 수 있습니다. 예를 참조하세요.

> 흥미로운 세부 사항은 실제로 _3_개의 `queryClient`가 관련되어 있다는 것입니다. 프레임워크 로더는 렌더링 전에 발생하는 "사전 로드" 단계의 형태이며, 이 단계에는 프리페치를 수행하는 자체 `queryClient`가 있습니다. 이 단계의 탈수된 결과는 각각 고유한 `queryClient`를 가지고 있는 서버 렌더링 프로세스 **와** 클라이언트 렌더링 프로세스 모두에 전달됩니다. 이렇게 하면 둘 다 동일한 데이터로 시작하여 동일한 마크업을 반환할 수 있습니다.

> 서버 구성 요소는 React 구성 요소 트리의 일부를 "미리 로드"(사전 렌더링)할 수도 있는 "미리 로드" 단계의 또 다른 형태입니다. [고급 서버 렌더링 가이드](advanced-ssr.md)에서 자세한 내용을 읽어보세요.

### 전체 Next.js 페이지 라우터 예시

> 앱 라우터 문서는 [고급 서버 렌더링 가이드](advanced-ssr.md)를 참조하세요.

초기 설정:

```tsx
// _app.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export default function MyApp({ Component, pageProps }) {
  const [queryClient] = React.useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
            // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
            staleTime: 60 * 1000,
          },
        },
      }),
  )

  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  )
}
```
각 경로에서:

```tsx
// 페이지/게시물.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
  useQuery,
} from '@tanstack/react-query'

// getServerSideProps일 수도 있습니다.
export async function getStaticProps() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return {
    props: {
      dehydratedState: dehydrate(queryClient),
    },
  }
}

function Posts() {
  // 이 useQuery는 더 깊은 어린이에게서도 일어날 수 있습니다.
  // <PostsRoute>, 데이터는 어느 쪽이든 즉시 사용할 수 있습니다.
  const { data } = useQuery({ queryKey: ['posts'], queryFn: getPosts })

  // 이 query는 서버에서 프리페치되지 않았으며 시작되지 않습니다.
  // 클라이언트까지 가져오는 동안 두 패턴을 혼합해도 괜찮습니다.
  const { data: commentsData } = useQuery({
    queryKey: ['posts-comments'],
    queryFn: getComments,
  })

  // ...
}

export default function PostsRoute({ dehydratedState }) {
  return (
    <HydrationBoundary state={dehydratedState}>
      <Posts />
    </HydrationBoundary>
  )
}
```
### 전체 리믹스 예시

초기 설정:

```tsx
// 앱/root.tsx
import { Outlet } from '@remix-run/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export default function MyApp() {
  const [queryClient] = React.useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
            // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
            staleTime: 60 * 1000,
          },
        },
      }),
  )

  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  )
}
```
각 경로에서 중첩된 경로에서도 이 작업을 수행하는 것이 좋습니다.

```tsx
// 앱/경로/posts.tsx
import { json } from '@remix-run/node'
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
  useQuery,
} from '@tanstack/react-query'

export async function loader() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return json({ dehydratedState: dehydrate(queryClient) })
}

function Posts() {
  // 이 useQuery는 더 깊은 어린이에게서도 일어날 수 있습니다.
  // <PostsRoute>, 데이터는 어느 쪽이든 즉시 사용할 수 있습니다.
  const { data } = useQuery({ queryKey: ['posts'], queryFn: getPosts })

  // 이 query는 서버에서 프리페치되지 않았으며 시작되지 않습니다.
  // 클라이언트까지 가져오는 동안 두 패턴을 혼합해도 괜찮습니다.
  const { data: commentsData } = useQuery({
    queryKey: ['posts-comments'],
    queryFn: getComments,
  })

  // ...
}

export default function PostsRoute() {
  const { dehydratedState } = useLoaderData<typeof loader>()
  return (
    <HydrationBoundary state={dehydratedState}>
      <Posts />
    </HydrationBoundary>
  )
}
```
## 선택 사항 - 상용구 제거

모든 경로에 이 부분이 있으면 너무 많은 상용구처럼 보일 수 있습니다.

```tsx
export default function PostsRoute({ dehydratedState }) {
  return (
    <HydrationBoundary state={dehydratedState}>
      <Posts />
    </HydrationBoundary>
  )
}
```
이 접근 방식에는 아무런 문제가 없지만 이 상용구를 제거하려는 경우 Next.js에서 설정을 수정하는 방법은 다음과 같습니다.

```tsx
// _app.tsx
import {
  HydrationBoundary,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

export default function MyApp({ Component, pageProps }) {
  const [queryClient] = React.useState(() => new QueryClient())

  return (
    <QueryClientProvider client={queryClient}>
      <HydrationBoundary state={pageProps.dehydratedState}>
        <Component {...pageProps} />
      </HydrationBoundary>
    </QueryClientProvider>
  )
}

// 페이지/게시물.tsx
// HydrationBoundary를 사용하여 PostsRoute를 제거하고 대신 게시물을 직접 내보냅니다.
export default function Posts() { ... }
```
Remix의 경우 이는 좀 더 복잡하므로 [use-dehydrated-state](https://github.com/maplegrove-io/use-dehydrated-state) 패키지를 확인하는 것이 좋습니다.

## 프리패치 종속 queries

프리페칭 가이드에서 [종속적 queries 프리페치](prefetching.md#dependent-queries-code-splitting) 방법을 배웠지만 프레임워크 로더에서는 이를 어떻게 수행합니까? [종속 Queries 가이드](dependent-queries.md)에서 가져온 다음 코드를 고려하세요.

```tsx
// 사용자 확보
const { data: user } = useQuery({
  queryKey: ['user', email],
  queryFn: getUserByEmail,
})

const userId = user?.id

// 그런 다음 사용자의 프로젝트를 가져옵니다.
const {
  status,
  fetchStatus,
  data: projects,
} = useQuery({
  queryKey: ['projects', userId],
  queryFn: getProjectsByUser,
  // query는 userId가 존재할 때까지 실행되지 않습니다.
  enabled: !!userId,
})
```
서버에서 렌더링할 수 있도록 이를 어떻게 미리 가져오나요? 예는 다음과 같습니다.

```tsx
// Remix의 경우 이름을 loader로 바꾸세요.
export async function getServerSideProps() {
  const queryClient = new QueryClient()

  const user = await queryClient.fetchQuery({
    queryKey: ['user', email],
    queryFn: getUserByEmail,
  })

  if (user?.userId) {
    await queryClient.prefetchQuery({
      queryKey: ['projects', userId],
      queryFn: getProjectsByUser,
    })
  }

  // 리믹스의 경우:
  // json({ dehydratedState: dehydrate(queryClient) }) 반환
  return { props: { dehydratedState: dehydrate(queryClient) } }
}
```
물론 이것은 더 복잡해질 수 있지만 이러한 로더 함수는 단지 JavaScript이므로 언어의 모든 기능을 사용하여 논리를 구축할 수 있습니다. 서버 렌더링을 원하는 모든 queries를 프리페치해야 합니다.

## 오류 처리

React Query는 기본적으로 단계적 성능 저하 전략을 사용합니다. 이는 다음을 의미합니다.

- `queryClient.prefetchQuery(...)`에서는 오류가 발생하지 않습니다.
- `dehydrate(...)`에는 성공한 queries만 포함되고 실패한 queries만 포함됩니다.

이로 인해 실패한 queries가 클라이언트에서 재시도되고 서버 렌더링 출력에 전체 콘텐츠 대신 로드 상태가 포함됩니다.

좋은 기본값이지만 때로는 원하는 것이 아닐 수도 있습니다. 중요한 콘텐츠가 누락된 경우 상황에 따라 404 또는 500 상태 코드로 응답할 수 있습니다. 이러한 경우에는 대신 `queryClient.fetchQuery(...)`를 사용하세요. 실패하면 오류가 발생하므로 적절한 방식으로 작업을 처리할 수 있습니다.

```tsx
let result

try {
  result = await queryClient.fetchQuery(...)
} catch (error) {
  // 오류를 처리하고 프레임워크 문서를 참조하세요.
}

// 여기에서 잘못된 `결과`를 확인하고 처리할 수도 있습니다.
```
어떤 이유로 재시도를 피하기 위해 실패한 queries를 탈수 상태에 포함시키려는 경우 `shouldDehydrateQuery` 옵션을 사용하여 기본 기능을 재정의하고 고유한 논리를 구현할 수 있습니다.

```tsx
dehydrate(queryClient, {
  shouldDehydrateQuery: (query) => {
    // 여기에는 실패한 queries가 모두 포함됩니다.
    // 하지만 `query`를 검사하여 자신만의 논리를 구현할 수도 있습니다.
    return true
  },
})
```
## 직렬화

Next.js에서 `return { props: { dehydratedState: dehydrate(queryClient) } }`를 수행하거나 Remix에서 `return json({ dehydratedState: dehydrate(queryClient) })`를 수행할 때 `queryClient`의 `dehydratedState` 표현이 프레임워크에 의해 직렬화되어 마크업에 포함되어 클라이언트로 전송될 수 있습니다.

기본적으로 이러한 프레임워크는 안전하게 직렬화/구문 분석 가능한 항목 반환만 지원하므로 `undefined`, `Error`, `Date`, `Map`, `Set`, `BigInt`, `Infinity`를 지원하지 않습니다. `NaN`, `-0`, 정규식 등. 이는 또한 queries에서 이러한 항목을 반환할 수 없음을 의미합니다. 이러한 값을 반환하는 것이 원하는 경우 [superjson](https://github.com/blitz-js/superjson) 또는 유사한 패키지를 확인하세요.

사용자 정의 SSR 설정을 사용하는 경우 이 단계를 직접 처리해야 합니다. 첫 번째 본능은 `JSON.stringify(dehydratedState)`를 사용하는 것이지만 이는 기본적으로 `<script>alert('Oh no..')</script>`와 같은 것을 이스케이프하지 않기 때문에 애플리케이션에서 쉽게 **XSS 취약점**으로 이어질 수 있습니다. [superjson](https://github.com/blitz-js/superjson)은 값을 **이스케이프하지 않으며** 사용자 지정 SSR 설정에서 자체적으로 사용하는 것이 안전하지 않습니다(출력을 이스케이프하기 위한 추가 단계를 추가하지 않는 한). 대신에 기본적으로 XSS 삽입에 대해 안전한 [JavaScript 직렬화](https://github.com/yahoo/serialize-javascript) 또는 [devalue](https://github.com/Rich-Harris/devalue)와 같은 라이브러리를 사용하는 것이 좋습니다.

## 요청 폭포에 대한 참고 사항

[성능 및 요청 폭포수 가이드](request-waterfalls.md)에서 우리는 서버 렌더링이 더 복잡한 중첩 폭포수 중 하나를 어떻게 변경하는지 다시 살펴볼 것이라고 언급했습니다. [구체적인 코드 예](request-waterfalls.md#code-splitting)를 다시 확인하세요. 다시 한번 강조하자면 `<Feed>` 구성 요소 내부에 코드 분할 `<GraphFeedItem>` 구성 요소가 있습니다. 이는 피드에 그래프 항목이 포함되어 있고 두 구성 요소 모두 자체 데이터를 가져오는 경우에만 렌더링됩니다. 클라이언트 렌더링을 사용하면 다음과 같은 요청 폭포가 발생합니다.

```
1. |> Markup (without content)
2.   |> JS for <Feed>
3.     |> getFeed()
4.       |> JS for <GraphFeedItem>
5.         |> getGraphDataById()
```
서버 렌더링의 좋은 점은 위의 내용을 다음과 같이 바꿀 수 있다는 것입니다.

```
1. |> Markup (with content AND initial data)
2.   |> JS for <Feed>
2.   |> JS for <GraphFeedItem>
```
queries는 더 이상 클라이언트에서 가져오지 않으며 대신 해당 데이터가 마크업에 포함되었습니다. 이제 JS를 병렬로 로드할 수 있는 이유는 `<GraphFeedItem>`가 서버에서 렌더링되었기 때문에 클라이언트에서도 이 JS가 필요하다는 것을 알고 마크업에 이 청크에 대한 스크립트 태그를 삽입할 수 있기 때문입니다. 서버에는 여전히 다음과 같은 요청 폭포가 있습니다.

```
1. |> getFeed()
2.   |> getGraphDataById()
```
그래프 데이터도 가져와야 하는지 피드를 가져오기 전에는 알 수 없습니다. 이는 종속적 queries입니다. 이는 일반적으로 대기 시간이 낮고 안정적인 서버에서 발생하기 때문에 그다지 큰 문제가 되지 않는 경우가 많습니다.

놀랍게도 우리는 폭포를 대부분 평평하게 만들었습니다! 하지만 문제가 있습니다. 이 페이지를 `/feed` 페이지라고 부르고 `/posts`와 같은 다른 페이지도 있다고 가정해 보겠습니다. URL 표시줄에 `www.example.com/feed`를 직접 입력하고 Enter 키를 누르면 이러한 훌륭한 서버 렌더링 이점을 모두 얻을 수 있지만 대신 `www.example.com/posts`를 입력한 다음 `/feed`에 대한 **링크를 클릭**하면 다음으로 돌아갑니다.

```
1. |> JS for <Feed>
2.   |> getFeed()
3.     |> JS for <GraphFeedItem>
4.       |> getGraphDataById()
```
이는 SPA를 사용하면 서버 렌더링이 후속 탐색이 아닌 초기 페이지 로드에만 작동하기 때문입니다.

최신 프레임워크는 초기 코드와 데이터를 병렬로 가져와서 이 문제를 해결하려고 하는 경우가 많습니다. 따라서 종속 queries를 프리페치하는 방법을 포함하여 이 가이드에 설명된 프리페치 패턴과 함께 Next.js 또는 Remix를 사용하는 경우 실제로는 다음과 같습니다.

```
1. |> JS for <Feed>
1. |> getFeed() + getGraphDataById()
2.   |> JS for <GraphFeedItem>
```
이것이 훨씬 낫지만 이를 더욱 개선하려면 서버 구성 요소를 사용하여 단일 왕복으로 이를 평면화할 수 있습니다. [고급 서버 렌더링 가이드](advanced-ssr.md)에서 방법을 알아보세요.

## 팁, 요령 및 주의 사항

### 오래된 상태는 서버에서 query를 가져온 시점부터 측정됩니다.

query는 `dataUpdatedAt`였던 시기에 따라 오래된 것으로 간주됩니다. 여기서 주의할 점은 이것이 제대로 작동하려면 서버의 정확한 시간이 필요하지만 UTC 시간이 사용되므로 시간대는 이를 고려하지 않는다는 것입니다.

`staleTime`의 기본값은 `0`이므로 queries는 기본적으로 페이지 로드 시 백그라운드에서 다시 가져옵니다. 특히 마크업을 캐시하지 않는 경우 이러한 이중 가져오기를 방지하려면 더 높은 `staleTime`를 사용하는 것이 좋습니다.

오래된 queries를 다시 가져오는 것은 CDN에서 마크업을 캐싱할 때 완벽하게 일치합니다! 서버에서 페이지를 다시 렌더링할 필요가 없도록 페이지 자체의 캐시 시간을 상당히 높게 설정할 수 있지만, 사용자가 페이지를 방문하자마자 백그라운드에서 데이터를 다시 가져오도록 queries의 `staleTime`를 더 낮게 구성할 수 있습니다. 일주일 동안 페이지를 캐시하고 싶지만 하루보다 오래된 경우 페이지 로드 시 자동으로 데이터를 다시 가져오고 싶을 수도 있습니다.

### 서버의 높은 메모리 소비

모든 요청에 ​​대해 `QueryClient`를 생성하는 경우 React Query는 이 클라이언트에 대해 격리된 캐시를 생성하며 이는 `gcTime` 기간 동안 메모리에 보존됩니다. 해당 기간 동안 요청 수가 많은 경우 서버의 메모리 소비가 높아질 수 있습니다.

서버에서 `gcTime`는 수동 가비지 수집을 비활성화하고 요청이 완료되면 자동으로 메모리를 지우는 `Infinity`로 기본 설정됩니다. Infinity가 아닌 `gcTime`를 명시적으로 설정하는 경우 캐시를 조기에 지워야 합니다.

`gcTime`를 `0`로 설정하면 hydration 오류가 발생할 수 있으므로 설정하지 마세요. 이는 [hydration](../reference/hydration.md#hydrationboundary)가 렌더링을 위해 필요한 데이터를 캐시에 배치하기 때문에 발생하지만, 렌더링이 완료되기 전에 가비지 수집기가 데이터를 제거하면 문제가 발생할 수 있습니다. 더 짧은 `gcTime`가 필요한 경우 앱이 데이터를 참조하는 데 충분한 시간을 허용하도록 `2 * 1000`로 설정하는 것이 좋습니다.

필요하지 않은 캐시를 지우고 메모리 소비를 줄이려면 요청이 처리되고 탈수 상태가 클라이언트에 전송된 후 [QueryClient](../../../reference/QueryClient.md#queryclientclear)에 대한 호출을 추가할 수 있습니다.

또는 더 작은 `gcTime`를 설정할 수 있습니다.

### Next.js 재작성에 대한 주의사항

[자동 정적 최적화](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) 또는 `getStaticProps`와 함께 [Next.js의 재작성 기능](https://nextjs.org/docs/app/api-reference/next-config-js/rewrites)을 사용하는 경우 문제가 있습니다. hydration by React Query. 그 이유는 [Next.js가 클라이언트에서 재작성을 구문 분석](https://nextjs.org/docs/app/api-reference/next-config-js/rewrites#rewrite-parameters)하고 hydration 이후의 모든 매개변수를 수집하여 `router.query`에서 제공될 수 있도록 해야 하기 때문입니다.

그 결과 모든 hydration 데이터에 대한 참조 동등성이 누락되었습니다. 예를 들어 데이터가 구성 요소의 소품으로 사용되거나 `useEffect`s/`useMemo`s의 종속성 배열에서 사용될 때마다 트리거됩니다.