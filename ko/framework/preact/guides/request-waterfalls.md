---
id: request-waterfalls
title: 성능 및 요청 폭포
---




애플리케이션 성능은 광범위하고 복잡한 영역이며 Preact Query는 API 속도를 높일 수 없지만 최고의 성능을 보장하기 위해 Preact Query를 사용하는 방법에 유의해야 할 사항이 여전히 있습니다.

Preact Query 또는 실제로 구성 요소 내부에서 데이터를 가져올 수 있는 데이터 가져오기 라이브러리를 사용할 때 가장 큰 성능 기반은 요청 폭포입니다. 이 페이지의 나머지 부분에서는 이러한 현상이 무엇인지, 이를 발견하는 방법, 이를 방지하기 위해 애플리케이션이나 API를 재구성하는 방법에 대해 설명합니다.

[프리페칭 및 라우터 통합 가이드](../../react/guides/prefetching.md)는 이를 기반으로 하며 애플리케이션이나 API를 재구성하는 것이 불가능하거나 가능하지 않을 때 미리 데이터를 프리페치하는 방법을 알려줍니다.

[서버 렌더링 및 Hydration 가이드](../../react/guides/ssr.md)에서는 서버에서 데이터를 미리 가져오고 해당 데이터를 클라이언트에 전달하여 다시 가져올 필요가 없도록 하는 방법을 알려줍니다.



[고급 서버 렌더링 가이드](../../react/guides/advanced-ssr.md)에서는 이러한 패턴을 서버 구성 요소 및 스트리밍 서버 렌더링에 적용하는 방법을 자세히 설명합니다.



## 요청 폭포수란 무엇인가요?

요청 폭포는 리소스(코드, CSS, 이미지, 데이터)에 대한 요청이 리소스에 대한 다른 요청이 완료될 _후_까지 시작되지 않을 때 발생합니다.

웹페이지를 생각해 보세요. CSS, JS 등과 같은 항목을 로드하려면 먼저 브라우저에서 마크업을 로드해야 합니다. 이것은 요청 폭포입니다.

```
1. |-> Markup
2.   |-> CSS
2.   |-> JS
2.   |-> Image
```
JS 파일 내에서 CSS를 가져오면 이제 이중 폭포가 생성됩니다.

```
1. |-> Markup
2.   |-> JS
3.     |-> CSS
```
해당 CSS가 배경 이미지를 사용하는 경우 이는 삼중 폭포입니다.

```
1. |-> Markup
2.   |-> JS
3.     |-> CSS
4.       |-> Image
```
요청 폭포수를 찾아 분석하는 가장 좋은 방법은 일반적으로 브라우저 개발자 도구의 "네트워크" 탭을 여는 것입니다.

각 폭포는 리소스가 로컬로 캐시되지 않는 한 서버에 대한 최소 한 번의 왕복을 나타냅니다. 실제로 이러한 폭포 중 일부는 브라우저가 앞뒤로 연결을 설정해야 하기 때문에 두 번 이상의 왕복을 나타낼 수 있지만 여기서는 이를 무시하겠습니다. 이로 인해 요청 폭포의 부정적인 영향은 사용자 대기 시간에 크게 좌우됩니다. 실제로 4번의 서버 왕복을 나타내는 삼중 폭포의 예를 생각해 보세요. 3g 네트워크나 나쁜 네트워크 조건에서는 일반적이지 않은 250ms의 대기 시간을 사용하면 총 4\*250=1000ms **만 계산된 대기 시간**이 됩니다. 왕복 2번만 사용하여 첫 번째 예제로 이를 평면화할 수 있다면 대신 500ms를 얻게 되며 배경 이미지를 로드하는 데 걸리는 시간이 절반이 됩니다!

## 폭포 요청 및 Preact Query

이제 Preact Query를 고려해 보겠습니다. 먼저 서버 렌더링이 없는 경우에 중점을 둘 것입니다. query 만들기를 시작하기 전에 JS를 로드해야 하므로 해당 데이터를 화면에 표시하기 전에 이중 폭포가 있습니다.

