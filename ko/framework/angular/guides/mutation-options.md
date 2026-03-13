---
id: query-options
title: Mutation 옵션
---




여러 장소 간에 mutation 옵션을 공유하는 가장 좋은 방법 중 하나는
`mutationOptions` 도우미를 사용하는 것입니다. 런타임 시 이 도우미는 전달된 내용을 모두 반환합니다.
하지만 [TypeScript](../typescript.md#typing-query-options) 사용할 때 많은 장점이 있습니다.
mutation에 대해 가능한 모든 옵션을 한 곳에서 정의할 수 있습니다.
또한 모든 항목에 대한 유형 추론 및 유형 안전성도 얻을 수 있습니다.

```ts
export class QueriesService {
  private http = inject(HttpClient)

  updatePost(id: number) {
    return mutationOptions({
      mutationFn: (post: Post) => Promise.resolve(post),
      mutationKey: ['updatePost', id],
      onSuccess: (newPost) => {
        //           ^? newPost: 게시
        this.queryClient.setQueryData(['posts', id], newPost)
      },
    })
  }
}
```
