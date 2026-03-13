---
id: background-fetching-indicators
title: 배경 가져오기 표시기
---




query의 `status === 'pending'` 상태는 query의 초기 하드 로딩 상태를 표시하기에 충분하지만 때로는 query가 백그라운드에서 다시 가져오고 있다는 추가 표시기를 표시할 수도 있습니다. 이를 위해 queries는 `status` 변수의 상태에 관계없이 가져오기 상태에 있음을 표시하는 데 사용할 수 있는 `isFetching` boolean도 제공합니다.



```angular-ts
@Component({
  selector: 'todos',
  template: `
    @if (todosQuery.isPending()) {
      Loading...
    } @else if (todosQuery.isError()) {
      An error has occurred: {{ todosQuery.error().message }}
    } @else if (todosQuery.isSuccess()) {
      @if (todosQuery.isFetching()) {
        Refreshing...
      }
      @for (todos of todosQuery.data(); track todo.id) {
        <todo [todo]="todo" />
      }
    }
  `,
})
class TodosComponent {
  todosQuery = injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  }))
}
```



## 전역 배경 가져오기 로드 상태 표시

개별 query 로딩 상태 외에도 **모든** queries를 가져올 때(백그라운드 포함) 전역 로딩 표시기를 표시하려면 `injectIsFetching` 함수를 사용할 수 있습니다.



```angular-ts
import { injectIsFetching } from '@tanstack/angular-query-experimental'

@Component({
  selector: 'global-loading-indicator',
  template: `
    @if (isFetching()) {
      <div>Queries are fetching in the background...</div>
    }
  `,
})
export class GlobalLoadingIndicatorComponent {
  isFetching = injectIsFetching()
}
```


