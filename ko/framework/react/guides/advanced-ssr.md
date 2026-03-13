---
id: advanced-ssr
title: 고급 서버 렌더링
---




스트리밍, 서버 구성 요소 및 Next.js 앱 라우터와 함께 React Query를 사용하는 방법에 대해 모두 배울 수 있는 고급 서버 렌더링 가이드에 오신 것을 환영합니다.

이 가이드 전에 [서버 렌더링 및 Hydration 가이드](ssr.md)를 읽어보는 것이 좋습니다. 이 가이드에서는 SSR과 함께 React Query를 사용하기 위한 기본 사항을 설명하고, [성능 및 요청 워터폴](request-waterfalls.md)과 [프리페칭 및 라우터 통합](prefetching.md)에도 귀중한 배경 지식이 포함되어 있습니다.

시작하기 전에 SSR 가이드에 설명된 `initialData` 접근 방식이 서버 구성 요소에서도 작동하지만 이 가이드에서는 hydration API에 중점을 둘 것입니다.

## 서버 구성 요소 및 Next.js 앱 라우터

여기서는 서버 구성 요소를 자세히 다루지 않지만 간략하게 설명하면 초기 페이지 보기와 **페이지 전환 시** 모두 서버에서 _만_ 실행이 보장되는 구성 요소라는 점입니다. 이는 Next.js `getServerSideProps`/`getStaticProps` 및 Remix `loader`가 작동하는 방식과 유사합니다. 이들 역시 항상 서버에서 실행되지만 데이터만 반환할 수 있지만 서버 구성 요소는 더 많은 작업을 수행할 수 있습니다. 그러나 데이터 부분은 React Query의 핵심이므로 이에 집중하겠습니다.

