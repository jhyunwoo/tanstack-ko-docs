---
id: window-focus-refetching
title: 창 포커스 다시 가져오기
---




사용자가 애플리케이션을 떠났다가 돌아오고 query 데이터가 오래된 경우 **TanStack Query는 백그라운드에서 자동으로 새로운 데이터를 요청합니다**. `refetchOnWindowFocus` 옵션을 사용하여 전역적으로 또는 query별로 이를 비활성화할 수 있습니다.

#### 전역적으로 비활성화

[//]: # 'Example'

```tsx
//
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // 기본값: 참
    },
  },
})

function App() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}
```
[//]: # 'Example'

#### Per-Query 비활성화

[//]: # 'Example2'

```tsx
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  refetchOnWindowFocus: false,
})
```
[//]: # 'Example2'

## 사용자 정의 창 포커스 이벤트

드문 경우지만 재검증을 위해 TanStack Query를 트리거하는 자체 창 포커스 이벤트를 관리할 수 있습니다. 이를 위해 TanStack Query는 창에 포커스가 있을 때 실행되어야 하는 콜백을 제공하고 사용자가 자신의 이벤트를 설정할 수 있도록 하는 `focusManager.setEventListener` 함수를 제공합니다. `focusManager.setEventListener`를 호출하면 이전에 설정된 핸들러가 제거되고(대부분의 경우 기본 핸들러가 됨) 새 핸들러가 대신 사용됩니다. 예를 들어, 기본 처리기는 다음과 같습니다.

[//]: # 'Example3'

```tsx
focusManager.setEventListener((handleFocus) => {
  // 가시성 변경 듣기
  if (typeof window !== 'undefined' && window.addEventListener) {
    const visibilitychangeHandler = () => {
      handleFocus(document.visibilityState === 'visible')
    }
    window.addEventListener('visibilitychange', visibilitychangeHandler, false)
    return () => {
      // 새로운 핸들러가 설정되면 구독을 취소하세요.
      window.removeEventListener('visibilitychange', visibilitychangeHandler)
    }
  }
})
```
[//]: # 'Example3'
[//]: # 'ReactNative'

## React Native에서 포커스 관리하기

`window`의 이벤트 리스너 대신 React Native는 [`AppState` 모듈](https://reactnative.dev/docs/appstate#app-states)을 통해 포커스 정보를 제공합니다. `AppState` "변경" 이벤트를 사용하여 앱 상태가 "활성"으로 변경될 때 업데이트를 트리거할 수 있습니다.

```tsx
import { AppState } from 'react-native'
import { focusManager } from '@tanstack/react-query'

function onAppStateChange(status: AppStateStatus) {
  if (Platform.OS !== 'web') {
    focusManager.setFocused(status === 'active')
  }
}

useEffect(() => {
  const subscription = AppState.addEventListener('change', onAppStateChange)

  return () => subscription.remove()
}, [])
```
[//]: # 'ReactNative'

## 포커스 상태 관리

[//]: # 'Example4'

```tsx
import { focusManager } from '@tanstack/react-query'

// 기본 포커스 상태 재정의
focusManager.setFocused(true)

// 기본 초점 확인으로 대체
focusManager.setFocused(undefined)
```
[//]: # 'Example4'
