---
id: createPersister
title: experimental_createPersister
---




## 설치

이 유틸리티는 별도의 패키지로 제공되며 `'@tanstack/query-persist-client-core'` 가져오기에서 사용할 수 있습니다.

```bash
npm install @tanstack/query-persist-client-core
```
또는

```bash
pnpm add @tanstack/query-persist-client-core
```
또는

```bash
yarn add @tanstack/query-persist-client-core
```
또는

```bash
bun add @tanstack/query-persist-client-core
```
> 참고: 이 유틸리티는 `@tanstack/preact-query-persist-client` 패키지에도 포함되어 있으므로 해당 패키지를 사용하는 경우 별도로 설치할 필요가 없습니다.

## 용법

- `experimental_createQueryPersister` 기능 가져오기
- 새로운 `experimental_createQueryPersister` 생성
  - `AsyncStorage` 인터페이스를 준수하는 `storage`를 전달할 수 있습니다. 아래 예에서는 React Native의 비동기 저장소를 사용합니다.
- 해당 `persister`를 Query에 옵션으로 전달하세요. 이 작업은 `QueryClient`의 `defaultOptions` 또는 `useQuery` 후크 인스턴스에 전달하여 수행할 수 있습니다.
  - 이 `persister`를 `defaultOptions`로 전달하면 모든 queries가 제공된 `storage`에 유지됩니다. `filters`를 전달하여 이 범위를 추가로 좁힐 수도 있습니다. `persistClient` 플러그인과 달리 이는 전체 query 클라이언트를 단일 항목으로 유지하지 않고 각 query를 별도로 유지합니다. 키로는 query 해시가 사용됩니다.
  - 이 `persister`를 단일 `useQuery` 후크에 제공하면 이 Query만 유지됩니다.
- 참고: `queryClient.setQueryData()` 작업은 지속되지 않습니다. 즉, query가 무효화되기 전에 낙관적 업데이트를 수행하고 페이지를 새로 고치면 query 데이터에 대한 변경 사항이 손실됩니다. https://github.com/TanStack/query/issues/6310을 참조하세요.

이렇게 하면 전체 `QueryClient`를 저장할 필요가 없지만 애플리케이션에 유지할 가치가 있는 것을 선택합니다. 각 query는 느리게 복원되고(Query가 처음 사용될 때) 지속되므로(`queryFn`를 실행할 때마다) 조절이 필요하지 않습니다. `staleTime`도 Query를 복원한 후 존중되므로 데이터가 `stale`로 간주되면 복원 후 즉시 다시 가져옵니다. 데이터가 `fresh`인 경우 `queryFn`는 실행되지 않습니다.

메모리에서 Query를 수집하는 가비지는 지속된 데이터에 **영향을 주지 않습니다**. 이는 Queries가 더 짧은 시간 동안 메모리에 유지되어 **메모리 효율성**을 높일 수 있음을 의미합니다. 다음에 사용하면 영구 저장소에서 다시 복원됩니다.

```tsx
import AsyncStorage from '@react-native-async-storage/async-storage'
import { QueryClient } from '@tanstack/preact-query'
import { experimental_createQueryPersister } from '@tanstack/query-persist-client-core'

const persister = experimental_createQueryPersister({
  storage: AsyncStorage,
  maxAge: 1000 * 60 * 60 * 12, // 12시간
})

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 30, // 30초
      persister: persister.persisterFn,
    },
  },
})
```
### 적응된 기본값

`createPersister` 플러그인은 기술적으로 `queryFn`를 래핑하므로 `queryFn`가 실행되지 않으면 복원되지 않습니다. 이러한 방식으로 Query와 네트워크 사이의 캐싱 계층 역할을 합니다. 따라서 지속자가 사용될 때 `networkMode`는 기본적으로 `'offlineFirst'`로 설정되므로 네트워크 연결이 없더라도 영구 저장소에서 복원할 수도 있습니다.

## 추가 유틸리티

`experimental_createQueryPersister`를 호출하면 사용자 영역 기능을 더 쉽게 구현할 수 있도록 `persisterFn` 외에 추가 유틸리티가 반환됩니다.

### `persistQueryByKey(queryKey: QueryKey, queryClient: QueryClient): Promise<void>`

이 함수는 지속기를 생성할 때 정의된 스토리지 및 키에 `Query`를 유지합니다.  
이 유틸리티는 무효화를 기다리지 않고 스토리지에 대한 낙관적 업데이트를 유지하기 위해 `setQueryData`와 함께 사용될 수 있습니다.

```tsx
const persister = experimental_createQueryPersister({
  storage: AsyncStorage,
  maxAge: 1000 * 60 * 60 * 12, // 12시간
})

const queryClient = useQueryClient()

useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    ...
    // 낙관적으로 새 값으로 업데이트
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo])
    // 그리고 이를 스토리지에 유지합니다.
    persister.persistQueryByKey(['todos'], queryClient)
    ...
  },
})
```
### `retrieveQuery<T>(queryHash: string): Promise<T | undefined>`

이 함수는 `queryHash`로 지속된 query를 검색하려고 시도합니다.  
`query`가 `expired`, `busted` 또는 `malformed`인 경우 대신 스토리지에서 제거되고 `undefined`가 반환됩니다.

