---
id: useQuery
title: useQuery
---





```tsx
const {
  data,
  dataUpdatedAt,
  error,
  errorUpdatedAt,
  failureCount,
  failureReason,
  fetchStatus,
  isError,
  isFetched,
  isFetchedAfterMount,
  isFetching,
  isInitialLoading,
  isLoading,
  isLoadingError,
  isPaused,
  isPending,
  isPlaceholderData,
  isRefetchError,
  isRefetching,
  isStale,
  isSuccess,
  refetch,
  status,
} = useQuery(
  () => ({
    queryKey,
    queryFn,
    enabled,
    select,
    placeholderData,
    deferStream,
    reconcile,
    gcTime,
    networkMode,
    initialData,
    initialDataUpdatedAt,
    meta,
    queryKeyHashFn,
    refetchInterval,
    refetchIntervalInBackground,
    refetchOnMount,
    refetchOnReconnect,
    refetchOnWindowFocus,
    retry,
    retryOnMount,
    retryDelay,
    staleTime,
    throwOnError,
  }),
  () => queryClient,
)
```
## 사용예

다음은 Solid Query에서 `useQuery` 기본 요소를 사용하는 방법에 대한 몇 가지 예입니다.

### 기초적인

`useQuery`의 가장 기본적인 사용법은 API에서 데이터를 가져오는 query를 만드는 것입니다.

```tsx
import { useQuery } from '@tanstack/solid-query'

function App() {
  const todos = useQuery(() => ({
    queryKey: 'todos',
    queryFn: async () => {
      const response = await fetch('/api/todos')
      if (!response.ok) {
        throw new Error('Failed to fetch todos')
      }
      return response.json()
    },
  }))

  return (
    <div>
      <Show when={todos.isError}>
        <div>Error: {todos.error.message}</div>
      </Show>
      <Show when={todos.isLoading}>
        <div>Loading...</div>
      </Show>
      <Show when={todos.isSuccess}>
        <div>
          <div>Todos:</div>
          <ul>
            <For each={todos.data}>{(todo) => <li>{todo.title}</li>}</For>
          </ul>
        </div>
      </Show>
    </div>
  )
}
```
### 반응형 옵션

`useQuery`가 객체를 반환하는 함수를 허용하는 이유는 반응형 옵션을 허용하기 위해서입니다. 이는 query 옵션이 시간이 지남에 따라 변경될 수 있는 다른 값/신호에 의존할 때 유용합니다. Solid Query는 반응 범위에서 전달된 함수를 추적하고 종속성이 변경될 때마다 다시 실행할 수 있습니다.

```tsx
import { useQuery } from '@tanstack/solid-query'

function App() {
  const [filter, setFilter] = createSignal('all')

  const todos = useQuery(() => ({
    queryKey: ['todos', filter()],
    queryFn: async () => {
      const response = await fetch(`/api/todos?filter=${filter()}`)
      if (!response.ok) {
        throw new Error('Failed to fetch todos')
      }
      return response.json()
    },
  }))

  return (
    <div>
      <div>
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('active')}>Active</button>
        <button onClick={() => setFilter('completed')}>Completed</button>
      </div>
      <Show when={todos.isError}>
        <div>Error: {todos.error.message}</div>
      </Show>
      <Show when={todos.isLoading}>
        <div>Loading...</div>
      </Show>
      <Show when={todos.isSuccess}>
        <div>
          <div>Todos:</div>
          <ul>
            <For each={todos.data}>{(todo) => <li>{todo.title}</li>}</For>
          </ul>
        </div>
      </Show>
    </div>
  )
}
```
### `Suspense`와 함께 사용

`useQuery`는 query가 보류 중이거나 오류 상태일 때 SolidJS `Suspense` 및 `ErrorBoundary` 구성 요소 트리거를 지원합니다. 이를 통해 구성 요소의 로드 및 오류 상태를 쉽게 처리할 수 있습니다.

