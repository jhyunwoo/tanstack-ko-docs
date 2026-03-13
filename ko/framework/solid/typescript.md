---
id: typescript
title: TypeScript
---




Solid Query는 **TypeScript**로 작성되어 라이브러리와 프로젝트가 유형에 안전한지 확인합니다!

명심해야 할 사항:

- TanStack Query는 [DefinitelyTyped 지원 창](https://github.com/DefinitelyTyped/DefinitelyTyped#support-window)을 따르며 최근 2년 이내에 출시된 TypeScript 버전을 지원합니다. 현재 이는 TypeScript **5.4** 이상을 의미합니다.
- 이 저장소의 유형에 대한 변경 사항은 **비해킹**으로 간주되며 일반적으로 **패치** semver 변경으로 릴리스됩니다(그렇지 않으면 모든 유형 향상이 주요 버전이 됩니다!).
- **solid-query 패키지 버전을 특정 패치 릴리스로 고정하고 모든 릴리스 간에 유형이 수정되거나 업그레이드될 수 있다는 기대를 갖고 업그레이드하는 것이 좋습니다**
- Solid Query의 유형과 관련되지 않은 공개 API는 여전히 semver를 매우 엄격하게 따릅니다.

## 유형 추론

Solid Query의 유형은 일반적으로 매우 잘 흐르므로 직접 유형 주석을 제공할 필요가 없습니다.

```tsx
import { useQuery } from '@tanstack/solid-query'

const query = useQuery(() => ({
  queryKey: ['number'],
  queryFn: () => Promise.resolve(5),
}))

query.data
//    ^? (속성) 데이터: 숫자 | 한정되지 않은
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQK5pQCecAvnAGZQQhwDkAAjBgHYDOzyA1gPRsQAbYABMAtAEcCxOgFgAUP OQR28SYRIBeFOiy4pRABQGAlHA0A+OAYTy4duGuIBpNEQBccANp0WeEACNCOgBdABo4W3tHIgAxFg8TM0sABWoQYDY0ADp0fgEANzQDAFZjeVJjMoU5aKzhLAx5Hh57OAA9AH55brkgA)

```tsx
import { useQuery } from '@tanstack/solid-query'

const query = useQuery(() => ({
  queryKey: ['test'],
  queryFn: () => Promise.resolve(5),
  select: (data) => data.toString(),
}))

query.data
//    ^? (속성) 데이터: 문자열 | 한정되지 않은
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQK5pQCecAvnAGZQQhwDkAAjBgHYDOzyA1gPRsQAbYABMAtAEcCxOgFgAUPOQR28SYRIBeFOiy4p RABQGAlHA0A+OAYTy4duGuIBpNEQBccANp1sHOgF0AGjhbe0ciADEWDxMzSwAFahBgNjQAOnR+AQA3 NAMAVmNA0LtUgTRkGBjhLAxTCzga5jSYCABlGChgFgBzE2K5UmNjeXlwtKaMeR4eezgAPQB+UYU5IA)

이는 `queryFn`에 잘 정의된 반환 유형이 있는 경우 가장 잘 작동합니다. 대부분의 데이터 가져오기 라이브러리는 기본적으로 `any`를 반환하므로 올바른 유형의 함수로 추출해야 합니다.

