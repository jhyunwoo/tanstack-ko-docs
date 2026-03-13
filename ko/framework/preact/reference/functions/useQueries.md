---
id: useQueries
title: useQueries
---




# 함수: useQueries()

```ts
function useQueries<T, TCombinedResult>(__namedParameters, queryClient?): TCombinedResult;
```
정의 위치: [preact-query/src/useQueries.ts:207](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQueries.ts#L207)

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TCombinedResult

`TCombinedResult` = `T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseQueryResult`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseQueryResult`\<`Head`\>, `GetUseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseQueryResult`\<`Head`\>, `GetUseQueryResult`\<`Head`\>, `GetUseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : \[`...{ [K in (...)]: (...) }[]`\] : \[...\{ \[문자열의 K \| 번호 \| 기호\]: GetUseQueryResult\<Tails\[K\<(...)\>\]\> \}\[\]\] : \{ \[K 문자열 \| 번호 \| 기호\]: GetUseQueryResult\<T\[K\<K\>\]\> \}

## 매개변수

### \_\_namedParameters

#### 결합하다?

(`result`) => `TCombinedResult`

#### queries

\| readonly \[`T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseQueryOptionsForUseQueries`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseQueryOptionsForUseQueries`\<`Head`\>, `GetUseQueryOptionsForUseQueries`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : readonly ...[] *extends* \[`...(...)[]`\] ? \[`...(...)[]`\] : ... *extends* ... ? ... : ... : readonly `unknown`[] *extends* `T` ? `T` : `T` *extends* `UseQueryOptionsForUseQueries`\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[] ? `UseQueryOptionsForUseQueries`\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[] : `UseQueryOptionsForUseQueries`\<`unknown`, `Error`, `unknown`, readonly ...[]\>[]\]
  \| readonly \[\{ \[K 문자열 \| 번호 \| 기호\]: GetUseQueryOptionsForUseQueries\<T\[K\<K\>\]\> \}\]

#### 구독하셨나요?

`boolean`

### queryClient?

`QueryClient`

## 반환값

`TCombinedResult`