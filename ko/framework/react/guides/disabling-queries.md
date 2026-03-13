---
id: disabling-queries
title: Queries 비활성화/일시 중지
---




query가 자동으로 실행되는 것을 비활성화하려면 `enabled = false` 옵션을 사용할 수 있습니다. 활성화된 옵션은 boolean을 반환하는 콜백도 허용합니다.

`enabled`가 `false`인 경우:

- query에 캐시된 데이터가 있는 경우 query는 `status === 'success'` 또는 `isSuccess` 상태에서 초기화됩니다.
- query에 캐시된 데이터가 없는 경우 query는 `status === 'pending'` 및 `fetchStatus === 'idle'` 상태에서 시작됩니다.
- query는 마운트 시 자동으로 가져오지 않습니다.
- query는 백그라운드에서 자동으로 다시 가져오지 않습니다.
- query는 일반적으로 query 다시 가져오기를 발생시키는 query 클라이언트 `invalidateQueries` 및 `refetchQueries` 호출을 무시합니다.
- `useQuery`에서 반환된 `refetch`를 사용하여 query를 수동으로 트리거하여 가져올 수 있습니다. 그러나 `skipToken`에서는 작동하지 않습니다.

> TypeScript 사용자는 `enabled = false` 대신 [skipToken](#typesafe-disabling-of-queries-using-skiptoken)을 사용하는 것을 선호할 수 있습니다.

[//]: # 'Example'

```tsx
function Todos() {
  const { isLoading, isError, data, error, refetch, isFetching } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodoList,
    enabled: false,
  })

  return (
    <div>
      <button onClick={() => refetch()}>Fetch Todos</button>

      {data ? (
        <ul>
          {data.map((todo) => (
            <li key={todo.id}>{todo.title}</li>
          ))}
        </ul>
      ) : isError ? (
        <span>Error: {error.message}</span>
      ) : isLoading ? (
        <span>Loading...</span>
      ) : (
        <span>Not ready ...</span>
      )}

      <div>{isFetching ? 'Fetching...' : null}</div>
    </div>
  )
}
```
[//]: # 'Example'

query를 영구적으로 비활성화하면 TanStack Query가 제공해야 하는 많은 훌륭한 기능(예: 백그라운드 다시 가져오기)이 선택 해제되며 이는 또한 관용적인 방법도 아닙니다. 선언적 접근 방식(query가 실행되어야 할 때 종속성 정의)에서 명령형 모드(여기를 클릭할 때마다 가져오기)로 이동합니다. `refetch`에 매개변수를 전달하는 것도 불가능합니다. 종종 원하는 것은 초기 가져오기를 연기하는 게으른 query입니다.

## 게으른 Queries

활성화된 옵션은 query를 영구적으로 비활성화하는 데 사용할 수 있을 뿐만 아니라 나중에 활성화/비활성화하는 데도 사용할 수 있습니다. 좋은 예는 사용자가 필터 값을 입력한 후에 첫 번째 요청만 시작하려는 필터 양식입니다.

[//]: # 'Example2'

```tsx
function Todos() {
  const [filter, setFilter] = React.useState('')

  const { data } = useQuery({
    queryKey: ['todos', filter],
    queryFn: () => fetchTodos(filter),
    // ⬇️ 필터가 비어 있는 한 비활성화됩니다.
    enabled: !!filter,
  })

  return (
    <div>
      // 🚀 필터를 적용하면 query가 활성화되고 실행됩니다.
      <FiltersForm onApply={setFilter} />
      {data && <TodosTable data={data} />}
    </div>
  )
}
```
[//]: # 'Example2'

### isLoading(이전: `isInitialLoading`)

Lazy queries는 처음부터 바로 `status: 'pending'`에 있을 것입니다. 왜냐하면 `pending`는 아직 데이터가 없다는 것을 의미하기 때문입니다. 이는 기술적으로는 사실입니다. 그러나 현재 데이터를 가져오지 않기 때문에(query가 _활성화_되지 않았기 때문에) 이는 또한 이 플래그를 사용하여 로딩 스피너를 표시할 수 없다는 의미이기도 합니다.

비활성화되거나 게으른 queries를 사용하는 경우 대신 `isLoading` 플래그를 사용할 수 있습니다. 이는 다음에서 계산되는 파생 플래그입니다.

`isPending && isFetching`

따라서 query가 현재 처음으로 가져오는 경우에만 해당됩니다.

## `skipToken`를 사용하여 queries의 형식 안전 비활성화

TypeScript를 사용하는 경우 `skipToken`를 사용하여 query를 비활성화할 수 있습니다. 이는 조건에 따라 query를 비활성화하고 싶지만 여전히 query가 유형에 안전하도록 하려는 경우에 유용합니다.

> **중요**: `useQuery`의 `refetch`는 `skipToken`와 작동하지 않습니다. `skipToken`를 사용하는 query에서 `refetch()`를 호출하면 실행할 유효한 query 함수가 없기 때문에 `Missing queryFn` 오류가 발생합니다. queries를 수동으로 트리거해야 하는 경우 대신 `refetch()`가 제대로 작동할 수 있도록 `enabled: false`를 사용하는 것이 좋습니다. 이 제한 사항을 제외하면 `skipToken`는 `enabled: false`와 동일하게 작동합니다.

[//]: # 'Example3'

```tsx
import { skipToken, useQuery } from '@tanstack/react-query'

function Todos() {
  const [filter, setFilter] = React.useState<string | undefined>()

  const { data } = useQuery({
    queryKey: ['todos', filter],
    // ⬇️ 필터가 정의되지 않거나 비어 있는 한 비활성화됩니다.
    queryFn: filter ? () => fetchTodos(filter) : skipToken,
  })

  return (
    <div>
      // 🚀 필터를 적용하면 query가 활성화되고 실행됩니다.
      <FiltersForm onApply={setFilter} />
      {data && <TodosTable data={data} />}
    </div>
  )
}
```
[//]: # 'Example3'