```tsx
const fetchGroups = (): Promise<Group[]> =>
  axios.get('/groups').then((response) => response.data)

const query = useQuery(() => ({
  queryKey: ['groups'],
  queryFn: fetchGroups,
}))

query.data
//    ^? (속성) 데이터: 그룹[] | 한정되지 않은
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?ssl=11&ssc=4&pln=6&pc=1#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQ K5pQCecAvnAGZQQhwDkAAjBgHYDOzyA1gPRsQAbYABMATAEcCxOgFgAUKEiw4GAB7AIbStVp01GtrLnyYRMGjgBxanjBwAvIjgiAXHBZ4QA I0Jl585Ah2eAo0GGQAC2sIWy1HAAoASjcABR1gNjQAHmjbAG0AXQA+BxL9TQA6AHMw+LoeKpswQ0SKmAi0Fnj0Nkh2C3sSnr7MiuEsDET- OUDguElCEkdUTGx8Rfik0rh4hHk4A-mpIgBpNCI3PLpGmOa6AoAaOH3DheIAMRY3UPCoprYHvJSIkpsY5G8iGMJvIeDxDnAAHoAfmm8iAA)

## 유형 축소

Solid Query는 `status` 필드와 파생된 상태 boolean 플래그로 구별되는 query 결과에 [차별화된 공용체 유형](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-func.html#discriminated-unions)을 사용합니다. 이를 통해 예를 들어 `data`를 정의하기 위한 `success` 상태를 확인할 수 있습니다:

```tsx
const query = useQuery(() => ({
  queryKey: ['number'],
  queryFn: () => Promise.resolve(5),
}))

if (query.isSuccess) {
  const data = query.data
  //     ^? const 데이터: 숫자
}
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQK5pQC ecAvnAGZQQhwDkAAjBgHYDOzyA1gPRsQAbYABMATAEcCxOgFgAUKEixEKdFjQBRChTTJ45KjXr8hYgFZtZc+cgjt 4kwiQC8qzNnxOAFF4CUcZwA+OC8EeTg4R2IAaTQiAC44AG06FjwQACNCOgBdABpwyKkiADEWRL8A4IAFahBgNjQA OnQTADc0LwBWXwK5Ul9feXlgChCooiaGgGU8ZGQ0NjZ-MLkIiNt7OGEsDACipyad5kKInh51iIA9AH55UmHrOSA)

## 오류 필드 입력

오류 유형은 대부분의 사용자가 기대하는 `Error`로 기본 설정됩니다.

```tsx
const query = useQuery(() => ({
  queryKey: ['groups'],
  queryFn: fetchGroups,
}))

query.error
//    ^? (속성) 오류: 오류 | null
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQK5pQCecAvnAGZQQhwD kAAjBgHYDOzyA1gPRsQAbYABMAtAEcCxOgFgAUKEiw4GAB7AIbStVp01GtrLnyYRMGjgBxanjBwAvIjgiAXHBZ4QAI0Jl585Ah2eAo 0GGQAC2sIWy1HAAoASjcABR1gNjQAHmjbAG0AXQA+BxL9TQA6AHMw+LoeKpswQ0SKmAi0Fnj0Nkh2C3sSnr7MiuEsDET-OUDguElC EkdUTGx8Rfik0rh4hHk4A-mpIgBpNCI3PLpGmOa6AoAaOH3DheIAMRY3UPCoprYHvJSIkpsY5G8iBVCNQoPieDxDnAAHoAfmm8iAA)

사용자 정의 오류나 `Error`가 아닌 오류를 발생시키려는 경우 오류 필드의 유형을 지정할 수 있습니다.

```tsx
const query = useQuery<Group[], string>(() => ({
  queryKey: ['groups'],
  queryFn: fetchGroups,
}))

query.error
//    ^? (속성) 오류: 문자열 | null
```
그러나 이는 `useQuery`의 다른 모든 제네릭에 대한 유형 추론이 더 이상 작동하지 않는다는 단점이 있습니다. 일반적으로 `Error`가 아닌 것을 던지는 것은 좋은 습관으로 간주되지 않습니다. 따라서 `AxiosError`와 같은 하위 클래스가 있는 경우 _유형 축소_를 사용하여 오류 필드를 더 구체적으로 만들 수 있습니다.

```tsx
import axios from 'axios'

const query = useQuery(() => ({
  queryKey: ['groups'],
  queryFn: fetchGroups,
}))

query.error
//    ^? (속성) 오류: 오류 | null

