---
id: createQueries
title: createQueries
---




# 함수: createQueries()

```ts
function createQueries<T, TCombinedResult>(createQueriesOptions, queryClient?): TCombinedResult;
```
정의 위치: [packages/svelte-query/src/createQueries.svelte.ts:189](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createQueries.svelte.ts#L189)

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TCombinedResult

`TCombinedResult` = `T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetCreateQueryResult`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetCreateQueryResult`\<`Head`\>, `GetCreateQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetCreateQueryResult`\<`Head`\>, `GetCreateQueryResult`\<`Head`\>, `GetCreateQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : \[`...{ [K in (...)]: (...) }[]`\] : \[...\{ \[문자열의 K \| 번호 \| 기호\]: GetCreateQueryResult\<Tails\[K\<(...)\>\]\> \}\[\]\] : \{ \[K 문자열 \| 번호 \| 기호\]: GetCreateQueryResult\<T\[K\<K\>\]\> \}

## 매개변수

### createQueriesOptions

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<\{
  `combine?`: (`result`) => `TCombinedResult`;
  `queries`: \| readonly \[`T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetCreateQueryOptionsForCreateQueries`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetCreateQueryOptionsForCreateQueries`\<...\>, `GetCreateQueryOptionsForCreateQueries`\<...\>\] : \[`...(...)[]`\] *extends* \[..., `...(...)[]`\] ? ... *extends* ... ? ... : ... : ... *extends* ... ? ... : ... : readonly `unknown`[] *extends* `T` ? `T` : `T` *extends* `CreateQueryOptionsForCreateQueries`\<..., ..., ..., ...\>[] ? `CreateQueryOptionsForCreateQueries`\<..., ..., ..., ...\>[] : `CreateQueryOptionsForCreateQueries`\<..., ..., ..., ...\>[]\]
     \| readonly \[\{ \[K 문자열 \| 번호 \| 기호\]: GetCreateQueryOptionsForCreateQueries\<T\[K\<K\>\]\> \}\];
\}\>

### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

## 반환값

`TCombinedResult`