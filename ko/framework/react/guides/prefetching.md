---
id: prefetching
title: 프리패치 및 라우터 통합
---




특정 데이터 조각이 필요하다는 것을 알고 있거나 의심되는 경우 프리페칭을 사용하여 미리 해당 데이터로 캐시를 채워 더 빠른 경험을 제공할 수 있습니다.

몇 가지 프리페치 패턴이 있습니다.

1. 이벤트 핸들러에서
2. 구성 요소에서
3. 라우터 통합을 통해
4. 서버 렌더링 중(라우터 통합의 또 다른 형태)

이 가이드에서는 처음 세 가지를 살펴보고, 네 번째는 [서버 렌더링 & Hydration 가이드](ssr.md) 및 [고급 서버 렌더링 가이드](advanced-ssr.md)에서 자세히 설명합니다.

프리페칭의 구체적인 용도 중 하나는 요청 폭포수를 방지하는 것입니다. 이에 대한 심층적인 배경과 설명은 [성능 및 요청 폭포수 가이드](request-waterfalls.md)를 참조하세요.

## prefetchQuery & prefetchInfiniteQuery

다양한 특정 프리페치 패턴을 살펴보기 전에 `prefetchQuery` 및 `prefetchInfiniteQuery` 기능을 살펴보겠습니다. 먼저 몇 가지 기본 사항:

- 기본적으로 이러한 기능은 `queryClient`에 대해 구성된 기본 `staleTime`를 사용하여 캐시의 기존 데이터가 최신인지 또는 다시 가져와야 하는지 확인합니다.
- 다음과 같이 특정 `staleTime`를 전달할 수도 있습니다: `prefetchQuery({ queryKey: ['todos'], queryFn: fn, staleTime: 5000 })`
  - 이 `staleTime`는 프리페치에만 사용되며 모든 `useQuery` 호출에도 설정해야 합니다.
  - `staleTime`를 무시하고 대신 캐시에 사용 가능한 데이터가 있으면 항상 반환하려는 경우 `ensureQueryData` 함수를 사용할 수 있습니다.
  - 팁: 서버에서 프리페치를 수행하는 경우 각 프리페치 호출에 특정 `staleTime`를 전달할 필요가 없도록 해당 `queryClient`에 대해 기본 `staleTime`를 `0`보다 높게 설정하세요.
- 프리패치된 query에 대해 `useQuery`의 인스턴스가 나타나지 않으면 `gcTime`에 지정된 시간 이후에 삭제되고 가비지 수집됩니다.
- 이 함수는 `Promise<void>`를 반환하므로 query 데이터를 반환하지 않습니다. 이것이 필요한 경우 대신 `fetchQuery`/`fetchInfiniteQuery`를 사용하세요.
- 프리페치 함수는 일반적으로 멋진 폴백인 `useQuery`에서 다시 가져오기를 시도하기 때문에 오류를 발생시키지 않습니다. 오류를 포착해야 하는 경우 대신 `fetchQuery`/`fetchInfiniteQuery`를 사용하세요.

`prefetchQuery`를 사용하는 방법은 다음과 같습니다.

