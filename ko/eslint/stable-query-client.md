---
id: stable-query-client
title: 안정적인 Query 클라이언트
---




QueryClient에는 QueryCache가 포함되어 있으므로 애플리케이션의 수명 주기 동안 QueryClient의 인스턴스 하나만 생성하면 됩니다. 렌더링할 때마다 새 인스턴스가 _아닙니다_.

> 예외: 비동기 함수는 서버에서 한 번만 호출되므로 비동기 서버 구성 요소 내에 새 QueryClient를 생성하는 것이 허용됩니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/stable-query-client": "오류" */

function App() {
  const queryClient = new QueryClient()
  return (
    <QueryClientProvider client={queryClient}>
      <Home />
    </QueryClientProvider>
  )
}
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
function App() {
  const [queryClient] = useState(() => new QueryClient())
  return (
    <QueryClientProvider client={queryClient}>
      <Home />
    </QueryClientProvider>
  )
}
```

```tsx
const queryClient = new QueryClient()
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Home />
    </QueryClientProvider>
  )
}
```

```tsx
async function App() {
  const queryClient = new QueryClient()
  await queryClient.prefetchQuery(options)
}
```
## 속성

- [x] ✅ 추천
- [x] 🔧 수정 가능