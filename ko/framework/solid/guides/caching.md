---
id: caching
title: 캐싱 예
---




> 본 가이드를 읽기 전에 [중요 기본값](../../react/guides/important-defaults.md)을 자세히 읽어보시기 바랍니다.

## 기본 예

이 캐싱 예제는 다음 항목의 스토리와 수명 주기를 보여줍니다.

- 캐시 데이터가 있거나 없는 Query 인스턴스
- 백그라운드 다시 가져오기
- 비활성 Queries
- 쓰레기 수거

**5분**의 기본 `gcTime`와 `0`의 기본 `staleTime`를 사용한다고 가정해 보겠습니다.

- `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))`의 새로운 인스턴스가 마운트됩니다.
  - `['todos']` query 키로 다른 queries가 만들어지지 않았으므로 이 query는 하드 로딩 상태를 표시하고 데이터를 가져오기 위해 네트워크 요청을 합니다.
  - 네트워크 요청이 완료되면 반환된 데이터는 `['todos']` 키 아래에 캐시됩니다.
  - 구성된 `staleTime` 이후 데이터는 오래된 것으로 표시됩니다(기본값은 `0`이거나 즉시).
- `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))`의 두 번째 인스턴스가 다른 곳에 마운트됩니다.
  - 캐시에 첫 번째 query의 `['todos']` 키에 대한 데이터가 이미 있으므로 해당 데이터가 즉시 캐시에서 반환됩니다.
  - 새 인스턴스는 query 함수를 사용하여 새 네트워크 요청을 트리거합니다.
    - 두 `fetchTodos` query 함수가 동일한지 여부에 관계없이 두 queries' [useQuery](../../react/reference/useQuery.md)가 모두 업데이트됩니다(`isFetching` 포함, `isPending` 및 기타 관련 값) 동일한 query 키를 가지고 있기 때문입니다.
  - 요청이 성공적으로 완료되면 `['todos']` 키 아래의 캐시 데이터가 새 데이터로 업데이트되고 두 인스턴스 모두 새 데이터로 업데이트됩니다.
- `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))` query의 두 인스턴스가 모두 마운트 해제되어 더 이상 사용되지 않습니다.
  - 이 query의 활성 인스턴스가 더 이상 없기 때문에 `gcTime`를 사용하여 가비지 수집 제한 시간이 설정되어 query를 삭제하고 가비지 수집합니다(기본값은 **5분**).
- 캐시 시간 초과(gcTime)가 완료되기 전에 `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))`의 다른 인스턴스가 마운트됩니다. query는 `fetchTodos` 함수가 백그라운드에서 실행되는 동안 사용 가능한 캐시 데이터를 즉시 반환합니다. 성공적으로 완료되면 캐시에 새로운 데이터가 채워집니다.
- `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))`의 마지막 인스턴스가 마운트 해제됩니다.
- **5분** 내에 더 이상 `useQuery(() => ({ queryKey: ['todos'], queryFn: fetchTodos }))` 인스턴스가 나타나지 않습니다.
  - `['todos']` 키 아래에 캐시된 데이터가 삭제되고 가비지 수집됩니다.