---
id: quick-start
title: 빠른 시작
---




> 중요: 이 라이브러리는 현재 실험 단계에 있습니다. 즉, 마이너 AND 패치 릴리스에서 주요 변경 사항이 발생합니다. 신중하게 업그레이드하세요. 실험 단계에 있는 프로덕션에서 이 기능을 사용하는 경우 예상치 못한 주요 변경을 방지하기 위해 버전을 패치 수준 버전으로 잠그십시오.

[//]: # 'Example'

완벽하게 작동하는 예제를 찾고 있다면 [기본 코드샌드박스 예제](examples/basic.md)를 살펴보세요.

### 앱에 클라이언트 제공

```ts
import { provideHttpClient } from '@angular/common/http'
import {
  provideTanStackQuery,
  QueryClient,
} from '@tanstack/angular-query-experimental'

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient(), provideTanStackQuery(new QueryClient())],
})
```
또는 NgModule 기반 앱에서

```ts
import { provideHttpClient } from '@angular/common/http'
import {
  provideTanStackQuery,
  QueryClient,
} from '@tanstack/angular-query-experimental'

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule],
  providers: [provideTanStackQuery(new QueryClient())],
  bootstrap: [AppComponent],
})
export class AppModule {}
```
### query 및 mutation가 포함된 구성 요소

```angular-ts
import { Component, Injectable, inject } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { lastValueFrom } from 'rxjs'

import {
  injectMutation,
  injectQuery,
  QueryClient,
} from '@tanstack/angular-query-experimental'

@Component({
  template: `
    <div>
      <button (click)="onAddTodo()">Add Todo</button>

      <ul>
        @for (todo of query.data(); track todo.title) {
          <li>{{ todo.title }}</li>
        }
      </ul>
    </div>
  `,
})
export class TodosComponent {
  todoService = inject(TodoService)
  queryClient = inject(QueryClient)

  query = injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: () => this.todoService.getTodos(),
  }))

  mutation = injectMutation(() => ({
    mutationFn: (todo: Todo) => this.todoService.addTodo(todo),
    onSuccess: () => {
      this.queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  }))

  onAddTodo() {
    this.mutation.mutate({
      id: Date.now().toString(),
      title: 'Do Laundry',
    })
  }
}

@Injectable({ providedIn: 'root' })
export class TodoService {
  private http = inject(HttpClient)

  getTodos(): Promise<Todo[]> {
    return lastValueFrom(
      this.http.get<Todo[]>('https://jsonplaceholder.typicode.com/todos'),
    )
  }

  addTodo(todo: Todo): Promise<Todo> {
    return lastValueFrom(
      this.http.post<Todo>('https://jsonplaceholder.typicode.com/todos', todo),
    )
  }
}

interface Todo {
  id: string
  title: string
}
```
[//]: # 'Example'
