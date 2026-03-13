---
id: useMutationState
title: useMutationState
---




`useMutationState`는 `MutationCache`의 모든 mutations에 대한 액세스를 제공하는 후크입니다. `filters`를 전달하여 mutations 범위를 좁히고 `select`를 전달하여 mutation 상태를 변환할 수 있습니다.

**예제 1: 실행 중인 모든 mutations의 모든 변수 가져오기**

```tsx
import { useMutationState } from '@tanstack/react-query'

const variables = useMutationState({
  filters: { status: 'pending' },
  select: (mutation) => mutation.state.variables,
})
```
**예 2: `mutationKey`를 통해 특정 mutations에 대한 모든 데이터 가져오기**

```tsx
import { useMutation, useMutationState } from '@tanstack/react-query'

const mutationKey = ['posts']

// 상태를 가져오려는 일부 mutation
const mutation = useMutation({
  mutationKey,
  mutationFn: (newPost) => {
    return axios.post('/posts', newPost)
  },
})

const data = useMutationState({
  // 이 mutation 키는 지정된 mutation의 mutation 키와 일치해야 합니다(위 참조).
  filters: { mutationKey },
  select: (mutation) => mutation.state.data,
})
```
**예 3: `mutationKey`를 통해 최신 mutation 데이터에 액세스합니다**.
`mutate`를 호출할 때마다 `gcTime` 밀리초 동안 mutation 캐시에 새 항목이 추가됩니다.

최신 호출에 액세스하려면 `useMutationState`가 반환하는 마지막 항목을 확인할 수 있습니다.

```tsx
import { useMutation, useMutationState } from '@tanstack/react-query'

const mutationKey = ['posts']

// 상태를 가져오려는 일부 mutation
const mutation = useMutation({
  mutationKey,
  mutationFn: (newPost) => {
    return axios.post('/posts', newPost)
  },
})

const data = useMutationState({
  // 이 mutation 키는 지정된 mutation의 mutation 키와 일치해야 합니다(위 참조).
  filters: { mutationKey },
  select: (mutation) => mutation.state.data,
})

// 최신 mutation 데이터
const latest = data[data.length - 1]
```
**옵션**

- `options`
  - `filters?: MutationFilters`: [Mutation 필터](../guides/filters.md#mutation-필터)
  - `select?: (mutation: Mutation) => TResult`
    - mutation 상태를 변환하려면 이를 사용합니다.
- `queryClient?: QueryClient`
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

**보고**

- `Array<TResult>`
  - 일치하는 각 mutation에 대해 `select`가 반환하는 배열이 됩니다.