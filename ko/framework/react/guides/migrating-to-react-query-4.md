---
id: migrating-to-react-query-4
title: React Query 4로 마이그레이션
---




## 주요 변경 사항

v4는 주요 버전이므로 알아야 할 몇 가지 주요 변경 사항이 있습니다.

### 반응-query는 이제 @tanstack/react-query입니다.

종속성을 제거/설치하고 가져오기를 변경해야 합니다.

```
npm uninstall react-query
npm install @tanstack/react-query
npm install @tanstack/react-query-devtools
```

```tsx
- import { useQuery } from 'react-query' // [!코드-]
- import { ReactQueryDevtools } from 'react-query/devtools' // [!코드-]

+ import { useQuery } from '@tanstack/react-query' // [!코드 ++]
+ import { ReactQueryDevtools } from '@tanstack/react-query-devtools' // [!코드 ++]
```
#### 코드모드

가져오기 마이그레이션을 더 쉽게 만들기 위해 v4에는 codemod가 함께 제공됩니다.

> codemod는 주요 변경 사항을 마이그레이션하는 데 도움이 되는 최선의 노력입니다. 생성된 코드를 철저하게 검토하세요! 또한, 코드 모드에서 발견할 수 없는 극단적인 경우도 있으므로 로그 출력을 계속 지켜봐 주시기 바랍니다.

다음 명령 중 하나(또는 둘 다)를 사용하여 쉽게 적용할 수 있습니다.

`.js` 또는 `.jsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift ./path/to/src/ \
  --extensions=js,jsx \
  --transform=./node_modules/@tanstack/react-query/codemods/v4/replace-import-specifier.js
```
`.ts` 또는 `.tsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift ./path/to/src/ \
  --extensions=ts,tsx \
  --parser=tsx \
  --transform=./node_modules/@tanstack/react-query/codemods/v4/replace-import-specifier.js
```
`TypeScript`의 경우 `tsx`를 파서로 사용해야 합니다. 그렇지 않으면 codemod가 제대로 적용되지 않습니다!

**참고:** codemod를 적용하면 코드 형식이 손상될 수 있으므로 codemod를 적용한 후 `prettier` 및/또는 `eslint`를 실행하는 것을 잊지 마세요!

**참고:** codemod는 가져오기만 _만_ 변경합니다. 여전히 별도의 devtools 패키지를 수동으로 설치해야 합니다.

### Query 키(및 Mutation 키)는 배열이어야 합니다.

v3에서는 Query 및 Mutation 키가 문자열 또는 배열일 수 있습니다. 내부적으로 React Query는 항상 배열 키로만 작동했으며 때때로 이를 소비자에게 노출했습니다. 예를 들어, `queryFn`에서는 [기본 Query 함수](default-query-function.md) 작업을 더 쉽게 만들기 위해 항상 키를 배열로 가져옵니다.

그러나 우리는 이 개념을 모든 API에 적용하지는 않았습니다. 예를 들어, [Query 필터](filters.md)에서 `predicate` 함수를 사용하면 원시 Query 키를 얻게 됩니다. 이로 인해 배열과 문자열이 혼합된 Query 키를 사용하는 경우 이러한 기능을 사용하기가 어렵습니다. 전역 콜백을 사용할 때도 마찬가지였습니다.

모든 API를 간소화하기 위해 모든 키를 배열로만 만들기로 결정했습니다.

```tsx
;-useQuery('todos', fetchTodos) + // [!코드-]
  useQuery(['todos'], fetchTodos) // [!코드 ++]
```
#### 코드모드

이 마이그레이션을 더 쉽게 하기 위해 우리는 codemod를 제공하기로 결정했습니다.

> codemod는 주요 변경 사항을 마이그레이션하는 데 도움이 되는 최선의 노력입니다. 생성된 코드를 철저하게 검토하세요! 또한, 코드 모드에서 발견할 수 없는 극단적인 경우도 있으므로 로그 출력을 계속 지켜봐 주시기 바랍니다.

다음 명령 중 하나(또는 둘 다)를 사용하여 쉽게 적용할 수 있습니다.

