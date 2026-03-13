---
id: query-cancellation
title: Query 취소
---




TanStack Query는 [`AbortSignal` 인스턴스](https://developer.mozilla.org/docs/Web/API/AbortSignal)와 함께 각 query 함수를 제공합니다. query가 오래되거나 비활성화되면 이 `signal`가 중단됩니다. 이는 모든 queries를 취소할 수 있으며 원하는 경우 query 함수 내에서 취소에 응답할 수 있음을 의미합니다. 가장 좋은 점은 자동 취소의 모든 이점을 얻으면서 일반 async/await 구문을 계속 사용할 수 있다는 것입니다.

`AbortController` API는 [대부분의 런타임 환경](https://developer.mozilla.org/docs/Web/API/AbortController#browser_compatibility)에서 사용할 수 있지만 런타임 환경에서 이를 지원하지 않는 경우 폴리필을 제공해야 합니다. [여러 가지 사용 가능](https://www.npmjs.com/search?q=abortcontroller%20polyfill)이 있습니다.

## 기본 동작

기본적으로 Promise이 해결되기 전에 마운트 해제되거나 사용되지 않는 queries는 취소되지 _않습니다_. 이는 Promise가 해결된 후 결과 데이터를 캐시에서 사용할 수 있음을 의미합니다. 이는 query 수신을 시작했지만 완료되기 전에 구성요소를 마운트 해제한 경우에 유용합니다. 구성 요소를 다시 마운트하고 query가 아직 가비지 수집되지 않은 경우 데이터를 사용할 수 있습니다.

그러나 `AbortSignal`를 사용하면 Promise가 취소되므로(예: 가져오기 중단) Query도 취소해야 합니다. query를 취소하면 상태가 이전 상태로 _복귀_됩니다.

## `fetch` 사용하기



```tsx
const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: async ({ signal }) => {
    const todosResponse = await fetch('/todos', {
      // 신호를 원 페치로 전달
      signal,
    })
    const todos = await todosResponse.json()

    const todoDetails = todos.map(async ({ details }) => {
      const response = await fetch(details, {
        // 아니면 여러 사람에게 전달하세요.
        signal,
      })
      return response.json()
    })

    return Promise.all(todoDetails)
  },
}))
```



## `axios` 사용 [v0.22.0+](https://github.com/axisios/axisios/releases/tag/v0.22.0)



```tsx
import axios from 'axios'

const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) =>
    axios.get('/todos', {
      // 'axios'에 신호 전달
      signal,
    }),
}))
```



### v0.22.0보다 낮은 버전의 `axios` 사용



```tsx
import axios from 'axios'

const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) => {
    // 이 요청에 대한 새 CancelToken 소스를 만듭니다.
    const CancelToken = axios.CancelToken
    const source = CancelToken.source()

    const promise = axios.get('/todos', {
      // 요청에 소스 토큰을 전달하세요.
      cancelToken: source.token,
    })

    // TanStack Query가 중단 신호를 보내는 경우 요청을 취소하세요.
    signal?.addEventListener('abort', () => {
      source.cancel('Query was cancelled by TanStack Query')
    })

    return promise
  },
}))
```



## `XMLHttpRequest` 사용하기



```tsx
const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) => {
    return new Promise((resolve, reject) => {
      var oReq = new XMLHttpRequest()
      oReq.addEventListener('load', () => {
        resolve(JSON.parse(oReq.responseText))
      })
      signal?.addEventListener('abort', () => {
        oReq.abort()
        reject()
      })
      oReq.open('GET', '/todos')
      oReq.send()
    })
  },
}))
```



## `graphql-request` 사용하기

`AbortSignal`는 클라이언트 `request` 메소드에서 설정할 수 있습니다.



```tsx
const client = new GraphQLClient(endpoint)

const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) => {
    client.request({ document: query, signal })
  },
}))
```



## v4.0.0 미만 버전의 `graphql-request` 사용

`AbortSignal`는 `GraphQLClient` 생성자에서 설정할 수 있습니다.



```tsx
const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: ({ signal }) => {
    const client = new GraphQLClient(endpoint, {
      signal,
    })
    return client.request(query, variables)
  },
}))
```



## 수동 취소

query를 수동으로 취소할 수도 있습니다. 예를 들어 요청을 완료하는 데 오랜 시간이 걸리는 경우 사용자가 취소 버튼을 클릭하여 요청을 중지하도록 허용할 수 있습니다. 이렇게 하려면 `queryClient.cancelQueries({ queryKey })`를 호출하면 됩니다. 그러면 query가 취소되고 이전 상태로 되돌아갑니다. query 함수에 전달된 `signal`를 소비한 경우 TanStack Query도 Promise를 추가로 취소합니다.



```tsx
const todosQuery = useQuery(() => ({
  queryKey: ['todos'],
  queryFn: async ({ signal }) => {
    const resp = await fetch('/todos', { signal })
    return resp.json()
  },
}))

const queryClient = useQueryClient()

return (
  <button
    onClick={(e) => {
      e.preventDefault()
      queryClient.cancelQueries({ queryKey: ['todos'] })
    }}
  >
    Cancel
  </button>
)
```



## `Cancel Options`

취소 옵션은 query 취소 작업의 동작을 제어하는 ​​데 사용됩니다.

```tsx
// 특정 queries를 자동으로 취소
await queryClient.cancelQueries({ queryKey: ['posts'] }, { silent: true })
```
취소 옵션 개체는 다음 속성을 지원합니다.

- `silent?: boolean`
  - `true`로 설정하면 `CancelledError`가 관찰자(예: `onError` 콜백) 및 관련 알림에 전파되는 것을 억제하고 거부하는 대신 재시도 Promise을 반환합니다.
  - 기본값은 `false`입니다.
- `revert?: boolean`
  - `true`로 설정하면 기내 가져오기 직전부터 query의 상태(데이터 및 상태)를 복원하고, `fetchStatus`를 `idle`로 다시 설정하며, 이전 데이터가 없는 경우에만 발생합니다.
  - 기본값은 `true`입니다.

## 제한사항



