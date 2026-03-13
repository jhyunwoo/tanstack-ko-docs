---
id: placeholder-query-data
title: 자리 표시자 Query 데이터
---




## 자리표시자 데이터란 무엇인가요?

자리 표시자 데이터를 사용하면 query가 `initialData` 옵션과 유사하게 이미 데이터가 있는 것처럼 동작할 수 있지만 **데이터가 캐시에 유지되지 않습니다**. 이는 실제 데이터를 백그라운드에서 가져오는 동안 query를 성공적으로 렌더링하기에 충분한 부분(또는 가짜) 데이터가 있는 상황에 유용합니다.

> 예: 개별 블로그 게시물 query는 제목과 게시물 본문의 작은 조각만 포함하는 블로그 게시물의 상위 목록에서 "미리 보기" 데이터를 가져올 수 있습니다. 이 부분 데이터를 개별 query의 query 결과에 유지하고 싶지는 않지만 실제 query가 전체 개체 가져오기를 완료하는 동안 콘텐츠 레이아웃을 최대한 빨리 표시하는 데 유용합니다.

query에 대한 자리 표시자 데이터가 필요하기 전에 캐시에 제공하는 몇 가지 방법이 있습니다.

- 선언적으로:
  - query에 `placeholderData`를 제공하여 비어 있는 경우 캐시를 미리 채웁니다.
- 반드시:
  - [`queryClient` 및 `placeholderData` 옵션을 사용하여 데이터 프리페치 또는 페치](prefetching.md)

`placeholderData`를 사용하면 Query는 `pending` 상태가 아닙니다. 표시할 `data`가 있기 때문에 `success` 상태로 시작됩니다. 해당 데이터가 단지 "자리 표시자" 데이터인 경우에도 마찬가지입니다. "실제" 데이터와 구별하기 위해 Query 결과에서 `isPlaceholderData` 플래그를 `true`로 설정합니다.

## 값으로서의 자리 표시자 데이터

[//]: # 'ExampleValue'

```tsx
function Todos() {
  const result = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/todos'),
    placeholderData: placeholderTodos,
  })
}
```
[//]: # 'ExampleValue'
[//]: # 'Memoization'

### 자리 표시자 데이터 메모

query의 자리 표시자 데이터에 액세스하는 프로세스가 집중적이거나 모든 렌더링에서 수행하고 싶은 작업이 아닌 경우 값을 메모할 수 있습니다.

```tsx
function Todos() {
  const placeholderData = useMemo(() => generateFakeTodos(), [])
  const result = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/todos'),
    placeholderData,
  })
}
```
[//]: # 'Memoization'

## 함수로서의 자리 표시자 데이터

`placeholderData`는 "이전" 성공한 Query의 데이터 및 Query 메타 정보에 액세스할 수 있는 함수일 수도 있습니다. 이는 한 query의 데이터를 다른 query의 자리 표시자 데이터로 사용하려는 상황에 유용합니다. QueryKey가 변경되는 경우. `['todos', 1]`에서 `['todos', 2]`까지, 데이터가 하나의 Query에서 다음 Query로 _전환_되는 동안 로딩 스피너를 표시할 필요 없이 "이전" 데이터를 계속 표시할 수 있습니다. 자세한 내용은 [페이지 매김 Queries](paginated-queries.md)를 참조하세요.

[//]: # 'ExampleFunction'

```tsx
const result = useQuery({
  queryKey: ['todos', id],
  queryFn: () => fetch(`/todos/${id}`),
  placeholderData: (previousData, previousQuery) => previousData,
})
```
[//]: # 'ExampleFunction'

### 캐시의 자리 표시자 데이터

어떤 상황에서는 캐시된 다른 결과에서 query에 대한 자리 표시자 데이터를 제공할 수 있습니다. 이에 대한 좋은 예는 블로그 게시물 목록 query에서 캐시된 데이터를 검색하여 게시물의 미리 보기 버전을 검색한 다음 이를 개별 게시물 query의 자리 표시자 데이터로 사용하는 것입니다.

[//]: # 'ExampleCache'

```tsx
function BlogPost({ blogPostId }) {
  const queryClient = useQueryClient()
  const result = useQuery({
    queryKey: ['blogPost', blogPostId],
    queryFn: () => fetch(`/blogPosts/${blogPostId}`),
    placeholderData: () => {
      // 'blogPosts'에서 blogPost의 더 작은/미리보기 버전을 사용하세요.
      // 이 블로그의 자리 표시자 데이터인 queryPost query
      return queryClient
        .getQueryData(['blogPosts'])
        ?.find((d) => d.id === blogPostId)
    },
  })
}
```
[//]: # 'ExampleCache'
[//]: # 'Materials'

## 추가 자료

`Placeholder Data`와 `Initial Data`의 비교는 [TkDodo 글](https://tkdodo.eu/blog/placeholder-and-initial-data-in-react-query)을 참조하세요.

[//]: # 'Materials'
