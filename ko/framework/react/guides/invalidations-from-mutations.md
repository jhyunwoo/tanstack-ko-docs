---
id: invalidations-from-mutations
title: Mutations의 무효화
---




queries를 무효화하는 것은 전투의 절반에 불과합니다. **언제** 무효화해야 하는지 아는 것이 나머지 절반입니다. 일반적으로 앱의 mutation가 성공하면 mutation의 새로운 변경 사항을 설명하기 위해 무효화하고 다시 가져와야 하는 관련 queries가 애플리케이션에 있을 가능성이 매우 높습니다.

예를 들어, 새 할 일을 게시하기 위한 mutation가 있다고 가정합니다.

[//]: # 'Example'

```tsx
const mutation = useMutation({ mutationFn: postTodo })
```
[//]: # 'Example'

성공적인 `postTodo` mutation가 발생하면 모든 `todos` queries가 무효화되고 새 할일 항목을 표시하기 위해 다시 가져오기를 원할 것입니다. 이렇게 하려면 `useMutation`의 `onSuccess` 옵션과 `client`의 `invalidateQueries` 기능을 사용할 수 있습니다.

[//]: # 'Example2'

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'

const queryClient = useQueryClient()

// 이 mutation가 성공하면 'todos' 또는 'reminders' query 키를 사용하여 모든 queries를 무효화합니다.
const mutation = useMutation({
  mutationFn: addTodo,
  onSuccess: async () => {
    // 단일 query를 무효화하는 경우
    await queryClient.invalidateQueries({ queryKey: ['todos'] })

    // 여러 queries를 무효화하는 경우
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['todos'] }),
      queryClient.invalidateQueries({ queryKey: ['reminders'] }),
    ])
  },
})
```
[//]: # 'Example2'

`onSuccess`에 대한 Promise를 반환하면 mutation가 완전히 완료되기 전에 데이터가 업데이트되도록 합니다(즉, onSuccess가 충족될 때까지 isPending이 true임).

[//]: # 'Example2'

[Mutations](mutations.md)에서 사용 가능한 콜백을 사용하여 무효화가 발생하도록 연결할 수 있습니다.

[//]: # 'Materials'

## 추가 자료

Mutations 이후 Queries를 자동으로 무효화하는 기술에 대해서는 [다음 이후 자동 Query 무효화에 대한 TkDodo의 기사를 참조하십시오. Mutations](https://tkdodo.eu/blog/automatic-query-invalidation-after-mutations).

[//]: # 'Materials'
