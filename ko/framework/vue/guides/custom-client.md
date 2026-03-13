---
id: custom-client
title: 맞춤형 클라이언트
---




### 맞춤 클라이언트

Vue Query를 사용하면 Vue 컨텍스트에 대한 사용자 정의 `QueryClient`를 제공할 수 있습니다.

Vue 컨텍스트에 액세스할 수 없는 다른 라이브러리와 통합하기 위해 미리 `QueryClient`를 생성해야 할 때 유용할 수 있습니다.

이러한 이유로 `VueQueryPlugin`는 `QueryClientConfig` 또는 `QueryClient`를 플러그인 옵션으로 허용합니다.

`QueryClientConfig`를 제공하면 `QueryClient` 인스턴스가 내부적으로 생성되어 Vue 컨텍스트에 제공됩니다.

```tsx
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClientConfig: {
    defaultOptions: { queries: { staleTime: 3600 } },
  },
}
app.use(VueQueryPlugin, vueQueryPluginOptions)
```

```tsx
const myClient = new QueryClient(queryClientConfig)
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClient: myClient,
}
app.use(VueQueryPlugin, vueQueryPluginOptions)
```
### 사용자 정의 컨텍스트 키

Vue 컨텍스트에서 `QueryClient`에 액세스할 수 있는 키를 사용자 정의할 수도 있습니다. 이는 Vue2를 사용하여 동일한 페이지에 있는 여러 앱 간의 이름 충돌을 피하려는 경우에 유용할 수 있습니다.

기본 및 사용자 정의 `QueryClient` 모두에서 작동합니다.

```tsx
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClientKey: 'Foo',
}
app.use(VueQueryPlugin, vueQueryPluginOptions)
```

```tsx
const myClient = new QueryClient(queryClientConfig)
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClient: myClient,
  queryClientKey: 'Foo',
}
app.use(VueQueryPlugin, vueQueryPluginOptions)
```
커스텀 클라이언트 키를 사용하려면 query 옵션으로 제공해야 합니다.

```js
useQuery({
  queryKey: ['query1'],
  queryFn: fetcher,
  queryClientKey: 'foo',
})
```
내부적으로 사용자 정의 키는 기본 query 키와 접미사로 결합됩니다. 하지만 사용자는 이에 대해 걱정할 필요가 없습니다.

```tsx
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClientKey: 'Foo',
}
app.use(VueQueryPlugin, vueQueryPluginOptions) // -> VUE_QUERY_CLIENT:푸
```
