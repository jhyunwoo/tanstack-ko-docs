---
id: hydration
title: hydration
---




## `dehydrate`

`dehydrate`는 나중에 `HydrationBoundary` 또는 `hydrate`로 수화될 수 있는 `cache`의 동결 표현을 생성합니다. 이는 프리페치된 queries를 서버에서 클라이언트로 전달하거나 queries를 localStorage 또는 기타 영구 위치에 유지하는 데 유용합니다. 기본적으로 현재 성공한 queries만 포함됩니다.

```tsx
import { dehydrate } from '@tanstack/react-query'

const dehydratedState = dehydrate(queryClient, {
  shouldDehydrateQuery,
  shouldDehydrateMutation,
})
```
**옵션**

- `client: QueryClient`
  - **필수**
  - 탈수가 필요한 `queryClient`
- `options: DehydrateOptions`
  - 선택사항
  - `shouldDehydrateMutation: (mutation: Mutation) => boolean`
    - 선택사항
    - mutations 탈수 여부.
    - 캐시에 있는 mutation마다 함수가 호출됩니다.
      - 이 mutation를 탈수에 포함하려면 `true`를 반환하고 그렇지 않으면 `false`를 반환합니다.
    - 기본값은 일시 중지된 mutations만 포함하는 것입니다.
    - 기본 동작을 유지하면서 기능을 확장하려면 return 문의 일부로 `defaultShouldDehydrateMutation`를 가져와서 실행하세요.
  - `shouldDehydrateQuery: (query: Query) => boolean`
    - 선택사항
    - queries 탈수 여부.
    - 캐시에 있는 각 query에 대해 함수가 호출됩니다.
      - 탈수에 이 query를 포함하려면 `true`를 반환하고 그렇지 않으면 `false`를 반환합니다.
    - 기본값은 성공한 queries만 포함하는 것입니다.
    - 기본 동작을 유지하면서 기능을 확장하려면 return 문의 일부로 `defaultShouldDehydrateQuery`를 가져와서 실행하세요.
  - `serializeData?: (data: any) => any` 탈수 시 데이터를 변환(직렬화)하는 기능입니다.
  - `shouldRedactErrors?: (error: unknown) => boolean`
    - 선택사항
    - 탈수 중 서버의 오류를 수정할지 여부입니다.
    - 캐시의 각 오류에 대해 함수가 호출됩니다.
      - 이 오류를 수정하려면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다.
    - 기본적으로 모든 오류를 수정합니다.

**보고**

- `dehydratedState: DehydratedState`
  - 여기에는 나중에 `queryClient`를 수화하는 데 필요한 모든 것이 포함됩니다.
  - 이 응답의 정확한 형식에 의존해서는 안 됩니다**. 이는 공개 API의 일부가 아니며 언제든지 변경될 수 있습니다.
  - 이 결과는 직렬화된 형식이 아니므로 원하는 경우 직접 수행해야 합니다.

### 제한사항

일부 저장소 시스템(예: 브라우저 [웹 저장소 API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API))에는 값이 JSON 직렬화 가능해야 합니다. JSON으로 자동으로 직렬화할 수 없는 값(예: `Error` 또는 `undefined`)을 디하이드레이트해야 하는 경우 해당 값을 직접 직렬화해야 합니다. 기본적으로 성공한 queries만 포함되므로 `Errors`도 포함하려면 다음과 같이 `shouldDehydrateQuery`를 제공해야 합니다.

```tsx
// 섬기는 사람
const state = dehydrate(client, { shouldDehydrateQuery: () => true }) // 오류도 포함하려면
const serializedState = mySerialize(state) // 오류 인스턴스를 객체로 변환

// 고객
const state = myDeserialize(serializedState) // 객체를 오류 인스턴스로 다시 변환
hydrate(client, state)
```
## `hydrate`

`hydrate`는 이전에 탈수된 상태를 `cache`에 추가합니다.

```tsx
import { hydrate } from '@tanstack/react-query'

hydrate(queryClient, dehydratedState, options)
```
**옵션**

- `client: QueryClient`
  - **필수**
  - 상태를 수화시키는 `queryClient`
- `dehydratedState: DehydratedState`
  - **필수**
  - 클라이언트에 수화할 상태
- `options: HydrateOptions`
  - 선택사항
  - `defaultOptions: DefaultOptions`
    - 선택사항
    - `mutations: MutationOptions` 수화된 mutations에 사용할 기본 mutation 옵션입니다.
    - `queries: QueryOptions` 수화된 queries에 사용할 기본 query 옵션입니다.
    - `deserializeData?: (data: any) => any` 데이터를 캐시에 넣기 전에 변환(역직렬화)하는 기능입니다.
  - `queryClient?: QueryClient`
    - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

### 제한사항

하이드레이션하려는 queries가 queryCache에 이미 존재하는 경우 `hydrate`는 데이터가 캐시에 있는 데이터보다 최신인 경우에만 이를 덮어씁니다. 그렇지 않으면 적용되지 **않습니다**.

[//]: # 'HydrationBoundary'

## `HydrationBoundary`

`HydrationBoundary`는 `useQueryClient()`에서 반환할 `queryClient`에 이전에 탈수된 상태를 추가합니다. 클라이언트에 이미 데이터가 포함되어 있는 경우 새 queries는 업데이트 타임스탬프를 기반으로 지능적으로 병합됩니다.

```tsx
import { HydrationBoundary } from '@tanstack/react-query'

function App() {
  return <HydrationBoundary state={dehydratedState}>...</HydrationBoundary>
}
```
> 참고: `queries`만 `HydrationBoundary`로 탈수할 수 있습니다.

**옵션**

- `state: DehydratedState`
  - 수분을 공급하는 상태
- `options: HydrateOptions`
  - 선택사항
  - `defaultOptions: QueryOptions`
    - 수화된 queries에 사용할 기본 query 옵션입니다.
  - `queryClient?: QueryClient`
    - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

[//]: # 'HydrationBoundary'