`.js` 또는 `.jsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift ./path/to/src/ \
  --extensions=js,jsx \
  --transform=./node_modules/@tanstack/react-query/codemods/v4/key-transformation.js
```
`.ts` 또는 `.tsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift ./path/to/src/ \
  --extensions=ts,tsx \
  --parser=tsx \
  --transform=./node_modules/@tanstack/react-query/codemods/v4/key-transformation.js
```
`TypeScript`의 경우 `tsx`를 파서로 사용해야 합니다. 그렇지 않으면 codemod가 제대로 적용되지 않습니다!

**참고:** codemod를 적용하면 코드 형식이 손상될 수 있으므로 codemod를 적용한 후 `prettier` 및/또는 `eslint`를 실행하는 것을 잊지 마세요!

### 유휴 상태가 제거되었습니다.

더 나은 오프라인 지원을 위한 새로운 [Queries](queries.md#fetchstatus)가 도입되면서 `idle` 상태는 더 이상 의미가 없게 되었습니다. 왜냐하면 `fetchStatus: 'idle'`가 동일한 상태를 더 잘 캡처하기 때문입니다. 자세한 내용은 [Queries](queries.md#why-two-other-states)를 읽어보세요.

이는 이전에 `idle` 상태에 있었던 것처럼 아직 `data`가 없는 `disabled` queries에 주로 영향을 미칩니다.

```tsx
- status: 'idle' // [!코드-]
+ status: 'loading'  // [!코드 ++]
+ fetchStatus: 'idle' // [!코드 ++]
```
또한 [종속 queries에 대한 가이드](dependent-queries.md)를 살펴보세요.

#### 비활성화됨 queries

이 변경으로 인해 비활성화된 queries(일시적으로 비활성화된 경우라도)는 `loading` 상태에서 시작됩니다. 마이그레이션을 더 쉽게 하려면, 특히 로딩 스피너를 표시할 시기를 알 수 있는 좋은 플래그를 가지려면 `isLoading` 대신 `isInitialLoading`를 확인하면 됩니다.

```tsx
;-isLoading + // [!코드-]
  isInitialLoading // [!코드 ++]
```
[queries 비활성화](disabling-queries.md#isloading-previous-isinitialloading)에 대한 가이드도 참조하세요.

### `useQueries`용 새 API

이제 `useQueries` 후크는 `queries` 소품을 입력으로 사용하는 개체를 허용합니다. `queries` prop의 값은 queries의 배열입니다(이 배열은 v3에서 `useQueries`에 전달된 것과 동일합니다).

```tsx
;-useQueries([
  { queryKey1, queryFn1, options1 },
  { queryKey2, queryFn2, options2 },
]) + // [!코드-]
  useQueries({
    queries: [
      { queryKey1, queryFn1, options1 },
      { queryKey2, queryFn2, options2 },
    ],
  }) // [!코드 ++]
```
### 정의되지 않음은 queries 성공에 대한 잘못된 캐시 값입니다.

`undefined`를 반환하여 업데이트를 구제할 수 있도록 하려면 `undefined`를 잘못된 캐시 값으로 만들어야 했습니다. 이는 반응-query의 다른 개념과 일치합니다. 예를 들어 [initialData 함수](initial-query-data.md#initial-data-function)에서 `undefined`를 반환하면 데이터가 _not_ 설정됩니다.

또한 queryFn에 로깅을 추가하여 `Promise<void>`를 생성하는 것은 쉬운 버그입니다.

```tsx
useQuery(['key'], () =>
  axios.get(url).then((result) => console.log(result.data)),
)
```
이는 이제 유형 수준에서 허용되지 않습니다. 런타임 시 `undefined`는 _실패한 Promise_으로 변환됩니다. 즉, `error`를 얻게 되며 개발 모드에서 콘솔에도 기록됩니다.

### Queries 및 mutations는 ​​기본적으로 실행하려면 네트워크 연결이 필요합니다.

온라인/오프라인 지원에 대한 [새로운 기능 공지](#proper-offline-support)와 [네트워크 모드](network-mode.md)에 대한 전용 페이지를 읽어보세요.

React Query는 Promise를 생성하는 모든 것에 사용할 수 있는 비동기 상태 관리자이지만 데이터 가져오기 라이브러리와 함께 데이터 가져오기에 가장 자주 사용됩니다. 따라서 네트워크 연결이 없는 경우 기본적으로 queries 및 mutations는 ​​`paused`가 됩니다. 이전 동작을 선택하려면 queries 및 mutations 모두에 대해 `networkMode: offlineFirst`를 전역적으로 설정할 수 있습니다.

```tsx
new QueryClient({
  defaultOptions: {
    queries: {
      networkMode: 'offlineFirst',
    },
    mutations: {
      networkMode: 'offlineFirst',
    },
  },
})
```
### `notifyOnChangeProps` 속성은 더 이상 `"tracked"`를 값으로 허용하지 않습니다.

`notifyOnChangeProps` 옵션은 더 이상 `"tracked"` 값을 허용하지 않습니다. 대신 `useQuery`는 기본적으로 추적 속성을 사용합니다. `notifyOnChangeProps: "tracked"`를 사용하는 모든 queries는 이 옵션을 제거하여 업데이트해야 합니다.

queries에서 이를 우회하여 query가 변경될 때마다 다시 렌더링하는 v3 기본 동작을 에뮬레이션하려는 경우 이제 `notifyOnChangeProps`는 기본 스마트 추적 최적화를 선택 해제하기 위해 `"all"` 값을 허용합니다.

### `notifyOnChangePropsExclusion`가 제거되었습니다.

v4에서 `notifyOnChangeProps`는 기본적으로 `undefined` 대신 v3의 `"tracked"` 동작을 사용합니다. 이제 `"tracked"`가 v4의 기본 동작이므로 이 구성 옵션을 포함하는 것은 더 이상 의미가 없습니다.

### `cancelRefetch`의 일관된 동작

`cancelRefetch` 옵션은 query를 명령적으로 가져오는 모든 함수에 전달될 수 있습니다.

- `queryClient.refetchQueries`
- `queryClient.invalidateQueries`
- `queryClient.resetQueries`
- `refetch`는 `useQuery`에서 반환되었습니다.
- `useInfiniteQuery`에서 반환된 `fetchNextPage` 및 `fetchPreviousPage`

`fetchNextPage` 및 `fetchPreviousPage`를 제외하고 이 플래그는 기본적으로 `false`로 설정되어 있었으며 이는 일관성이 없고 잠재적으로 문제가 있었습니다. 이전 느린 가져오기가 이미 진행 중인 경우 mutation 이후에 `refetchQueries` 또는 `invalidateQueries`를 호출하면 최신 결과가 생성되지 않을 수 있습니다. 건너뛰었습니다.

우리는 귀하가 작성한 일부 코드에 의해 query가 적극적으로 다시 가져오는 경우 기본적으로 가져오기를 다시 시작해야 한다고 믿습니다.

이것이 바로 위에서 언급한 모든 방법에 대해 이 플래그가 이제 기본적으로 _true_로 설정되는 이유입니다. 이는 또한 `refetchQueries`를 기다리지 않고 연속으로 두 번 호출하면 이제 첫 번째 가져오기를 취소하고 두 번째 가져오기로 다시 시작한다는 의미입니다.

```
queryClient.refetchQueries({ queryKey: ['todos'] })
// 이전 다시 가져오기를 중단하고 새 가져오기를 시작합니다.
queryClient.refetchQueries({ queryKey: ['todos'] })
```
`cancelRefetch:false`를 명시적으로 전달하여 이 동작을 선택 해제할 수 있습니다.

```
queryClient.refetchQueries({ queryKey: ['todos'] })
// 이는 이전 다시 가져오기를 중단하지 않고 무시됩니다.
queryClient.refetchQueries({ queryKey: ['todos'] }, { cancelRefetch: false })
```
> 참고: 자동으로 트리거된 가져오기 동작에는 변화가 없습니다. query 마운트 또는 창 포커스 다시 가져오기 때문입니다.

### Query 필터

[query 필터](filters.md)는 query와 일치하는 특정 조건이 있는 개체입니다. 역사적으로 필터 옵션은 대부분 boolean 플래그의 조합이었습니다. 그러나 이러한 플래그를 결합하면 불가능한 상태가 발생할 수 있습니다. 구체적으로:

```
active?: boolean
  - When set to true it will match active queries.
  - When set to false it will match inactive queries.
inactive?: boolean
  - When set to true it will match inactive queries.
  - When set to false it will match active queries.
```
이러한 플래그는 상호 배타적이기 때문에 함께 사용하면 제대로 작동하지 않습니다. 두 플래그 모두에 대해 `false`를 설정하면 설명에 따라 모든 queries와 일치하거나 queries와 일치하지 않을 수 있습니다. 이는 별로 의미가 없습니다.

v4에서는 이러한 필터가 단일 필터로 결합되어 의도를 더 잘 보여줍니다.

```tsx
- active?: boolean // [!코드-]
- inactive?: boolean // [!코드-]
+ type?: 'active' | 'inactive' | 'all' // [!코드 ++]
```
필터의 기본값은 `all`이며, `active` 또는 `inactive` queries와만 일치하도록 선택할 수 있습니다.

#### refetchActive / refetchInactive

[QueryClient](../../../reference/QueryClient.md#queryclientinvalidatequeries)에는 두 개의 추가 유사한 플래그가 있습니다.

```
refetchActive: Boolean
  - Defaults to true
  - When set to false, queries that match the refetch predicate and are actively being rendered
    via useQuery and friends will NOT be refetched in the background, and only marked as invalid.
refetchInactive: Boolean
  - Defaults to false
  - When set to true, queries that match the refetch predicate and are not being rendered
    via useQuery and friends will be both marked as invalid and also refetched in the background
```
같은 이유로 다음도 결합되었습니다.

```tsx
- refetchActive?: boolean // [!코드-]
- refetchInactive?: boolean // [!코드-]
+ refetchType?: 'active' | 'inactive' | 'all' | 'none' // [!코드 ++]
```
`refetchActive`의 기본값은 `true`이므로 이 플래그의 기본값은 `active`입니다. 이는 `invalidateQueries`에게 전혀 다시 가져오지 않도록 지시하는 방법도 필요하다는 것을 의미하며, 이것이 바로 여기에서 네 번째 옵션(`none`)도 허용되는 이유입니다.

### `onSuccess`는 더 이상 `setQueryData`에서 호출되지 않습니다.

이는 많은 사람들에게 혼란을 주었고 `setQueryData`가 `onSuccess` 내에서 호출된 경우 무한 루프도 생성되었습니다. 또한 `staleTime`와 결합할 때 오류가 자주 발생했습니다. 캐시에서만 데이터를 읽는 경우 `onSuccess`는 호출되지 _않았_기 때문입니다.

`onError` 및 `onSettled`와 유사하게 `onSuccess` 콜백은 이제 요청에 연결됩니다. 요청 없음 -> 콜백 없음.

`data` 필드의 변경 사항을 수신하려면 `useEffect`를 사용하는 것이 가장 좋습니다. 여기서 `data`는 종속성 배열의 일부입니다. React Query는 구조적 공유를 통해 안정적인 데이터를 보장하므로 백그라운드를 다시 가져올 때마다 효과가 실행되지 않고 데이터 내의 내용이 변경된 경우에만 효과가 실행됩니다.

```
const { data } = useQuery({ queryKey, queryFn })
React.useEffect(() => mySideEffectHere(data), [data])
```
### `persistQueryClient` 및 해당 지속 플러그인은 더 이상 실험적이지 않으며 이름이 변경되었습니다.

플러그인 `createWebStoragePersistor` 및 `createAsyncStoragePersistor`는 각각 [createSyncStoragePersister](../plugins/createSyncStoragePersister.md) 및 [createAsyncStoragePersister](../plugins/createAsyncStoragePersister.md)로 이름이 변경되었습니다. `persistQueryClient`의 인터페이스 `Persistor`도 `Persister`로 이름이 변경되었습니다. 이 변경의 동기는 [이 stackexchange](https://english.stackexchange.com/questions/206893/persister-or-persistor)에서 확인하세요.

이 플러그인은 더 이상 실험적이지 않으므로 가져오기 경로도 업데이트되었습니다.

```tsx
- import { persistQueryClient } from 'react-query/persistQueryClient-experimental' // [!코드-]
- import { createWebStoragePersistor } from 'react-query/createWebStoragePersistor-experimental' // [!코드-]
- import { createAsyncStoragePersistor } from 'react-query/createAsyncStoragePersistor-experimental' // [!코드-]

+ import { persistQueryClient } from '@tanstack/react-query-persist-client' // [!코드 ++]
+ import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister' // [!코드 ++]
+ import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister'  // [!코드 ++]
```
### Promise의 `cancel` 메서드는 더 이상 지원되지 않습니다.

이전 `cancel` 메서드(프로미스에서 `cancel` 함수를 정의할 수 있고 라이브러리에서 query 취소를 지원하는 데 사용됨)가 제거되었습니다. query 취소에는 내부적으로 [`AbortController` API](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)를 사용하고 [`AbortSignal` 인스턴스](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)를 query 함수에서 query 취소를 지원합니다.

### TypeScript

이제 유형에는 TypeScript v4.1 이상을 사용해야 합니다.

### 지원되는 브라우저

v4부터 React Query는 최신 브라우저에 최적화되어 있습니다. 보다 현대적이고 성능이 뛰어나며 작은 번들을 생성하기 위해 브라우저 목록을 업데이트했습니다. 요구 사항은 [여기](../installation.md#requirements)에서 확인할 수 있습니다.

### `setLogger`가 제거되었습니다.

`setLogger`를 호출하여 로거를 전역적으로 변경할 수 있었습니다. v4에서는 `QueryClient`를 생성할 때 해당 기능이 선택적 필드로 대체됩니다.

```tsx
- import { QueryClient, setLogger } from 'react-query'; // [!코드-]
+ import { QueryClient } from '@tanstack/react-query'; // [!코드 ++]

- setLogger(customLogger) // [!코드-]
- const queryClient = new QueryClient(); // [!코드-]
+ const queryClient = new QueryClient({ logger: customLogger }) // [!코드 ++]
```
### 아니요 _default_ 수동 가비지 수집 서버측

v3에서 React Query는 기본적으로 5분 동안 query 결과를 캐시한 다음 해당 데이터를 수동으로 가비지 수집합니다. 이 기본값은 서버측 React Query에도 적용되었습니다.

이로 인해 메모리 소비가 늘어나고 수동 가비지 수집이 완료되기를 기다리는 프로세스가 중단됩니다. v4에서는 기본적으로 서버 측 `cacheTime`가 `Infinity`로 설정되어 수동 가비지 수집을 효과적으로 비활성화합니다(요청이 완료되면 NodeJS 프로세스가 모든 것을 지웁니다).

이 변경 사항은 Next.js와 같은 서버측 React Query 사용자에게만 영향을 미칩니다. `cacheTime`를 수동으로 설정하는 경우에는 영향을 미치지 않습니다(비록 동작을 미러링하려는 경우도 있음).

### 프로덕션에 로그인 중

v4부터 React-query는 많은 사람들에게 혼란을 주었기 때문에 프로덕션 모드에서 더 이상 오류(예: 실패한 가져오기)를 콘솔에 기록하지 않습니다.
개발 모드에서는 오류가 계속 표시됩니다.

### ESM 지원

React Query는 이제 [package.json `"exports"`](https://nodejs.org/api/packages.html#exports)를 지원하며 CommonJS 및 ESM 모두에 대한 Node의 기본 해상도와 완벽하게 호환됩니다. 이것이 대부분의 사용자에게 큰 변화가 될 것으로 예상하지는 않지만, 이는 공식적으로 지원하는 진입점으로만 프로젝트로 가져올 수 있는 파일을 제한합니다.

### 간소화된 NotifyEvents

`QueryCache`를 수동으로 구독하면 항상 `QueryCacheNotifyEvent`가 제공되지만 `MutationCache`의 경우에는 그렇지 않습니다. 우리는 동작을 간소화하고 그에 따라 이벤트 이름도 조정했습니다.

#### QueryCacheNotifyEvent

```tsx
- type: 'queryAdded' // [!코드-]
+ type: 'added' // [!코드 ++]
- type: 'queryRemoved' // [!코드-]
+ type: 'removed' // [!코드 ++]
- type: 'queryUpdated' // [!코드-]
+ type: 'updated' // [!코드 ++]
```
#### MutationCacheNotifyEvent

`MutationCacheNotifyEvent`는 `QueryCacheNotifyEvent`와 동일한 유형을 사용합니다.

> 참고: 이는 `queryCache.subscribe` 또는 `mutationCache.subscribe`를 통해 캐시를 수동으로 구독하는 경우에만 관련됩니다.

### 별도의 hydration 내보내기가 제거되었습니다.

버전 [3.22.0](https://github.com/tannerlinsley/react-query/releases/tag/v3.22.0)에서는 hydration 유틸리티가 React Query 코어로 이동되었습니다. v3에서는 `react-query/hydration`의 이전 내보내기를 계속 사용할 수 있지만 v4에서는 이러한 내보내기가 제거되었습니다.

```tsx
- import { dehydrate, hydrate, useHydrate, Hydrate } from 'react-query/hydration' // [!코드-]
+ import { dehydrate, hydrate, useHydrate, Hydrate } from '@tanstack/react-query' // [!코드 ++]
```
### `queryClient`, `query` 및 `mutation`에서 문서화되지 않은 메서드를 제거했습니다.

`QueryClient`의 `cancelMutations` 및 `executeMutation` 메서드는 문서화되지 않았고 내부적으로 사용되지 않았으므로 제거했습니다. 이는 `mutationCache`에서 사용할 수 있는 메서드에 대한 래퍼일 뿐이므로 `executeMutation`의 기능을 계속 사용할 수 있습니다.

```tsx
- executeMutation< // [!코드-]
-   TData = unknown, // [!코드-]
-   TError = unknown, // [!코드-]
-   TVariables = void, // [!코드-]
-   TContext = unknown // [!코드-]
- >( // [!코드-]
-   options: MutationOptions<TData, TError, TVariables, TContext> // [!코드-]
- ): Promise<TData> { // [!코드-]
-   return this.mutationCache.build(this, options).execute() // [!코드-]
- } // [!코드-]
```
또한 `query.setDefaultOptions`도 사용되지 않았기 때문에 제거되었습니다. `mutation.cancel`는 나가는 요청을 실제로 취소하지 않았기 때문에 제거되었습니다.

### `src/react` 디렉토리 이름이 `src/reactjs`로 변경되었습니다.

이전에 React Query에는 `react` 모듈에서 가져온 `react`라는 디렉터리가 있었습니다. 이로 인해 일부 Jest 구성에 문제가 발생하여 다음과 같은 테스트를 실행할 때 오류가 발생할 수 있습니다.

```
TypeError: Cannot read property 'createContext' of undefined
```
이름이 변경된 디렉토리를 사용하면 더 이상 문제가 되지 않습니다.

프로젝트에서 직접 `'react-query/react'`에서 항목을 가져오는 경우(`'react-query'`만 가져오는 것이 아니라) 가져오기를 업데이트해야 합니다.

```tsx
- import { QueryClientProvider } from 'react-query/react'; // [!코드-]
+ import { QueryClientProvider } from '@tanstack/react-query/reactjs'; // [!코드 ++]
```
## 새로운 기능 🚀

v4에는 다음과 같은 멋진 새로운 기능이 포함되어 있습니다.

### React 18 지원

React 18은 올해 초에 출시되었으며 v4는 이제 이에 대한 최고 수준의 지원과 함께 제공되는 새로운 동시 기능을 제공합니다.

### 적절한 오프라인 지원

v3에서는 React Query가 항상 queries 및 mutations를 실행했지만 다시 시도하려면 인터넷에 연결해야 한다고 가정했습니다. 이로 인해 몇 가지 혼란스러운 상황이 발생했습니다.

- 오프라인 상태이고 query를 마운트합니다. 로드 상태로 전환되고 요청이 실패하며 실제로 가져오는 중이 아니더라도 다시 온라인으로 전환될 때까지 로드 상태를 유지합니다.
- 마찬가지로 오프라인 상태이고 재시도가 꺼진 경우 query가 실행되고 실패하며 query는 오류 상태로 전환됩니다.
- 오프라인 상태이고 네트워크 연결이 반드시 필요하지 않은 query를 실행하려고 하지만(데이터 가져오기 이외의 용도로 React Query를 사용할 수_ 있기 때문에) 다른 이유로 실패합니다. 이제 다시 온라인에 접속할 때까지 해당 query가 일시 중지됩니다.
- 오프라인 상태에서는 창 포커스 다시 가져오기가 전혀 작동하지 않았습니다.

v4를 통해 React Query는 이러한 모든 문제를 해결하기 위해 새로운 `networkMode`를 도입합니다. 자세한 내용은 새로운 [네트워크 모드](network-mode.md)에 대한 전용 페이지를 읽어보세요.

### 기본적으로 Queries를 추적했습니다.

React Query는 기본적으로 query 속성을 "추적"하여 렌더링 최적화를 크게 향상시킵니다. 이 기능은 [v3.6.0](https://github.com/tannerlinsley/react-query/releases/tag/v3.6.0)부터 존재했으며 이제 v4의 기본 동작이 되었습니다.

### setQueryData로 업데이트 중단

[QueryClient](../../../reference/QueryClient.md#queryclientsetquerydata)을 사용하는 경우 이제 `undefined`를 반환하여 업데이트를 피할 수 있습니다. 이는 `undefined`가 `previousValue`로 제공되는 경우 유용합니다. 즉, 현재 캐시된 항목이 존재하지 않고 할 일을 전환하는 예에서와 같이 항목을 생성하고 싶지 않거나 생성할 수 없음을 의미합니다.

```tsx
queryClient.setQueryData(['todo', id], (previousTodo) =>
  previousTodo ? { ...previousTodo, done: true } : undefined,
)
```
### Mutation 캐시 가비지 수집

Mutations는 이제 queries처럼 자동으로 가비지 수집될 수도 있습니다. mutations의 기본 `cacheTime`도 5분으로 설정됩니다.

### 여러 공급자를 위한 사용자 정의 컨텍스트

이제 일치하는 `Provider`와 후크를 쌍으로 연결하기 위해 사용자 정의 컨텍스트를 지정할 수 있습니다. 이는 구성 요소 트리에 여러 개의 React Query `Provider` 인스턴스가 있을 수 있고 후크가 올바른 `Provider` 인스턴스를 사용하는지 확인해야 하는 경우 중요합니다.

예:

1. 데이터 패키지를 생성합니다.

```tsx
// 첫 번째 데이터 패키지: @my-scope/container-data

const context = React.createContext<QueryClient | undefined>(undefined)
const queryClient = new QueryClient()

export const useUser = () => {
  return useQuery(USER_KEY, USER_FETCHER, {
    context,
  })
}

export const ContainerDataProvider = ({
  children,
}: {
  children: React.ReactNode
}) => {
  return (
    <QueryClientProvider client={queryClient} context={context}>
      {children}
    </QueryClientProvider>
  )
}
```
2. 두 번째 데이터 패키지를 생성합니다.

```tsx
// 두 번째 데이터 패키지: @my-scope/my-comComponent-data

const context = React.createContext<QueryClient | undefined>(undefined)
const queryClient = new QueryClient()

export const useItems = () => {
  return useQuery(ITEMS_KEY, ITEMS_FETCHER, {
    context,
  })
}

export const MyComponentDataProvider = ({
  children,
}: {
  children: React.ReactNode
}) => {
  return (
    <QueryClientProvider client={queryClient} context={context}>
      {children}
    </QueryClientProvider>
  )
}
```
3. 애플리케이션에서 이 두 데이터 패키지를 사용하십시오.

```tsx
// 우리의 응용 프로그램

import { ContainerDataProvider, useUser } from "@my-scope/container-data";
import { AppDataProvider } from "@my-scope/app-data";
import { MyComponentDataProvider, useItems } from "@my-scope/my-component-data";

<ContainerDataProvider> // <-- 자체 React Query 공급자를 사용하여 컨테이너 데이터(예: "사용자")를 제공합니다.
  ...
  <AppDataProvider> // <-- 자체 React Query 공급자를 사용하여 앱 데이터를 제공합니다(이 예에서는 사용되지 않음)
    ...
      <MyComponentDataProvider> // <-- 자체 React Query 공급자를 사용하여 구성 요소 데이터(예: "항목")를 제공합니다.
        <MyComponent />
      </MyComponentDataProvider>
    ...
  </AppDataProvider>
  ...
</ContainerDataProvider>

// 위의 "DataProvider" 구성 요소가 제공하는 후크의 예:
const MyComponent = () => {
  const user = useUser() // <-- ContainerDataProvider에 지정된 컨텍스트를 사용합니다.
  const items = useItems() // <-- MyComponentDataProvider에 지정된 컨텍스트를 사용합니다.
  ...
}
```
