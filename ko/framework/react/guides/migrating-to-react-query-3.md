---
id: migrating-to-react-query-3
title: React Query 3으로 마이그레이션
---




React Query의 이전 버전은 훌륭했으며 몇 가지 놀라운 새 기능, ​​더 많은 마법 및 전반적으로 더 나은 경험을 라이브러리에 제공했습니다. 그들은 또한 도서관에 대규모 채택을 가져왔고 마찬가지로 도서관에 많은 개선 작업(문제/기여)을 가져왔고 도서관을 더욱 좋게 만들기 위해 더 많은 개선이 필요한 몇 가지 사항을 밝혔습니다. v3에는 매우 세련된 내용이 포함되어 있습니다.

## 개요

- 더욱 확장 가능하고 테스트 가능한 캐시 구성
- 더 나은 SSR 지원
- 어디서나 데이터 지연(이전에는 PaginatedQuery 사용)!
- 양방향 무한 Queries
- Query 데이터 선택기!
- 사용하기 전에 queries 및/또는 mutations에 대한 기본값을 완전히 구성합니다.
- 선택적 렌더링 최적화를 위한 더욱 세분성
- 새로운 `useQueries` 후크! (가변 길이 병렬 query 실행)
- `useIsFetching()` 후크에 대한 Query 필터 지원!
- mutations에 대한 재시도/오프라인/재생 지원
- React 외부에서 queries/mutations를 관찰하세요.
- 원하는 곳 어디에서나 React Query 코어 로직을 사용해보세요!
- `react-query/devtools`를 통해 번들/같은 위치에 배치된 Devtool
- 웹 저장소에 대한 캐시 지속성(`react-query/persistQueryClient-experimental` 및 `react-query/createWebStoragePersistor-experimental`를 통해 실험)

## 주요 변경 사항

### `QueryCache`는 `QueryClient`와 하위 수준 `QueryCache` 및 `MutationCache` 인스턴스로 분할되었습니다.

`QueryCache`에는 모든 queries가 포함되어 있고, `MutationCache`에는 모든 mutations가 포함되어 있으며, `QueryClient`를 사용하여 구성을 설정하고 상호 작용할 수 있습니다.

여기에는 몇 가지 이점이 있습니다.

- 다양한 유형의 캐시를 허용합니다.
- 서로 다른 구성을 가진 여러 클라이언트가 동일한 캐시를 사용할 수 있습니다.
- 클라이언트는 SSR의 공유 캐시에 사용할 수 있는 queries를 추적하는 데 사용할 수 있습니다.
- 클라이언트 API는 일반적인 사용에 더 중점을 둡니다.
- 개별 구성 요소를 테스트하기가 더 쉽습니다.

`new QueryClient()`를 생성할 때 `QueryCache` 및 `MutationCache`를 제공하지 않으면 자동으로 생성됩니다.

```tsx
import { QueryClient } from 'react-query'

const queryClient = new QueryClient()
```
### `ReactQueryConfigProvider` 및 `ReactQueryCacheProvider`는 모두 `QueryClientProvider`로 대체되었습니다.

이제 queries 및 mutations에 대한 기본 옵션을 `QueryClient`에서 지정할 수 있습니다.

**이제 defaultConfig 대신 defaultOptions입니다**

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // query 옵션
    },
    mutations: {
      // mutation 옵션
    },
  },
})
```
이제 `QueryClientProvider` 구성요소는 `QueryClient`를 애플리케이션에 연결하는 데 사용됩니다.

```tsx
import { QueryClient, QueryClientProvider } from 'react-query'

const queryClient = new QueryClient()

function App() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}
```
### 기본 `QueryCache`가 사라졌습니다. **이번엔 진짜로!**

이전에 더 이상 사용되지 않음을 언급한 것처럼 기본 패키지에서 생성되거나 내보내지는 기본 `QueryCache`가 더 이상 없습니다. **`new QueryClient()` 또는 `new QueryCache()`를 통해 직접 만들어야 합니다(그런 다음 `new QueryClient({ queryCache })`에 전달할 수 있음)**

### 더 이상 사용되지 않는 `makeQueryCache` 유틸리티가 제거되었습니다.

꽤 오랜 시간이 걸렸는데 드디어 사라졌네요 :)

### `QueryCache.prefetchQuery()`가 `QueryClient.prefetchQuery()`로 이동되었습니다.

새로운 `QueryClient.prefetchQuery()` 함수는 비동기식이지만 **query**에서 데이터를 반환하지 않습니다. 데이터가 필요한 경우 새로운 `QueryClient.fetchQuery()` 기능을 사용하십시오.

```tsx
// query 프리패치:
await queryClient.prefetchQuery('posts', fetchPosts)