if (axios.isAxiosError(query.error)) {
  query.error
  //    ^? (속성) 오류: AxiosError
}
```
[타이프스크립트 놀이터](https://www.typescriptlang.org/play/?#code/JYWwDg9gTgLgBAbzgYygUwIYzQRQK5pQCecAvnAGZQQhwDkAAjBgHYDOzy A1gPRsQAbYABMAtAEcCxOgFgAUKEiw4GAB7AIbStVp01GtrLnyYRMGjgBxanjBwAvIjgiAXHBZ4QAI0Jl585Ah2eAo0GGQAC2sIWy1HAAoASjcABR1 gNjQAHmjbAG0AXQA+BxL9TQA6AHMw+LoeKpswQ0SKmAi0Fnj0Nkh2C3sSnr7MiuEsDET-OUDguElCEkdUTGx8Rfik0rh4hHk4A-mpIgBpNCI3PLpGm Oa6AoAaOH3DheIAMRY3UPCoprYHvJSIkpsY5G8iBVCNQoPieDxDnAAHoAfmmwAoO3KbAqGQAgupNABRKAw+IQqGk6AgxAvA4U6HQOlweGI1FA+RAA)

[//]: # 'RegisterErrorType'

```tsx
import '@tanstack/solid-query'

declare module '@tanstack/solid-query' {
  interface Register {
    // 알 수 없음을 사용하면 호출 사이트가 명시적으로 범위를 좁혀야 합니다.
    defaultError: unknown
  }
}

const query = useQuery(() => ({
  queryKey: ['groups'],
  queryFn: fetchGroups,
}))

query.error
//    ^? (속성) 오류: 알 수 없음 | null
```
[//]: # 'RegisterErrorType'

## 글로벌 `Meta` 등록 중

[전역 오류 유형](#registering-a-global-error)을 등록하는 것과 마찬가지로 전역 `Meta` 유형을 등록할 수도 있습니다. 이렇게 하면 [useQuery](reference/useQuery.md) 및 [useMutation](reference/useMutation.md)의 선택적 `meta` 필드가 일관성을 유지하고 유형이 안전해집니다. 등록된 유형은 `meta`가 객체로 유지되도록 `Record<string, unknown>`를 확장해야 합니다.

```ts
import '@tanstack/solid-query'

interface MyMeta extends Record<string, unknown> {
  // 메타 유형 정의.
}

declare module '@tanstack/solid-query' {
  interface Register {
    queryMeta: MyMeta
    mutationMeta: MyMeta
  }
}
```
## Query 옵션 입력

query 옵션을 `useQuery`에 인라인하면 자동 유형 추론이 수행됩니다. 그러나 query 옵션을 별도의 함수로 추출하여 `useQuery`와 예를 들어 다음과 같이 공유할 수 있습니다. `prefetchQuery`. 이 경우 유형 추론이 손실됩니다. 다시 가져오려면 `queryOptions` 도우미를 사용할 수 있습니다.

```ts
import { queryOptions } from '@tanstack/solid-query'

function groupOptions() {
  return queryOptions({
    queryKey: ['groups'],
    queryFn: fetchGroups,
    staleTime: 5 * 1000,
  })
}

useQuery(groupOptions)
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
//    ^? const 데이터: 그룹[] | 한정되지 않은
```
`queryOptions`가 없으면 일반을 전달하지 않는 한 `data` 유형은 `unknown`가 됩니다.

```ts
const data = queryClient.getQueryData<Group[]>(['groups'])
```
## `skipToken`를 사용하여 queries의 형식 안전 비활성화

TypeScript를 사용하는 경우 `skipToken`를 사용하여 query를 비활성화할 수 있습니다. 이는 조건에 따라 query를 비활성화하고 싶지만 여전히 query를 유형 안전으로 유지하려는 경우에 유용합니다.

이에 대한 자세한 내용은 [Queries 비활성화](guides/disabling-queries.md) 가이드를 참조하세요.
