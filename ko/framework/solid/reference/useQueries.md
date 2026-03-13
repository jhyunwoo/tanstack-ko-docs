---
id: useQueries
title: useQueries
---




`useQueries` 후크를 사용하여 queries의 변수 번호를 가져올 수 있습니다.

```tsx
const ids = [1, 2, 3]
const results = useQueries(() => {
  queries: ids.map((id) => ({
    queryKey: ['post', id],
    queryFn: () => fetchPost(id),
    staleTime: Infinity,
  })),
})
```
**옵션**

`useQueries` 후크는 값이 [useQuery](../../react/reference/useQuery.md)와 동일한 query 옵션 개체가 있는 배열인 **queries** 키가 있는 옵션 개체를 허용합니다(`queryClient` 옵션 제외 - 왜냐하면 `QueryClient`는 최상위 수준에서 전달될 수 있습니다.

- `queryClient?: QueryClient`
  - 이를 사용하여 사용자 정의 QueryClient를 제공합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.
- `combine?: (result: UseQueriesResults) => TCombinedResult`
  - queries의 결과를 단일 값으로 결합하려면 이를 사용합니다.

> query 개체 배열에 동일한 query 키가 두 번 이상 있으면 queries 간에 일부 데이터가 공유될 수 있습니다. 이를 방지하려면 queries의 중복을 제거하고 결과를 원하는 구조에 다시 매핑하는 것이 좋습니다.

**placeholderData**

`placeholderData` 옵션은 `useQueries`에도 존재하지만 `useQuery`처럼 이전에 렌더링된 Queries에서 전달된 정보를 얻지 못합니다. 왜냐하면 `useQueries`에 대한 입력은 각 렌더링에서 Queries의 다른 수일 수 있기 때문입니다.

**보고**

`useQueries` 후크는 모든 query 결과가 포함된 배열을 반환합니다. 반환된 순서는 입력 순서와 동일합니다.

## 결합하다

결과의 `data`(또는 기타 Query 정보)를 단일 값으로 결합하려는 경우 `combine` 옵션을 사용할 수 있습니다. 결과는 가능한 한 참조적으로 안정적이도록 구조적으로 공유됩니다.

```tsx
const ids = [1, 2, 3]
const combinedQueries = useQueries(() => {
  queries: ids.map((id) => ({
    queryKey: ['post', id],
    queryFn: () => fetchPost(id),
  })),
  combine: (results) => {
    return {
      data: results.map((result) => result.data),
      pending: results.some((result) => result.isPending),
    }
  },
})
```
위의 예에서 `combinedQueries`는 `data` 및 `pending` 속성을 가진 개체가 됩니다. Query 결과의 다른 모든 속성은 손실됩니다.

### 메모

`combine` 기능은 다음과 같은 경우에만 다시 실행됩니다.

- `combine` 함수 자체가 참조적으로 변경되었습니다.
- query 결과 중 하나라도 변경되었습니다.

이는 위에 표시된 대로 인라인된 `combine` 함수가 모든 렌더링에서 실행된다는 것을 의미합니다. 이를 방지하려면 `useCallback`에서 `combine` 함수를 래핑하거나 종속성이 없는 경우 안정적인 함수 참조로 추출할 수 있습니다.