```
1. |-> Markup
2.   |-> JS
3.     |-> Query
```
이를 토대로 Preact Query에서 요청 폭포수로 이어질 수 있는 몇 가지 다른 패턴과 이를 방지하는 방법을 살펴보겠습니다.

- 단일 구성요소 폭포/직렬 Queries
- 중첩된 구성요소 폭포
- 코드 분할

### 단일 구성 요소 폭포/직렬 Queries

단일 구성 요소가 먼저 하나의 query를 가져온 다음 다른 구성 요소를 가져오는 경우 이는 요청 폭포입니다. 이는 두 번째 query가 [종속 Query](../../react/guides/dependent-queries.md)일 때 발생할 수 있습니다. 즉, 가져올 때 첫 번째 query의 데이터에 따라 다릅니다.



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



항상 가능하지는 않지만 최적의 성능을 위해서는 단일 query에서 이 두 가지를 모두 가져올 수 있도록 API를 재구성하는 것이 좋습니다. 위의 예에서 `getProjectsByUser`를 사용할 수 있도록 먼저 `getUserByEmail`를 가져오는 대신 새 `getProjectsByUserEmail` query를 도입하면 폭포가 평탄해집니다.



> API를 재구성하지 않고 종속 queries를 완화하는 또 다른 방법은 워터폴을 지연 시간이 더 낮은 서버로 이동하는 것입니다. 이는 [고급 서버 렌더링 가이드](../../react/guides/advanced-ssr.md)에서 다루는 서버 구성 요소 뒤에 있는 아이디어입니다.




직렬 queries의 또 다른 예는 Suspense와 함께 Preact Query를 사용하는 경우입니다.

```tsx
function App () {
  // 다음 queries는 직렬로 실행되어 서버에 대한 별도의 왕복을 유발합니다.
  const usersQuery = useSuspenseQuery({ queryKey: ['users'], queryFn: fetchUsers })
  const teamsQuery = useSuspenseQuery({ queryKey: ['teams'], queryFn: fetchTeams })
  const projectsQuery = useSuspenseQuery({ queryKey: ['projects'], queryFn: fetchProjects })

  // 위의 queries는 렌더링을 일시 중지하므로 데이터가 없습니다.
  // 모든 queries가 완료될 때까지 렌더링됩니다.
  ...
}
```
일반 `useQuery`를 사용하면 이러한 작업이 병렬로 발생합니다.

운 좋게도 구성 요소에 긴장감 넘치는 queries가 여러 개 있을 때 항상 후크 `useSuspenseQueries`를 사용하면 이 문제를 쉽게 해결할 수 있습니다.

```tsx
const [usersQuery, teamsQuery, projectsQuery] = useSuspenseQueries({
  queries: [
    { queryKey: ['users'], queryFn: fetchUsers },
    { queryKey: ['teams'], queryFn: fetchTeams },
    { queryKey: ['projects'], queryFn: fetchProjects },
  ],
})
```



### 중첩된 구성요소 폭포



중첩 구성 요소 폭포는 상위 구성 요소와 하위 구성 요소 모두에 queries가 포함되어 있고 상위 구성 요소가 query가 완료될 때까지 하위 구성 요소를 렌더링하지 않는 경우입니다. 이는 `useQuery` 및 `useSuspenseQuery` 모두에서 발생할 수 있습니다.



자식이 부모의 데이터를 기반으로 조건부로 렌더링하거나 자식이 query를 만들기 위해 부모로부터 prop으로 전달되는 결과의 일부에 의존하는 경우 _의존적_ 중첩 구성 요소 폭포가 있습니다.

먼저 자식이 부모에게 의존하지 **않는** 예를 살펴보겠습니다.



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



