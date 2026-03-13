---
id: updates-from-mutation-responses
title: Mutation 응답의 업데이트
---




서버에서 개체를 **업데이트**하는 mutations를 처리할 때 mutation의 응답으로 새 개체가 자동으로 반환되는 것이 일반적입니다. 해당 항목에 대한 queries를 다시 가져오고 이미 가지고 있는 데이터에 대한 네트워크 호출을 낭비하는 대신, mutation 함수에서 반환된 개체를 활용하고 [QueryClient](../../../reference/QueryClient.md#queryclientsetquerydata) 방법:

[//]: # 'Example'

```tsx
const queryClient = useQueryClient()

const mutation = useMutation({
  mutationFn: editTodo,
  onSuccess: (data) => {
    queryClient.setQueryData(['todo', { id: 5 }], data)
  },
})

mutation.mutate({
  id: 5,
  name: 'Do the laundry',
})

// 아래 query는 다음의 응답으로 업데이트됩니다.
// 성공적인 mutation
const { status, data, error } = useQuery({
  queryKey: ['todo', { id: 5 }],
  queryFn: fetchTodoById,
})
```
[//]: # 'Example'

`onSuccess` 로직을 재사용 가능한 mutation에 연결하고 싶을 수도 있습니다.
다음과 같이 사용자 정의 후크를 만듭니다.

[//]: # 'Example2'

```tsx
const useMutateTodo = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: editTodo,
    // 두 번째 인수는 `mutate` 함수가 받는 변수 객체입니다.
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['todo', { id: variables.id }], data)
    },
  })
}
```
[//]: # 'Example2'

## 불변성

`setQueryData`를 통한 업데이트는 _불변_ 방식으로 수행되어야 합니다. **하지 마십시오** 데이터(캐시에서 검색한)를 변경하여 캐시에 직접 쓰려고 시도하지 마십시오. 처음에는 작동할 수도 있지만 진행하면서 미묘한 버그가 발생할 수 있습니다.

[//]: # 'Example3'

```tsx
queryClient.setQueryData(['posts', { id }], (oldData) => {
  if (oldData) {
    // ❌ 이것을 시도하지 마세요
    oldData.title = 'my new post title'
  }
  return oldData
})

queryClient.setQueryData(
  ['posts', { id }],
  // ✅ 이 방법이에요
  (oldData) =>
    oldData
      ? {
          ...oldData,
          title: 'my new post title',
        }
      : oldData,
)
```
[//]: # 'Example3'
