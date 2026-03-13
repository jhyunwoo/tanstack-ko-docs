---
id: react-native
title: 리액트 네이티브
---




React Query는 React Native와 함께 즉시 작동하도록 설계되었습니다.

## DevTools 지원

React Native DevTools 통합에 사용할 수 있는 몇 가지 옵션이 있습니다.

1. **네이티브 macOS 앱**: 모든 js 기반 애플리케이션에서 React Query를 디버깅하기 위한 타사 앱:
   https://github.com/LovesWorking/rn-better-dev-tools

2. **Flipper 플러그인**: Flipper 사용자를 위한 타사 플러그인:
   https://github.com/bgaleotti/react-query-native-devtools

3. **Reactotron 플러그인**: Reactotron 사용자를 위한 타사 플러그인:
   https://github.com/hsndmr/reactotron-react-query

## 온라인 상태 관리

React Query는 이미 웹 브라우저에서 다시 연결 시 자동 다시 가져오기를 지원합니다.
React Native에 이 동작을 추가하려면 아래 예와 같이 React Query `onlineManager`를 사용해야 합니다.

```tsx
import NetInfo from '@react-native-community/netinfo'
import { onlineManager } from '@tanstack/react-query'

onlineManager.setEventListener((setOnline) => {
  return NetInfo.addEventListener((state) => {
    setOnline(!!state.isConnected)
  })
})
```
또는

```tsx
import { onlineManager } from '@tanstack/react-query'
import * as Network from 'expo-network'

onlineManager.setEventListener((setOnline) => {
  let initialised = false

  const eventSubscription = Network.addNetworkStateListener((state) => {
    initialised = true
    setOnline(!!state.isConnected)
  })

  Network.getNetworkStateAsync()
    .then((state) => {
      if (!initialised) {
        setOnline(!!state.isConnected)
      }
    })
    .catch(() => {
      // getNetworkStateAsync는 일부 플랫폼/SDK 버전에서 거부할 수 있습니다.
    })

  return eventSubscription.remove
})
```
## 앱 포커스 다시 가져오기

`window`의 이벤트 리스너 대신 React Native는 [`AppState` 모듈](https://reactnative.dev/docs/appstate#app-states)을 통해 포커스 정보를 제공합니다. `AppState` "변경" 이벤트를 사용하여 앱 상태가 "활성"으로 변경될 때 업데이트를 트리거할 수 있습니다.

```tsx
import { useEffect } from 'react'
import { AppState, Platform } from 'react-native'
import type { AppStateStatus } from 'react-native'
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
## 화면 초점 새로 고침

어떤 상황에서는 React Native Screen에 다시 초점이 맞춰지면 query를 다시 가져오고 싶을 수도 있습니다.
이 사용자 정의 후크는 화면에 다시 초점이 맞춰지면 **모든 활성 상태의 오래된 queries**를 다시 가져옵니다.

```tsx
import React from 'react'
import { useFocusEffect } from '@react-navigation/native'
import { useQueryClient } from '@tanstack/react-query'

export function useRefreshOnFocus() {
  const queryClient = useQueryClient()
  const firstTimeRef = React.useRef(true)

  useFocusEffect(
    React.useCallback(() => {
      if (firstTimeRef.current) {
        firstTimeRef.current = false
        return
      }

      // 오래된 활성 queries를 모두 다시 가져옵니다.
      queryClient.refetchQueries({
        queryKey: ['posts'],
        stale: true,
        type: 'active',
      })
    }, [queryClient]),
  )
}
```
위 코드에서는 `useFocusEffect`가 화면 포커스 외에 마운트 시 콜백을 호출하기 때문에 첫 번째 포커스(화면이 처음 마운트될 때)를 건너뜁니다.

## 초점이 맞지 않는 화면에서 queries를 비활성화합니다.

화면의 초점이 맞지 않는 동안 특정 queries가 "라이브" 상태로 유지되는 것을 원하지 않으면 useQuery에서 구독된 소품을 사용할 수 있습니다. 이 소품을 사용하면 query가 업데이트 구독 상태를 유지할지 여부를 제어할 수 있습니다. React Navigation의 useIsFocused와 결합하면 화면에 초점이 맞지 않을 때 queries에서 원활하게 구독을 취소할 수 있습니다.

사용 예:

```tsx
import React from 'react'
import { useIsFocused } from '@react-navigation/native'
import { useQuery } from '@tanstack/react-query'
import { Text } from 'react-native'

function MyComponent() {
  const isFocused = useIsFocused()

  const { dataUpdatedAt } = useQuery({
    queryKey: ['key'],
    queryFn: () => fetch(...),
    subscribed: isFocused,
  })

  return <Text>DataUpdatedAt: {dataUpdatedAt}</Text>
}
```
구독이 false이면 query는 업데이트 구독을 취소하고 다시 렌더링을 트리거하거나 해당 화면에 대한 새 데이터를 가져오지 않습니다. 다시 true가 되면(예: 화면에 초점이 다시 맞춰지면) query는 다시 구독하고 최신 상태를 유지합니다.