// query 가져오기:
try {
  const data = await queryClient.fetchQuery('posts', fetchPosts)
} catch (error) {
  // 오류 처리
}
```
### `ReactQueryErrorResetBoundary` 및 `QueryCache.resetErrorBoundaries()`는 `QueryErrorResetBoundary` 및 `useQueryErrorResetBoundary()`로 대체되었습니다.

두 가지 모두 이전과 동일한 경험을 제공하지만 재설정할 구성 요소 트리를 선택할 수 있는 제어 기능이 추가되었습니다. 자세한 내용은 다음을 참조하세요.

- [QueryErrorResetBoundary](../reference/QueryErrorResetBoundary.md)
- [useQueryErrorResetBoundary](../reference/useQueryErrorResetBoundary.md)

### `QueryCache.getQuery()`가 `QueryCache.find()`로 대체되었습니다.

이제 `QueryCache.find()`를 사용하여 캐시에서 개별 queries를 조회해야 합니다.

### `QueryCache.getQueries()`가 `QueryCache.findAll()`로 이동되었습니다.

이제 `QueryCache.findAll()`를 사용하여 캐시에서 여러 queries를 조회해야 합니다.

### `QueryCache.isFetching`가 `QueryClient.isFetching()`로 이동되었습니다.

**이제는 속성이 아닌 함수입니다**

### `useQueryCache` 후크가 `useQueryClient` 후크로 대체되었습니다.

구성 요소 트리에 대해 제공된 `queryClient`를 반환하며 이름 바꾸기 외에는 많은 조정이 필요하지 않습니다.

### Query 주요 부품/조각은 더 이상 query 기능에 자동으로 확산되지 않습니다.

인라인 함수는 이제 query 함수에 매개변수를 전달하는 방법으로 제안됩니다.

```tsx
// 오래된
useQuery(['post', id], (_key, id) => fetchPost(id))

// 새로운
useQuery(['post', id], () => fetchPost(id))
```
여전히 인라인 함수를 사용하지 않으려면 새로 전달된 `QueryFunctionContext`를 사용할 수 있습니다.

```tsx
useQuery(['post', id], (context) => fetchPost(context.queryKey[1]))
```
### 무한 Query 이제 페이지 매개변수가 `QueryFunctionContext.pageParam`를 통해 전달됩니다.

이전에는 query 함수의 마지막 query 주요 매개변수로 추가되었지만 일부 패턴에서는 이것이 어려운 것으로 판명되었습니다.

```tsx
// 오래된
useInfiniteQuery(['posts'], (_key, pageParam = 0) => fetchPosts(pageParam))

// 새로운
useInfiniteQuery(['posts'], ({ pageParam = 0 }) => fetchPosts(pageParam))
```
### `keepPreviousData` 옵션을 위해 usePaginatedQuery()가 제거되었습니다.

새로운 `keepPreviousData` 옵션은 `useQuery` 및 `useInfiniteQuery` 모두에 사용할 수 있으며 데이터에 동일한 "지연" 효과를 갖습니다.

```tsx
import { useQuery } from 'react-query'

function Page({ page }) {
  const { data } = useQuery(['page', page], fetchPage, {
    keepPreviousData: true,
  })
}
```
### useInfiniteQuery()는 이제 양방향입니다.

`useInfiniteQuery()` 인터페이스는 양방향 무한 목록을 완벽하게 지원하도록 변경되었습니다.

- `options.getFetchMore`가 `options.getNextPageParam`로 이름이 변경되었습니다.
- `queryResult.canFetchMore`가 `queryResult.hasNextPage`로 이름이 변경되었습니다.
- `queryResult.fetchMore`가 `queryResult.fetchNextPage`로 이름이 변경되었습니다.
- `queryResult.isFetchingMore`가 `queryResult.isFetchingNextPage`로 이름이 변경되었습니다.
- `options.getPreviousPageParam` 옵션을 추가했습니다.
- `queryResult.hasPreviousPage` 속성을 추가했습니다.
- `queryResult.fetchPreviousPage` 속성을 추가했습니다.
- `queryResult.isFetchingPreviousPage` 추가
- 무한 query의 `data`는 이제 페이지를 가져오는 데 사용되는 `pages` 및 `pageParams`를 포함하는 객체입니다: `{ pages: [data, data, data], pageParams: [...]}`

한 방향:

```tsx
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
  useInfiniteQuery(
    'projects',
    ({ pageParam = 0 }) => fetchProjects(pageParam),
    {
      getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    },
  )