[//]: # 'ExamplePrefetchQuery'

```tsx
const prefetchTodos = async () => {
  // 이 query의 결과는 일반 query처럼 캐시됩니다.
  await queryClient.prefetchQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })
}
```
[//]: # 'ExamplePrefetchQuery'

Infinite Queries는 일반 Queries처럼 프리패치할 수 있습니다. 기본적으로 Query의 첫 번째 페이지만 프리페치되어 지정된 QueryKey에 저장됩니다. 두 개 이상의 페이지를 프리페치하려는 경우 `pages` 옵션을 사용할 수 있으며, 이 경우 `getNextPageParam` 기능도 제공해야 합니다.

[//]: # 'ExamplePrefetchInfiniteQuery'

```tsx
const prefetchProjects = async () => {
  // 이 query의 결과는 일반 query처럼 캐시됩니다.
  await queryClient.prefetchInfiniteQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
    initialPageParam: 0,
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    pages: 3, // 처음 3페이지 미리 가져오기
  })
}
```
[//]: # 'ExamplePrefetchInfiniteQuery'

다음으로 다양한 상황에서 이러한 방법과 다른 방법을 사용하여 프리페치를 수행하는 방법을 살펴보겠습니다.

## 이벤트 핸들러에서 프리패치

프리패치의 간단한 형태는 사용자가 무언가와 상호작용할 때 이를 수행하는 것입니다. 이 예에서는 `queryClient.prefetchQuery`를 사용하여 `onMouseEnter` 또는 `onFocus`에서 프리페치를 시작합니다.

[//]: # 'ExampleEventHandler'

```tsx
function ShowDetailsButton() {
  const queryClient = useQueryClient()

  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: ['details'],
      queryFn: getDetailsData,
      // 프리페치는 데이터가 staleTime보다 오래된 경우에만 실행됩니다.
      // 따라서 이와 같은 경우에는 확실히 하나를 설정하고 싶습니다
      staleTime: 60000,
    })
  }

  return (
    <button onMouseEnter={prefetch} onFocus={prefetch} onClick={...}>
      Show Details
    </button>
  )
}
```
[//]: # 'ExampleEventHandler'

## 구성 요소에서 프리페치

구성 요소 수명 주기 동안 프리페칭은 일부 하위 항목이나 하위 항목에 특정 데이터 조각이 필요하다는 것을 알고 있지만 다른 query가 로드를 완료할 때까지 해당 데이터를 렌더링할 수 없을 때 유용합니다. Request Waterfall 가이드의 예를 빌려 설명하겠습니다.

[//]: # 'ExampleComponent'

```tsx
function Article({ id }) {
  const { data: articleData, isPending } = useQuery({
    queryKey: ['article', id],
    queryFn: getArticleById,
  })

  if (isPending) {
    return 'Loading article...'
  }

  return (
    <>
      <ArticleHeader articleData={articleData} />
      <ArticleBody articleData={articleData} />
      <Comments id={id} />
    </>
  )
}

function Comments({ id }) {
  const { data, isPending } = useQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
  })

  ...
}
```
[//]: # 'ExampleComponent'

그 결과 다음과 같은 요청 폭포가 생성됩니다.

```
1. |> getArticleById()
2.   |> getArticleCommentsById()
```
해당 가이드에서 언급했듯이 이 폭포수를 평탄화하고 성능을 향상시키는 한 가지 방법은 `getArticleCommentsById` query를 상위 항목으로 끌어올리고 결과를 prop으로 전달하는 것입니다. 그러나 이것이 가능하지 않거나 바람직하지 않은 경우(예: 구성 요소가 관련이 없고 구성 요소 사이에 여러 수준이 있는 경우) 어떻게 될까요?

이 경우 상위 항목에서 query를 미리 가져올 수 있습니다. 이를 수행하는 가장 간단한 방법은 query를 사용하고 결과를 무시하는 것입니다.

[//]: # 'ExampleParentComponent'

```tsx
function Article({ id }) {
  const { data: articleData, isPending } = useQuery({
    queryKey: ['article', id],
    queryFn: getArticleById,
  })

  // 프리페치
  useQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
    // 이 query가 변경될 때 다시 렌더링을 방지하기 위한 선택적 최적화:
    notifyOnChangeProps: [],
  })

  if (isPending) {
    return 'Loading article...'
  }

  return (
    <>
      <ArticleHeader articleData={articleData} />
      <ArticleBody articleData={articleData} />
      <Comments id={id} />
    </>
  )
}

function Comments({ id }) {
  const { data, isPending } = useQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
  })

  ...
}
```
[//]: # 'ExampleParentComponent'

그러면 즉시 `'article-comments'` 가져오기가 시작되고 폭포가 평평해집니다.

```
1. |> getArticleById()
1. |> getArticleCommentsById()
```
[//]: # 'Suspense'

Suspense와 함께 프리패치하려면 작업을 조금 다르게 수행해야 합니다. 프리페치로 인해 구성 요소가 렌더링되지 않도록 차단하므로 `useSuspenseQueries`를 사용하여 프리페치를 할 수 없습니다. 또한 긴장감 넘치는 query가 해결될 때까지 프리페치가 시작되지 않으므로 프리페치에 `useQuery`를 사용할 수 없습니다. 이 시나리오에서는 라이브러리에서 사용할 수 있는 [usePrefetchQuery](../reference/usePrefetchQuery.md) 또는 [usePrefetchInfiniteQuery](../reference/usePrefetchInfiniteQuery.md) 후크를 사용할 수 있습니다.

이제 실제로 데이터가 필요한 구성 요소에서 `useSuspenseQuery`를 사용할 수 있습니다. 이 나중 구성 요소를 자체 `<Suspense>` 경계에 래핑하여 프리페치 중인 "보조" query가 "기본" 데이터의 렌더링을 차단하지 않도록 할 수도 있습니다.

```tsx
function ArticleLayout({ id }) {
  usePrefetchQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
  })

  return (
    <Suspense fallback="Loading article">
      <Article id={id} />
    </Suspense>
  )
}

function Article({ id }) {
  const { data: articleData, isPending } = useSuspenseQuery({
    queryKey: ['article', id],
    queryFn: getArticleById,
  })

  ...
}
```
또 다른 방법은 query 함수 내부에서 미리 가져오는 것입니다. 기사를 가져올 때마다 댓글도 필요할 가능성이 높다는 점을 알고 있다면 이는 의미가 있습니다. 이를 위해 `queryClient.prefetchQuery`를 사용합니다.

```tsx
const queryClient = useQueryClient()
const { data: articleData, isPending } = useQuery({
  queryKey: ['article', id],
  queryFn: (...args) => {
    queryClient.prefetchQuery({
      queryKey: ['article-comments', id],
      queryFn: getArticleCommentsById,
    })

    return getArticleById(...args)
  },
})
```
효과에서 미리 가져오기도 작동하지만 동일한 구성 요소에서 `useSuspenseQuery`를 사용하는 경우 이 효과는 query가 완료될 _후_까지 실행되지 않으므로 원하는 결과가 아닐 수 있습니다.

```tsx
const queryClient = useQueryClient()

useEffect(() => {
  queryClient.prefetchQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
  })
}, [queryClient, id])
```
요약하자면, 구성 요소 수명 주기 동안 query를 프리페치하려는 경우 몇 가지 방법이 있으며 상황에 가장 적합한 방법을 선택하세요.

- `usePrefetchQuery` 또는 `usePrefetchInfiniteQuery` 후크를 사용하여 suspense 경계 이전의 프리페치
- `useQuery` 또는 `useSuspenseQueries`를 사용하고 결과를 무시하세요.
- query 함수 내부의 프리패치
- 효과의 프리페치

다음에는 좀 더 발전된 사례를 살펴보겠습니다.

[//]: # 'Suspense'

### 종속 Queries 및 코드 분할

때때로 우리는 또 다른 가져오기 결과에 따라 조건부로 미리 가져오기를 원합니다. [성능 및 요청 폭포수 가이드](request-waterfalls.md)에서 빌린 다음 예를 고려해보세요.

[//]: # 'ExampleConditionally1'

```tsx
// 이 지연 로드는 GraphFeedItem 구성 요소를 로드합니다.
// 무언가가 렌더링될 때까지 로드가 시작되지 않습니다.
const GraphFeedItem = React.lazy(() => import('./GraphFeedItem'))

function Feed() {
  const { data, isPending } = useQuery({
    queryKey: ['feed'],
    queryFn: getFeed,
  })

  if (isPending) {
    return 'Loading feed...'
  }

  return (
    <>
      {data.map((feedItem) => {
        if (feedItem.type === 'GRAPH') {
          return <GraphFeedItem key={feedItem.id} feedItem={feedItem} />
        }

        return <StandardFeedItem key={feedItem.id} feedItem={feedItem} />
      })}
    </>
  )
}

// GraphFeedItem.tsx
function GraphFeedItem({ feedItem }) {
  const { data, isPending } = useQuery({
    queryKey: ['graph', feedItem.id],
    queryFn: getGraphDataById,
  })

  ...
}
```
[//]: # 'ExampleConditionally1'

해당 가이드에서 언급했듯이 이 예에서는 다음과 같은 이중 요청 폭포가 발생합니다.

```
1. |> getFeed()
2.   |> JS for <GraphFeedItem>
3.     |> getGraphDataById()
```
`getFeed()`가 필요할 때 `getGraphDataById()` 데이터도 반환하도록 API를 재구성할 수 없는 경우 `getFeed->getGraphDataById` 폭포를 제거할 수 있는 방법은 없지만 조건부 프리페칭을 활용하면 최소한 코드와 데이터를 병렬로 로드할 수 있습니다. 위에서 설명한 것처럼 이 작업을 수행하는 방법은 여러 가지가 있지만 이 예에서는 query 함수에서 수행하겠습니다.

[//]: # 'ExampleConditionally2'

```tsx
function Feed() {
  const queryClient = useQueryClient()
  const { data, isPending } = useQuery({
    queryKey: ['feed'],
    queryFn: async (...args) => {
      const feed = await getFeed(...args)

      for (const feedItem of feed) {
        if (feedItem.type === 'GRAPH') {
          queryClient.prefetchQuery({
            queryKey: ['graph', feedItem.id],
            queryFn: getGraphDataById,
          })
        }
      }

      return feed
    }
  })

  ...
}
```
[//]: # 'ExampleConditionally2'

그러면 코드와 데이터가 병렬로 로드됩니다.

```
1. |> getFeed()
2.   |> JS for <GraphFeedItem>
2.   |> getGraphDataById()
```
그러나 이제 `getGraphDataById`용 코드가 `JS for <GraphFeedItem>` 대신 상위 번들에 포함된다는 점에서 절충점이 있으므로 사례별로 최상의 성능 절충점이 무엇인지 결정해야 합니다. `GraphFeedItem`가 발생할 가능성이 있는 경우 상위 항목에 코드를 포함하는 것이 좋습니다. 매우 드물다면 아마도 그렇지 않을 것입니다.

[//]: # 'Router'

## 라우터 통합

구성 요소 트리 자체에서 데이터를 가져오면 폭포수 요청이 쉽게 발생할 수 있고 이에 대한 다양한 수정 사항이 애플리케이션 전체에 누적되어 번거로울 수 있으므로 프리페치를 수행하는 매력적인 방법은 이를 라우터 수준에서 통합하는 것입니다.

이 접근 방식에서는 각 _route_에 대해 해당 구성 요소 트리에 필요한 데이터를 미리 명시적으로 선언합니다. 서버 렌더링은 전통적으로 렌더링이 시작되기 전에 모든 데이터를 로드해야 했기 때문에 이는 오랫동안 SSR 앱에 대한 지배적인 접근 방식이었습니다. 이는 여전히 일반적인 접근 방식이며 [서버 렌더링 및 Hydration 가이드](ssr.md)에서 이에 대한 자세한 내용을 읽을 수 있습니다.

지금은 클라이언트 측 사례에 초점을 맞추고 [TanStack Router](https://tanstack.com/router)를 사용하여 이 작업을 수행할 수 있는 방법의 예를 살펴보겠습니다. 이 예에서는 간결함을 유지하기 위해 많은 설정과 상용구를 생략했습니다. [TanStack Router]에서 [전체 React Query 예](https://tanstack.com/router/latest/docs/framework/react/examples/basic-react-query-file-based)를 확인할 수 있습니다. 문서](https://tanstack.com/router/latest/docs).

라우터 수준에서 통합할 때 모든 데이터가 나타날 때까지 해당 경로의 렌더링을 _차단_하거나, 프리페치를 시작하고 결과를 기다리지 않을 수 있습니다. 이렇게 하면 가능한 한 빨리 경로 렌더링을 시작할 수 있습니다. 이 두 가지 접근 방식을 혼합하여 일부 중요한 데이터를 기다릴 수도 있지만 모든 보조 데이터 로드가 완료되기 전에 렌더링을 시작할 수도 있습니다. 이 예에서는 기사 데이터 로드가 완료될 때까지 렌더링하지 않고 가능한 한 빨리 댓글 미리 가져오기를 시작하지만 댓글 로드가 아직 완료되지 않은 경우 경로 렌더링을 차단하지 않도록 `/article` 경로를 구성합니다.

```tsx
const queryClient = new QueryClient()
const routerContext = new RouterContext()
const rootRoute = routerContext.createRootRoute({
  component: () => { ... }
})

const articleRoute = new Route({
  getParentRoute: () => rootRoute,
  path: 'article',
  beforeLoad: () => {
    return {
      articleQueryOptions: { queryKey: ['article'], queryFn: fetchArticle },
      commentsQueryOptions: { queryKey: ['comments'], queryFn: fetchComments },
    }
  },
  loader: async ({
    context: { queryClient },
    routeContext: { articleQueryOptions, commentsQueryOptions },
  }) => {
    // 댓글을 최대한 빨리 가져오되 차단하지는 마세요.
    queryClient.prefetchQuery(commentsQueryOptions)

    // 기사를 가져올 때까지 경로를 전혀 렌더링하지 마세요.
    await queryClient.prefetchQuery(articleQueryOptions)
  },
  component: ({ useRouteContext }) => {
    const { articleQueryOptions, commentsQueryOptions } = useRouteContext()
    const articleQuery = useQuery(articleQueryOptions)
    const commentsQuery = useQuery(commentsQueryOptions)

    return (
      ...
    )
  },
  errorComponent: () => 'Oh crap!',
})
```
다른 라우터와의 통합도 가능합니다. 다른 데모는 [react-router](../examples/react-router.md)를 참조하세요.

[//]: # 'Router'

## Query 수동 프라이밍

동기식으로 사용할 수 있는 query에 대한 데이터가 이미 있는 경우 해당 데이터를 프리페치할 필요가 없습니다. [QueryClient](../../../reference/QueryClient.md#queryclientsetquerydata)을 사용하여 query의 캐시된 결과를 키별로 직접 추가하거나 업데이트할 수 있습니다.

[//]: # 'ExampleManualPriming'

```tsx
queryClient.setQueryData(['todos'], todos)
```
[//]: # 'ExampleManualPriming'
[//]: # 'Materials'

## 추가 자료

가져오기 전에 Query 캐시에 데이터를 가져오는 방법에 대한 자세한 내용은 [TkDodo로 Query 캐시 시드 문서](https://tkdodo.eu/blog/seeding-the-query-cache)를 참조하세요.

서버 측 라우터 및 프레임워크와의 통합은 방금 본 것과 매우 유사하며, 데이터가 서버에서 클라이언트로 전달되어 캐시에 저장되어야 한다는 점만 추가됩니다. 방법을 알아보려면 [서버 렌더링 및 Hydration 가이드](ssr.md)를 계속 진행하세요.

[//]: # 'Materials'
