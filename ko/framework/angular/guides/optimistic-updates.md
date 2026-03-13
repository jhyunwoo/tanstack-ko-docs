---
id: optimistic-updates
title: 낙관적인 업데이트
---




Angular Query는 mutation가 완료되기 전에 UI를 낙관적으로 업데이트하는 두 가지 방법을 제공합니다. `onMutate` 옵션을 사용하여 캐시를 직접 업데이트하거나 반환된 `variables`를 활용하여 `injectMutation` 결과에서 UI를 업데이트할 수 있습니다.

## UI를 통해

이는 캐시와 직접 상호 작용하지 않으므로 더 간단한 변형입니다.



```ts
addTodo = injectMutation(() => ({
  mutationFn: (newTodo: string) => axios.post('/api/data', { text: newTodo }),
  // query 무효화로 인한 Promise을 _반환_해야 합니다.
  // 다시 가져오기가 완료될 때까지 mutation가 '보류 중' 상태로 유지됩니다.
  onSettled: async () => {
    return await queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
}))
```



그러면 추가된 할 일이 포함된 `addTodo.variables`에 액세스할 수 있습니다. query가 렌더링되는 UI 목록에서 mutation `isPending`가 다음과 같이 목록에 다른 항목을 추가할 수 있습니다.



```angular-ts
@Component({
  template: `
    @for (todo of todos.data(); track todo.id) {
      <li>{{ todo.title }}</li>
    }
    @if (addTodo.isPending()) {
      <li style="opacity: 0.5">{{ addTodo.variables() }}</li>
    }
  `,
})
class TodosComponent {}
```



mutation가 보류 중인 동안 다른 `opacity`를 사용하여 임시 항목을 렌더링하고 있습니다. 완료되면 항목이 더 이상 자동으로 렌더링되지 않습니다. 다시 가져오기가 성공했다면 해당 항목이 목록에 "일반 항목"으로 표시되어야 합니다.

mutation 오류가 발생하면 해당 항목도 사라집니다. 그러나 원하는 경우 mutation의 `isError` 상태를 확인하여 계속해서 표시할 수 있습니다. `variables`는 mutation 오류가 발생해도 지워지지 _않으므로_ 계속 액세스할 수 있으며 재시도 버튼을 표시할 수도 있습니다.



```angular-ts
@Component({
  template: `
    @if (addTodo.isError()) {
      <li style="color: red">
        {{ addTodo.variables() }}
        <button (click)="addTodo.mutate(addTodo.variables())">Retry</button>
      </li>
    }
  `,
})
class TodosComponent {}
```



### mutation와 query가 동일한 구성 요소에 있지 않은 경우

이 접근 방식은 mutation와 query가 동일한 구성 요소에 있는 경우 매우 효과적입니다. 그러나 전용 `injectMutationState` 기능을 통해 다른 구성 요소의 모든 mutations에도 액세스할 수 있습니다. `mutationKey`와 가장 잘 결합됩니다.



```ts
// 앱 어딘가에
addTodo = injectMutation(() => ({
  mutationFn: (newTodo: string) => axios.post('/api/data', { text: newTodo }),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  mutationKey: ['addTodo'],
}))

// 다른 곳에서 변수에 액세스

mutationState = injectMutationState<string>(() => ({
  filters: { mutationKey: ['addTodo'], status: 'pending' },
  select: (mutation) => mutation.state.variables,
}))
```



동시에 여러 개의 mutations가 실행될 수 있으므로 `variables`는 `Array`가 됩니다. 항목에 대한 고유 키가 필요한 경우 `mutation.state.submittedAt`를 선택할 수도 있습니다. 이렇게 하면 동시에 낙관적인 업데이트를 쉽게 표시할 수도 있습니다.

## 캐시를 통해

mutation를 수행하기 전에 낙관적으로 상태를 업데이트하면 mutation가 실패할 가능성이 있습니다. 이러한 실패 사례의 대부분에서는 낙관적인 queries에 대한 다시 가져오기를 트리거하여 실제 서버 상태로 되돌릴 수 있습니다. 그러나 일부 상황에서는 다시 가져오기가 올바르게 작동하지 않을 수 있으며 mutation 오류는 다시 가져오기를 불가능하게 하는 일부 유형의 서버 문제를 나타낼 수 있습니다. 이 경우 대신 업데이트를 롤백하도록 선택할 수 있습니다.