```
양방향:

```tsx
const {
  data,
  fetchNextPage,
  fetchPreviousPage,
  hasNextPage,
  hasPreviousPage,
  isFetchingNextPage,
  isFetchingPreviousPage,
} = useInfiniteQuery(
  'projects',
  ({ pageParam = 0 }) => fetchProjects(pageParam),
  {
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    getPreviousPageParam: (firstPage, pages) => firstPage.prevCursor,
  },
)
```
한 방향이 반전됨:

```tsx
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
  useInfiniteQuery(
    'projects',
    ({ pageParam = 0 }) => fetchProjects(pageParam),
    {
      select: (data) => ({
        pages: [...data.pages].reverse(),
        pageParams: [...data.pageParams].reverse(),
      }),
      getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    },
  )
```
### 이제 무한 Query 데이터에는 해당 페이지를 가져오는 데 사용되는 페이지 배열과 pageParam이 포함됩니다.

이를 통해 데이터 및 페이지 매개변수를 더 쉽게 조작할 수 있습니다. 예를 들어 매개변수와 함께 데이터의 첫 번째 페이지를 제거합니다.

```tsx
queryClient.setQueryData(['projects'], (data) => ({
  pages: data.pages.slice(1),
  pageParams: data.pageParams.slice(1),
}))
```
### useMutation는 이제 배열 대신 객체를 반환합니다.

예전 방식은 `useState`를 처음 발견했을 때의 따뜻하고 흐릿한 느낌을 주었지만 오래 가지 못했습니다. 이제 mutation 반환은 단일 개체입니다.

```tsx
// 오래된:
const [mutate, { status, reset }] = useMutation()

// 새로운:
const { mutate, status, reset } = useMutation()
```
### `mutation.mutate`는 더 이상 Promise을 반환하지 않습니다.

- `[mutate]` 변수가 `mutation.mutate` 기능으로 변경되었습니다.
- `mutation.mutateAsync` 기능 추가

사용자들은 Promise가 일반적인 Promise처럼 작동할 것으로 기대했기 때문에 이 동작에 관해 많은 질문을 받았습니다.

이로 인해 `mutate` 기능은 이제 `mutate` 및 `mutateAsync` 기능으로 분할됩니다.

콜백을 사용할 때 `mutate` 함수를 사용할 수 있습니다.

```tsx
const { mutate } = useMutation({ mutationFn: addTodo })

mutate('todo', {
  onSuccess: (data) => {
    console.log(data)
  },
  onError: (error) => {
    console.error(error)
  },
  onSettled: () => {
    console.log('settled')
  },
})
```
`mutateAsync` 함수는 async/await를 사용할 때 사용할 수 있습니다.

```tsx
const { mutateAsync } = useMutation({ mutationFn: addTodo })

try {
  const data = await mutateAsync('todo')
  console.log(data)
} catch (error) {
  console.error(error)
} finally {
  console.log('settled')
}
```
### useQuery의 객체 구문은 이제 축소된 구성을 사용합니다.

```tsx
// 오래된:
useQuery({
  queryKey: 'posts',
  queryFn: fetchPosts,
  config: { staleTime: Infinity },
})

// 새로운:
useQuery({
  queryKey: 'posts',
  queryFn: fetchPosts,
  staleTime: Infinity,
})
```
### 설정된 경우 QueryOptions.enabled 옵션은 boolean(`true`/`false`)이어야 합니다.

`enabled` query 옵션은 이제 값이 `false`인 경우에만 query를 비활성화합니다.
필요한 경우 `!!userId` 또는 `Boolean(userId)`를 사용하여 값을 캐스팅할 수 있으며 boolean이 아닌 값이 전달되면 편리한 오류가 발생합니다.

### QueryOptions.initialStale 옵션이 제거되었습니다.

`initialStale` query 옵션이 제거되었으며 이제 초기 데이터는 일반 데이터로 처리됩니다.
즉, `initialData`가 제공되면 query가 기본적으로 마운트 시 다시 가져옵니다.
즉시 다시 가져오지 않으려면 `staleTime`를 정의할 수 있습니다.

### `QueryOptions.forceFetchOnMount` 옵션이 `refetchOnMount: 'always'`로 대체되었습니다.

솔직히 우리는 너무 많은 `refetchOn____` 옵션을 누적하고 있었기 때문에 문제가 해결될 것입니다.

### `QueryOptions.refetchOnMount` 옵션은 이제 모든 query 관찰자가 아닌 상위 구성요소에만 적용됩니다.

`refetchOnMount`가 `false`로 설정된 경우 추가 구성 요소가 마운트 시 다시 가져오는 것이 방지되었습니다.
버전 3에서는 옵션이 설정된 구성요소만 마운트 시 다시 가져오지 않습니다.

### 새로운 `QueryFunctionContext` 개체를 위해 `QueryOptions.queryFnParamsFilter`가 제거되었습니다.

이제 query 함수가 query 키 대신 `QueryFunctionContext` 개체를 가져오기 때문에 `queryFnParamsFilter` 옵션이 제거되었습니다.

`QueryFunctionContext`에도 query 키가 포함되어 있으므로 매개변수는 query 기능 자체 내에서 계속 필터링될 수 있습니다.

### `QueryOptions.notifyOnStatusChange` 옵션은 새로운 `notifyOnChangeProps` 및 `notifyOnChangePropsExclusions` 옵션으로 대체되었습니다.

이러한 새로운 옵션을 사용하면 구성 요소를 세부적인 수준에서 다시 렌더링해야 하는 시기를 구성할 수 있습니다.

`data` 또는 `error` 속성이 변경된 경우에만 다시 렌더링하십시오.

```tsx
import { useQuery } from 'react-query'

