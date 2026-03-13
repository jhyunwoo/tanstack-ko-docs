---
id: query-functions
title: Query 기능
---




query 함수는 문자 그대로 **프라미스를 반환하는** 모든 함수일 수 있습니다. 반환되는 Promise는 **데이터를 해결**하거나 **오류를 발생**해야 합니다.

다음은 모두 유효한 query 기능 구성입니다.



```tsx
useQuery({ queryKey: ['todos'], queryFn: fetchAllTodos })
useQuery({ queryKey: ['todos', todoId], queryFn: () => fetchTodoById(todoId) })
useQuery({
  queryKey: ['todos', todoId],
  queryFn: async () => {
    const data = await fetchTodoById(todoId)
    return data
  },
})
useQuery({
  queryKey: ['todos', todoId],
  queryFn: ({ queryKey }) => fetchTodoById(queryKey[1]),
})
```



## 오류 처리 및 발생

TanStack Query가 query에 오류가 발생했는지 확인하려면 query 함수가 **거부된 Promise**을 발생시키거나 반환해야 합니다. query 함수에서 발생하는 모든 오류는 query의 `error` 상태에서 지속됩니다.



```tsx
const { error } = useQuery({
  queryKey: ['todos', todoId],
  queryFn: async () => {
    if (somethingGoesWrong) {
      throw new Error('Oh no!')
    }
    if (somethingElseGoesWrong) {
      return Promise.reject(new Error('Oh no!'))
    }

    return data
  },
})
```



## 기본적으로 throw되지 않는 `fetch` 및 기타 클라이언트와의 사용법

`axios` 또는 `graphql-request`와 같은 대부분의 유틸리티는 실패한 HTTP 호출에 대해 자동으로 오류를 발생시키지만 `fetch`와 같은 일부 유틸리티는 기본적으로 오류를 발생시키지 않습니다. 그렇다면 스스로 던져야합니다. 인기 있는 `fetch` API를 사용하여 이를 수행하는 간단한 방법은 다음과 같습니다.



```tsx
useQuery({
  queryKey: ['todos', todoId],
  queryFn: async () => {
    const response = await fetch('/todos/' + todoId)
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    return response.json()
  },
})
```



## Query 함수 변수

Query 키는 가져오는 데이터를 고유하게 식별하는 데 사용될 뿐만 아니라 QueryFunctionContext의 일부로 query 함수에 편리하게 전달됩니다. 항상 필요한 것은 아니지만 필요한 경우 query 함수를 추출할 수 있습니다.



```js
const result = useQuery({
  queryKey: ['todos', { status, page }],
  queryFn: fetchTodoList,
})

// query 함수에서 키, 상태 및 페이지 변수에 액세스하세요!
function fetchTodoList({ queryKey }) {
  const [_key, { status, page }] = queryKey
  return new Promise()
}
```



### QueryFunctionContext

`QueryFunctionContext`는 각 query 함수에 전달되는 개체입니다. 그것은 다음으로 구성됩니다:

- `queryKey: QueryKey`: [Query 키](../../react/guides/query-keys.md)
- `client: QueryClient`: [QueryClient](../../../reference/QueryClient.md)
- `signal?: AbortSignal`
  - TanStack Query에서 제공하는 [AbortSignal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) 인스턴스
  - [Query 취소](../../react/guides/query-cancellation.md)에 사용할 수 있습니다.
- `meta: Record<string, unknown> | undefined`
  - query에 대한 추가 정보를 입력할 수 있는 선택 필드입니다.

또한 [Infinite Queries](../../react/guides/infinite-queries.md)에는 다음 옵션이 전달됩니다.

- `pageParam: TPageParam`
  - 현재 페이지를 가져오는 데 사용되는 페이지 매개변수
- `direction: 'forward' | 'backward'`
  - **지원 중단됨**
  - 현재 페이지를 가져오는 방향
  - 현재 페이지 가져오기 방향에 액세스하려면 `getNextPageParam` 및 `getPreviousPageParam`에서 `pageParam`에 방향을 추가하세요.