`<Comments>`는 상위 항목에서 `id` 소품을 가져오지만 해당 ID는 `<Article>`가 렌더링될 때 이미 사용 가능하므로 기사와 동시에 댓글을 가져올 수 없는 이유가 없습니다. 실제 응용 프로그램에서 하위 항목은 상위 항목보다 훨씬 아래에 중첩될 수 있으며 이러한 종류의 폭포수는 발견하고 수정하기가 더 까다로울 수 있습니다. 그러나 이 예에서는 폭포수를 평탄화하는 한 가지 방법은 대신 query 주석을 상위 항목으로 끌어올리는 것입니다.



```tsx
function Article({ id }) {
  const { data: articleData, isPending: articlePending } = useQuery({
    queryKey: ['article', id],
    queryFn: getArticleById,
  })

  const { data: commentsData, isPending: commentsPending } = useQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
  })

  if (articlePending) {
    return 'Loading article...'
  }

  return (
    <>
      <ArticleHeader articleData={articleData} />
      <ArticleBody articleData={articleData} />
      {commentsPending ? (
        'Loading comments...'
      ) : (
        <Comments commentsData={commentsData} />
      )}
    </>
  )
}
```




이제 두 개의 queries가 병렬로 가져옵니다. suspense를 사용하는 경우 대신 이 두 개의 queries를 단일 `useSuspenseQueries`로 결합하는 것이 좋습니다.



이 폭포수를 평면화하는 또 다른 방법은 `<Article>` 구성 요소의 주석을 프리페치하거나 페이지 로드 또는 페이지 탐색 시 라우터 수준에서 이러한 queries를 모두 프리페치하는 것입니다. 이에 대한 자세한 내용은 [프리페칭 및 라우터 통합 가이드](../../react/guides/prefetching.md)를 참조하세요.

다음으로 _종속 중첩 구성 요소 폭포_를 살펴보겠습니다.



```tsx
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

function GraphFeedItem({ feedItem }) {
  const { data, isPending } = useQuery({
    queryKey: ['graph', feedItem.id],
    queryFn: getGraphDataById,
  })

  ...
}
```



두 번째 query `getGraphDataById`는 두 가지 방식으로 상위 항목에 종속됩니다. 우선, `feedItem`가 그래프가 아니면 절대 발생하지 않으며, 둘째, 상위로부터 `id`가 필요합니다.

```
1. |> getFeed()
2.   |> getGraphDataById()
```



이 예에서는 query를 상위 항목으로 끌어올리거나 프리페칭을 추가하는 것만으로는 폭포를 간단하게 평탄화할 수 없습니다. 이 가이드의 시작 부분에 있는 종속 query 예제와 마찬가지로 한 가지 옵션은 `getFeed` query에 그래프 데이터를 포함하도록 API를 리팩터링하는 것입니다. 또 다른 고급 솔루션은 서버 구성 요소를 활용하여 지연 시간이 더 낮은 서버로 워터폴을 이동하는 것입니다([고급 서버 렌더링 가이드](../../react/guides/advanced-ssr.md)에서 이에 대한 자세한 내용을 읽어보세요). 그러나 이는 매우 큰 아키텍처 변경이 될 수 있습니다.



여기저기에 몇 개의 query 워터폴이 있어도 좋은 성능을 얻을 수 있습니다. 이는 일반적인 성능 문제라는 점을 알고 주의하세요. 특히 교활한 버전은 코드 분할이 관련된 경우입니다. 다음에서 이에 대해 살펴보겠습니다.

### 코드 분할

애플리케이션 JS 코드를 더 작은 청크로 분할하고 필요한 부분만 로드하는 것은 일반적으로 좋은 성능을 달성하는 데 중요한 단계입니다. 그러나 종종 요청 폭포가 발생한다는 점에서 단점이 있습니다. 해당 코드 분할 코드 내부에 query도 있으면 이 문제는 더욱 악화됩니다.

이것을 피드 예제의 약간 수정된 버전이라고 생각하세요.



