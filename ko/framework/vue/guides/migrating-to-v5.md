---
id: migrating-to-tanstack-query-5
title: TanStack Query v5로 마이그레이션
---




## 주요 변경 사항

v5는 주요 버전이므로 알아야 할 몇 가지 주요 변경 사항이 있습니다.

### 단일 서명, 단일 객체 지원

useQuery와 친구들은 TypeScript에서 많은 오버로드를 겪었습니다. 함수를 호출하는 방법이 다양했습니다. 이는 유지 관리가 어려웠을 뿐만 아니라 유형에 따라 옵션을 올바르게 생성하기 위해 첫 번째 및 두 번째 매개 변수가 어떤 유형인지 확인하기 위해 런타임 검사도 필요했습니다.

이제 우리는 객체 형식만 지원합니다.

```tsx
useQuery(key, fn, options) // [!코드-]
useQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
useInfiniteQuery(key, fn, options) // [!코드-]
useInfiniteQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
useMutation(fn, options) // [!코드-]
useMutation({ mutationFn, ...options }) // [!코드 ++]
useIsFetching(key, filters) // [!코드-]
useIsFetching({ queryKey, ...filters }) // [!코드 ++]
useIsMutating(key, filters) // [!코드-]
useIsMutating({ mutationKey, ...filters }) // [!코드 ++]
```

```tsx
queryClient.isFetching(key, filters) // [!코드-]
queryClient.isFetching({ queryKey, ...filters }) // [!코드 ++]
queryClient.ensureQueryData(key, filters) // [!코드-]
queryClient.ensureQueryData({ queryKey, ...filters }) // [!코드 ++]
queryClient.getQueriesData(key, filters) // [!코드-]
queryClient.getQueriesData({ queryKey, ...filters }) // [!코드 ++]
queryClient.setQueriesData(key, updater, filters, options) // [!코드-]
queryClient.setQueriesData({ queryKey, ...filters }, updater, options) // [!코드 ++]
queryClient.removeQueries(key, filters) // [!코드-]
queryClient.removeQueries({ queryKey, ...filters }) // [!코드 ++]
queryClient.resetQueries(key, filters, options) // [!코드-]
queryClient.resetQueries({ queryKey, ...filters }, options) // [!코드 ++]
queryClient.cancelQueries(key, filters, options) // [!코드-]
queryClient.cancelQueries({ queryKey, ...filters }, options) // [!코드 ++]
queryClient.invalidateQueries(key, filters, options) // [!코드-]
queryClient.invalidateQueries({ queryKey, ...filters }, options) // [!코드 ++]
queryClient.refetchQueries(key, filters, options) // [!코드-]
queryClient.refetchQueries({ queryKey, ...filters }, options) // [!코드 ++]
queryClient.fetchQuery(key, fn, options) // [!코드-]
queryClient.fetchQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
queryClient.prefetchQuery(key, fn, options) // [!코드-]
queryClient.prefetchQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
queryClient.fetchInfiniteQuery(key, fn, options) // [!코드-]
queryClient.fetchInfiniteQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
queryClient.prefetchInfiniteQuery(key, fn, options) // [!코드-]
queryClient.prefetchInfiniteQuery({ queryKey, queryFn, ...options }) // [!코드 ++]
```

```tsx
queryCache.find(key, filters) // [!코드-]
queryCache.find({ queryKey, ...filters }) // [!코드 ++]
queryCache.findAll(key, filters) // [!코드-]
queryCache.findAll({ queryKey, ...filters }) // [!코드 ++]
```
### `queryClient.getQueryData`는 이제 queryKey를 인수로만 허용합니다.

`queryClient.getQueryData` 인수는 `queryKey`만 허용하도록 변경되었습니다.

```tsx
queryClient.getQueryData(queryKey, filters) // [!코드-]
queryClient.getQueryData(queryKey) // [!코드 ++]
```
### `queryClient.getQueryState`는 이제 queryKey를 인수로만 허용합니다.

`queryClient.getQueryState` 인수는 `queryKey`만 허용하도록 변경되었습니다.

```tsx
queryClient.getQueryState(queryKey, filters) // [!코드-]
queryClient.getQueryState(queryKey) // [!코드 ++]
```
#### 코드모드

