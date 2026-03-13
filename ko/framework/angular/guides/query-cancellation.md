---
id: query-cancellation
title: Query 취소
---




TanStack Query는 [`AbortSignal` 인스턴스](https://developer.mozilla.org/docs/Web/API/AbortSignal)와 함께 각 query 함수를 제공합니다. query가 오래되거나 비활성화되면 이 `signal`가 중단됩니다. 이는 모든 queries를 취소할 수 있으며 원하는 경우 query 함수 내에서 취소에 응답할 수 있음을 의미합니다. 가장 좋은 점은 자동 취소의 모든 이점을 얻으면서 일반 async/await 구문을 계속 사용할 수 있다는 것입니다.

## 기본 동작

기본적으로 Promise이 해결되기 전에 마운트 해제되거나 사용되지 않는 queries는 취소되지 _않습니다_. 이는 Promise가 해결된 후 결과 데이터를 캐시에서 사용할 수 있음을 의미합니다. 이는 query 수신을 시작했지만 완료되기 전에 구성요소를 마운트 해제한 경우에 유용합니다. 구성 요소를 다시 마운트하고 query가 아직 가비지 수집되지 않은 경우 데이터를 사용할 수 있습니다.

그러나 `AbortSignal`를 사용하면 Promise가 취소되므로(예: 가져오기 중단) Query도 취소해야 합니다. query를 취소하면 상태가 이전 상태로 _복귀_됩니다.

## `HttpClient` 사용하기

```ts
import { HttpClient } from '@angular/common/http'
import { injectQuery } from '@tanstack/angular-query-experimental'

postQuery = injectQuery(() => ({
  enabled: this.postId() > 0,
  queryKey: ['post', this.postId()],
  queryFn: async (context): Promise<Post> => {
    const abort$ = fromEvent(context.signal, 'abort')
    return lastValueFrom(this.getPost$(this.postId()).pipe(takeUntil(abort$)))
  },
}))
```
## `fetch` 사용하기

[//]: # 'Example2'

```ts
query = injectQuery(() => ({
  queryKey: ['todos'],
  queryFn: async ({ signal }) => {
    const todosResponse = await fetch('/todos', {
      // 신호를 원 페치로 전달
      signal,
    })
    const todos = await todosResponse.json()

    const todoDetails = todos.map(async ({ details }) => {
      const response = await fetch(details, {
        // 아니면 여러 사람에게 전달하세요.
        signal,
      })
      return response.json()
    })

    return Promise.all(todoDetails)
  },
}))
```
[//]: # 'Example2'

## `axios` 사용하기

[//]: # 'Example3'

```ts
import axios from 'axios'

const query = injectQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) =>
    axios.get('/todos', {
      // 'axios'에 신호 전달
      signal,
    }),
}))
```
[//]: # 'Example3'

## 수동 취소

query를 수동으로 취소할 수도 있습니다. 예를 들어 요청을 완료하는 데 오랜 시간이 걸리는 경우 사용자가 취소 버튼을 클릭하여 요청을 중지하도록 허용할 수 있습니다. 이렇게 하려면 `queryClient.cancelQueries({ queryKey })`를 호출하면 됩니다. 그러면 query가 취소되고 이전 상태로 되돌아갑니다. query 함수에 전달된 `signal`를 소비한 경우 TanStack Query도 Promise를 추가로 취소합니다.

[//]: # 'Example7'

```angular-ts
@Component({
  template: `<button (click)="onCancel()">Cancel</button>`,
})
export class TodosComponent {
  query = injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: async ({ signal }) => {
      const resp = await fetch('/todos', { signal })
      return resp.json()
    },
  }))

  queryClient = inject(QueryClient)

  onCancel() {
    this.queryClient.cancelQueries(['todos'])
  }
}
```
[//]: # 'Example7'