### `persisterGc(): Promise<void>`

이 기능은 `expired`, `busted` 또는 `malformed` 항목에서 저장소를 산발적으로 정리하는 데 사용할 수 있습니다.

이 기능이 작동하려면 스토리지에서 `key-value tuple array`를 반환하는 `entries` 메서드를 노출해야 합니다.  
예를 들어 `localStorage`의 경우 `Object.entries(localStorage)` 또는 `idb-keyval`의 `entries`입니다.

### `restoreQueries(queryClient: QueryClient, filters): Promise<void>`

이 기능은 현재 지속기에 저장된 queries를 복원하는 데 사용할 수 있습니다.  
예를 들어 앱이 오프라인 모드에서 시작되거나 이전 세션의 전체 또는 특정 데이터만 중간 `loading` 상태 없이 즉시 사용 가능하도록 하려는 경우입니다.

필터 개체는 다음 속성을 지원합니다.

- `queryKey?: QueryKey`
  - 일치시킬 query 키를 정의하려면 이 속성을 설정합니다.
- `exact?: boolean`
  - queries를 query 키로 포괄적으로 검색하지 않으려면 `exact: true` 옵션을 전달하여 전달한 정확한 query 키가 있는 query만 반환할 수 있습니다.

이 기능이 작동하려면 스토리지에서 `key-value tuple array`를 반환하는 `entries` 메서드를 노출해야 합니다.  
예를 들어 `localStorage`의 경우 `Object.entries(localStorage)` 또는 `idb-keyval`의 `entries`입니다.

### `removeQueries(filters): Promise<void>`

`queryClient.removeQueries`를 사용하는 경우 데이터는 지속기에 남아 있으므로 별도로 제거해야 합니다.
이 함수는 현재 지속기에 저장되어 있는 queries를 제거하는 데 사용할 수 있습니다.

필터 개체는 다음 속성을 지원합니다.

- `queryKey?: QueryKey`
  - 일치시킬 query 키를 정의하려면 이 속성을 설정합니다.
- `exact?: boolean`
  - queries를 query 키로 포괄적으로 검색하지 않으려면 `exact: true` 옵션을 전달하여 전달한 정확한 query 키가 있는 query만 반환할 수 있습니다.

이 기능이 작동하려면 스토리지에서 `key-value tuple array`를 반환하는 `entries` 메서드를 노출해야 합니다.  
예를 들어 `localStorage`의 경우 `Object.entries(localStorage)` 또는 `idb-keyval`의 `entries`입니다.

## API

### `experimental_createQueryPersister`

```tsx
experimental_createQueryPersister(options: StoragePersisterOptions)
```
#### `Options`

```tsx
export interface StoragePersisterOptions {
  /* * 캐시에서 항목을 설정하고 검색하는 데 사용되는 스토리지 클라이언트입니다.
   * '정의되지 않음'의 SSR 패스의 경우. */
  storage: AsyncStorage | Storage | undefined | null
  /* *
   * 데이터를 스토리지에 직렬화하는 방법.
   * @default `JSON.stringify` */
  serialize?: (persistedQuery: PersistedQuery) => string
  /* *
   * 저장소에서 데이터를 역직렬화하는 방법.
   * @default `JSON.parse` */
  deserialize?: (cachedString: string) => PersistedQuery
  /* *
   * 기존 캐시를 강제로 무효화하는 데 사용할 수 있는 고유 문자열,
   * 동일한 버스터 스트링을 공유하지 않는 경우 */
  buster?: string
  /* *
   * 캐시의 최대 허용 기간(밀리초)입니다.
   * 이보다 오래된 지속형 캐시가 발견된 경우
   * 시간이 지나면 폐기됩니다.
   * @default 24시간 */
  maxAge?: number
  /* *
   * 저장소 키에 사용되는 접두사입니다.
   * 스토리지 키는 `prefix-queryHash` 형식의 접두사와 query 해시의 조합입니다. */
  prefix?: string
  /* *
   * 'true'로 설정하면 데이터가 오래된 경우 query가 성공적인 query 복원 시 다시 가져옵니다.
   * 'false'로 설정하면 query 복원 성공 시 query가 다시 가져오지 않습니다.
   * `'항상'`으로 설정된 경우 query는 성공적인 query 복원 시 항상 다시 가져옵니다.
   * 기본값은 `true`입니다. */
  refetchOnRestore?: boolean | 'always'
  /* *
   * 지속되어야 하는 Queries의 범위를 좁히는 필터입니다. */
  filters?: QueryFilters
}

interface AsyncStorage<TStorageValue = string> {
  getItem: (key: string) => MaybePromise<TStorageValue | undefined | null>
  setItem: (key: string, value: TStorageValue) => MaybePromise<unknown>
  removeItem: (key: string) => MaybePromise<void>
  entries?: () => MaybePromise<Array<[key: string, value: TStorageValue]>>
}
```
기본 옵션은 다음과 같습니다.

```tsx
{
  prefix = 'tanstack-query',
  maxAge = 1000 * 60 * 60 * 24,
  serialize = JSON.stringify,
  deserialize = JSON.parse,
  refetchOnRestore = true,
}
```