과부하 제거 마이그레이션을 더 쉽게 만들기 위해 v5에는 codemod가 함께 제공됩니다.

> codemod는 주요 변경 사항을 마이그레이션하는 데 도움이 되는 최선의 노력입니다. 생성된 코드를 철저하게 검토하세요! 또한, 코드 모드에서 발견할 수 없는 극단적인 경우도 있으므로 로그 출력을 계속 지켜봐 주시기 바랍니다.

`.js` 또는 `.jsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift@latest ./path/to/src/ \
  --extensions=js,jsx \
  --transform=./node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads/remove-overloads.cjs
```
`.ts` 또는 `.tsx` 파일에 대해 실행하려면 아래 명령을 사용하십시오.

```
npx jscodeshift@latest ./path/to/src/ \
  --extensions=ts,tsx \
  --parser=tsx \
  --transform=./node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads/remove-overloads.cjs
```
`TypeScript`의 경우 `tsx`를 파서로 사용해야 합니다. 그렇지 않으면 codemod가 제대로 적용되지 않습니다!

**참고:** codemod를 적용하면 코드 형식이 손상될 수 있으므로 codemod를 적용한 후 `prettier` 및/또는 `eslint`를 실행하는 것을 잊지 마세요!

codemod 작동 방식에 대한 몇 가지 참고 사항:

- 일반적으로 우리는 첫 번째 매개 변수가 개체 표현식이고 "queryKey" 또는 "mutationKey" 속성을 포함하는 행운의 사례를 찾고 있습니다(어떤 후크/메서드 호출이 변환되는지에 따라 다름). 이 경우 코드는 이미 새 서명과 일치하므로 codemod는 이를 건드리지 않습니다. 🎉
- 위의 조건이 충족되지 않으면 codemod는 첫 번째 매개변수가 배열 표현식인지 아니면 배열 표현식을 참조하는 식별자인지 확인합니다. 이 경우 codemod는 이를 객체 표현식에 넣고 첫 번째 매개변수가 됩니다.
- 객체 매개변수를 추론할 수 있는 경우 codemod는 기존 속성을 새로 생성된 속성에 복사하려고 시도합니다.
- codemod가 사용법을 추론할 수 없으면 콘솔에 메시지를 남깁니다. 메시지에는 파일 이름과 사용 행 번호가 포함됩니다. 이 경우 마이그레이션을 수동으로 수행해야 합니다.
- 변환 결과 오류가 발생하면 콘솔에도 메시지가 표시됩니다. 이 메시지는 예상치 못한 일이 발생했음을 알리는 메시지입니다. 마이그레이션을 수동으로 수행하십시오.

### useQuery(및 QueryObserver)의 콜백이 제거되었습니다.