이를 위해 `injectMutation`의 `onMutate` 핸들러 옵션을 사용하면 나중에 `onError` 및 `onSettled` 핸들러 모두에 마지막 인수로 전달될 값을 반환할 수 있습니다. 대부분의 경우 롤백 기능을 전달하는 것이 가장 유용합니다.

### 새 할 일 추가 시 할 일 목록 업데이트



```ts
queryClient = inject(QueryClient)

updateTodo = injectMutation(() => ({
  mutationFn: updateTodo,
  // mutate가 호출되는 경우:
  onMutate: async (newTodo, context) => {
    // 나가는 다시 가져오기 취소
    // (그래서 그들은 우리의 낙관적 업데이트를 덮어쓰지 않습니다)
    await context.client.cancelQueries({ queryKey: ['todos'] })

    // 이전 값의 스냅샷
    const previousTodos = context.client.getQueryData(['todos'])

    // 낙관적으로 새 값으로 업데이트
    context.client.setQueryData(['todos'], (old) => [...old, newTodo])

    // 스냅샷된 값으로 결과 객체를 반환합니다.
    return { previousTodos }
  },
  // mutation가 실패하는 경우,
  // onMutate에서 반환된 결과를 사용하여 롤백
  onError: (err, newTodo, onMutateResult, context) => {
    context.client.setQueryData(['todos'], onMutateResult.previousTodos)
  },
  // 오류나 성공 후에는 항상 다시 가져옵니다.
  onSettled: (data, error, variables, onMutateResult, context) => {
    context.client.invalidateQueries({ queryKey: ['todos'] })
  },
}))
```



### 단일 할일 업데이트



```ts
queryClient = inject(QueryClient)

updateTodo = injectMutation(() => ({
  mutationFn: updateTodo,
  // mutate가 호출되는 경우:
  onMutate: async (newTodo, context) => {
    // 나가는 다시 가져오기 취소
    // (그래서 그들은 우리의 낙관적 업데이트를 덮어쓰지 않습니다)
    await context.client.cancelQueries({ queryKey: ['todos', newTodo.id] })

    // 이전 값의 스냅샷
    const previousTodo = context.client.getQueryData(['todos', newTodo.id])

    // 낙관적으로 새 값으로 업데이트
    context.client.setQueryData(['todos', newTodo.id], newTodo)

    // 이전 할 일과 새 할 일을 포함하여 결과를 반환합니다.
    return { previousTodo, newTodo }
  },
  // mutation가 실패하면 위에서 반환한 결과를 사용하세요.
  onError: (err, newTodo, onMutateResult, context) => {
    context.client.setQueryData(
      ['todos', onMutateResult.newTodo.id],
      onMutateResult.previousTodo,
    )
  },
  // 오류나 성공 후에는 항상 다시 가져옵니다.
  onSettled: (newTodo, error, variables, onMutateResult, context) => {
    context.client.invalidateQueries({ queryKey: ['todos', newTodo.id] })
  },
}))
```



원하는 경우 별도의 `onError` 및 `onSuccess` 핸들러 대신 `onSettled` 기능을 사용할 수도 있습니다.



```ts
injectMutation({
  mutationFn: updateTodo,
  // ...
  onSettled: (newTodo, error, variables, onMutateResult, context) => {
    if (error) {
      // 뭔가를 해라
    }
  },
})
```



## 언제 무엇을 사용할 것인가

낙관적인 결과를 표시해야 하는 위치가 하나만 있는 경우 `variables`를 사용하고 UI를 직접 업데이트하는 것이 코드가 덜 필요하고 일반적으로 추론하기 더 쉬운 접근 방식입니다. 예를 들어 롤백을 전혀 처리할 필요가 없습니다.

그러나 화면에 업데이트에 대해 알아야 할 여러 위치가 있는 경우 캐시를 직접 조작하면 이 작업이 자동으로 처리됩니다.



## 추가 자료

[동시 낙관적 업데이트](https://tkdodo.eu/blog/concurrent-optimistic-updates-in-react-query)에 대한 TkDodo의 가이드를 살펴보세요.