```tsx
import { lazy } from 'preact/iso'
// 이 지연 로드는 GraphFeedItem 구성 요소를 로드합니다.
// 무언가가 렌더링될 때까지 로드가 시작되지 않습니다.
const GraphFeedItem = lazy(() => import('./GraphFeedItem'))

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



이 예에는 다음과 같은 이중 폭포가 있습니다.

```
1. |> getFeed()
2.   |> JS for <GraphFeedItem>
3.     |> getGraphDataById()
```
하지만 이는 예제의 코드만 보는 것입니다. 이 페이지의 첫 번째 페이지 로드가 어떻게 보이는지 고려하면 실제로 그래프를 렌더링하기 전에 서버로 5번의 왕복을 완료해야 합니다!

```
1. |> Markup
2.   |> JS for <Feed>
3.     |> getFeed()
4.       |> JS for <GraphFeedItem>
5.         |> getGraphDataById()
```
이는 서버 렌더링 시 약간 다르게 보이므로 [서버 렌더링 및 Hydration 가이드](../../react/guides/ssr.md)에서 자세히 살펴보겠습니다. 또한 `<Feed>`가 포함된 경로가 코드 분할되어 또 다른 홉이 추가되는 경우도 드물지 않습니다.

코드 분할의 경우 실제로 `getGraphDataById` query를 `<Feed>` 구성 요소로 끌어올려 조건부로 만들거나 조건부 프리페치를 추가하는 것이 도움이 될 수 있습니다. 그런 다음 query를 코드와 병렬로 가져와 예제 부분을 다음과 같이 바꿀 수 있습니다.

```
1. |> getFeed()
2.   |> getGraphDataById()
2.   |> JS for <GraphFeedItem>
```
그러나 이것은 매우 절충안입니다. 이제 `<Feed>`와 동일한 번들에 `getGraphDataById`에 대한 데이터 가져오기 코드가 포함되어 있으므로 귀하의 사례에 가장 적합한 것이 무엇인지 평가하십시오. [프리페칭 및 라우터 통합 가이드](../../react/guides/prefetching.md)에서 이 작업을 수행하는 방법에 대해 자세히 알아보세요.



> 다음 사이의 절충안:
>
> - 거의 사용하지 않더라도 모든 데이터 가져오기 코드를 기본 번들에 포함합니다.
> - 코드 분할 번들에 데이터 가져오기 코드를 넣습니다. 단, 요청 폭포수를 사용합니다.
>
>는 훌륭하지 않으며 서버 구성 요소에 대한 동기 중 하나였습니다. 서버 구성 요소를 사용하면 두 가지를 모두 피할 수 있습니다. [고급 서버 렌더링 가이드](../../react/guides/advanced-ssr.md)에서 이것이 Preact Query에 어떻게 적용되는지 자세히 알아보세요.



## 요약 및 시사점

요청 폭포수는 많은 절충안이 있는 매우 일반적이고 복잡한 성능 문제입니다. 실수로 애플리케이션에 이를 도입하는 방법에는 여러 가지가 있습니다.

- 부모에게 이미 query가 있다는 사실을 깨닫지 못한 채 자식에게 query를 추가하는 경우
- 하위에 이미 query가 있음을 깨닫지 못한 채 상위에 query를 추가하는 경우
- query가 있는 하위 항목이 있는 구성 요소를 query가 있는 상위 항목이 있는 새 상위 항목으로 이동
- 등등..

이러한 우발적인 복잡성으로 인해 폭포수를 염두에 두고 이를 찾는 애플리케이션을 정기적으로 검사하는 것이 좋습니다(가끔 네트워크 탭을 검사하는 것이 좋은 방법입니다!). 좋은 성능을 얻기 위해 반드시 그것들을 모두 평면화할 필요는 없지만 영향력이 큰 항목을 주의 깊게 살펴보세요.

다음 가이드에서는 [프리페칭 및 라우터 통합](../../react/guides/prefetching.md)을 활용하여 워터폴을 평면화하는 더 많은 방법을 살펴보겠습니다.