---
id: queries
title: Queries
---




## Query 기본 사항

query는 **고유 키**에 연결된 비동기 데이터 소스에 대한 선언적 종속성입니다. query는 Promise 기반 방법(GET 및 POST 방법 포함)과 함께 사용하여 서버에서 데이터를 가져올 수 있습니다. 귀하의 방법이 서버의 데이터를 수정하는 경우 [Mutations](../../react/guides/mutations.md)를 대신 사용하는 것이 좋습니다.



구성 요소 또는 서비스에서 query를 구독하려면 최소한 다음을 사용하여 `injectQuery`를 호출하세요.



- **query용 고유 키**
- 다음과 같은 Promise이나 관찰 가능 항목을 반환하는 함수:
  - 데이터를 해결하거나
  - 오류가 발생합니다.



```ts
import { injectQuery } from '@tanstack/angular-query-experimental'

export class TodosComponent {
  info = injectQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodoList }))
}
```



귀하가 제공하는 **고유 키**는 애플리케이션 전체에서 queries를 다시 가져오고, 캐싱하고, 공유하는 데 내부적으로 사용됩니다.

`injectQuery`에서 반환된 query 결과에는 템플릿 작성 및 기타 데이터 사용에 필요한 query에 대한 모든 정보가 포함되어 있습니다.



```ts
result = injectQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodoList }))
```



`result` 객체에는 생산성을 높이기 위해 알아야 할 몇 가지 매우 중요한 상태가 포함되어 있습니다. query는 특정 순간에 다음 상태 중 하나에만 있을 수 있습니다.

- `isPending` 또는 `status === 'pending'` - query에는 아직 데이터가 없습니다.
- `isError` 또는 `status === 'error'` - query에 오류가 발생했습니다.
- `isSuccess` 또는 `status === 'success'` - query가 성공했으며 데이터를 사용할 수 있습니다.

이러한 기본 상태 외에도 query의 상태에 따라 더 많은 정보를 사용할 수 있습니다.

- `error` - query가 `isError` 상태인 경우 `error` 속성을 통해 오류를 확인할 수 있습니다.
- `data` - query가 `isSuccess` 상태인 경우 `data` 속성을 통해 데이터를 사용할 수 있습니다.
- `isFetching` - 어떤 상태에서든 query가 언제든지 가져오는 경우(백그라운드 다시 가져오기 포함) `isFetching`는 ​​`true`가 됩니다.

**대부분** queries의 경우 일반적으로 `isPending` 상태를 확인한 다음 `isError` 상태를 확인한 다음 마지막으로 데이터가 사용 가능하다고 가정하고 성공적인 상태를 렌더링하는 것으로 충분합니다.



```angular-ts
@Component({
  selector: 'todos',
  template: `
    @if (todos.isPending()) {
      <span>Loading...</span>
    } @else if (todos.isError()) {
      <span>Error: {{ todos.error()?.message }}</span>
    } @else {
      <!-- 이 시점에서 상태 === '성공'이라고 가정할 수 있습니다. -->
      @for (todo of todos.data(); track todo.id) {
        <li>{{ todo.title }}</li>
      } @empty {
        <li>No todos found</li>
      }
    }
  `,
})
export class PostsComponent {
  todos = injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodoList,
  }))
}
```



boolean이 마음에 들지 않으면 언제든지 `status` 상태를 사용할 수도 있습니다.



```angular-ts
@Component({
  selector: 'todos',
  template: `
    @switch (todos.status()) {
      @case ('pending') {
        <span>Loading...</span>
      }
      @case ('error') {
        <span>Error: {{ todos.error()?.message }}</span>
      }
      <!-- status === '성공'도 있지만 "else" 논리도 작동합니다. -->
      @default {
        <ul>
          @for (todo of todos.data(); track todo.id) {
            <li>{{ todo.title }}</li>
          } @empty {
            <li>No todos found</li>
          }
        </ul>
      }
    }
  `,
})
class TodosComponent {}
```



또한 TypeScript는 `data`에 액세스하기 전에 `pending` 및 `error`를 확인한 경우 `data` 유형을 올바르게 좁힙니다.

### FetchStatus

`status` 필드 외에도 다음 옵션을 사용하여 추가 `fetchStatus` 속성도 얻을 수 있습니다.

- `fetchStatus === 'fetching'` - 현재 query를 가져오는 중입니다.
- `fetchStatus === 'paused'` - query를 가져오려고 했으나 일시 중지되었습니다. 이에 대한 자세한 내용은 [네트워크 모드](../../react/guides/network-mode.md) 가이드를 참조하세요.
- `fetchStatus === 'idle'` - query는 현재 아무 작업도 수행하지 않습니다.

### 왜 두 가지 상태가 다른가요?

백그라운드 다시 가져오기 및 재검증 중 오래된 논리를 통해 `status` 및 `fetchStatus`에 대한 모든 조합이 가능해졌습니다. 예를 들어:

- `success` 상태의 query는 일반적으로 `idle` fetchStatus에 있지만 백그라운드 다시 가져오기가 발생하는 경우 `fetching`에 있을 수도 있습니다.
- 마운트되었지만 데이터가 없는 query는 일반적으로 `pending` 상태 및 `fetching` fetchStatus에 있지만 네트워크 연결이 없는 경우 `paused`일 수도 있습니다.

따라서 query는 실제로 데이터를 가져오지 않고도 `pending` 상태에 있을 수 있다는 점을 명심하세요. 경험상 다음과 같습니다.

- `status`는 `data`에 대한 정보를 제공합니다. 어떤 것이 있습니까?
- `fetchStatus`는 `queryFn`에 대한 정보를 제공합니다. 실행 중입니까?



