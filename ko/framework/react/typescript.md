---
id: typescript
title: TypeScript
---




React Query는 이제 **TypeScript**로 작성되어 라이브러리와 프로젝트가 유형에 안전한지 확인합니다!

명심해야 할 사항:

- TanStack Query는 [DefinitelyTyped 지원 창](https://github.com/DefinitelyTyped/DefinitelyTyped#support-window)을 따르며 최근 2년 이내에 출시된 TypeScript 버전을 지원합니다. 현재 이는 TypeScript **5.4** 이상을 의미합니다.
- 이 저장소의 유형에 대한 변경 사항은 **비해킹**으로 간주되며 일반적으로 **패치** semver 변경으로 릴리스됩니다(그렇지 않으면 모든 유형 향상이 주요 버전이 됩니다!).
- **react-query 패키지 버전을 특정 패치 릴리스로 잠그고 모든 릴리스 간에 유형이 수정되거나 업그레이드될 수 있다는 예상으로 업그레이드하는 것이 좋습니다**
- React Query의 유형과 관련되지 않은 공개 API는 여전히 semver를 매우 엄격하게 따릅니다.

## 유형 추론

React Query의 유형은 일반적으로 매우 잘 흐르므로 직접 유형 주석을 제공할 필요가 없습니다.

[//]: # 'TypeInference1'

```tsx
const { data } = useQuery({
  //    ^? const 데이터: 숫자 | 한정되지 않은
  queryKey: ['test'],
  queryFn: () => Promise.resolve(5),
})
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZlBCHAORToCGAxjALQC OO+VAsAFC8MQAdqnhIAJnRh0icALwoM2XHgAUAbSqDkIAEa4qAXQA0cFQEo5APjgAFciGAYAdLVQQANgDd0KgKxmzXgB6ILgw8IA9AH5eIA)

[//]: # 'TypeInference1'
[//]: # 'TypeInference2'

```tsx
const { data } = useQuery({
  //      ^? const 데이터: 문자열 | 한정되지 않은
  queryKey: ['test'],
  queryFn: () => Promise.resolve(5),
  select: (data) => data.toString(),
})
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZlBCHAORToCGAxjALQCOO+VAsAFC8MQAdqn hIAJnRh0icALwoM2XHgAUAbSox0IqgF0ANHBUBKOQD44ABXIhgGAHS1UEADYA3dCoCsxw0gwu6EwAXHASUuZhknT2MBAAyjBQwIIA5iaExrwA9Nlw+QUAegD8vEA)

[//]: # 'TypeInference2'

이는 `queryFn`에 잘 정의된 반환 유형이 있는 경우 가장 잘 작동합니다. 대부분의 데이터 가져오기 라이브러리는 기본적으로 `any`를 반환하므로 올바른 유형의 함수로 추출해야 합니다.

[//]: # 'TypeInference3'

```tsx
const fetchGroups = (): Promise<Group[]> =>
  axios.get('/groups').then((response) => response.data)

const { data } = useQuery({ queryKey: ['groups'], queryFn: fetchGroups })
//      ^? const 데이터: 그룹[] | 한정되지 않은
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZ lbCHAORToCGAxjALQCOO+VAsAFCiSw4dAB7AIquuUpURY1Nx68YeMOjgBxcsjBwAvIjjAAJgC44AO2QgARriK9eDCOd TwS6GawAWmiNon6ABQAlGYAClLAGAA8vtoA2gC6AHx6qbLiAHQA5h6BVAD02Vpg8sGZMF7o5oG0qJAuarqpdQ0YmUZ0 MHTBDjxOLvBInd1EeigY2Lh4gfFUxX6lVIkanKQe3nGlvTwFBXAHhwB6APxwA65wI3RmW0lwAD4o5kboJMDm6Ea8QA)

[//]: # 'TypeInference3'

## 유형 축소

React Query는 `status` 필드와 파생된 상태 boolean 플래그로 구별되는 query 결과에 대해 [차별화된 공용체 유형](https://www.typescriptlang.org/docs/handbook/typescript-in-5- Minutes-func.html#차별화된-unions)을 사용합니다. 이를 통해 예를 들어 확인할 수 있습니다. `data`를 정의하기 위한 `success` 상태:

[//]: # 'TypeNarrowing'

```tsx
const { data, isSuccess } = useQuery({
  queryKey: ['test'],
  queryFn: () => Promise.resolve(5),
})

if (isSuccess) {
  data
  //  ^? const 데이터: 숫자
}
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZlBCHAORToCGAxjALQCOO+VAsAFC8MQAdqnhI AJnRh0ANHGCoAysgYN0qVETgBeFBmy48ACgDaVGGphUAurMMBKbQD44ABXIh56AHS1UEADYAbuiGAKx2dry8wCRwhvJKKmqoDgi8cBlwElK8APS5GQB6APy8hLxAA)

[//]: # 'TypeNarrowing'

## 오류 필드 입력

오류 유형은 대부분의 사용자가 기대하는 `Error`로 기본 설정됩니다.

[//]: # 'TypingError'

```tsx
const { error } = useQuery({ queryKey: ['groups'], queryFn: fetchGroups })
//      ^? const 오류: 오류
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZlBCHAOQACMAhgHaoMDGA1gPRTr2swBaAI458VALAAoUJFhx6AD2ARUpcpSqLlqCZKkw8YdHADi5ZGDgBeRH GAATAFxxGyEACNcRKVNYRm8CToMKwAFmYQFqo2ABQAlM4ACurAGAA8ERYA2gC6AHzWBVoqAHQA5sExVJxl5mA6 cSUwoeiMMTyokMzGVgUdXRgl9vQMcT6SfgG2uORQRNYoGNi4eDFZVLWR9VQ5ADSkwWGZ9WOSnJxwl1cAegD8QA)

[//]: # 'TypingError'

사용자 정의 오류나 `Error`가 아닌 오류를 발생시키려는 경우 오류 필드의 유형을 지정할 수 있습니다.

[//]: # 'TypingError2'

```tsx
const { error } = useQuery<Group[], string>(['groups'], fetchGroups)
//      ^? const 오류: 문자열 | null
```
[//]: # 'TypingError2'

그러나 이는 `useQuery`의 다른 모든 제네릭에 대한 유형 추론이 더 이상 작동하지 않는다는 단점이 있습니다. 일반적으로 `Error`가 아닌 것을 던지는 것은 좋은 습관으로 간주되지 않습니다. 따라서 `AxiosError`와 같은 하위 클래스가 있는 경우 _유형 축소_를 사용하여 오류 필드를 더 구체적으로 만들 수 있습니다.

[//]: # 'TypingError3'

```tsx
import axios from 'axios'

const { error } = useQuery({ queryKey: ['groups'], queryFn: fetchGroups })
//      ^? const 오류: 오류 | null

if (axios.isAxiosError(error)) {
  error
  // ^? const 오류: AxiosError
}
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAbzgVwM4FMCKz1QJ5wC+cAZlBCHAOQACMAhgH aoMDGA1gPRTr2swBaAI458VALAAoUJFhx6AD2ARUpcpSqLlqCZKkw8YdHADi5ZGDgBeRHGAATAFxxGyEACNcRKVNYRm8CToMKwAFmYQFq o2ABQAlM4ACurAGAA8ERYA2gC6AHzWBVoqAHQA5sExVJxl5mA6cSUwoeiMMTyokMzGVgUdXRgl9vQMcT6SfgG2uORQRNYoGNi4eDFIIi sa0uh4zllUtZH1VDkANHAb+ABijM5BieF1qoRjkpyccJ9fAHoA-OPAEhwGLFVAlVIAQSUKgAolBZjEZtA4nFEFJPkioOi4O84H8pIQgA)

[//]: # 'TypingError3'

### 전역 오류 등록

TanStack Query v5에서는 `Register` 인터페이스를 수정하여 호출 측에서 제네릭을 지정할 필요 없이 모든 것에 대해 전역 오류 유형을 설정할 수 있는 방법을 허용합니다. 이렇게 하면 추론이 계속 작동하지만 오류 필드는 지정된 유형이 됩니다. 호출 측에서 명시적인 유형 축소를 수행해야 하도록 하려면 `defaultError`를 `unknown`로 설정합니다.

[//]: # 'RegisterErrorType'

```tsx
import '@tanstack/react-query'

declare module '@tanstack/react-query' {
  interface Register {
    // 알 수 없음을 사용하면 호출 사이트가 명시적으로 범위를 좁혀야 합니다.
    defaultError: unknown
  }
}

const { error } = useQuery({ queryKey: ['groups'], queryFn: fetchGroups })
//      ^? const 오류: 알 수 없음 | null
```
[//]: # 'RegisterErrorType'
[//]: # 'TypingMeta'

## 메타 입력 중

### 글로벌 메타 등록 중

[전역 오류 유형](#registering-a-global-error)을 등록하는 것과 마찬가지로 전역 `Meta` 유형을 등록할 수도 있습니다. 이렇게 하면 [useQuery](reference/useQuery.md) 및 [useMutation](reference/useMutation.md)의 선택적 `meta` 필드가 일관성을 유지하고 유형이 안전해집니다. 등록된 유형은 `meta`가 객체로 유지되도록 `Record<string, unknown>`를 확장해야 합니다.

```ts
import '@tanstack/react-query'

interface MyMeta extends Record<string, unknown> {
  // 메타 유형 정의.
}

declare module '@tanstack/react-query' {
  interface Register {
    queryMeta: MyMeta
    mutationMeta: MyMeta
  }
}
```
[//]: # 'TypingMeta'
[//]: # 'TypingQueryAndMutationKeys'

## query 및 mutation 키 입력

### query 및 mutation 키 유형 등록

또한 [전역 오류 유형](#registering-a-global-error)을 등록하는 것과 유사하게 전역 `QueryKey` 및 `MutationKey` 유형을 등록할 수도 있습니다. 이를 통해 애플리케이션의 계층 구조와 일치하는 키에 더 많은 구조를 제공하고 라이브러리의 전체 표면에 키를 입력할 수 있습니다. 등록된 유형은 `Array` 유형을 확장해야 키가 배열로 유지됩니다.

```ts
import '@tanstack/react-query'

type QueryKey = ['dashboard' | 'marketing', ...ReadonlyArray<unknown>]

declare module '@tanstack/react-query' {
  interface Register {
    queryKey: QueryKey
    mutationKey: QueryKey
  }
}
```
[//]: # 'TypingQueryAndMutationKeys'
[//]: # 'TypingQueryOptions'

## Query 옵션 입력

query 옵션을 `useQuery`에 인라인하면 자동 유형 추론이 수행됩니다. 그러나 query 옵션을 별도의 함수로 추출하여 `useQuery`와 예를 들어 다음과 같이 공유할 수 있습니다. `prefetchQuery`. 이 경우 유형 추론이 손실됩니다. 다시 가져오려면 `queryOptions` 도우미를 사용할 수 있습니다.

```ts
import { queryOptions } from '@tanstack/react-query'

function groupOptions() {
  return queryOptions({
    queryKey: ['groups'],
    queryFn: fetchGroups,
    staleTime: 5 * 1000,
  })
}

useQuery(groupOptions())
queryClient.prefetchQuery(groupOptions())
```
또한 `queryOptions`에서 반환된 `queryKey`는 이와 관련된 `queryFn`에 대해 알고 있으며 해당 유형 정보를 활용하여 `queryClient.getQueryData`와 같은 함수도 해당 유형을 인식하도록 할 수 있습니다.

```ts
function groupOptions() {
  return queryOptions({
    queryKey: ['groups'],
    queryFn: fetchGroups,
    staleTime: 5 * 1000,
  })
}

const data = queryClient.getQueryData(groupOptions().queryKey)
//     ^? const 데이터: 그룹[] | 한정되지 않은
```
`queryOptions`가 없으면 일반을 전달하지 않는 한 `data` 유형은 `unknown`가 됩니다.

```ts
const data = queryClient.getQueryData<Group[]>(['groups'])
```
`queryOptions`를 통한 유형 추론은 `queryClient.getQueriesData`에 대해 작동하지 _않습니다_. 이는 이질적인 `unknown` 데이터가 포함된 튜플 배열을 반환하기 때문입니다. query가 반환할 데이터 유형을 확신하는 경우 명시적으로 지정하세요.

```ts
const entries = queryClient.getQueriesData<Group[]>(groupOptions().queryKey)
//     ^? const 항목: Array<[QueryKey, Group[] | 정의되지 않음]>
```
## Mutation 옵션 입력

`queryOptions`와 마찬가지로 `mutationOptions`를 사용하여 mutation 옵션을 별도의 함수로 추출할 수 있습니다.

```ts
function groupMutationOptions() {
  return mutationOptions({
    mutationKey: ['addGroup'],
    mutationFn: addGroup,
  })
}

useMutation({
  ...groupMutationOptions(),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['groups'] }),
})
useIsMutating(groupMutationOptions())
queryClient.isMutating(groupMutationOptions())
```
[//]: # 'TypingQueryOptions'

## `skipToken`를 사용하여 queries의 형식 안전 비활성화

TypeScript를 사용하는 경우 `skipToken`를 사용하여 query를 비활성화할 수 있습니다. 이는 조건에 따라 query를 비활성화하고 싶지만 여전히 query를 유형 안전으로 유지하려는 경우에 유용합니다.
이에 대한 자세한 내용은 [Queries 비활성화](guides/disabling-queries.md) 가이드를 참조하세요.

[//]: # 'Materials'

## 추가 자료

유형 추론에 대한 팁과 요령은 [React Query 및 TypeScript](https://tkdodo.eu/blog/react-query-and-type-script) 문서를 참조하세요. 가능한 최상의 유형 안전성을 얻는 방법을 알아보려면 [Type-safe React Query](https://tkdodo.eu/blog/type-safe-react-query)를 읽어보세요. [Query 옵션 API](https://tkdodo.eu/blog/the-query-options-api)에서는 `queryOptions` 도우미 함수와 함께 유형 추론이 작동하는 방식을 간략하게 설명합니다.

[//]: # 'Materials'
