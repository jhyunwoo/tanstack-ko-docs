---
id: overview
title: 개요
---




Solid Query는 웹 애플리케이션에서 **서버 상태 가져오기, 캐싱, 동기화 및 업데이트**를 쉽게 만들어주는 TanStack Query의 공식 SolidJS 어댑터입니다.

## 동기 부여

SolidJS는 사용자 인터페이스 구축을 위한 빠르고 반응적이며 선언적인 라이브러리로 인기를 얻고 있습니다. 그것은 기본적으로 많은 기능을 갖추고 있습니다. `createSignal`, `createStore`와 같은 기본 요소는 클라이언트 상태를 관리하는 데 적합합니다. 그리고 다른 UI 라이브러리와 달리 SolidJS는 비동기 데이터 관리에 대한 강한 의견을 가지고 있습니다. `createResource` API는 SolidJS 앱에서 서버 상태를 처리하기 위한 훌륭한 기본 요소입니다. `resource`는 데이터가 로드 상태에 있을 때 `Suspense` 경계를 트리거하는 데 사용할 수 있는 특별한 종류의 신호입니다.

```tsx
import { createResource, ErrorBoundary, Suspense } from 'solid-js'
import { render } from 'solid-js/web'

function App() {
  const [repository] = createResource(async () => {
    const result = await fetch('https://api.github.com/repos/TanStack/query')
    if (!result.ok) throw new Error('Failed to fetch data')
    return result.json()
  })

  return (
    <div>
      <div>Static Content</div>
      {/* 가져오는 동안 발생한 오류는 ErrorBoundary에 의해 포착됩니다. */}
      <ErrorBoundary fallback={<div>Something went wrong!</div>}>
        {/* Suspense는 데이터를 가져오는 동안 로드 상태를 트리거합니다. */}
        <Suspense fallback={<div>Loading...</div>}>
          <div>{repository()?.updated_at}</div>
        </Suspense>
      </ErrorBoundary>
    </div>
  )
}

const root = document.getElementById('root')

render(() => <App />, root!)
```
정말 놀랍습니다! 몇 줄의 코드만으로 API에서 데이터를 가져오고 로드 및 오류 상태를 처리할 수 있습니다. 그러나 애플리케이션이 복잡해짐에 따라 서버 상태를 효과적으로 관리하려면 더 많은 기능이 필요합니다. **서버 상태는 클라이언트 상태와 완전히 다르기 때문입니다**. 우선 서버 상태는 다음과 같습니다.

- 귀하가 통제하거나 소유하지 않는 위치에 원격으로 지속됩니다.
- 가져오기 및 업데이트를 위한 비동기 API가 필요합니다.
- 공유 소유권을 암시하며 귀하도 모르게 다른 사람이 변경할 수 있습니다.
- 주의하지 않으면 애플리케이션이 "구식"이 될 수 있습니다.

애플리케이션에서 서버 상태의 특성을 파악하고 나면 **더 많은 문제가 발생하게 됩니다**. 예를 들면 다음과 같습니다.

- 캐싱... (아마도 프로그래밍에서 가장 어려운 일)
- 동일한 데이터에 대한 여러 요청을 단일 요청으로 중복 제거
- 백그라운드에서 "오래된" 데이터 업데이트
- 데이터가 "오래된" 시기를 파악
- 업데이트된 데이터를 최대한 빠르게 반영
- 페이지 매김 및 지연 로딩 데이터와 같은 성능 최적화
- 서버 상태의 메모리 및 가비지 수집 관리
- 구조적 공유를 통해 query 결과를 메모합니다.

**Solid Query**가 등장하는 곳입니다. 라이브러리는 `createResource`를 둘러싸며 서버 상태를 효과적으로 관리하기 위한 후크 및 유틸리티 세트를 제공합니다. 놀라울 정도로 잘 작동하며 별도의 구성 없이 바로 사용할 수 있으며 애플리케이션이 성장함에 따라 원하는 대로 사용자 정의할 수 있습니다**.

보다 기술적인 측면에서 Solid Query는 다음과 같은 가능성이 있습니다.

