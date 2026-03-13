---
id: default-query-function
title: 기본 Query 기능
---




어떤 이유로든 전체 앱에 동일한 query 기능을 공유하고 query 키를 사용하여 가져와야 할 항목을 식별하고 싶다면 **기본 query 기능**을 TanStack Query에 제공하면 됩니다.

[//]: # 'Example'

```tsx
// query 키를 수신할 기본 query 함수를 정의합니다.
const defaultQueryFn = async ({ queryKey }) => {
  const { data } = await axios.get(
    `https://jsonplaceholder.typicode.com${queryKey[0]}`,
  )
  return data
}

// defaultOptions를 사용하여 앱에 기본 query 기능을 제공하세요.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: defaultQueryFn,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  )
}

// 이제 해야 할 일은 키를 전달하는 것 뿐입니다!
function Posts() {
  const { status, data, error, isFetching } = useQuery({ queryKey: ['/posts'] })

  // ...
}

// queryFn를 생략하고 바로 옵션으로 들어갈 수도 있습니다.
function Post({ postId }) {
  const { status, data, error, isFetching } = useQuery({
    queryKey: [`/posts/${postId}`],
    enabled: !!postId,
  })

  // ...
}
```
[//]: # 'Example'

기본 queryFn를 재정의하려면 평소와 같이 직접 제공하면 됩니다.