---
id: query-retries
title: Query 재시도
---




`useQuery` query가 실패할 때(query 함수에서 오류가 발생함) 해당 query의 요청이 최대 연속 재시도 횟수에 도달하지 않은 경우 TanStack Query는 자동으로 query를 재시도합니다(기본값: `3`) 또는 재시도 허용 여부를 확인하는 기능이 제공됩니다.

전역 수준과 개별 query 수준 모두에서 재시도를 구성할 수 있습니다.

- `retry = false`를 설정하면 재시도가 비활성화됩니다.
- `retry = 6`를 설정하면 함수에서 발생한 최종 오류가 표시되기 전에 실패한 요청을 6번 재시도합니다.
- `retry = true`를 설정하면 실패한 요청을 무한히 재시도합니다.
- `retry = (failureCount, error) => ...`를 설정하면 요청이 실패한 이유에 따라 사용자 정의 논리를 사용할 수 있습니다. 첫 번째 재시도에서는 `failureCount`가 `0`에서 시작됩니다.



> 서버에서는 기본적으로 `0`로 재시도하여 서버 렌더링을 최대한 빠르게 만듭니다.




```tsx
import { useQuery } from '@tanstack/preact-query'

// 특정 query가 특정 횟수만큼 재시도하도록 합니다.
const result = useQuery({
  queryKey: ['todos', 1],
  queryFn: fetchTodoListPage,
  retry: 10, // 오류가 표시되기 전에 실패한 요청을 10번 재시도합니다.
})
```



> 정보: `error` 속성의 내용은 마지막 재시도 시도까지 `useQuery`의 `failureReason` 응답 속성의 일부가 됩니다. 따라서 위의 예에서 오류 내용은 처음 9번의 재시도(전체 10번 시도)에 대해 `failureReason` 속성의 일부가 되며 모든 재시도 후에도 오류가 지속되면 마지막 시도 이후 `error` 속성의 일부가 됩니다.

## 재시도 지연

기본적으로 TanStack Query의 재시도는 요청이 실패한 직후에 발생하지 않습니다. 표준에 따라 각 재시도에 백오프 지연이 점차적으로 적용됩니다.

기본 `retryDelay`는 시도할 때마다 두 배(`1000`ms에서 시작)로 설정되지만 30초를 초과하지 않습니다.



```tsx
// 모든 queries에 대해 구성
import {
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/preact-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
})

function App() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}
```



권장되지는 않지만 공급자 및 개별 query 옵션 모두에서 `retryDelay` 함수/정수를 재정의할 수 있습니다. 함수 대신 정수로 설정하면 지연 시간은 항상 같은 시간이 됩니다.



```tsx
const result = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodoList,
  retryDelay: 1000, // 재시도 횟수에 관계없이 항상 재시도를 위해 1000ms를 기다립니다.
})
```



## 백그라운드 재시도 동작

`refetchInterval`를 `refetchIntervalInBackground: true`와 함께 사용하는 경우 브라우저 탭이 비활성화되면 재시도가 일시 중지됩니다. 이는 재시도가 일반 다시 가져오기와 동일한 포커스 동작을 따르기 때문에 발생합니다.

백그라운드에서 지속적인 재시도가 필요한 경우 재시도를 비활성화하고 사용자 정의 다시 가져오기 전략을 구현하는 것이 좋습니다.



```tsx
const result = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  refetchInterval: (query) => {
    // 오류 상태일 때 더 자주 다시 가져오기
    return query.state.status === 'error' ? 5000 : 30000
  },
  refetchIntervalInBackground: true,
  retry: false, // 내장된 재시도 비활성화
})
```



이 접근 방식을 사용하면 백그라운드에서 다시 가져오기를 활성화하면서 재시도 타이밍을 수동으로 제어할 수 있습니다.