function User() {
  const { data } = useQuery(['user'], fetchUser, {
    notifyOnChangeProps: ['data', 'error'],
  })
  return <div>Username: {data.username}</div>
}
```
`isStale` 속성이 변경되면 다시 렌더링을 방지합니다.

```tsx
import { useQuery } from 'react-query'

function User() {
  const { data } = useQuery(['user'], fetchUser, {
    notifyOnChangePropsExclusions: ['isStale'],
  })
  return <div>Username: {data.username}</div>
}
```
### `QueryResult.clear()` 기능의 이름이 `QueryResult.remove()`로 변경되었습니다.

`clear`라고 불렸지만 실제로는 캐시에서 query만 제거했습니다. 이제 이름이 기능과 일치합니다.

### `QueryResult.updatedAt` 속성은 `QueryResult.dataUpdatedAt` 및 `QueryResult.errorUpdatedAt` 속성으로 분할되었습니다.

데이터와 오류가 동시에 존재할 수 있으므로 `updatedAt` 속성은 `dataUpdatedAt` 및 `errorUpdatedAt`로 분할되었습니다.

### `setConsole()`는 새로운 `setLogger()` 기능으로 대체되었습니다.

```tsx
import { setLogger } from 'react-query'

// Sentry로 기록
setLogger({
  error: (error) => {
    Sentry.captureException(error)
  },
})

// 윈스턴으로 로그인
setLogger(winston.createLogger())
```
### React Native에서는 더 이상 로거 재정의가 필요하지 않습니다.

query가 실패할 때 React Native에서 오류 화면이 표시되는 것을 방지하려면 콘솔을 수동으로 변경해야 했습니다.

```tsx
import { setConsole } from 'react-query'

setConsole({
  log: console.log,
  warn: console.warn,
  error: console.warn,
})
```
버전 3에서는 **React Native에서 React Query를 사용하면 자동으로 수행됩니다**.

### 타이프스크립트

#### `QueryStatus`가 [enum](https://www.typescriptlang.org/docs/handbook/enums.html#string-enums)에서 [union 유형](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types)으로 변경되었습니다.

따라서 QueryStatus 열거형 속성에 대해 query 또는 mutation의 상태 속성을 확인하는 경우 이제 각 속성에 대해 이전에 보유했던 열거형 문자열 리터럴과 비교하여 확인해야 합니다.

따라서 열거형 속성을 다음과 같이 동등한 문자열 리터럴로 변경해야 합니다.

- `QueryStatus.Idle` -> `'idle'`
- `QueryStatus.Loading` -> `'loading'`
- `QueryStatus.Error` -> `'error'`
- `QueryStatus.Success` -> `'success'`

다음은 변경해야 할 사항의 예입니다.

```tsx
- import { useQuery, QueryStatus } from 'react-query'; // [!코드-]
+ import { useQuery } from 'react-query'; // [!코드 ++]

const { data, status } = useQuery(['post', id], () => fetchPost(id))

