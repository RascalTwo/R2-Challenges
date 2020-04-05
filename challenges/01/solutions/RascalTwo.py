from typing import List, Optional, Tuple, Union, Set

def smartest(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
	subs: Set[Union[int, float]] = set()
	for num in nums:
		if target / num in subs:
			return target / num, num
		subs.add(num)

one_liner = lambda nums, target: next(((x, nums[j]) for i, x in enumerate(nums) for j in range(i + 1, len(nums)) if i != j and x * nums[j] == target), None)

SOLUTIONS = [smartest, one_liner]