```tsx
import { useQuery } from '@tanstack/solid-query'

function App() {
  const todos = useQuery(() => ({
    queryKey: 'todos',
    queryFn: async () => {
      const response = await fetch('/api/todos')
      if (!response.ok) {
        throw new Error('Failed to fetch todos')
      }
      return response.json()
    },
    throwOnError: true,
  }))

  return (
    <ErrorBoundary fallback={<div>Error: {todos.error.message}</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <div>
          <div>Todos:</div>
          <ul>
            <For each={todos.data}>{(todo) => <li>{todo.title}</li>}</For>
          </ul>
        </div>
      </Suspense>
    </ErrorBoundary>
  )
}
```
## `useQuery` 매개변수

- ### Query 옵션 - `Accessor<QueryOptions>`
  - ##### `queryKey: unknown[]`
    - **필수**
    - 이 query에 사용할 query 키입니다.
    - query 키는 안정적인 해시로 해시됩니다. 자세한 내용은 [Query 키](../guides/query-keys.md)를 참조하세요.
    - 이 키가 변경되면 query가 자동으로 업데이트됩니다(`enabled`가 `false`로 설정되지 않은 경우).
  - ##### `queryFn: (context: QueryFunctionContext) => Promise<TData>`
    - **필수이지만 기본 query 함수가 정의되지 않은 경우에만** 자세한 내용은 [기본 Query 함수](../guides/default-query-function.md)를 참조하세요.
    - query가 데이터를 요청하는 데 사용할 기능입니다.
    - [QueryFunctionContext](../guides/query-functions.md#queryfunctioncontext)를 수신합니다.
    - 데이터를 해결하거나 오류를 발생시키는 Promise를 반환해야 합니다. 데이터는 `undefined`일 수 없습니다.
  - ##### `enabled: boolean`
    - 이 query가 자동으로 실행되지 않도록 하려면 이를 `false`로 설정합니다.
    - 자세한 내용은 [종속 Queries](../guides/dependent-queries.md)에 사용할 수 있습니다.
  - ##### `select: (data: TData) => unknown`
    - 선택사항
    - 이 옵션은 query 함수에서 반환된 데이터의 일부를 변환하거나 선택하는 데 사용할 수 있습니다. 이는 반환된 `data` 값에 영향을 주지만 query 캐시에 저장되는 내용에는 영향을 주지 않습니다.
    - `select` 기능은 `data`가 변경되거나 `select` 기능 자체에 대한 참조가 변경되는 경우에만 실행됩니다. 최적화하려면 `useCallback`에 함수를 래핑하세요.
  - ##### `placeholderData: TData | (previousValue: TData | undefined; previousQuery: Query | undefined,) => TData`
    - 선택사항
    - 설정된 경우 이 값은 query가 여전히 `pending` 상태에 있는 동안 이 특정 query 관찰자에 대한 자리 표시자 데이터로 사용됩니다.
    - `placeholderData`는 캐시에 **지속되지 않습니다**.
    - `placeholderData`에 대한 함수를 제공하는 경우 첫 번째 인수로 이전에 관찰한 query 데이터(사용 가능한 경우)를 수신하고 두 번째 인수는 완전한 이전 쿼리 인스턴스가 됩니다.
  - ##### `deferStream: boolean`
    - 선택사항
    - 기본값은 `false`입니다.
    - 스트리밍을 사용하여 서버에서 queries를 렌더링하는 동안에만 적용 가능합니다.
    - 스트림을 플러시하기 전에 query가 서버에서 확인될 때까지 기다리려면 `deferStream`를 `true`로 설정합니다.
    - 이는 query가 해결되기 전에 클라이언트에 로딩 상태를 보내는 것을 방지하는 데 유용할 수 있습니다.
  - ##### `reconcile: false | string | ((oldData: TData | undefined, newData: TData) => TData)`
    - 선택사항
    - 기본값은 `false`입니다.
    - 문자열 키를 기반으로 query 결과 간의 조정을 활성화하려면 이를 문자열로 설정합니다.
    - 기존 데이터와 새 데이터를 받아들이고 동일한 유형의 해결된 데이터를 반환하는 함수로 설정하여 맞춤형 조정 로직을 구현합니다.
  - ##### `gcTime: number | Infinity`
    - SSR 중에는 기본적으로 `5 * 60 * 1000`(5분) 또는 `Infinity`로 설정됩니다.
    - 사용되지 않은/비활성 캐시 데이터가 메모리에 남아 있는 시간(밀리초)입니다. query의 캐시가 사용되지 않거나 비활성화되면 해당 캐시 데이터는 이 기간 이후에 가비지 수집됩니다. 서로 다른 가비지 수집 시간이 지정되면 가장 긴 시간이 사용됩니다.- 참고: 최대 허용 시간은 약 [24일](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout#maximum_delay_value)이지만 [TimeoutManager](../../../reference/timeoutManager.md#timeoutmanagersettimeoutprovider)를 사용하여 이 제한을 해결할 수 있습니다.
    - `Infinity`로 설정하면 가비지 수집이 비활성화됩니다.
  - ##### `networkMode: 'online' | 'always' | 'offlineFirst'`
    - 선택사항
    - 기본값은 `'online'`입니다.
    - 자세한 내용은 [네트워크 모드](../guides/network-mode.md)를 참조하세요.
  - ##### `initialData: TData | () => TData`
    - 선택사항
    - 설정된 경우 이 값은 query 캐시의 초기 데이터로 사용됩니다(query가 아직 생성되거나 캐시되지 않은 경우).
    - 함수로 설정되면 공유/루트 query 초기화 중에 함수가 **한 번** 호출되고 initialData를 동기적으로 반환할 것으로 예상됩니다.
    - `staleTime`가 설정되지 않은 한 초기 데이터는 기본적으로 오래된 것으로 간주됩니다.
    - `initialData`는 캐시에 **지속됩니다**
  - ##### `initialDataUpdatedAt: number | (() => number | undefined)`
    - 선택사항
    - 설정되면 이 값은 `initialData` 자체가 마지막으로 업데이트된 시간(밀리초)으로 사용됩니다.
  - ##### `meta: Record<string, unknown>`
    - 선택사항
    - 설정된 경우 필요에 따라 사용할 수 있는 query 캐시 항목에 대한 추가 정보를 저장합니다. `query`를 사용할 수 있는 모든 곳에서 액세스할 수 있으며 `queryFn`에 제공되는 `QueryFunctionContext`의 일부이기도 합니다.
  - ##### `queryKeyHashFn: (queryKey: QueryKey) => string`
    - 선택사항
    - 지정된 경우 이 함수는 `queryKey`를 문자열로 해시하는 데 사용됩니다.
  - ##### `refetchInterval: number | false | ((query: Query) => number | false | undefined)`
    - 선택사항
    - 숫자로 설정하면 모든 queries가 밀리초 단위로 이 빈도로 지속적으로 다시 가져옵니다.
    - 함수로 설정하면 query로 함수가 실행되어 주파수를 계산합니다.
  - ##### `refetchIntervalInBackground: boolean`
    - 선택사항
    - `true`로 설정된 경우 `refetchInterval`를 사용하여 지속적으로 다시 가져오도록 설정된 queries는 탭/창이 백그라운드에 있는 동안 계속해서 다시 가져옵니다.
  - ##### `refetchOnMount: boolean | "always" | ((query: Query) => boolean | "always")`
    - 선택사항
    - 기본값은 `true`입니다.
    - `true`로 설정된 경우 데이터가 오래되면 query가 마운트 시 다시 가져옵니다.
    - `false`로 설정된 경우 query는 마운트 시 다시 가져오지 않습니다.
    - `"always"`로 설정된 경우 query는 마운트 시 항상 다시 가져옵니다.
    - 함수로 설정된 경우 해당 함수는 query로 실행되어 값을 계산합니다.
  - ##### `refetchOnWindowFocus: boolean | "always" | ((query: Query) => boolean | "always")`
    - 선택사항
    - 기본값은 `true`입니다.
    - `true`로 설정된 경우 데이터가 오래되면 query가 창 포커스를 다시 가져옵니다.
    - `false`로 설정된 경우 query는 창 포커스를 다시 가져오지 않습니다.
    - `"always"`로 설정된 경우 query는 항상 창 포커스를 다시 가져옵니다.
    - 함수로 설정된 경우 해당 함수는 query로 실행되어 값을 계산합니다.
  - ##### `refetchOnReconnect: boolean | "always" | ((query: Query) => boolean | "always")`
    - 선택사항
    - 기본값은 `true`입니다.
    - `true`로 설정된 경우 query는 데이터가 오래된 경우 재연결 시 다시 가져옵니다.
    - `false`로 설정된 경우 query는 다시 연결할 때 다시 가져오지 않습니다.- `"always"`로 설정된 경우 query는 재연결 시 항상 다시 가져옵니다.
    - 함수로 설정된 경우 해당 함수는 query로 실행되어 값을 계산합니다.
  - ##### `retry: boolean | number | (failureCount: number, error: TError) => boolean`
    - `false`인 경우, 실패한 queries는 기본적으로 재시도하지 않습니다.
    - `true`, 실패한 queries의 경우 무한 재시도합니다.
    - `number`로 설정된 경우, 예: `3`, 실패 queries는 실패한 query 수가 해당 숫자를 충족할 때까지 재시도합니다.
    - 클라이언트의 기본값은 `3`이고 서버의 `0`입니다.
  - ##### `retryOnMount: boolean`
    - `false`로 설정된 경우 query에 오류가 있으면 마운트 시 재시도되지 않습니다. 기본값은 `true`입니다.
  - ##### `retryDelay: number | (retryAttempt: number, error: TError) => number`
    - 이 함수는 `retryAttempt` 정수와 실제 오류를 수신하고 다음 시도 전에 적용할 지연을 밀리초 단위로 반환합니다.
    - `attempt => Math.min(attempt > 1 ? 2 ** attempt * 1000 : 1000, 30 * 1000)`와 같은 기능은 지수 백오프를 적용합니다.
    - `attempt => attempt * 1000`와 같은 기능은 선형 백오프를 적용합니다.
  - ##### `staleTime: number | Infinity`
    - 선택사항
    - 기본값은 `0`입니다.
    - 데이터가 오래된 것으로 간주된 후의 시간(밀리초)입니다. 이 값은 정의된 후크에만 적용됩니다.
    - `Infinity`로 설정하면 데이터가 오래된 것으로 간주되지 않습니다.
  - ##### `throwOnError: undefined | boolean | (error: TError, query: Query) => boolean`
    - 렌더링 단계에서 오류가 발생하고 가장 가까운 오류 경계로 전파되도록 하려면 이를 `true`로 설정합니다.
    - 오류 경계에 오류를 던지는 `suspense`의 기본 동작을 비활성화하려면 이를 `false`로 설정합니다.
    - 함수로 설정하면 오류와 query가 전달되며 오류 경계에 오류를 표시할지(`true`) 또는 오류를 상태로 반환할지(`false`)를 나타내는 boolean을 반환해야 합니다.

- ### Query 클라이언트 - `Accessor<QueryClient>`
  - 선택사항
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

## `useQuery` 반환 값 - `Store<QueryResult<TData, TError>>`

`useQuery`는 다음 속성을 가진 SolidJS 저장소를 반환합니다.

- ##### `status: QueryStatus`
  - 될 것입니다 :
    - 캐시된 데이터가 없고 query 시도가 아직 완료되지 않은 경우 `pending`입니다.
    - query 시도로 인해 오류가 발생한 경우 `error`. 해당 `error` 속성에는 가져오기 시도에서 수신된 오류가 있습니다.
    - query가 오류 없이 응답을 수신하고 해당 데이터를 표시할 준비가 된 경우 `success`입니다. query의 해당 `data` 속성은 성공적인 가져오기에서 수신된 데이터이거나 query의 `enabled` 속성이 `false`로 설정되어 있고 아직 가져오지 않은 경우 `data`는 제공된 첫 번째 `initialData`입니다. 초기화 시 query.
- ##### `isPending: boolean`
  - 편의를 위해 위의 `status` 변수에서 파생된 boolean이 제공됩니다.
- ##### `isSuccess: boolean`
  - 편의를 위해 위의 `status` 변수에서 파생된 boolean이 제공됩니다.
- ##### `isError: boolean`
  - 편의를 위해 위의 `status` 변수에서 파생된 boolean이 제공됩니다.
- ##### `isLoadingError: boolean`
  - 처음 가져오는 동안 query가 실패한 경우 `true`가 됩니다.
- ##### `isRefetchError: boolean`
  - 다시 가져오는 동안 query가 실패한 경우 `true`가 됩니다.
- ##### `data: Resource<TData>`
  - 기본값은 `undefined`입니다.
  - query에 대한 마지막으로 성공적으로 해결된 데이터입니다.
  - **중요**: `data` 속성은 SolidJS 리소스입니다. 즉, `<Suspense>` 구성 요소 아래에서 데이터에 액세스하면
    데이터를 아직 사용할 수 없는 경우 Suspense 경계를 트리거합니다.
- ##### `dataUpdatedAt: number`
  - query가 가장 최근에 `status`를 `"success"`로 반환한 시점의 타임스탬프입니다.
- ##### `error: null | TError`
  - 기본값은 `null`입니다.
  - 오류가 발생한 경우 query에 대한 오류 개체입니다.
- ##### `errorUpdatedAt: number`
  - query가 가장 최근에 `status`를 `"error"`로 반환한 시점의 타임스탬프입니다.
- ##### `isStale: boolean`
  - 캐시의 데이터가 무효화되거나 데이터가 지정된 `staleTime`보다 오래된 경우 `true`가 됩니다.
- ##### `isPlaceholderData: boolean`
  - 표시된 데이터가 자리 표시자 데이터인 경우 `true`가 됩니다.
- ##### `isFetched: boolean`
  - query를 가져온 경우 `true`가 됩니다.
- ##### `isFetchedAfterMount: boolean`
  - 구성요소가 마운트된 후 query를 가져온 경우 `true`가 됩니다.
  - 이 속성은 이전에 캐시된 데이터를 표시하지 않는 데 사용할 수 있습니다.
- ##### `fetchStatus: FetchStatus`
  - `fetching`: queryFn가 실행될 때마다 `true`입니다. 여기에는 초기 `pending` 및 백그라운드 다시 가져오기가 포함됩니다.
  - `paused`: query를 가져오려고 했지만 `paused`였습니다.
  - `idle`: query를 가져오지 않습니다.
  - 자세한 내용은 [네트워크 모드](../guides/network-mode.md)를 참조하세요.
- ##### `isFetching: boolean`
  - 편의를 위해 위의 `fetchStatus` 변수에서 파생된 boolean이 제공됩니다.
- ##### `isPaused: boolean`
  - 편의를 위해 위의 `fetchStatus` 변수에서 파생된 boolean이 제공됩니다.
- ##### `isRefetching: boolean`
  - 백그라운드 다시 가져오기가 진행 중일 때마다 `true`입니다. 이는 초기 `pending`를 포함하지 _않습니다_
  -`isFetching && !isPending`와 동일합니다.- ##### `isLoading: boolean`
  - query에 대한 첫 번째 가져오기가 진행 중일 때마다 `true`입니다.
  - `isFetching && isPending`와 동일합니다.
- ##### `isInitialLoading: boolean`
  - **지원 중단됨**
  - `isLoading`의 별칭은 다음 주요 버전에서 제거됩니다.
- ##### `failureCount: number`
  - query의 실패 횟수입니다.
  - query가 실패할 때마다 증가합니다.
  - query가 성공하면 `0`로 재설정됩니다.
- ##### `failureReason: null | TError`
  - query 재시도 실패 이유입니다.
  - query가 성공하면 `null`로 재설정됩니다.
- ##### `errorUpdateCount: number`
  - 모든 오류의 합계입니다.
- ##### `refetch: (options: { throwOnError: boolean, cancelRefetch: boolean }) => Promise<UseQueryResult>`
  - query를 수동으로 다시 가져오는 기능입니다.
  - query 오류가 발생한 경우 해당 오류만 기록됩니다. 오류가 발생하도록 하려면 `throwOnError: true` 옵션을 전달하세요.
  - `cancelRefetch?: boolean`
    - 기본값은 `true`입니다.
      - 기본적으로 현재 실행 중인 요청은 새 요청이 이루어지기 전에 취소됩니다.
    - `false`로 설정하면 이미 실행 중인 요청이 있는 경우 다시 가져오기가 수행되지 않습니다.