- if (status === QueryStatus.Loading) { // [!코드-]
+ if (status === 'loading') { // [!코드 ++]
  ...
}

- if (status === QueryStatus.Error) { // [!코드-]
+ if (status === 'error') { // [!코드 ++]
  ...
}
```
## 새로운 기능

#### Query 데이터 선택기

`useQuery` 및 `useInfiniteQuery` 후크에는 이제 query 결과의 일부를 선택하거나 변환하는 `select` 옵션이 있습니다.

```tsx
import { useQuery } from 'react-query'

function User() {
  const { data } = useQuery(['user'], fetchUser, {
    select: (user) => user.username,
  })
  return <div>Username: {data}</div>
}
```
선택한 데이터가 변경될 때만 다시 렌더링하려면 `notifyOnChangeProps` 옵션을 `['data', 'error']`로 설정하세요.

#### 가변 길이 병렬 query 실행을 위한 useQueries() 후크

루프에서 `useQuery`를 실행할 수 있기를 원하십니까? 후크의 규칙은 그렇지 않다고 말하지만, 새로운 `useQueries()` 후크를 사용하면 가능합니다!

```tsx
import { useQueries } from 'react-query'

function Overview() {
  const results = useQueries([
    { queryKey: ['post', 1], queryFn: fetchPost },
    { queryKey: ['post', 2], queryFn: fetchPost },
  ])
  return (
    <ul>
      {results.map(({ data }) => data && <li key={data.id}>{data.title})</li>)}
    </ul>
  )
}
```
#### 재시도/오프라인 mutations

기본적으로 React Query는 오류 발생 시 mutation를 재시도하지 않지만 `retry` 옵션을 사용하면 가능합니다.

```tsx
const mutation = useMutation({
  mutationFn: addTodo,
  retry: 3,
})
```
장치가 오프라인이어서 mutations가 실패하는 경우 장치가 다시 연결될 때 동일한 순서로 재시도됩니다.

#### 지속 mutations

이제 Mutations를 스토리지에 유지하고 나중에 다시 시작할 수 있습니다. 자세한 내용은 mutations 설명서에서 확인할 수 있습니다.

#### QueryObserver

`QueryObserver`를 사용하여 query를 생성 및/또는 시청할 수 있습니다.

```tsx
const observer = new QueryObserver(queryClient, { queryKey: 'posts' })

const unsubscribe = observer.subscribe((result) => {
  console.log(result)
  unsubscribe()
})
```
#### InfiniteQueryObserver

`InfiniteQueryObserver`를 사용하여 무한 query를 생성 및/또는 시청할 수 있습니다.

```tsx
const observer = new InfiniteQueryObserver(queryClient, {
  queryKey: 'posts',
  queryFn: fetchPosts,
  getNextPageParam: (lastPage, allPages) => lastPage.nextCursor,
  getPreviousPageParam: (firstPage, allPages) => firstPage.prevCursor,
})

const unsubscribe = observer.subscribe((result) => {
  console.log(result)
  unsubscribe()
})
```
#### QueriesObserver

`QueriesObserver`를 사용하여 여러 queries를 생성 및/또는 시청할 수 있습니다.

```tsx
const observer = new QueriesObserver(queryClient, [
  { queryKey: ['post', 1], queryFn: fetchPost },
  { queryKey: ['post', 2], queryFn: fetchPost },
])

const unsubscribe = observer.subscribe((result) => {
  console.log(result)
  unsubscribe()
})
```
#### 특정 queries에 대한 기본 옵션 설정

`QueryClient.setQueryDefaults()` 방법을 사용하여 특정 queries에 대한 기본 옵션을 설정할 수 있습니다.

```tsx
queryClient.setQueryDefaults(['posts'], { queryFn: fetchPosts })

function Component() {
  const { data } = useQuery(['posts'])
}
```
#### 특정 mutations에 대한 기본 옵션 설정

`QueryClient.setMutationDefaults()` 방법을 사용하여 특정 mutations에 대한 기본 옵션을 설정할 수 있습니다.

```tsx
queryClient.setMutationDefaults(['addPost'], { mutationFn: addPost })

function Component() {
  const { mutate } = useMutation({ mutationKey: ['addPost'] })
}
```
#### useIsFetching()

이제 `useIsFetching()` 후크는 예를 들어 특정 유형의 queries에 대한 스피너만 표시하는 데 사용할 수 있는 필터를 허용합니다.

```tsx
const fetches = useIsFetching({ queryKey: ['posts'] })
```
#### 코어 분리

React Query의 핵심은 이제 React와 완전히 분리되어 독립형 또는 다른 프레임워크에서도 사용할 수 있습니다. 핵심 기능만 가져오려면 `react-query/core` 진입점을 사용하세요.

```tsx
import { QueryClient } from 'react-query/core'
```
### Devtools는 이제 기본 저장소 및 npm 패키지의 일부입니다.

이제 devtools는 `react-query/devtools` 가져오기 아래의 `react-query` 패키지 자체에 포함되어 있습니다. `react-query-devtools` 가져오기를 `react-query/devtools`로 간단히 교체하세요.