`onSuccess`, `onError` 및 `onSettled`가 Queries에서 제거되었습니다. Mutations에 대해서는 손대지 않았습니다. 이 변경의 동기와 대신 수행할 작업은 [이 RFC](https://github.com/TanStack/query/discussions/5279)를 참조하세요.

### `refetchInterval` 콜백 함수는 `query`만 통과합니다.

이는 콜백이 호출되는 방법을 간소화하고(`refetchOnWindowFocus`, `refetchOnMount` 및 `refetchOnReconnect` 콜백은 모두 query만 전달함) 콜백이 `select`에 의해 변환된 데이터를 가져올 때 일부 입력 문제를 해결합니다.

```tsx
- refetchInterval: number | false | ((data: TData | undefined, query: Query) => number | false | undefined) // [!코드-]
+ refetchInterval: number | false | ((query: Query) => number | false | undefined) // [!코드 ++]
```
`query.state.data`를 사용하여 데이터에 계속 액세스할 수 있지만 `select`로 변환된 데이터는 아닙니다. 변환된 데이터에 액세스해야 하는 경우 `query.state.data`에서 변환을 다시 호출할 수 있습니다.

### `remove` 메서드가 useQuery에서 제거되었습니다.

이전에는 관찰자에게 알리지 않고 queryCache에서 query를 제거하는 데 사용된 메서드를 제거했습니다. 더 이상 필요하지 않은 데이터를 필수적으로 제거하는 데 가장 적합했습니다. 사용자가 로그아웃할 때.

그러나 query가 여전히 활성 상태인 동안 이 작업을 수행하는 것은 의미가 없습니다. 왜냐하면 다음 재렌더링 시 하드 로딩 상태를 트리거하기 때문입니다.

여전히 query를 제거해야 하는 경우 `queryClient.removeQueries({queryKey: key})`를 사용할 수 있습니다.

```tsx
const queryClient = useQueryClient()
const query = useQuery({ queryKey, queryFn })

query.remove() // [!코드-]
queryClient.removeQueries({ queryKey }) // [!코드 ++]
```
### 필요한 최소 TypeScript 버전은 이제 4.7입니다.

주로 유형 추론을 중심으로 중요한 수정 사항이 제공되었기 때문입니다. 자세한 내용은 이 [TypeScript 문제](https://github.com/microsoft/TypeScript/issues/43371)를 참조하세요.

### `isDataEqual` 옵션이 useQuery에서 제거되었습니다.

이전에는 query에 대한 해결 데이터로 이전 `data`(`true`)를 사용할지, 새 데이터(`false`)를 사용할지 여부를 나타내는 데 이 기능을 사용했습니다.

대신 `structuralSharing`에 함수를 전달하여 동일한 기능을 얻을 수 있습니다.

```tsx
import { replaceEqualDeep } from '@tanstack/react-query'

- isDataEqual: (oldData, newData) => customCheck(oldData, newData) // [!코드-]
+ structuralSharing: (oldData, newData) => customCheck(oldData, newData) ? oldData : replaceEqualDeep(oldData, newData) // [!코드 ++]
```
### 더 이상 사용되지 않는 맞춤 로거가 제거되었습니다.

사용자 정의 로거는 이미 4에서 더 이상 사용되지 않으며 이 버전에서는 제거되었습니다. 로깅은 사용자 정의 로거 전달이 필요하지 않은 개발 모드에서만 효과가 있었습니다.

### 지원되는 브라우저

보다 현대적이고 성능이 뛰어나며 작은 번들을 생성하기 위해 브라우저 목록을 업데이트했습니다. 요구 사항은 [여기](../../react/installation.md#requirements)에서 확인할 수 있습니다.

### 비공개 클래스 필드 및 메서드

TanStack Query에는 항상 클래스에 비공개 필드와 메서드가 있었지만 실제로는 비공개가 아니었습니다. `TypeScript`에서는 비공개였습니다. 이제 [ECMAScript Private 클래스 기능](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields)을 사용합니다. 즉, 해당 필드는 이제 진정한 비공개이며 런타임 시 외부에서 액세스할 수 없습니다.

### `cacheTime`의 이름을 `gcTime`로 바꿉니다.

거의 모든 사람들이 `cacheTime`를 잘못 알고 있습니다. "데이터가 캐시되는 시간"처럼 들리지만 이는 정확하지 않습니다.

`cacheTime`는 query가 아직 사용 중인 한 아무 작업도 수행하지 않습니다. query가 사용되지 않는 즉시 시작됩니다. 시간이 지나면 캐시가 커지는 것을 방지하기 위해 데이터가 "가비지 수집"됩니다.

`gc`는 "가비지 수집" 시간을 나타냅니다. 좀 더 기술적이지만 컴퓨터 과학 분야에서는 꽤 [잘 알려진 약어](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science))이기도 합니다.

```tsx
const MINUTE = 1000 * 60;

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
-      cacheTime: 10 * MINUTE, // [!코드-]
+      gcTime: 10 * MINUTE, // [!코드 ++]
    },
  },
})
```
### `useErrorBoundary` 옵션의 이름이 `throwOnError`로 변경되었습니다.

`useErrorBoundary` 옵션을 프레임워크에 더욱 독립적으로 만들고 후크에 대해 설정된 React 함수 접두사 "`use`" 및 "ErrorBoundary" 구성 요소 이름과의 혼동을 피하기 위해 해당 기능을 보다 정확하게 반영하기 위해 이름이 `throwOnError`로 변경되었습니다.

### TypeScript: `Error`는 이제 `unknown` 대신 오류의 기본 유형입니다.

JavaScript에서는 무엇이든 `throw`할 수 있지만(`unknown`가 가장 정확한 유형이 됨) 거의 항상 `Errors`(또는 `Error`의 하위 클래스)가 발생합니다. 이 변경으로 인해 대부분의 경우 TypeScript에서 `error` 필드 작업이 더 쉬워졌습니다.

오류가 아닌 것을 발생시키려면 이제 직접 일반을 설정해야 합니다.

```ts
useQuery<number, string>({
  queryKey: ['some-query'],
  queryFn: async () => {
    if (Math.random() > 0.5) {
      throw 'some error'
    }
    return 42
  },
})
```
다른 종류의 오류를 전역적으로 설정하는 방법은 [TypeScript](../../react/typescript.md#registering-a-global-error)를 참조하세요.

### eslint `prefer-query-object-syntax` 규칙이 제거되었습니다.

이제 지원되는 유일한 구문은 객체 구문이므로 이 규칙은 더 이상 필요하지 않습니다.

### `placeholderData` 식별 기능을 위해 `keepPreviousData`를 제거했습니다.

`keepPreviousData` 옵션과 `isPreviousData` 플래그는 `placeholderData` 및 `isPlaceholderData` 플래그와 거의 동일한 작업을 수행했기 때문에 제거했습니다.

`keepPreviousData`와 동일한 기능을 달성하기 위해 이전 query `data`를 항등 함수를 허용하는 `placeholderData`에 인수로 추가했습니다. 따라서 `placeholderData`에 ID 기능을 제공하거나 TanStack Query에 포함된 `keepPreviousData` 기능을 사용하면 됩니다.

> 여기서 참고할 점은 `useQueries`는 `placeholderData` 함수에서 `previousData`를 인수로 받지 않는다는 것입니다. 이는 배열에 전달된 queries의 동적 특성으로 인해 발생하며, 자리 표시자와 queryFn의 결과 모양이 다를 수 있습니다.

```tsx
import {
   useQuery,
+  keepPreviousData // [!코드 ++]
} from "@tanstack/react-query";

const {
   data,
-  isPreviousData, // [!코드-]
+  isPlaceholderData, // [!코드 ++]
} = useQuery({
  queryKey,
  queryFn,
- keepPreviousData: true, // [!코드-]
+ placeholderData: keepPreviousData // [!코드 ++]
});
```
TanStack Query의 맥락에서 항등 함수는 제공된 인수(즉, 데이터)를 항상 변경 없이 반환하는 함수를 나타냅니다.

```ts
useQuery({
  queryKey,
  queryFn,
  placeholderData: (previousData, previousQuery) => previousData, // `keepPreviousData`와 동일한 동작을 갖는 신원 함수
})
```
하지만 이 변경 사항에는 다음과 같은 몇 가지 주의 사항이 있습니다.

- `placeholderData`는 항상 `success` 상태에 들어가고, `keepPreviousData`는 이전 query 상태를 제공합니다. 데이터를 성공적으로 가져온 후 백그라운드 다시 가져오기 오류가 발생한 경우 해당 상태는 `error`일 수 있습니다. 그러나 오류 자체는 공유되지 않았으므로 `placeholderData`의 동작을 고수하기로 결정했습니다.
- `keepPreviousData`는 이전 데이터의 `dataUpdatedAt` 타임스탬프를 제공한 반면, `placeholderData`를 사용하면 `dataUpdatedAt`는 `0`에 유지됩니다. 해당 타임스탬프를 화면에 계속 표시하려는 경우 이는 성가실 수 있습니다. 그러나 `useEffect`를 사용하면 이 문제를 해결할 수 있습니다.

``ts
  const [updatedAt, setUpdatedAt] = useState(0)

const { 데이터, dataUpdatedAt } = useQuery({
    queryKey: ['프로젝트', 페이지],
    queryFn: () => fetchProjects(페이지),
  })

useEffect(() => {
    if (dataUpdatedAt > updateAt) {
      setUpdatedAt(dataUpdatedAt)
    }
  }, [dataUpdatedAt])
  ````

### 창 포커스 다시 가져오기는 더 이상 `focus` 이벤트를 수신하지 않습니다.

이제 `visibilitychange` 이벤트가 독점적으로 사용됩니다. 이는 `visibilitychange` 이벤트를 지원하는 브라우저만 지원하기 때문에 가능한 일입니다. 이는 [여기에 나열된](https://github.com/TanStack/query/pull/4805) 여러 문제를 해결합니다.

### 네트워크 상태는 더 이상 `navigator.onLine` 속성에 의존하지 않습니다.

`navigator.onLine`는 Chromium 기반 브라우저에서 제대로 작동하지 않습니다. 거짓 부정과 관련된 [많은 문제](https://bugs.chromium.org/p/chromium/issues/list?q=navigator.online)가 있으며 이로 인해 Queries가 `offline`로 잘못 표시됩니다.

이를 방지하기 위해 이제 항상 `online: true`로 시작하고 `online` 및 `offline` 이벤트만 수신하여 상태를 업데이트합니다.

이렇게 하면 거짓 부정 가능성이 줄어들지만, 인터넷 연결 없이도 작동할 수 있는 serviceWorkers를 통해 로드되는 오프라인 앱의 경우 거짓 긍정이 발생할 수 있습니다.

### 사용자 지정 `queryClient` 인스턴스를 위해 사용자 지정 `context` 소품을 제거했습니다.

v4에서는 사용자 정의 `context`를 모든 반응 query 후크에 전달할 수 있는 가능성을 도입했습니다. 이를 통해 MicroFrontends를 사용할 때 적절한 격리가 가능해졌습니다.

그러나 `context`는 반응 전용 기능입니다. `context`가 수행하는 작업은 `queryClient`에 대한 액세스 권한을 제공하는 것뿐입니다. 사용자 정의 `queryClient`를 직접 전달함으로써 동일한 격리를 달성할 수 있습니다.
그러면 다른 프레임워크가 프레임워크에 구애받지 않는 방식으로 동일한 기능을 가질 수 있게 됩니다.

```tsx
import { queryClient } from './my-client'

const { data } = useQuery(
  {
    queryKey: ['users', id],
    queryFn: () => fetch(...),
-   context: customContext // [!코드-]
  },
+  queryClient, // [!코드 ++]
)
```
### `maxPages`를 대신하여 `refetchPage`를 제거했습니다.

v4에서는 `refetchPage` 함수를 사용하여 무한 queries에 대해 다시 가져올 페이지를 정의할 수 있는 가능성을 도입했습니다.

그러나 모든 페이지를 다시 가져오면 UI 불일치가 발생할 수 있습니다. 또한 이 옵션은 다음과 같은 곳에서도 사용할 수 있습니다. `queryClient.refetchQueries`, 그러나 "정상" queries가 아닌 무한 queries에 대해서만 작업을 수행합니다.

v5에는 무한 queries에 대한 새로운 `maxPages` 옵션이 포함되어 query 데이터에 저장하고 다시 가져올 페이지 수를 제한합니다. 이 새로운 기능은 관련 문제 없이 `refetchPage` 페이지 기능에 대해 처음에 식별된 사용 사례를 처리합니다.

### 새로운 `dehydrate` API

`dehydrate`에 전달할 수 있는 옵션이 단순화되었습니다. Queries 및 Mutations는 항상 탈수됩니다(기본 함수 구현에 따라). 이 동작을 변경하려면 제거된 boolean 옵션 `dehydrateMutations` 및 `dehydrateQueries`를 사용하는 대신 `shouldDehydrateQuery` 또는 `shouldDehydrateMutation`와 동등한 함수를 구현할 수 있습니다. queries/mutations에 전혀 수분을 공급하지 않는 이전 동작을 얻으려면 `() => false`를 전달하세요.

```tsx
- dehydrateMutations?: boolean // [!코드-]
- dehydrateQueries?: boolean // [!코드-]
```
### 무한 queries 이제 `initialPageParam`가 필요합니다.

이전에는 `undefined`를 `queryFn`에 `pageParam`로 전달했으며 `queryFn` 함수 서명의 `pageParam` 매개 변수에 기본값을 할당할 수 있었습니다. 이는 직렬화할 수 없는 `queryCache`에 `undefined`를 저장하는 단점이 있었습니다.

대신 이제 명시적인 `initialPageParam`를 무한 query 옵션에 전달해야 합니다. 이는 첫 번째 페이지의 `pageParam`로 사용됩니다.

```tsx
useInfiniteQuery({
   queryKey,
-  queryFn: ({ pageParam = 0 }) => fetchSomething(pageParam), // [!코드-]
+  queryFn: ({ pageParam }) => fetchSomething(pageParam), // [!코드 ++]
+  initialPageParam: 0, // [!코드 ++]
   getNextPageParam: (lastPage) => lastPage.next,
})
```
### 무한 queries 수동 모드가 제거되었습니다.

이전에는 `pageParam` 값을 `fetchNextPage` 또는 `fetchPreviousPage`에 직접 전달하여 `getNextPageParam` 또는 `getPreviousPageParam`에서 반환되는 `pageParams`를 덮어쓸 수 있도록 허용했습니다. 이 기능은 다시 가져오기에서는 전혀 작동하지 않았으며 널리 알려지거나 사용되지 않았습니다. 이는 또한 이제 무한 queries에 `getNextPageParam`가 필요함을 의미합니다.

### `getNextPageParam` 또는 `getPreviousPageParam`에서 `null`를 반환하면 이제 사용 가능한 페이지가 더 이상 없음을 나타냅니다.

v4에서는 사용 가능한 추가 페이지가 없음을 나타내기 위해 명시적으로 `undefined`를 반환해야 했습니다. 우리는 `null`를 포함하도록 이 검사를 확대했습니다.

### 서버에서 재시도가 없습니다.

서버에서 `retry`는 이제 `3` 대신 `0`로 기본 설정됩니다. 프리페치의 경우 항상 `0` 재시도를 기본값으로 설정했지만, `suspense`가 활성화된 queries는 이제 서버에서도 직접 실행할 수 있으므로(React18 이후) 서버에서 전혀 재시도하지 않도록 해야 합니다.

### `status: loading`는 `status: pending`로 변경되었으며 `isLoading`는 `isPending`로 변경되었으며 `isInitialLoading`는 이제 `isLoading`로 이름이 변경되었습니다.

`loading` 상태는 `pending`로 이름이 바뀌었고, 마찬가지로 파생된 `isLoading` 플래그도 `isPending`로 이름이 바뀌었습니다.

mutations의 경우에도 `status`가 `loading`에서 `pending`로 변경되었고 `isLoading` 플래그가 `isPending`로 변경되었습니다.

마지막으로, 새로 파생된 `isLoading` 플래그가 `isPending && isFetching`로 구현된 queries에 추가되었습니다. 이는 `isLoading`와 `isInitialLoading`가 동일하지만 `isInitialLoading`는 현재 더 이상 사용되지 않으며 다음 주요 버전에서 제거될 것임을 의미합니다.

이 변경의 이유를 이해하려면 [v5 로드맵 토론](https://github.com/TanStack/query/discussions/4252)을 확인하세요.

### `hashQueryKey`가 `hashKey`로 이름이 변경되었습니다.

이는 또한 mutation 키를 해시하고 `useIsMutating` 및 `useMutationState`의 `predicate` 함수 내에서 사용될 수 있기 때문에 mutations가 전달됩니다.



## Vue Query 주요 변경 사항

### `useQueries` 컴포저블은 `reactive` 대신 `ref`를 반환합니다.

Vue 2와의 호환성을 수정하기 위해 이제 `useQueries` 컴포저블은 `ref`에 래핑된 `queries` 배열을 반환합니다.
이전에는 `reactive`가 반환되어 여러 문제가 발생했습니다.

- 사용자는 반응성을 잃어 반환 값을 확산시킬 수 있습니다.
- 반환 값에 사용된 `readonly` 래퍼가 Vue 2 반응성 감지 메커니즘을 중단했습니다. 이는 Vue 2.6에서는 조용한 문제였지만 Vue 2.7에서는 오류로 나타났습니다.
- Vue 2는 `reactive`의 루트 값으로 배열을 지원하지 않습니다.

이번 변경으로 이러한 문제가 모두 해결되었습니다.

또한 이는 모든 값을 `refs`로 반환하는 다른 컴포저블과 `useQueries`를 정렬합니다.

### 이제 Vue v3.3이 필요합니다

Vue 릴리스 이후 새로운 기능을 제공하려면 이제 Vue 3이 최소한 v3.3 버전이어야 합니다.
Vue 2.x에 대한 요구 사항은 변경되지 않았습니다.



## 새로운 기능 🚀

v5에는 다음과 같은 새로운 기능도 포함되어 있습니다.

### 단순화된 낙관적 업데이트

`useMutation`에서 반환된 `variables`를 활용하여 낙관적 업데이트를 수행하는 새롭고 간단한 방법이 있습니다.

```tsx
const queryInfo = useTodos()
const addTodoMutation = useMutation({
  mutationFn: (newTodo: string) => axios.post('/api/data', { text: newTodo }),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
})

if (queryInfo.data) {
  return (
    <ul>
      {queryInfo.data.items.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
      {addTodoMutation.isPending && (
        <li key={String(addTodoMutation.submittedAt)} style={{ opacity: 0.5 }}>
          {addTodoMutation.variables}
        </li>
      )}
    </ul>
  )
}
```
여기서는 데이터를 캐시에 직접 쓰는 대신 mutation가 실행 중일 때 UI가 표시되는 방식만 변경합니다. 이는 낙관적 업데이트를 표시해야 하는 위치가 한 곳뿐인 경우 가장 잘 작동합니다. 자세한 내용은 [낙관적 업데이트 문서](../../react/guides/optimistic-updates.md)를 참조하세요.

### 새로운 maxPages 옵션이 포함된 제한적, 무한 Queries

무한 queries는 무한 스크롤이나 페이지 매김이 필요할 때 유용합니다.
그러나 더 많은 페이지를 가져오면 더 많은 메모리를 소비하게 되고 모든 페이지가 순차적으로 다시 가져오기 때문에 query 다시 가져오기 프로세스도 느려집니다.

버전 5에는 무한 queries를 위한 새로운 `maxPages` 옵션이 있습니다. 이를 통해 개발자는 query 데이터에 저장되고 나중에 다시 가져오는 페이지 수를 제한할 수 있습니다.
전달하고자 하는 UX 및 리페치 성능에 따라 `maxPages` 값을 조정할 수 있습니다.

무한 목록은 양방향이어야 하며 이를 위해서는 `getNextPageParam` 및 `getPreviousPageParam`를 모두 정의해야 합니다.

### Infinite Queries는 여러 페이지를 미리 가져올 수 있습니다.

Infinite Queries는 일반 Queries처럼 프리패치할 수 있습니다. 기본적으로 Query의 첫 번째 페이지만 프리페치되어 지정된 QueryKey에 저장됩니다. 두 페이지 이상을 프리페치하려면 `pages` 옵션을 사용할 수 있습니다. 자세한 내용은 [프리페칭 가이드](../../react/guides/prefetching.md)를 읽어보세요.

### `useQueries`를 위한 새로운 `combine` 옵션

자세한 내용은 [useQueries](../../react/reference/useQueries.md#combine)를 참조하세요.

### 실험적 `fine grained storage persister`

자세한 내용은 [experimental_createQueryPersister](../../react/plugins/createPersister.md)를 참조하세요.



### `injectionContext`에서 `vue-query` 컴포저블을 실행하는 기능

이전에는 `vue-query` 컴포저블은 구성요소의 `setup` 기능 내에서만 실행할 수 있었습니다.  
사용자가 구성 가능한 옵션으로 `queryClient`를 제공하는 경우 해당 후크를 어디에서나 실행할 수 있도록 탈출구가 마련되어 있었습니다.

이제 `injectionContext`를 지원하는 모든 함수에서 `vue-query` 컴포저블을 사용할 수 있습니다. 전. 라우터 네비게이션 가드.
이 새로운 기능을 사용할 때 `vue-query` 컴포저블이 `effectScope` 내에서 실행되고 있는지 확인하세요. 그렇지 않으면 메모리 누수가 발생할 수 있습니다.
사용자에게 잠재적인 오용을 알리기 위해 `dev-only` 경고를 추가했습니다.

