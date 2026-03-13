---
id: NotifyManager
title: NotifyManager
---




`notifyManager`는 TanStack Query에서 예약 및 일괄 처리 콜백을 처리합니다.

다음 메서드를 공개합니다.

- [배치](#notifymanager배치)
- [batchCalls](#notifymanagerbatchcalls)
- [일정](#notifymanagers일정)
- [setNotifyFunction](#notifymanagersetnotifyfunction)
- [setBatchNotifyFunction](#notifymanagersetbatchnotifyfunction)
- [setScheduler](#notifymanagersetscheduler)

## `notifyManager.batch`

`batch`를 사용하면 전달된 콜백 내에서 예약된 모든 업데이트를 일괄 처리할 수 있습니다.
이는 주로 queryClient 업데이트를 최적화하기 위해 내부적으로 사용됩니다.

```ts
function batch<T>(callback: () => T): T
```
## `notifyManager.batchCalls`

`batchCalls`는 콜백을 가져와서 래핑하는 고차 함수입니다.
래핑된 함수에 대한 모든 호출은 콜백이 다음 배치에서 실행되도록 예약합니다.

```ts
type BatchCallsCallback<T extends Array<unknown>> = (...args: T) => void

function batchCalls<T extends Array<unknown>>(
  callback: BatchCallsCallback<T>,
): BatchCallsCallback<T>
```
## `notifyManager.schedule`

`schedule`는 다음 배치에서 실행될 기능을 예약합니다. 기본적으로 일괄 처리가 실행됩니다.
setTimeout을 사용하지만 이를 구성할 수 있습니다.

```ts
function schedule(callback: () => void): void
```
## `notifyManager.setNotifyFunction`

`setNotifyFunction`는 알림 기능을 재정의합니다. 이 함수는
실행되어야 할 때 콜백. 기본 informFunction은 이를 호출합니다.

예를 들어 테스트를 실행하는 동안 `React.act`로 알림을 래핑하는 데 사용할 수 있습니다.

```ts
import { notifyManager } from '@tanstack/react-query'
import { act } from 'react-dom/test-utils'

notifyManager.setNotifyFunction(act)
```
## `notifyManager.setBatchNotifyFunction`

`setBatchNotifyFunction`는 일괄 업데이트에 사용할 기능을 설정합니다.

프레임워크가 사용자 정의 일괄 처리 기능을 지원하는 경우 informManager.setBatchNotifyFunction을 호출하여 TanStack Query에 이를 알릴 수 있습니다.

예를 들어, 다음은 solid-query에서 배치 기능이 설정되는 방식입니다.

```ts
import { notifyManager } from '@tanstack/query-core'
import { batch } from 'solid-js'

notifyManager.setBatchNotifyFunction(batch)
```
## `notifyManager.setScheduler`

`setScheduler`는 다음 시간을 예약해야 하는 사용자 정의 콜백을 구성합니다.
일괄 실행됩니다. 기본 동작은 `setTimeout(callback, 0)`입니다.

```ts
import { notifyManager } from '@tanstack/react-query'

// 다음 마이크로태스크의 배치 예약
notifyManager.setScheduler(queueMicrotask)

// 다음 프레임이 렌더링되기 전에 배치 예약
notifyManager.setScheduler(requestAnimationFrame)

// 나중에 일괄 처리 예약
notifyManager.setScheduler((cb) => setTimeout(cb, 10))
```