- 애플리케이션에서 **많은** 복잡하고 오해된 코드 줄을 제거하고 몇 줄의 Solid Query 논리로 대체할 수 있도록 도와주세요.
- 새로운 서버 상태 데이터 소스 연결에 대한 걱정 없이 애플리케이션을 더욱 쉽게 유지 관리하고 새로운 기능을 구축하기 쉽게 만듭니다.
- 애플리케이션의 속도와 반응성이 이전보다 더 빨라진 느낌을 주어 최종 사용자에게 직접적인 영향을 미칩니다.
- 잠재적으로 대역폭을 절약하고 메모리 성능을 높이는 데 도움이 됩니다.

## 얘기는 이쯤하고 코드를 보여주세요!

아래 예에서는 TanStack Query GitHub 프로젝트 자체에 대한 GitHub 통계를 가져오는 데 사용되는 가장 기본적이고 간단한 형식의 Solid Query를 볼 수 있습니다.

```tsx
import { ErrorBoundary, Suspense } from 'solid-js'
import {
  useQuery,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/solid-query'

function App() {
  const repositoryQuery = useQuery(() => ({
    queryKey: ['TanStack Query'],
    queryFn: async () => {
      const result = await fetch('https://api.github.com/repos/TanStack/query')
      if (!result.ok) throw new Error('Failed to fetch data')
      return result.json()
    },
    staleTime: 1000 * 60 * 5, // 5분
    throwOnError: true, // query가 실패하면 오류 발생
  }))

  return (
    <div>
      <div>Static Content</div>
      {/* 가져오는 동안 발생한 오류는 ErrorBoundary에 의해 포착됩니다. */}
      <ErrorBoundary fallback={<div>Something went wrong!</div>}>
        {/* Suspense는 데이터를 가져오는 동안 로드 상태를 트리거합니다. */}
        <Suspense fallback={<div>Loading...</div>}>
          {/* query의 `data` 속성은 SolidJS 리소스입니다.  
            따라서 Suspense와 함께 작동하고 즉시 전환됩니다! */}
          <div>{repositoryQuery.data?.updated_at}</div>
        </Suspense>
      </ErrorBoundary>
    </div>
  )
}

const root = document.getElementById('root')
const client = new QueryClient()

render(
  () => (
    <QueryClientProvider client={client}>
      <App />
    </QueryClientProvider>
  ),
  root!,
)
```
## 음, 같은 일을 하는 데 코드가 더 많은 것 같나요?

그렇습니다! 하지만 이 몇 줄의 코드로 완전히 새로운 가능성의 세계가 열립니다. 위의 예에서 query는 5분 동안 캐시됩니다. 즉, 5분 이내에 동일한 query를 사용하는 앱의 어느 위치에나 새 구성 요소가 마운트되면 데이터를 다시 가져오지 않고 대신 캐시된 데이터를 사용합니다. 이는 Solid Query가 기본적으로 제공하는 많은 기능 중 하나일 뿐입니다. 다른 기능은 다음과 같습니다:

- **자동 다시 가져오기**: Queries는 "부실" 상태가 되면 백그라운드에서 자동으로 다시 가져옵니다(`staleTime` 옵션에 따라 오래됨).
- **자동 캐싱**: Queries는 기본적으로 캐시되고 애플리케이션 전체에서 공유됩니다.
- **중복 제거 요청**: 여러 구성 요소가 동일한 query를 공유하고 한 번의 요청을 할 수 있습니다.
- **자동 가비지 수집**: Queries는 더 이상 필요하지 않을 때 가비지 수집됩니다.
- **창 포커스 다시 가져오기**: Queries는 애플리케이션에 다시 포커스가 맞춰지면 자동으로 다시 가져옵니다.
- **페이지 매김**: 페이지 매김 지원 내장
- **취소 요청**: 오래되었거나 원치 않는 요청을 자동으로 취소합니다.
- **폴링/실시간**: 간단한 `refetchInterval` 옵션을 사용하여 queries에 폴링 또는 실시간 업데이트를 쉽게 추가할 수 있습니다.
- **SSR 지원**: Solid Query는 서버 측 렌더링과 잘 작동합니다.
- **낙관적 업데이트**: 낙관적 업데이트로 캐시를 쉽게 업데이트하세요.
- **그리고 훨씬 더...**