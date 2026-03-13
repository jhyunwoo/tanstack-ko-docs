---
id: quick-start
title: 빠른 시작
---

이 코드 조각은 React Query의 3가지 핵심 개념을 매우 간략하게 보여줍니다.

- [Queries](guides/queries.md)
- [Mutations](guides/mutations.md)
- [Query 무효화](guides/query-invalidation.md)

[//]: # 'Example'

완벽하게 작동하는 예제를 찾고 있다면 [간단한 StackBlitz 예제](examples/simple.md)를 살펴보세요.

```tsx
import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { getTodos, postTodo } from '../my-api'

// 클라이언트 만들기
const queryClient = new QueryClient()

function App() {
  return (
    // 앱에 클라이언트 제공
    <QueryClientProvider client={queryClient}>
      <Todos />
    </QueryClientProvider>
  )
}

function Todos() {
  // 클라이언트에 액세스
  const queryClient = useQueryClient()

  // Queries
  const query = useQuery({ queryKey: ['todos'], queryFn: getTodos })

  // Mutations
  const mutation = useMutation({
    mutationFn: postTodo,
    onSuccess: () => {
      // 무효화하고 다시 가져오기
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return (
    <div>
      <ul>
        {query.data?.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>

      <button
        onClick={() => {
          mutation.mutate({
            id: Date.now(),
            title: 'Do Laundry',
          })
        }}
      >
        Add Todo
      </button>
    </div>
  )
}

render(<App />, document.getElementById('root'))
```
[//]: # 'Example'

이 세 가지 개념은 React Query의 핵심 기능의 대부분을 구성합니다. 문서의 다음 섹션에서는 이러한 핵심 개념 각각에 대해 자세히 설명합니다.