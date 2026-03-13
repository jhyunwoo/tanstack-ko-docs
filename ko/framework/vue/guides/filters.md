---
id: filters
title: 필터
---




TanStack Query 내의 일부 메소드는 `QueryFilters` 또는 `MutationFilters` 객체를 허용합니다.

## `Query Filters`

query 필터는 query를 다음과 일치시키는 특정 조건이 있는 개체입니다.

```tsx
// 모두 취소 queries
await queryClient.cancelQueries()

// 키에서 `posts`로 시작하는 모든 비활성 queries를 제거합니다.
queryClient.removeQueries({ queryKey: ['posts'], type: 'inactive' })

// 모든 활성 queries를 다시 가져옵니다.
await queryClient.refetchQueries({ type: 'active' })

// 키에서 `posts`로 시작하는 모든 활성 queries를 다시 가져옵니다.
await queryClient.refetchQueries({ queryKey: ['posts'], type: 'active' })
```
query 필터 객체는 다음 속성을 지원합니다.

- `queryKey?: QueryKey`
  - 일치시킬 query 키를 정의하려면 이 속성을 설정합니다.
- `exact?: boolean`
  - queries를 query 키로 포괄적으로 검색하지 않으려면 `exact: true` 옵션을 전달하여 전달한 정확한 query 키가 있는 query만 반환할 수 있습니다.
- `type?: 'active' | 'inactive' | 'all'`
  - 기본값은 `all`입니다.
  - `active`로 설정하면 활성 queries와 일치합니다.
  - `inactive`로 설정하면 비활성 queries와 일치합니다.
- `stale?: boolean`
  - `true`로 설정하면 오래된 queries와 일치합니다.
  - `false`로 설정하면 새로운 queries와 일치합니다.
- `fetchStatus?: FetchStatus`
  - `fetching`로 설정하면 현재 가져오는 queries와 일치합니다.
  - `paused`로 설정하면 가져오려고 했지만 `paused`였던 queries와 일치합니다.
  - `idle`로 설정하면 가져오지 않는 queries와 일치합니다.
- `predicate?: (query: Query) => boolean`
  - 이 조건자 함수는 일치하는 모든 queries에 대한 최종 필터로 사용됩니다. 다른 필터가 지정되지 않은 경우 이 함수는 캐시의 모든 query에 대해 평가됩니다.

## `Mutation Filters`

mutation 필터는 mutation를 다음과 일치시키는 특정 조건이 있는 개체입니다.

```tsx
// mutations를 가져오는 모든 개수를 가져옵니다.
await queryClient.isMutating()

// mutationKey로 mutations 필터링
await queryClient.isMutating({ mutationKey: ['post'] })

// 조건자 함수를 사용하여 mutations 필터링
await queryClient.isMutating({
  predicate: (mutation) => mutation.state.variables?.id === 1,
})
```
mutation 필터 객체는 다음 속성을 지원합니다.

- `mutationKey?: MutationKey`
  - 일치시킬 mutation 키를 정의하려면 이 속성을 설정합니다.
- `exact?: boolean`
  - mutation 키로 mutations를 포괄적으로 검색하지 않으려면 `exact: true` 옵션을 전달하여 전달한 정확한 mutation 키가 포함된 mutation만 반환할 수 있습니다.
- `status?: MutationStatus`
  - 상태에 따라 mutations를 필터링할 수 있습니다.
- `predicate?: (mutation: Mutation) => boolean`
  - 이 조건자 함수는 일치하는 모든 mutations에 대한 최종 필터로 사용됩니다. 다른 필터가 지정되지 않은 경우 이 함수는 캐시의 모든 mutation에 대해 평가됩니다.

## 유틸리티

### `matchQuery`

```tsx
const isMatching = matchQuery(filters, query)
```
query가 제공된 query 필터 세트와 일치하는지 여부를 나타내는 boolean을 반환합니다.

### `matchMutation`

```tsx
const isMatching = matchMutation(filters, mutation)
```
mutation가 제공된 mutation 필터 세트와 일치하는지 여부를 나타내는 boolean을 반환합니다.