[프레임워크 로더에서 미리 가져온 데이터를 앱에 전달](ssr.md#using-the-hydration-apis)에 대해 서버 렌더링 가이드에서 배운 내용을 어떻게 서버 구성 요소 및 Next.js 앱 라우터에 적용합니까? 이에 대해 생각하기 시작하는 가장 좋은 방법은 서버 구성 요소를 "그냥" 또 다른 프레임워크 로더로 간주하는 것입니다.

### 용어에 대한 간단한 참고 사항

지금까지 이 가이드에서는 _server_와 _client_에 대해 이야기했습니다. 혼란스럽게도 이는 _서버 구성 요소_ 및 _클라이언트 구성 요소_와 1-1로 일치하지 않는다는 점에 유의하는 것이 중요합니다. 서버 구성 요소는 서버에서만 실행되도록 보장되지만 클라이언트 구성 요소는 실제로 두 위치 모두에서 실행될 수 있습니다. 그 이유는 초기 _서버 렌더링_ 패스 중에도 렌더링할 수 있기 때문입니다.

이를 생각하는 한 가지 방법은 서버 구성 요소도 _렌더링_하더라도 "로더 단계"(항상 서버에서 발생) 중에 발생하는 반면 클라이언트 구성 요소는 "응용 프로그램 단계" 중에 실행된다는 것입니다. 해당 애플리케이션은 SSR 동안 서버와 브라우저 등에서 모두 실행될 수 있습니다. 해당 애플리케이션이 정확히 실행되는 위치와 SSR 중에 실행되는지 여부는 프레임워크마다 다를 수 있습니다.

### 초기 설정

React Query 설정의 첫 번째 단계는 항상 `queryClient`를 생성하고 애플리케이션을 `QueryClientProvider`에 래핑하는 것입니다. 서버 구성 요소를 사용하면 이는 프레임워크 전체에서 거의 동일하게 보입니다. 한 가지 차이점은 파일 이름 규칙입니다.

```tsx
// Next.js에서 이 파일은 app/providers.tsx라고 합니다.
'use client'

// QueryClientProvider는 내부적으로 useContext를 사용하므로 'use client'를 맨 위에 놓아야 합니다.
import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
        // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
        staleTime: 60 * 1000,
      },
    },
  })
}

let browserQueryClient: QueryClient | undefined = undefined

function getQueryClient() {
  if (isServer) {
    // 서버: 항상 새로운 query 클라이언트를 만드세요
    return makeQueryClient()
  } else {
    // 브라우저: 아직 없는 경우 새 query 클라이언트를 만듭니다.
    // 이는 매우 중요하므로 React가 다음과 같은 경우 새 클라이언트를 다시 만들지 않습니다.
    // 초기 렌더링 중에 일시 중지됩니다. 다음과 같은 경우에는 이것이 필요하지 않을 수도 있습니다.
    // query 클라이언트 생성 아래에 suspense 경계가 있습니다.
    if (!browserQueryClient) browserQueryClient = makeQueryClient()
    return browserQueryClient
  }
}

export default function Providers({ children }: { children: React.ReactNode }) {
  // 참고: query 클라이언트를 초기화할 때 useState를 사용하지 마세요.
  //       이 코드와 코드 사이에 suspense 경계가 있습니다.
  //       React가 초기에 클라이언트를 버릴 것이기 때문에 일시 중지하세요.
  //       일시 중단되고 경계가 없는 경우 렌더링
  const queryClient = getQueryClient()

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}
```

```tsx
// Next.js에서 이 파일은 app/layout.tsx라고 합니다.
import Providers from './providers'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head />
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```
이 부분은 SSR 가이드에서 수행한 작업과 매우 유사합니다. 두 개의 다른 파일로 분할하면 됩니다.

### 데이터 미리 가져오기 및 디하이드레이션

다음으로 실제로 데이터를 프리페치한 후 디하이드레이션(dehydrate) 및 하이드레이션(hydrate)하는 방법을 살펴보겠습니다. **Next.js Pages Router**를 사용한 모습은 다음과 같습니다.

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
  //
  // 여기서는 useSuspenseQuery 대신 useQuery를 사용하고 있습니다.
  // 이 데이터는 이미 프리페치되었으므로 따로 작업할 필요가 없습니다.
  // 구성 요소 자체에서 일시 중지됩니다. 잊어버리거나 제거한 경우
  // 프리페치하면 대신 클라이언트에서 데이터를 가져옵니다.
  // useSuspenseQuery를 사용하면 부작용이 더 심해졌습니다.
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
이것을 앱 라우터로 변환하는 것은 실제로 매우 유사해 보이지만 약간만 이동하면 됩니다. 먼저, 프리페치 부분을 수행하기 위해 서버 구성 요소를 만듭니다.

```tsx
// 앱/게시물/page.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import Posts from './posts'

export default async function PostsPage() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return (
    // 정돈된! 이제 직렬화는 props를 전달하는 것만큼 쉽습니다.
    // HydrationBoundary는 ​​클라이언트 구성 요소이므로 hydration가 여기에서 발생합니다.
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}
```
다음으로 클라이언트 구성 요소 부분이 어떻게 보이는지 살펴보겠습니다.

```tsx
// 앱/게시물/posts.tsx
'use client'

export default function Posts() {
  // 이 useQuery는 좀 더 깊은 곳에서도 일어날 수 있습니다.
  // <Posts>의 하위 항목인 경우 어느 쪽이든 즉시 데이터를 사용할 수 있습니다.
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: () => getPosts(),
  })

  // 이 query는 서버에서 프리페치되지 않았으며 시작되지 않습니다.
  // 클라이언트에서 가져오는 동안 두 패턴을 혼합해도 괜찮습니다.
  const { data: commentsData } = useQuery({
    queryKey: ['posts-comments'],
    queryFn: getComments,
  })

  // ...
}
```
위의 예에서 한 가지 좋은 점은 여기에서 Next.js와 관련된 유일한 것은 파일 이름이고 다른 모든 것은 서버 구성 요소를 지원하는 다른 프레임워크에서 동일하게 보일 것이라는 것입니다.

SSR 가이드에서 모든 경로에 `<HydrationBoundary>`가 있다는 상용구를 제거할 수 있다고 언급했습니다. 이는 서버 구성 요소에서는 불가능합니다.

> 참고: `5.1.3`보다 낮은 TypeScript 버전 및 `18.2.8`보다 낮은 `@types/react` 버전으로 비동기 서버 구성 요소를 사용하는 동안 유형 오류가 발생하는 경우 두 가지 모두 최신 버전으로 업데이트하는 것이 좋습니다. 또는 다른 구성 요소 내부에서 이 구성 요소를 호출할 때 `{/* @ts-expect-error Server Component */}`를 추가하는 임시 해결 방법을 사용할 수 있습니다. 자세한 내용은 Next.js 13 문서의 [비동기 서버 구성 요소 TypeScript 오류](https://nextjs.org/docs/app/building-your-application/configuring/typescript#async-server-comComponent-typescript-error)를 참조하세요.

> 참고: `Only plain objects, and a few built-ins, can be passed to Server Actions. Classes or null prototypes are not supported.` 오류가 발생하는 경우 함수 참조를 queryFn에 전달하지 **않았는지** 확인하세요. 대신 queryFn args에 많은 속성이 있고 일부 속성이 직렬화되지 않기 때문에 함수를 호출하세요. [서버 작업은 queryFn가 참조가 아닌 경우에만 작동합니다](https://github.com/TanStack/query/issues/6264)를 참조하세요.

### 중첩 서버 구성 요소

서버 구성 요소의 좋은 점은 React 트리의 여러 수준에 중첩되어 존재할 수 있다는 것입니다. 이를 통해 애플리케이션의 맨 위(Remix 로더와 마찬가지로)에서만 데이터를 사용하는 대신 실제로 사용되는 위치에 더 가까운 위치에서 데이터를 미리 가져올 수 있습니다. 이는 서버 구성요소가 다른 서버 구성요소를 렌더링하는 것처럼 간단할 수 있습니다(간결함을 위해 이 예에서는 클라이언트 구성요소를 생략하겠습니다).

```tsx
// 앱/게시물/page.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import Posts from './posts'
import CommentsServerComponent from './comments-server'

export default async function PostsPage() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
      <CommentsServerComponent />
    </HydrationBoundary>
  )
}

// 앱/게시물/comments-server.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import Comments from './comments'

export default async function CommentsServerComponent() {
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts-comments'],
    queryFn: getComments,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Comments />
    </HydrationBoundary>
  )
}
```
보시다시피 `<HydrationBoundary>`를 여러 장소에서 사용하고 프리페칭을 위해 여러 `queryClient`를 만들고 탈수하는 것은 완벽합니다.

`CommentsServerComponent`를 렌더링하기 전에 `getPosts`를 기다리고 있기 때문에 서버 측 워터폴로 이어질 수 있습니다.

```
1. |> getPosts()
2.   |> getComments()
```
데이터에 대한 서버 대기 시간이 짧은 경우 이는 큰 문제가 아닐 수 있지만 여전히 지적할 가치가 있습니다.

Next.js에서는 `page.tsx`의 데이터를 미리 가져오는 것 외에도 `layout.tsx` 및 [병렬 경로](https://nextjs.org/docs/app/building-your-application/routing/parallel-routes)에서도 수행할 수 있습니다. 이것들은 모두 라우팅의 일부이기 때문에 Next.js는 그것들을 모두 병렬로 가져오는 방법을 알고 있습니다. 따라서 위의 `CommentsServerComponent`를 대신 병렬 경로로 표현하면 폭포가 자동으로 평탄해집니다.

더 많은 프레임워크가 서버 구성 요소를 지원하기 시작하면 다른 라우팅 규칙이 있을 수 있습니다. 자세한 내용은 프레임워크 문서를 읽어보세요.

### 대안: 프리페치에 단일 `queryClient` 사용

위의 예에서는 데이터를 가져오는 각 서버 구성 요소에 대해 새 `queryClient`를 만듭니다. 이는 권장되는 접근 방식이지만 원하는 경우 모든 서버 구성 요소에서 재사용되는 단일 접근 방식을 만들 수도 있습니다.

```tsx
// 앱/getQueryClient.tsx
import { QueryClient } from '@tanstack/react-query'
import { cache } from 'react'

// 캐시()는 요청별로 범위가 지정되므로 요청 간에 데이터가 누출되지 않습니다.
const getQueryClient = cache(() => new QueryClient())
export default getQueryClient
```
이것의 이점은 `getQueryClient()`를 호출하여 유틸리티 기능을 포함하여 서버 구성 요소에서 호출되는 모든 위치에서 이 클라이언트를 확보할 수 있다는 것입니다. 단점은 `dehydrate(getQueryClient())`를 호출할 때마다 이전에 이미 직렬화되었으며 불필요한 오버헤드가 되는 현재 서버 구성 요소와 관련되지 않은 queries를 포함하여 _전체_ `queryClient`를 직렬화한다는 것입니다.

Next.js는 이미 `fetch()`를 활용하는 요청을 중복 제거하지만, `queryFn`에서 다른 것을 사용 중이거나 이러한 요청을 자동으로 중복 제거하지 _않는_ 프레임워크를 사용하는 경우 중복된 직렬화에도 불구하고 위에 설명된 단일 `queryClient`를 사용하는 것이 합리적일 수 있습니다.

> 향후 개선 사항으로 `dehydrateNew()`에 대한 마지막 호출 이후 _새로운_ queries만 탈수하는 `dehydrateNew()` 함수(이름 미정) 생성을 고려할 수 있습니다. 이 내용이 흥미롭고 도움을 주고 싶은 내용이라면 언제든지 연락해 주세요!

### 데이터 소유권 및 재검증

서버 구성 요소에서는 데이터 소유권과 재검증에 대해 생각하는 것이 중요합니다. 이유를 설명하기 위해 위에서 수정된 예를 살펴보겠습니다.

```tsx
// 앱/게시물/page.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import Posts from './posts'

export default async function PostsPage() {
  const queryClient = new QueryClient()

  // 지금은 fetchQuery()를 사용하고 있습니다.
  const posts = await queryClient.fetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      {/* 이게 새로운 부분이에요 */}
      <div>Nr of posts: {posts.length}</div>
      <Posts />
    </HydrationBoundary>
  )
}
```
이제 서버 구성 요소와 클라이언트 구성 요소 모두에서 `getPosts` query의 데이터를 렌더링하고 있습니다. 초기 페이지 렌더링에는 문제가 없지만 `staleTime`가 전달되었을 때 어떤 이유로 클라이언트에서 query가 재검증되면 어떻게 됩니까?

React Query는 _서버 구성 요소의 유효성을 다시 검사_하는 방법을 모르므로 클라이언트에서 데이터를 다시 가져오면 React가 게시물 목록을 다시 렌더링하게 되고 `Nr of posts: {posts.length}`는 결국 동기화되지 않게 됩니다.

`staleTime: Infinity`를 설정하면 React Query가 재검증되지 않도록 설정하면 괜찮지만 처음에 React Query를 사용하는 경우에는 원하는 것이 아닐 수도 있습니다.

다음과 같은 경우 서버 구성요소와 함께 React Query를 사용하는 것이 가장 적합합니다.

- React Query를 사용하는 앱이 있고 모든 데이터 가져오기를 다시 작성하지 않고 서버 구성 요소로 마이그레이션하고 싶습니다.
- 친숙한 프로그래밍 패러다임을 원하지만 가장 적합한 곳에 서버 구성 요소의 이점을 계속 적용하고 싶습니다.
- React Query에서 다루는 사용 사례가 있지만 선택한 프레임워크에서 다루지 않는 경우가 있습니다.

React Query를 서버 구성요소와 페어링하는 것이 적합한지 여부에 대해 일반적인 조언을 제공하기는 어렵습니다. **새 서버 구성 요소 앱을 시작하는 경우 프레임워크에서 제공하는 데이터 가져오기 도구로 시작하고 실제로 필요할 때까지 React Query를 가져오지 않는 것이 좋습니다.** 절대 그렇지 않을 수도 있지만 괜찮습니다. 작업에 적합한 도구를 사용하세요!

이를 사용하는 경우 오류를 잡아야 하는 경우가 아니면 `queryClient.fetchQuery`를 피하는 것이 좋은 경험 법칙입니다. 이를 사용하는 경우 결과를 서버에 렌더링하거나 결과를 다른 구성 요소(클라이언트 구성 요소라도 포함)에 전달하지 마십시오.

React Query 관점에서 볼 때 서버 구성 요소를 데이터를 미리 가져오는 장소로 취급합니다.

물론 서버 구성 요소가 일부 데이터를 소유하고 클라이언트 구성 요소가 다른 데이터를 소유하는 것은 괜찮습니다. 다만 이 두 가지 현실이 동기화되지 않는지 확인하세요.

## 서버 구성 요소를 사용한 스트리밍

Next.js 앱 라우터는 가능한 한 빨리 브라우저에 표시할 준비가 된 애플리케이션의 모든 부분을 자동으로 스트리밍하므로 아직 보류 중인 콘텐츠를 기다리지 않고 완성된 콘텐츠를 즉시 표시할 수 있습니다. `<Suspense>` 경계선을 따라 이 작업을 수행합니다. `loading.tsx` 파일을 생성하면 자동으로 내부적으로 `<Suspense>` 경계가 생성됩니다.

위에서 설명한 프리페치 패턴을 사용하면 React Query는 이러한 형태의 스트리밍과 완벽하게 호환됩니다. 각 Suspense 경계에 대한 데이터가 확인되면 Next.js는 완성된 콘텐츠를 브라우저에 렌더링하고 스트리밍할 수 있습니다. 프리페치를 `await`할 때 일시중단이 실제로 발생하기 때문에 위에 설명된 대로 `useQuery`를 사용하는 경우에도 작동합니다.

React Query v5.40.0부터는 `await`가 작동하기 위해 모든 프리페치를 수행할 필요가 없습니다. `pending` Queries도 탈수되어 클라이언트에 전송될 수 있기 때문입니다. 이를 통해 전체 Suspense 경계를 차단하지 않고 가능한 한 빨리 프리페치를 시작할 수 있으며 query가 완료되면 _data_를 클라이언트로 스트리밍할 수 있습니다. 예를 들어 일부 사용자 상호 작용 후에만 표시되는 일부 콘텐츠를 프리페치하려는 경우 또는 `await`를 수행하고 무한 query의 첫 번째 페이지를 렌더링하되 렌더링을 차단하지 않고 페이지 2 프리페치를 시작하는 경우에 유용할 수 있습니다.

이 작업을 수행하려면 `queryClient`에 Queries 보류 중인 `dehydrate`도 지시해야 합니다. 이를 전역적으로 수행하거나 해당 옵션을 `dehydrate`에 직접 전달하여 수행할 수 있습니다.

또한 서버 구성 요소와 클라이언트 공급자에서 사용하려면 `getQueryClient()` 기능을 `app/providers.tsx` 파일 밖으로 이동해야 합니다.

```tsx
// 앱/get-query-client.ts
import {
  isServer,
  QueryClient,
  defaultShouldDehydrateQuery,
} from '@tanstack/react-query'

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
      },
      dehydrate: {
        // 탈수에 보류 중인 queries 포함
        shouldDehydrateQuery: (query) =>
          defaultShouldDehydrateQuery(query) ||
          query.state.status === 'pending',
        shouldRedactErrors: (error) => {
          // Next.js 서버 오류를 잡아서는 안 됩니다.
          // 이것이 Next.js가 동적 페이지를 감지하는 방법입니다.
          // 그래서 우리는 그것들을 수정할 수 없습니다.
          // Next.js는 자동으로 오류를 수정합니다.
          // 더 나은 다이제스트와 함께.
          return false
        },
      },
    },
  })
}

let browserQueryClient: QueryClient | undefined = undefined

export function getQueryClient() {
  if (isServer) {
    // 서버: 항상 새로운 query 클라이언트를 만드세요
    return makeQueryClient()
  } else {
    // 브라우저: 아직 없는 경우 새 query 클라이언트를 만듭니다.
    // 이는 매우 중요하므로 React가 다음과 같은 경우 새 클라이언트를 다시 만들지 않습니다.
    // 초기 렌더링 중에 일시 중지됩니다. 다음과 같은 경우에는 이것이 필요하지 않을 수도 있습니다.
    // query 클라이언트 생성 아래에 suspense 경계가 있습니다.
    if (!browserQueryClient) browserQueryClient = makeQueryClient()
    return browserQueryClient
  }
}
```
> 참고: 이는 React가 Promise를 클라이언트 구성 요소에 전달할 때 유선을 통해 직렬화할 수 있기 때문에 NextJ 및 서버 구성 요소에서 작동합니다.

그런 다음 우리가 해야 할 일은 `HydrationBoundary`를 제공하는 것뿐이지만 더 이상 `await` 프리페치가 필요하지 않습니다.

```tsx
// 앱/게시물/page.tsx
import { dehydrate, HydrationBoundary } from '@tanstack/react-query'
import { getQueryClient } from './get-query-client'
import Posts from './posts'

// 함수는 아무것도 '기다리지' 않기 때문에 '비동기'일 필요가 없습니다.
export default function PostsPage() {
  const queryClient = getQueryClient()

  // 봐봐 엄마, 안돼 기다려
  queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}
```
클라이언트에서는 Promise가 QueryCache에 저장됩니다. 즉, 이제 `Posts` 구성 요소 내에서 `useSuspenseQuery`를 호출하여 해당 Promise(서버에서 생성됨)를 "사용"할 수 있습니다.

```tsx
// 앱/게시물/posts.tsx
'use client'

export default function Posts() {
  const { data } = useSuspenseQuery({ queryKey: ['posts'], queryFn: getPosts })

  // ...
}
```
> `useSuspenseQuery` 대신 `useQuery`를 사용할 수도 있으며 Promise는 여전히 올바르게 선택됩니다. 그러나 이 경우 NextJ는 일시 중지되지 않으며 구성 요소는 `pending` 상태로 렌더링되며 서버 콘텐츠 렌더링도 옵트아웃됩니다.

JSON이 아닌 데이터 유형을 사용하고 서버에서 query 결과를 직렬화하는 경우 `dehydrate.serializeData` 및 `hydrate.deserializeData` 옵션을 지정하여 경계 양쪽의 데이터를 직렬화 및 역직렬화하여 캐시의 데이터가 서버와 클라이언트 모두에서 동일한 형식이 되도록 할 수 있습니다.

```tsx
// 앱/get-query-client.ts
import { QueryClient, defaultShouldDehydrateQuery } from '@tanstack/react-query'
import { deserialize, serialize } from './transformer'

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      // ...
      hydrate: {
        deserializeData: deserialize,
      },
      dehydrate: {
        serializeData: serialize,
      },
    },
  })
}

// ...
```

```tsx
// 앱/게시물/page.tsx
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import { getQueryClient } from './get-query-client'
import { serialize } from './transformer'
import Posts from './posts'

export default function PostsPage() {
  const queryClient = getQueryClient()

  // 봐봐 엄마, 안돼 기다려
  queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: () => getPosts().then(serialize), // <-- 서버의 데이터를 직렬화합니다.
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}
```

```tsx
// 앱/게시물/posts.tsx
'use client'

export default function Posts() {
  const { data } = useSuspenseQuery({ queryKey: ['posts'], queryFn: getPosts })

  // ...
}
```
이제 `getPosts` 함수는 예를 들어 다음을 반환할 수 있습니다. 변환기가 해당 데이터 유형을 직렬화 및 역직렬화할 수 있다고 가정하면 `Temporal` 날짜/시간 개체와 데이터는 클라이언트에서 직렬화 및 역직렬화됩니다.

자세한 내용은 [Prefetching 예제가 포함된 Next.js 앱](../examples/nextjs-app-prefetching.md)을 확인하세요.

### 스트리밍에 지속 어댑터 사용

[서버 구성 요소를 사용한 스트리밍](#streaming-with-server-comComponents) 기능과 함께 지속 어댑터를 사용하는 경우 Promise을 저장소에 저장하지 않도록 주의해야 합니다. 보류 중인 queries는 디하이드레이션되어 클라이언트로 스트리밍될 수 있으므로 성공적인 queries만 유지하도록 지속기를 구성해야 합니다.

```tsx
<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,
    // Promise를 스토리지에 저장하고 싶지 않으므로 성공적인 queries만 유지합니다.
    dehydrateOptions: { shouldDehydrateQuery: defaultShouldDehydrateQuery },
  }}
>
  {children}
</PersistQueryClientProvider>
```
이렇게 하면 성공적으로 해결된 queries만 스토리지에 유지되어 보류 중인 Promise과 관련된 직렬화 문제를 방지할 수 있습니다.

## Next.js에서 미리 가져오지 않고 실험적으로 스트리밍

위에 자세히 설명된 프리페치 솔루션은 초기 페이지 로드 및 후속 페이지 탐색 모두에서 요청 워터폴을 평탄화하므로 권장되지만, 프리페치를 완전히 건너뛰고 스트리밍 SSR 작업을 계속 수행할 수 있는 실험적인 방법이 있습니다. `@tanstack/react-query-next-experimental`

이 패키지를 사용하면 구성 요소에서 `useSuspenseQuery`를 호출하여 서버(클라이언트 구성 요소)에서 데이터를 가져올 수 있습니다. 그런 다음 SuspenseBoundaries가 해결되면 결과가 서버에서 클라이언트로 스트리밍됩니다. `<Suspense>` 경계에 래핑하지 않고 `useSuspenseQuery`를 호출하면 가져오기가 해결될 때까지 HTML 응답이 시작되지 않습니다. 이는 상황에 따라 원할 때일 수 있지만 이로 인해 TTFB가 손상될 수 있다는 점을 명심하세요.

이를 달성하려면 `ReactQueryStreamedHydration` 구성 요소에 앱을 래핑하세요.

```tsx
// 앱/providers.tsx
'use client'

import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import * as React from 'react'
import { ReactQueryStreamedHydration } from '@tanstack/react-query-next-experimental'

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // SSR을 사용하면 일반적으로 일부 기본 staleTime를 설정하려고 합니다.
        // 클라이언트에서 즉시 다시 가져오는 것을 방지하려면 0 이상
        staleTime: 60 * 1000,
      },
    },
  })
}

let browserQueryClient: QueryClient | undefined = undefined

function getQueryClient() {
  if (isServer) {
    // 서버: 항상 새로운 query 클라이언트를 만드세요
    return makeQueryClient()
  } else {
    // 브라우저: 아직 없는 경우 새 query 클라이언트를 만듭니다.
    // 이는 매우 중요하므로 React가 다음과 같은 경우 새 클라이언트를 다시 만들지 않습니다.
    // 초기 렌더링 중에 일시 중지됩니다. 다음과 같은 경우에는 이것이 필요하지 않을 수도 있습니다.
    // query 클라이언트 생성 아래에 suspense 경계가 있습니다.
    if (!browserQueryClient) browserQueryClient = makeQueryClient()
    return browserQueryClient
  }
}

export function Providers(props: { children: React.ReactNode }) {
  // 참고: query 클라이언트를 초기화할 때 useState를 사용하지 마세요.
  //       이 코드와 코드 사이에 suspense 경계가 있습니다.
  //       React가 초기에 클라이언트를 버릴 것이기 때문에 일시 중지하세요.
  //       일시 중단되고 경계가 없는 경우 렌더링
  const queryClient = getQueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryStreamedHydration>
        {props.children}
      </ReactQueryStreamedHydration>
    </QueryClientProvider>
  )
}
```
자세한 내용은 [NextJs Suspense 스트리밍 예제](../examples/nextjs-suspense-streaming.md)를 확인하세요.

가장 큰 장점은 SSR 작업을 위해 더 이상 수동으로 queries를 프리페치할 필요가 없으며 결과도 계속 스트리밍된다는 것입니다! 이는 놀라운 DX와 낮은 코드 복잡성을 제공합니다.

성능 및 요청 폭포수 가이드의 [복잡한 요청 폭포수 예시](request-waterfalls.md#code-splitting)를 살펴보면 단점을 가장 쉽게 설명할 수 있습니다. 프리페칭 기능이 있는 서버 구성 요소는 초기 페이지 로드 **및** 후속 탐색 모두에 대한 요청 폭포를 효과적으로 제거합니다. 그러나 이 프리페치 없는 접근 방식은 초기 페이지 로드 시 폭포수를 평탄화할 뿐이지만 페이지 탐색의 원래 예와 동일한 깊은 폭포수로 끝납니다.

```
1. |> JS for <Feed>
2.   |> getFeed()
3.     |> JS for <GraphFeedItem>
4.       |> getGraphDataById()
```
이는 `getServerSideProps`/`getStaticProps`보다 훨씬 더 나쁩니다. 왜냐하면 최소한 데이터 및 코드 가져오기를 병렬화할 수 있기 때문입니다.

성능보다 코드 복잡성이 낮은 DX/반복/배송 속도를 중시하거나 queries를 깊게 중첩하지 않거나 `useSuspenseQueries`와 같은 도구를 사용하여 병렬 가져오기를 통해 요청 폭포 위에 있는 경우 이는 좋은 절충안이 될 수 있습니다.

> 두 가지 접근 방식을 결합하는 것이 가능할 수도 있지만 아직 시도해 본 적은 없습니다. 이 방법을 시도한다면 결과를 다시 보고하거나 몇 가지 팁으로 이 문서를 업데이트하세요!

## 마지막 말

서버 구성 요소 및 스트리밍은 여전히 ​​상당히 새로운 개념이며 우리는 React Query가 어떻게 적용되고 API에 어떤 개선 사항을 적용할 수 있는지 계속 파악하고 있습니다. 제안, 피드백, 버그 신고를 환영합니다!

마찬가지로, 첫 번째 시도에서 이 새로운 패러다임의 모든 복잡성을 하나의 가이드로 모두 가르치는 것은 불가능합니다. 여기에 누락된 정보가 있거나 이 콘텐츠를 개선하는 방법에 대한 제안이 있거나 연락을 주거나 더 나은 경우 아래의 "GitHub에서 편집" 버튼을 클릭하여 도움을 주세요.

[//]: # 'Materials'

## 추가 자료

서버 구성 요소도 사용할 때 애플리케이션이 React Query의 이점을 누릴 수 있는지 이해하려면 [React Query가 필요하지 않을 수도 있음](https://tkdodo.eu/blog/you-might-not-need-react-query) 문서를 참조하세요.

[//]: # 'Materials'
