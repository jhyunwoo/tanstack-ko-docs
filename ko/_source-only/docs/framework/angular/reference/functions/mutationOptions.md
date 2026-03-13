---
id: mutationOptions
title: mutationOptions
---




# 함수: mutationOptions()

유형이 안전한 방식으로 mutation 옵션을 공유하고 재사용할 수 있습니다.

**예**

```ts
export class QueriesService {
  private http = inject(HttpClient)
  private queryClient = inject(QueryClient)

  updatePost(id: number) {
    return mutationOptions({
      mutationFn: (post: Post) => Promise.resolve(post),
      mutationKey: ["updatePost", id],
      onSuccess: (newPost) => {
        //           ^? newPost: 게시
        this.queryClient.setQueryData(["posts", id], newPost)
      },
    });
  }
}

class ComponentOrService {
  queries = inject(QueriesService)
  id = signal(0)
  mutation = injectMutation(() => this.queries.updatePost(this.id()))

  save() {
    this.mutation.mutate({ title: 'New Title' })
  }
}
```
## 매개변수

mutation 옵션.

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): WithRequired<CreateMutationOptions<TData, TError, TVariables, TOnMutateResult>, "mutationKey">;
```
정의 위치: [mutation-options.ts:39](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/mutation-options.ts#L39)

유형이 안전한 방식으로 mutation 옵션을 공유하고 재사용할 수 있습니다.

**예**

```ts
export class QueriesService {
  private http = inject(HttpClient)
  private queryClient = inject(QueryClient)

  updatePost(id: number) {
    return mutationOptions({
      mutationFn: (post: Post) => Promise.resolve(post),
      mutationKey: ["updatePost", id],
      onSuccess: (newPost) => {
        //           ^? newPost: 게시
        this.queryClient.setQueryData(["posts", id], newPost)
      },
    });
  }
}

class ComponentOrService {
  queries = inject(QueriesService)
  id = signal(0)
  mutation = injectMutation(() => this.queries.updatePost(this.id()))

  save() {
    this.mutation.mutate({ title: 'New Title' })
  }
}
```
### 타입 매개변수

#### TData

`TData` = `unknown`

#### TError

`TError` = `Error`

#### T변수

`TVariables` = `void`

#### TOnMutateResult

`TOnMutateResult` = `unknown`

### 매개변수

#### 옵션

`WithRequired`\<[CreateMutationOptions](../interfaces/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

mutation 옵션.

### 반환값

`WithRequired`\<[CreateMutationOptions](../interfaces/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

Mutation 옵션.

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): Omit<CreateMutationOptions<TData, TError, TVariables, TOnMutateResult>, "mutationKey">;
```
정의 위치: [mutation-options.ts:53](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/mutation-options.ts#L53)

유형이 안전한 방식으로 mutation 옵션을 공유하고 재사용할 수 있습니다.

**예**

```ts
export class QueriesService {
  private http = inject(HttpClient)
  private queryClient = inject(QueryClient)

  updatePost(id: number) {
    return mutationOptions({
      mutationFn: (post: Post) => Promise.resolve(post),
      mutationKey: ["updatePost", id],
      onSuccess: (newPost) => {
        //           ^? newPost: 게시
        this.queryClient.setQueryData(["posts", id], newPost)
      },
    });
  }
}

class ComponentOrService {
  queries = inject(QueriesService)
  id = signal(0)
  mutation = injectMutation(() => this.queries.updatePost(this.id()))

  save() {
    this.mutation.mutate({ title: 'New Title' })
  }
}
```
### 타입 매개변수

#### TData

`TData` = `unknown`

#### TError

`TError` = `Error`

#### T변수

`TVariables` = `void`

#### TOnMutateResult

`TOnMutateResult` = `unknown`

### 매개변수

#### 옵션

`Omit`\<[CreateMutationOptions](../interfaces/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

mutation 옵션.

### 반환값

`Omit`\<[CreateMutationOptions](../interfaces/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

Mutation 옵션.