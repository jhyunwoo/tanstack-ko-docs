---
id: mutations
title: Mutations
---




queries와 달리 mutations는 ​​일반적으로 데이터 생성/업데이트/삭제 또는 서버 부작용을 수행하는 데 사용됩니다. 이를 위해 TanStack Query는 `useMutation` 후크를 내보냅니다.

다음은 서버에 새 할 일을 추가하는 mutation의 예입니다.



```tsx
function App() {
  const mutation = useMutation({
    mutationFn: (newTodo) => {
      return axios.post('/todos', newTodo)
    },
  })

  return (
    <div>
      {mutation.isPending ? (
        'Adding todo...'
      ) : (
        <>
          {mutation.isError ? (
            <div>An error occurred: {mutation.error.message}</div>
          ) : null}

          {mutation.isSuccess ? <div>Todo added!</div> : null}

          <button
            onClick={() => {
              mutation.mutate({ id: new Date(), title: 'Do Laundry' })
            }}
          >
            Create Todo
          </button>
        </>
      )}
    </div>
  )
}
```



mutation는 특정 순간에 다음 상태 중 하나에만 있을 수 있습니다.

- `isIdle` 또는 `status === 'idle'` - mutation는 현재 유휴 상태이거나 새로운/재설정 상태입니다.
- `isPending` 또는 `status === 'pending'` - mutation가 현재 실행 중입니다.
- `isError` 또는 `status === 'error'` - mutation에 오류가 발생했습니다.
- `isSuccess` 또는 `status === 'success'` - mutation가 성공했으며 mutation 데이터를 사용할 수 있습니다.

이러한 기본 상태 외에도 mutation의 상태에 따라 더 많은 정보를 사용할 수 있습니다.

- `error` - mutation가 `error` 상태인 경우 `error` 속성을 통해 오류를 확인할 수 있습니다.
- `data` - mutation가 `success` 상태인 경우 `data` 속성을 통해 데이터를 사용할 수 있습니다.

위의 예에서는 **단일 변수 또는 객체**로 `mutate` 함수를 호출하여 mutations 함수에 변수를 전달할 수 있다는 것도 확인했습니다.

