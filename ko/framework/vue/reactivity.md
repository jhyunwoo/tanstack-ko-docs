---
id: reactivity
title: 반동
---




Vue는 [신호 패러다임](https://vuejs.org/guide/extras/reactivity-in-length.html#connection-to-signals)을 사용하여 반응성을 처리하고 추적합니다. 주요 특징
이 시스템은 특별히 관찰된 반응 속성에 대해서만 업데이트를 트리거하는 반응 시스템입니다. 결과적으로 queries가 소비하는 값이 업데이트될 때 업데이트되도록 해야 합니다.

# Queries 반응성을 유지

query용 컴포저블을 만들 때 가장 먼저 선택할 수 있는 것은 다음과 같이 작성하는 것입니다.

```ts
export function useUserProjects(userId: string) {
  return useQuery(
    queryKey: ['userProjects', userId],
    queryFn: () => api.fetchUserProjects(userId),
  );
}
```
이 컴포저블을 다음과 같이 사용할 수 있습니다.

```ts
// 반응적 사용자 ID 참조.
const userId = ref('1')
// 사용자 1의 프로젝트를 가져옵니다.
const { data: projects } = useUserProjects(userId.value)

const onChangeUser = (newUserId: string) => {
  // userId를 편집하지만 query는 다시 가져오지 않습니다.
  userId.value = newUserId
}
```
이 코드는 의도한 대로 작동하지 않습니다. 이는 userId 참조에서 직접 값을 추출하기 때문입니다. Vue-query는 `userId` `ref`를 추적하지 않으므로 값이 변경되는 시기를 알 수 없습니다.

다행히도 이에 대한 해결 방법은 간단합니다. 값은 query 키에서 추적 가능해야 합니다. 컴포저블에서 직접 `ref`를 수락하고 query 키에 배치하면 됩니다.

```ts
export function useUserProjects(userId: Ref<string>) {
  return useQuery(
    queryKey: ['userProjects', userId],
    queryFn: () => api.fetchUserProjects(userId.value),
  );
}
```
이제 `userId`가 변경되면 query가 다시 가져옵니다.

```ts
const onChangeUser = (newUserId: string) => {
  // Query는 새로운 사용자 ID로 데이터를 다시 가져옵니다!
  userId.value = newUserId
}
```
vue query에서는 query 키 내의 모든 반응 속성이 자동으로 변경 사항을 추적합니다. 이를 통해 vue-query는 다음이 발생할 때마다 데이터를 다시 가져올 수 있습니다.
특정 요청 변경에 대한 매개변수입니다.

## 비반응성 Queries에 대한 설명

가능성은 훨씬 낮지만 때로는 비반응형 변수를 의도적으로 전달하는 경우도 있습니다. 예를 들어, 일부 엔터티는 한 번만 가져와야 하고 추적이 필요하지 않거나 mutation 이후의 mutation query 옵션 개체를 무효화합니다.
위에 정의된 맞춤 컴포저블을 사용하면 이 경우 사용법이 약간 이상하게 느껴집니다.

```ts
const { data: projects } = useUserProjects(ref('1'))
```
매개변수 유형을 호환 가능하게 만들기 위해 중간 `ref`를 생성해야 합니다. 우리는 여기서 더 잘할 수 있습니다. 대신 일반 값과 ​​반응형 값을 모두 허용하도록 컴포저블을 업데이트하겠습니다.

```ts
export function useUserProjects(userId: MaybeRef<string>) {
  return useQuery(
    queryKey: ['userProjects', userId],
    queryFn: () => api.fetchUserProjects(toValue(userId)),
  );
}
```
이제 일반 값과 ​​참조 모두와 함께 컴포저블을 사용할 수 있습니다.

```ts
// 사용자 1의 프로젝트를 가져오며 userId는 변경되지 않을 것으로 예상됩니다.
const { data: projects } = useUserProjects('1')

// 사용자 1의 프로젝트를 가져오며, queries는 userId의 변경 사항에 반응합니다.
const userId = ref('1')

// userId를 일부 변경합니다...

// Query는 userId에 대한 변경 사항을 기반으로 다시 가져옵니다.
const { data: projects } = useUserProjects(userId)
```
## Queries 내에서 파생 상태 사용

다른 반응 상태 소스에서 새로운 반응 상태를 파생시키는 것은 매우 일반적입니다. 일반적으로 이 문제는 구성요소 소품을 다루는 상황에서 나타납니다. `userId`가 컴포넌트에 전달된 prop이라고 가정해 보겠습니다.

```vue
<script setup lang="ts">
const props = defineProps<{
  userId: string
}>()
</script>
```
다음과 같이 query에서 소품을 직접 사용하고 싶을 수도 있습니다.

```ts
// props.userId의 변경 사항에 반응하지 않습니다.
const { data: projects } = useUserProjects(props.userId)
```
그러나 첫 번째 예와 유사하게 이는 반응적이지 않습니다. `reactive` 변수에 대한 속성 액세스로 인해 반응성이 손실됩니다. `computed`를 통해 이 파생 상태를 반응성으로 만들어 이 문제를 해결할 수 있습니다.

```ts
const userId = computed(() => props.userId)

// props.userId의 변경 사항에 반응합니다.
const { data: projects } = useUserProjects(userId)
```
이는 예상대로 작동하지만 이 솔루션이 항상 최적인 것은 아닙니다. 중간변수 도입 외에 다소 불필요한 메모화된 값도 생성합니다. 간단한 속성 액세스의 사소한 경우에는 `computed`가 실제 이점이 없는 최적화입니다. 이러한 경우 더 적절한 해결책은 [반응형 getter](https://blog.vuejs.org/posts/vue-3-3#better-getter-support-with-toref-and-tovalue)를 사용하는 것입니다. 반응형 게터는 `computed` 작동 방식과 유사하게 일부 반응 상태를 기반으로 값을 반환하는 단순한 함수입니다. `computed`와 달리 반응형 게터는 값을 기억하지 않으므로 간단한 속성 액세스에 적합합니다.

다시 한 번 컴포저블을 리팩터링해 보겠습니다. 단, 이번에는 `ref`, 일반 값 또는 반응형 getter를 허용하도록 하겠습니다.

```ts
export function useUserProjects(userId: MaybeRefOrGetter<string>) {
  ...
}
```
사용법을 조정하고 이제 반응형 getter를 사용해 보겠습니다.

```ts
// props.userId의 변경 사항에 반응합니다. '계산'이 필요하지 않습니다!
const { data: projects } = useUserProjects(() => props.userId)
```
이는 불필요한 메모 오버헤드 없이 필요한 간결한 구문과 반응성을 제공합니다.

## 기타 추적된 Query 옵션

위에서는 반응적 종속성을 추적하는 query 옵션 하나만 다루었습니다. 그러나 `queryKey` 외에도 `enabled`는 다음을 허용합니다.
반응 값의 사용. 이는 파생된 상태를 기반으로 query 가져오기를 제어하려는 상황에서 유용합니다.

```ts
export function useUserProjects(userId: MaybeRef<string>) {
  return useQuery(
    queryKey: ['userProjects', userId],
    queryFn: () => api.fetchUserProjects(toValue(userId)),
    enabled: () => userId.value === activeUserId.value,
  );
}
```
이 옵션에 대한 자세한 내용은 [useQuery](reference/useQuery.md) 페이지에서 확인할 수 있습니다.

## 불변성

`useQuery`의 결과는 항상 변경할 수 없습니다. 이는 성능 및 캐싱 목적에 필요합니다. `useQuery`에서 반환된 값을 변경해야 하는 경우 데이터 복사본을 생성해야 합니다.

이 디자인의 한 가지 의미는 `useQuery`에서 `v-model`와 같은 양방향 바인딩으로 값을 전달하는 것이 작동하지 않는다는 것입니다. 해당 위치에서 업데이트를 시도하기 전에 데이터의 변경 가능한 복사본을 생성해야 합니다.

# 주요 시사점

- `enabled` 및 `queryKey`는 반응 값을 수용할 수 있는 두 가지 query 옵션입니다.
- Vue에서 세 가지 유형의 값(refs, 일반 값 및 반응형 getter)을 모두 허용하는 query 옵션을 전달합니다.
- query가 소비하는 값에 따라 변경 사항에 반응할 것으로 예상되는 경우 값이 반응하는지 확인하세요. (즉, 참조를 query에 직접 전달하거나 반응성 게터를 사용하십시오)
- query가 반응형으로 필요하지 않은 경우 일반 값으로 전달합니다.
- 속성 액세스와 같은 사소한 파생 상태의 경우 `computed` 대신 반응형 게터 사용을 고려하세요.
- `useQuery`의 결과는 항상 변경할 수 없습니다.