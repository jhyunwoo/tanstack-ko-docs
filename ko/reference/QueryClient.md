---
id: QueryClient
title: QueryClient
---




## `QueryClient`

`QueryClient`는 캐시와 상호 작용하는 데 사용할 수 있습니다.

```tsx
import { QueryClient } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity,
    },
  },
})

await queryClient.prefetchQuery({ queryKey: ['posts'], queryFn: fetchPosts })
```
사용 가능한 방법은 다음과 같습니다.

- [`queryClient.fetchQuery`](#queryclientfetchquery)
- [`queryClient.fetchInfiniteQuery`](#queryclientfetchinfinitequery)
- [`queryClient.prefetchQuery`](#queryclientprefetchquery)
- [`queryClient.prefetchInfiniteQuery`](#queryclientprefetchinfinitequery)
- [`queryClient.getQueryData`](#queryclientgetquerydata)
- [`queryClient.ensureQueryData`](#queryclientensurequerydata)
- [`queryClient.ensureInfiniteQueryData`](#queryclientensureinfinitequerydata)
- [`queryClient.getQueriesData`](#queryclientgetqueriesdata)
- [`queryClient.setQueryData`](#queryclientsetquerydata)
- [`queryClient.getQueryState`](#queryclientgetquerystate)
- [`queryClient.setQueriesData`](#queryclientsetqueriesdata)
- [`queryClient.invalidateQueries`](#queryclientinvalidatequeries)
- [`queryClient.refetchQueries`](#queryclientrefetchqueries)
- [`queryClient.cancelQueries`](#queryclientcancelqueries)
- [`queryClient.removeQueries`](#queryclientremovequeries)
- [`queryClient.resetQueries`](#queryclientresetqueries)
- [`queryClient.isFetching`](#queryclientisfetching)
- [`queryClient.isMutating`](#queryclientsmutating)
- [`queryClient.getDefaultOptions`](#queryclientgetdefaultoptions)
- [`queryClient.setDefaultOptions`](#queryclientset기본 옵션)
- [`queryClient.getQueryDefaults`](#queryclientgetquerydefaults)
- [`queryClient.setQueryDefaults`](#queryclientsetquerydefaults)
- [`queryClient.getMutationDefaults`](#queryclientgetmutationdefaults)
- [`queryClient.setMutationDefaults`](#queryclientsetmutationdefaults)
- [`queryClient.getQueryCache`](#queryclientgetquerycache)
- [`queryClient.getMutationCache`](#queryclientgetmutationcache)
- [`queryClient.clear`](#queryclientclear)
- [`queryClient.resumePausedMutations`](#queryclientresumepausedmutations)

**옵션**

- `queryCache?: QueryCache`
  - 선택사항
  - 이 클라이언트가 연결된 query 캐시입니다.
- `mutationCache?: MutationCache`
  - 선택사항
  - 이 클라이언트가 연결된 mutation 캐시입니다.
- `defaultOptions?: DefaultOptions`
  - 선택사항
  - 이 queryClient를 사용하여 모든 queries 및 mutations에 대한 기본값을 정의합니다.
  - [hydration](../framework/react/reference/hydration.md)에 사용할 기본값을 정의할 수도 있습니다.

## `queryClient.fetchQuery`

`fetchQuery`는 query를 가져오고 캐시하는 데 사용할 수 있는 비동기 방법입니다. 데이터로 해결되거나 오류가 발생합니다. 결과가 필요하지 않고 query만 가져오려면 `prefetchQuery` 메서드를 사용하세요.

query가 존재하고 데이터가 무효화되지 않았거나 지정된 `staleTime`보다 오래된 경우 캐시의 데이터가 반환됩니다. 그렇지 않으면 최신 데이터를 가져오려고 시도합니다.

```tsx
try {
  const data = await queryClient.fetchQuery({ queryKey, queryFn })
} catch (error) {
  console.log(error)
}
```
데이터가 특정 시간보다 오래된 경우에만 가져오도록 `staleTime`를 지정합니다.

```tsx
try {
  const data = await queryClient.fetchQuery({
    queryKey,
    queryFn,
    staleTime: 10000,
  })
} catch (error) {
  console.log(error)
}
```
**옵션**

`fetchQuery`의 옵션은 다음을 제외하고 [useQuery](../framework/react/reference/useQuery.md)의 옵션과 정확히 동일합니다. `enabled, refetchInterval, refetchIntervalInBackground, refetchOnWindowFocus, refetchOnReconnect, refetchOnMount, notifyOnChangeProps, throwOnError, select, suspense, placeholderData`; 이는 useQuery 및 useInfiniteQuery에만 적용됩니다. 더 명확하게 알아보려면 [소스 코드](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/query-core/src/types.ts#L119)를 확인하세요.

**보고**

- `Promise<TData>`

## `queryClient.fetchInfiniteQuery`

`fetchInfiniteQuery`는 `fetchQuery`와 유사하지만 무한한 query를 가져오고 캐시하는 데 사용할 수 있습니다.

```tsx
try {
  const data = await queryClient.fetchInfiniteQuery({ queryKey, queryFn })
  console.log(data.pages)
} catch (error) {
  console.log(error)
}
```
**옵션**

`fetchInfiniteQuery`의 옵션은 [`fetchQuery`](#queryclientfetchquery)의 옵션과 완전히 동일합니다.

**보고**

- `Promise<InfiniteData<TData, TPageParam>>`

## `queryClient.prefetchQuery`

`prefetchQuery`는 query가 필요하거나 `useQuery` 및 친구들과 함께 렌더링되기 전에 query를 프리페치하는 데 사용할 수 있는 비동기 방법입니다. 이 방법은 데이터를 던지거나 반환하지 않는다는 점을 제외하면 `fetchQuery`와 동일하게 작동합니다.

```tsx
await queryClient.prefetchQuery({ queryKey, queryFn })
```
구성에서 기본 queryFn와 함께 사용할 수도 있습니다!

```tsx
await queryClient.prefetchQuery({ queryKey })
```
**옵션**

`prefetchQuery`의 옵션은 [`fetchQuery`](#queryclientfetchquery)의 옵션과 완전히 동일합니다.

**보고**

- `Promise<void>`
  - 가져오기가 필요하지 않거나 query가 실행된 후에 즉시 해결되는 Promise이 반환됩니다. 데이터를 반환하지 않으며 오류도 발생하지 않습니다.

## `queryClient.prefetchInfiniteQuery`

`prefetchInfiniteQuery`는 `prefetchQuery`와 유사하지만 무한 query를 미리 가져오고 캐시하는 데 사용할 수 있습니다.

```tsx
await queryClient.prefetchInfiniteQuery({ queryKey, queryFn })
```
**옵션**

`prefetchInfiniteQuery`의 옵션은 [`fetchQuery`](#queryclientfetchquery)의 옵션과 완전히 동일합니다.

**보고**

- `Promise<void>`
  - 가져오기가 필요하지 않거나 query가 실행된 후에 즉시 해결되는 Promise이 반환됩니다. 데이터를 반환하지 않으며 오류도 발생하지 않습니다.

## `queryClient.getQueryData`

`getQueryData`는 기존 query의 캐시된 데이터를 가져오는 데 사용할 수 있는 동기 함수입니다. query가 존재하지 않으면 `undefined`가 반환됩니다.

```tsx
const data = queryClient.getQueryData(queryKey)
```
**옵션**

- `queryKey: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)

**보고**

- `data: TQueryFnData | undefined`
  - 캐시된 query에 대한 데이터 또는 query가 존재하지 않는 경우 `undefined`에 대한 데이터입니다.

## `queryClient.ensureQueryData`

`ensureQueryData`는 기존 query의 캐시된 데이터를 가져오는 데 사용할 수 있는 비동기 함수입니다. query가 존재하지 않으면 `queryClient.fetchQuery`가 호출되고 해당 결과가 반환됩니다.

```tsx
const data = await queryClient.ensureQueryData({ queryKey, queryFn })
```
**옵션**

- [`fetchQuery`](#queryclientfetchquery)와 동일한 옵션
- `revalidateIfStale: boolean`
  - 선택사항
  - 기본값은 `false`입니다.
  - `true`로 설정하면 오래된 데이터는 백그라운드에서 다시 가져오지만, 캐시된 데이터는 즉시 반환됩니다.

**보고**

- `Promise<TData>`

## `queryClient.ensureInfiniteQueryData`

`ensureInfiniteQueryData`는 기존 무한 query의 캐시 데이터를 가져오는 데 사용할 수 있는 비동기 함수입니다. query가 존재하지 않으면 `queryClient.fetchInfiniteQuery`가 호출되고 해당 결과가 반환됩니다.

```tsx
const data = await queryClient.ensureInfiniteQueryData({
  queryKey,
  queryFn,
  initialPageParam,
  getNextPageParam,
})
```
**옵션**

- [`fetchInfiniteQuery`](#queryclientfetchinfinitequery)와 동일한 옵션
- `revalidateIfStale: boolean`
  - 선택사항
  - 기본값은 `false`입니다.
  - `true`로 설정하면 오래된 데이터는 백그라운드에서 다시 가져오지만, 캐시된 데이터는 즉시 반환됩니다.

**보고**

- `Promise<InfiniteData<TData, TPageParam>>`

## `queryClient.getQueriesData`

`getQueriesData`는 여러 queries의 캐시된 데이터를 가져오는 데 사용할 수 있는 동기 함수입니다. 전달된 queryKey 또는 queryFilter와 일치하는 queries만 반환됩니다. 일치하는 queries가 없으면 빈 배열이 반환됩니다.

```tsx
const data = queryClient.getQueriesData(filters)
```
**옵션**

- `filters: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
  - 필터가 전달되면 필터와 일치하는 queryKeys가 있는 데이터가 반환됩니다.

**보고**

- `[queryKey: QueryKey, data: TQueryFnData | undefined][]`
  - 일치하는 query 키에 대한 튜플 배열 또는 일치하는 항목이 없는 경우 `[]`. 튜플은 query 키 및 관련 데이터입니다.

**주의사항**

각 튜플에 반환된 데이터는 다양한 구조를 가질 수 있으므로(즉, 필터를 사용하여 "활성" queries를 반환하면 다른 데이터 유형을 반환할 수 있음) `TData` 일반 기본값은 `unknown`입니다. `TData`에 보다 구체적인 유형을 제공하는 경우 각 튜플의 데이터 항목이 모두 동일한 유형이라고 확신하는 것으로 가정됩니다.

이러한 구별은 어떤 구조가 반환될지 알고 있는 TS 개발자에게는 "편리함"에 더 가깝습니다.

## `queryClient.setQueryData`

`setQueryData`는 query의 캐시된 데이터를 즉시 업데이트하는 데 사용할 수 있는 동기 기능입니다. query가 존재하지 않으면 생성됩니다. **기본 `gcTime`인 5분 동안 query가 query 후크에 의해 활용되지 않으면 query가 가비지 수집됩니다**. 여러 queries를 한 번에 업데이트하고 query 키를 부분적으로 일치시키려면 [`queryClient.setQueriesData`](#queryclientsetqueriesdata)를 대신 사용해야 합니다.

> `setQueryData`와 `fetchQuery` 사용의 차이점은 `setQueryData`가 동기화되어 있고 이미 동기적으로 사용 가능한 데이터가 있다고 가정한다는 것입니다. 데이터를 비동기식으로 가져와야 하는 경우 query 키를 다시 가져오거나 `fetchQuery`를 사용하여 비동기식 가져오기를 처리하는 것이 좋습니다.

```tsx
queryClient.setQueryData(queryKey, updater)
```
**옵션**

- `queryKey: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)
- `updater: TQueryFnData | undefined | ((oldData: TQueryFnData | undefined) => TQueryFnData | undefined)`
  - 함수가 아닌 값이 전달되면 데이터가 이 값으로 업데이트됩니다.
  - 함수가 전달되면 이전 데이터 값을 수신하고 새 값을 반환할 것으로 예상됩니다.

**업데이터 값 사용**

```tsx
setQueryData(queryKey, newData)
```
값이 `undefined`인 경우 query 데이터가 업데이트되지 않습니다.

**업데이터 기능 사용하기**

구문의 편의를 위해 현재 데이터 값을 받고 새 값을 반환하는 업데이트 함수를 전달할 수도 있습니다.

```tsx
setQueryData(queryKey, (oldData) => newData)
```
업데이트 기능이 `undefined`를 반환하면 query 데이터가 업데이트되지 않습니다. 업데이터 함수가 `undefined`를 입력으로 받으면 `undefined`를 반환하여 업데이트를 피할 수 있으므로 새 캐시 항목을 생성하지 _않습니다_.

**불변성**

`setQueryData`를 통한 업데이트는 _불변_ 방식으로 수행되어야 합니다. **하지 마십시오** `oldData` 또는 `getQueryData`를 통해 검색한 데이터를 변경하여 캐시에 직접 쓰려고 시도하지 마십시오.

## `queryClient.getQueryState`

`getQueryState`는 기존 query의 상태를 가져오는 데 사용할 수 있는 동기 함수입니다. query가 존재하지 않으면 `undefined`가 반환됩니다.

```tsx
const state = queryClient.getQueryState(queryKey)
console.log(state.dataUpdatedAt)
```
**옵션**

- `queryKey: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)

## `queryClient.setQueriesData`

`setQueriesData`는 필터 기능을 사용하거나 query 키를 부분적으로 일치시켜 여러 queries의 캐시된 데이터를 즉시 업데이트하는 데 사용할 수 있는 동기 기능입니다. 전달된 queryKey 또는 queryFilter와 일치하는 queries만 업데이트되며 새 캐시 항목은 생성되지 않습니다. 내부적으로는 각 기존 query에 대해 [`setQueryData`](#queryclientsetquerydata)가 호출됩니다.

```tsx
queryClient.setQueriesData(filters, updater)
```
**옵션**

- `filters: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
  - 필터가 전달되면 필터와 일치하는 queryKey가 업데이트됩니다.
- `updater: TQueryFnData | (oldData: TQueryFnData | undefined) => TQueryFnData`
  - [setQueryData](#queryclientsetquerydata) 업데이트 함수 또는 새 데이터는 일치하는 각 queryKey에 대해 호출됩니다.

## `queryClient.invalidateQueries`

`invalidateQueries` 메서드는 query 키 또는 query의 기능적으로 액세스 가능한 다른 속성/상태를 기반으로 캐시에서 단일 또는 여러 queries를 무효화하고 다시 가져오는 데 사용할 수 있습니다. 기본적으로 일치하는 모든 queries는 즉시 유효하지 않은 것으로 표시되고 활성 queries는 백그라운드에서 다시 가져옵니다.

- **활성 queries를 다시 가져오는 것을 원하지 않고** 단순히 유효하지 않은 것으로 표시되는 경우 `refetchType: 'none'` 옵션을 사용할 수 있습니다.
- **비활성 queries를 다시 가져오려면** `refetchType: 'all'` 옵션을 사용하세요.
- 다시 가져오기를 위해서는 [queryClient.refetchQueries](#queryclientrefetchqueries)가 호출됩니다.

```tsx
await queryClient.invalidateQueries(
  {
    queryKey: ['posts'],
    exact,
    refetchType: 'active',
  },
  { throwOnError, cancelRefetch },
)
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
  - `queryKey?: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)
  - `refetchType?: 'active' | 'inactive' | 'all' | 'none'`
    - 기본값은 `'active'`입니다.
    - `active`로 설정하면 다시 가져오기 조건자와 일치하고 `useQuery` 및 친구를 통해 적극적으로 렌더링되는 queries만 백그라운드에서 다시 가져옵니다.
    - `inactive`로 설정하면 다시 가져오기 조건자와 일치하고 `useQuery` 및 친구를 통해 적극적으로 렌더링되지 않는 queries만 백그라운드에서 다시 가져옵니다.
    - `all`로 설정하면 다시 가져오기 조건자와 일치하는 모든 queries가 백그라운드에서 다시 가져옵니다.
    - `none`로 설정하면 queries가 다시 가져오지 않으며 다시 가져오기 조건자와 일치하는 항목은 유효하지 않은 것으로만 표시됩니다.
- `options?: InvalidateOptions`:
  - `throwOnError?: boolean`
    - `true`로 설정된 경우 query 다시 가져오기 작업 중 하나라도 실패하면 이 메서드가 발생합니다.
  - `cancelRefetch?: boolean`
    - 기본값은 `true`입니다.
      - 기본적으로 현재 실행 중인 요청은 새 요청이 이루어지기 전에 취소됩니다.
    - `false`로 설정하면 이미 실행 중인 요청이 있는 경우 다시 가져오기가 수행되지 않습니다.

## `queryClient.refetchQueries`

`refetchQueries` 메소드는 특정 조건에 따라 queries를 다시 가져오는 데 사용될 수 있습니다.

예:

```tsx
// 모든 queries를 다시 가져옵니다.
await queryClient.refetchQueries()

// 오래된 queries를 모두 다시 가져옵니다.
await queryClient.refetchQueries({ stale: true })

// query 키와 부분적으로 일치하는 모든 활성 queries를 다시 가져옵니다.
await queryClient.refetchQueries({ queryKey: ['posts'], type: 'active' })

// query 키와 정확히 일치하는 모든 활성 queries를 다시 가져옵니다.
await queryClient.refetchQueries({
  queryKey: ['posts', 1],
  type: 'active',
  exact: true,
})
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
- `options?: RefetchOptions`:
  - `throwOnError?: boolean`
    - `true`로 설정된 경우 query 다시 가져오기 작업 중 하나라도 실패하면 이 메서드가 발생합니다.
  - `cancelRefetch?: boolean`
    - 기본값은 `true`입니다.
      - 기본적으로 현재 실행 중인 요청은 새 요청이 이루어지기 전에 취소됩니다.
    - `false`로 설정하면 이미 실행 중인 요청이 있는 경우 다시 가져오기가 수행되지 않습니다.

**보고**

이 함수는 모든 queries 다시 가져오기가 완료되면 해결될 Promise을 반환합니다. 기본적으로 queries 다시 가져오기 중 하나라도 실패하면 오류가 발생하지 **않지만** `throwOnError` 옵션을 `true`로 설정하여 구성할 수 있습니다.

**참고**

- 관찰자만 비활성화되었기 때문에 "비활성화"된 Queries는 다시 가져오지 않습니다.
- Static StaleTime이 있는 관찰자만 있기 때문에 "정적"인 Queries는 다시 가져오지 않습니다.

## `queryClient.cancelQueries`

`cancelQueries` 메소드는 query 키 또는 query의 다른 기능적으로 액세스 가능한 속성/상태를 기반으로 나가는 queries를 취소하는 데 사용할 수 있습니다.

이는 낙관적 업데이트를 수행할 때 가장 유용합니다. 나가는 query 다시 가져오기를 취소하여 문제가 해결될 때 낙관적 업데이트를 방해하지 않도록 해야 하기 때문입니다.

```tsx
await queryClient.cancelQueries(
  { queryKey: ['posts'], exact: true },
  { silent: true },
)
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
- `cancelOptions?: CancelOptions`: [취소 옵션](../framework/react/guides/query-cancellation.md#cancel-options)

**보고**

이 메서드는 아무것도 반환하지 않습니다.

## `queryClient.removeQueries`

`removeQueries` 메서드는 query 키 또는 query의 기능적으로 액세스 가능한 다른 속성/상태를 기반으로 캐시에서 queries를 제거하는 데 사용할 수 있습니다.

```tsx
queryClient.removeQueries({ queryKey, exact: true })
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)

**보고**

이 메서드는 아무것도 반환하지 않습니다.

## `queryClient.resetQueries`

`resetQueries` 방법을 사용하여 캐시의 queries를 해당 캐시로 재설정할 수 있습니다.
query 키 또는 기타 기능적으로 액세스 가능한 키를 기반으로 한 초기 상태
query의 속성/상태.

구독자에게 알림이 전송됩니다 &mdash; 모든 것을 제거하는 `clear`와 달리
구독자 &mdash; query를 사전 로드된 상태로 재설정합니다. 달리
`invalidateQueries`. query에 `initialData`가 있는 경우 query의 데이터는 다음과 같습니다.
그걸로 재설정하세요. query가 활성 상태이면 다시 가져옵니다.

```tsx
queryClient.resetQueries({ queryKey, exact: true })
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)
- `options?: ResetOptions`:
  - `throwOnError?: boolean`
    - `true`로 설정된 경우 query 다시 가져오기 작업 중 하나라도 실패하면 이 메서드가 발생합니다.
  - `cancelRefetch?: boolean`
    - 기본값은 `true`입니다.
      - 기본적으로 현재 실행 중인 요청은 새 요청이 이루어지기 전에 취소됩니다.
    - `false`로 설정하면 이미 실행 중인 요청이 있는 경우 다시 가져오기가 수행되지 않습니다.

**보고**

이 메서드는 모든 활성 queries가 다시 페치되면 확인하는 Promise을 반환합니다.

## `queryClient.isFetching`

이 `isFetching` 메서드는 캐시에 현재 가져오는 queries 수(있는 경우)를 나타내는 `integer`를 반환합니다(백그라운드 가져오기, 새 페이지 로드 또는 더 많은 무한 query 결과 로드 포함).

```tsx
if (queryClient.isFetching()) {
  console.log('At least one query is fetching!')
}
```
TanStack Query는 또한 query 캐시에 대한 수동 구독을 만들지 않고도 구성 요소에서 이 상태를 구독할 수 있게 해주는 편리한 [useIsFetching](../framework/react/reference/useIsFetching.md) 후크를 내보냅니다.

**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)

**보고**

이 메소드는 queries를 가져온 횟수를 반환합니다.

## `queryClient.isMutating`

이 `isMutating` 메소드는 캐시에 현재 가져오는 mutations 수(있는 경우)를 나타내는 `integer`를 반환합니다.

```tsx
if (queryClient.isMutating()) {
  console.log('At least one mutation is fetching!')
}
```
TanStack Query는 또한 mutation 캐시에 대한 수동 구독을 만들지 않고도 구성 요소에서 이 상태를 구독할 수 있게 해주는 편리한 [useIsMutating](../framework/react/reference/useIsMutating.md) 후크를 내보냅니다.

**옵션**

- `filters: MutationFilters`: [Mutation 필터](../framework/react/guides/filters.md#mutation-filters)

**보고**

이 메소드는 mutations를 가져온 횟수를 반환합니다.

## `queryClient.getDefaultOptions`

`getDefaultOptions` 메소드는 클라이언트를 생성할 때 또는 `setDefaultOptions`를 사용하여 설정된 기본 옵션을 반환합니다.

```tsx
const defaultOptions = queryClient.getDefaultOptions()
```
## `queryClient.setDefaultOptions`

`setDefaultOptions` 메소드를 사용하여 이 queryClient에 대한 기본 옵션을 동적으로 설정할 수 있습니다. 이전에 정의된 기본 옵션을 덮어씁니다.

```tsx
queryClient.setDefaultOptions({
  queries: {
    staleTime: Infinity,
  },
})
```
## `queryClient.getQueryDefaults`

`getQueryDefaults` 메소드는 특정 queries에 대해 설정된 기본 옵션을 반환합니다.

```tsx
const defaultOptions = queryClient.getQueryDefaults(['posts'])
```
> 여러 개의 query 기본값이 지정된 query 키와 일치하는 경우 등록 순서에 따라 함께 병합됩니다.
> [`setQueryDefaults`](#queryclientsetquerydefaults)를 참조하세요.

## `queryClient.setQueryDefaults`

`setQueryDefaults`를 사용하여 특정 queries에 대한 기본 옵션을 설정할 수 있습니다.

```tsx
queryClient.setQueryDefaults(['posts'], { queryFn: fetchPosts })

function Component() {
  const { data } = useQuery({ queryKey: ['posts'] })
}
```
**옵션**

- `queryKey: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)
- `options: QueryOptions`

> [`getQueryDefaults`](#queryclientgetquerydefaults)에 명시된 대로 query 기본값 등록 순서가 중요합니다.
> 일치하는 기본값은 `getQueryDefaults`에 의해 병합되므로 등록은 **가장 일반적인 키**에서 **가장 덜 일반적인 키** 순서로 이루어져야 합니다.
> 이렇게 하면 보다 구체적인 기본값이 보다 일반적인 기본값보다 우선 적용됩니다.

## `queryClient.getMutationDefaults`

`getMutationDefaults` 메소드는 특정 mutations에 대해 설정된 기본 옵션을 반환합니다.

```tsx
const defaultOptions = queryClient.getMutationDefaults(['addPost'])
```
## `queryClient.setMutationDefaults`

`setMutationDefaults`를 사용하여 특정 mutations에 대한 기본 옵션을 설정할 수 있습니다.

```tsx
queryClient.setMutationDefaults(['addPost'], { mutationFn: addPost })

function Component() {
  const { data } = useMutation({ mutationKey: ['addPost'] })
}
```
**옵션**

- `mutationKey: unknown[]`
- `options: MutationOptions`

> [`setQueryDefaults`](#queryclientsetquerydefaults)와 마찬가지로 여기서는 등록 순서가 중요합니다.

## `queryClient.getQueryCache`

`getQueryCache` 메서드는 이 클라이언트가 연결된 query 캐시를 반환합니다.

```tsx
const queryCache = queryClient.getQueryCache()
```
## `queryClient.getMutationCache`

`getMutationCache` 메서드는 이 클라이언트가 연결된 mutation 캐시를 반환합니다.

```tsx
const mutationCache = queryClient.getMutationCache()
```
## `queryClient.clear`

`clear` 방법은 연결된 모든 캐시를 지웁니다.

```tsx
queryClient.clear()
```
## `queryClient.resumePausedMutations`

네트워크 연결이 없어 일시 중지된 mutations를 재개하는 데 사용할 수 있습니다.

```tsx
queryClient.resumePausedMutations()
```