변수만 있어도 mutations는 그다지 특별하지는 않지만, `onSuccess` 옵션과 함께 사용하면 [QueryClient](../../../reference/QueryClient.md#queryclientinvalidatequeries) 및 [QueryClient](../../../reference/QueryClient.md#queryclientsetquerydata), mutations는 매우 강력한 도구가 됩니다.






## Mutation 상태 재설정

mutation 요청의 `error` 또는 `data`를 지워야 하는 경우가 있습니다. 이를 위해 `reset` 함수를 사용하여 이를 처리할 수 있습니다.



```tsx
const CreateTodo = () => {
  const [title, setTitle] = useState('')
  const mutation = useMutation({ mutationFn: createTodo })

  const onCreateTodo = (e) => {
    e.preventDefault()
    mutation.mutate({ title })
  }

  return (
    <form onSubmit={onCreateTodo}>
      {mutation.error && (
        <h5 onClick={() => mutation.reset()}>{mutation.error}</h5>
      )}
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <br />
      <button type="submit">Create Todo</button>
    </form>
  )
}
```



## Mutation 부작용

`useMutation`에는 mutation 수명 주기 동안 모든 단계에서 빠르고 쉽게 부작용을 허용하는 몇 가지 도우미 옵션이 함께 제공됩니다. 이는 [mutations 이후 queries 무효화 및 다시 가져오기](../../react/guides/invalidations-from-mutations.md) 및 심지어 [낙관적 업데이트](../../react/guides/optimistic-updates.md)에도 유용합니다.



```tsx
useMutation({
  mutationFn: addTodo,
  onMutate: (variables, context) => {
    // mutation가 곧 발생합니다!

    // 선택적으로 롤백 등을 할 때 사용할 데이터가 포함된 결과를 반환합니다.
    return { id: 1 }
  },
  onError: (error, variables, onMutateResult, context) => {
    // 오류가 발생했습니다!
    console.log(`rolling back optimistic update with id ${onMutateResult.id}`)
  },
  onSuccess: (data, variables, onMutateResult, context) => {
    // 붐 베이비!
  },
  onSettled: (data, error, variables, onMutateResult, context) => {
    // 오류 또는 성공... 상관없습니다!
  },
})
```



콜백 함수에서 Promise를 반환할 때 다음 콜백이 호출되기 전에 먼저 기다려야 합니다.



```tsx
useMutation({
  mutationFn: addTodo,
  onSuccess: async () => {
    console.log("I'm first!")
  },
  onSettled: async () => {
    console.log("I'm second!")
  },
})
```



`mutate`를 호출할 때 `useMutation`에 정의된 것 이상으로 **추가 콜백을 트리거**하고 싶을 수도 있습니다. 이는 구성요소별 부작용을 유발하는 데 사용될 수 있습니다. 그렇게 하려면 mutation 변수 다음에 `mutate` 함수에 동일한 콜백 옵션을 제공할 수 있습니다. 지원되는 옵션에는 `onSuccess`, `onError` 및 `onSettled`가 포함됩니다. mutation가 완료되기 _전에_ 구성 요소를 마운트 해제하면 이러한 추가 콜백이 실행되지 않는다는 점을 명심하세요.



```tsx
useMutation({
  mutationFn: addTodo,
  onSuccess: (data, variables, onMutateResult, context) => {
    // 내가 먼저 발사할게
  },
  onError: (error, variables, onMutateResult, context) => {
    // 내가 먼저 발사할게
  },
  onSettled: (data, error, variables, onMutateResult, context) => {
    // 내가 먼저 발사할게
  },
})

mutate(todo, {
  onSuccess: (data, variables, onMutateResult, context) => {
    // 두 번째로 발사하겠습니다!
  },
  onError: (error, variables, onMutateResult, context) => {
    // 두 번째로 발사하겠습니다!
  },
  onSettled: (data, error, variables, onMutateResult, context) => {
    // 두 번째로 발사하겠습니다!
  },
})
```



### 연속 mutations

연속적인 mutations의 경우 `onSuccess`, `onError` 및 `onSettled` 콜백 처리에 약간의 차이가 있습니다. `mutate` 함수에 전달되면 구성 요소가 여전히 마운트되어 있는 경우에만 _한 번만_ 실행됩니다. 이는 `mutate` 함수가 호출될 때마다 mutation 관찰자가 제거되고 다시 구독된다는 사실 때문입니다. 반대로 `useMutation` 핸들러는 각 `mutate` 호출에 대해 실행됩니다.

> `useMutation`에 전달된 `mutationFn`는 비동기식일 가능성이 높습니다. 이 경우 mutations가 이행되는 순서는 `mutate` 함수 호출 순서와 다를 수 있습니다.



```tsx
useMutation({
  mutationFn: addTodo,
  onSuccess: (data, variables, onMutateResult, context) => {
    // 3번 호출됩니다
  },
})

const todos = ['Todo 1', 'Todo 2', 'Todo 3']
todos.forEach((todo) => {
  mutate(todo, {
    onSuccess: (data, variables, onMutateResult, context) => {
      // 마지막 mutation(Todo 3)에 대해 한 번만 실행됩니다.
      // 어떤 mutation가 먼저 해결되는지에 관계없이
    },
  })
})
```



## Promise

성공 시 해결되거나 오류가 발생하는 Promise을 얻으려면 `mutate` 대신 `mutateAsync`를 사용하세요. 예를 들어 이는 부작용을 구성하는 데 사용될 수 있습니다.



```tsx
const mutation = useMutation({ mutationFn: addTodo })

try {
  const todo = await mutation.mutateAsync(todo)
  console.log(todo)
} catch (error) {
  console.error(error)
} finally {
  console.log('done')
}
```



## 재시도

기본적으로 TanStack Query는 오류 시 mutation를 재시도하지 않지만 `retry` 옵션을 사용하면 가능합니다.



```tsx
const mutation = useMutation({
  mutationFn: addTodo,
  retry: 3,
})
```



장치가 오프라인이어서 mutations가 실패하는 경우 장치가 다시 연결될 때 동일한 순서로 재시도됩니다.

## 지속 mutations

필요한 경우 Mutations를 스토리지에 유지하고 나중에 다시 시작할 수 있습니다. 이는 hydration 함수를 사용하여 수행할 수 있습니다.



```tsx
const queryClient = new QueryClient()

// "addTodo" mutation를 정의합니다.
queryClient.setMutationDefaults(['addTodo'], {
  mutationFn: addTodo,
  onMutate: async (variables, context) => {
    // 할 일 목록에 대한 현재 queries 취소
    await context.client.cancelQueries({ queryKey: ['todos'] })

    // 낙관적인 할 일 만들기
    const optimisticTodo = { id: uuid(), title: variables.title }

    // 할 일 목록에 낙관적인 할 일 추가
    context.client.setQueryData(['todos'], (old) => [...old, optimisticTodo])

    // 낙관적인 할 일로 결과를 반환합니다.
    return { optimisticTodo }
  },
  onSuccess: (result, variables, onMutateResult, context) => {
    // 할 일 목록의 낙관적 할 일을 결과로 대체합니다.
    context.client.setQueryData(['todos'], (old) =>
      old.map((todo) =>
        todo.id === onMutateResult.optimisticTodo.id ? result : todo,
      ),
    )
  },
  onError: (error, variables, onMutateResult, context) => {
    // 할 일 목록에서 낙관적인 할 일을 제거하세요.
    context.client.setQueryData(['todos'], (old) =>
      old.filter((todo) => todo.id !== onMutateResult.optimisticTodo.id),
    )
  },
  retry: 3,
})

// 일부 구성 요소에서 mutation를 시작합니다.
const mutation = useMutation({ mutationKey: ['addTodo'] })
mutation.mutate({ title: 'title' })

// 예를 들어 장치가 오프라인이기 때문에 mutation가 일시 중지된 경우,
// 그런 다음 애플리케이션이 종료되면 일시 중지된 mutation가 탈수될 수 있습니다.
const state = dehydrate(queryClient)

// 그러면 애플리케이션이 시작될 때 mutation를 다시 수화할 수 있습니다.
hydrate(queryClient, state)

// 일시 중지된 mutations를 재개합니다.
queryClient.resumePausedMutations()
```




### 오프라인 유지 mutations

[persistQueryClient](../../react/plugins/persistQueryClient.md)을 사용하여 오프라인 mutations를 유지하는 경우 기본 mutation 기능을 제공하지 않으면 페이지를 다시 로드할 때 mutations를 재개할 수 없습니다.



이는 기술적 한계입니다. 외부 저장소에 지속되면 함수를 직렬화할 수 없으므로 mutations의 상태만 지속됩니다. hydration 이후에는 mutation를 트리거하는 구성요소가 마운트되지 않을 수 있으므로 `resumePausedMutations`를 호출하면 `No mutationFn found` 오류가 발생할 수 있습니다.



```tsx
const persister = createSyncStoragePersister({
  storage: window.localStorage,
})
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24시간
    },
  },
})

// 일시 중지된 mutations가 페이지를 다시 로드한 후 다시 시작할 수 있도록 기본 mutation 함수가 필요합니다.
queryClient.setMutationDefaults(['todos'], {
  mutationFn: ({ id, data }) => {
    return api.updateTodo(id, data)
  },
})

export default function App() {
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{ persister }}
      onSuccess={() => {
        // localStorage에서 초기 복원이 성공한 후 mutations를 재개합니다.
        queryClient.resumePausedMutations()
      }}
    >
      <RestOfTheApp />
    </PersistQueryClientProvider>
  )
}
```




또한 queries 및 mutations를 모두 다루는 광범위한 [오프라인 예시](../../react/examples/offline.md)도 있습니다.



## Mutation 스코프

기본적으로 동일한 mutation의 `.mutate()`를 여러 번 호출하더라도 모든 mutations는 ​​병렬로 실행됩니다. 이를 방지하기 위해 Mutations에 `id`와 함께 `scope`를 제공할 수 있습니다. 동일한 `scope.id`가 있는 모든 mutations는 ​​직렬로 실행됩니다. 즉, 해당 범위에 대해 진행 중인 mutation가 이미 있는 경우 트리거될 때 `isPaused: true` 상태에서 시작됩니다. 그들은 대기열에 들어가게 되며 대기열에 있는 시간이 지나면 자동으로 재개됩니다.



```tsx
const mutation = useMutation({
  mutationFn: addTodo,
  scope: {
    id: 'todo',
  },
})
```




## 추가 자료

mutations에 대한 자세한 내용은 [Preact Query에서 Mutations 마스터링에 대한 TkDodo의 기사](https://tkdodo.eu/blog/mastering-mutations-in-preact-query)를 참조하세요.
