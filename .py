"""Quicksort vs Mergesort - Performance Comparison"""
import random
import time
import sys

# ==================== ALGORITHMS ====================

def quicksort(items):
    """Return new list sorted using quicksort algorithm."""
    if len(items) <= 1:
        return items[:]
    
    pivot = items[len(items) // 2]
    left = [x for x in items if x < pivot]
    middle = [x for x in items if x == pivot]
    right = [x for x in items if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def mergesort(items):
    """Return new list sorted using mergesort algorithm."""
    if len(items) <= 1:
        return items[:]
    
    mid = len(items) // 2
    left = mergesort(items[:mid])
    right = mergesort(items[mid:])
    
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ==================== TESTING & TIMING ====================

def generate_data(size, data_type="random"):
    """Generate test data of different types."""
    if data_type == "random":
        return [random.randint(1, size * 10) for _ in range(size)]
    elif data_type == "sorted":
        return list(range(size))
    elif data_type == "reverse":
        return list(range(size, 0, -1))
    elif data_type == "nearly_sorted":
        arr = list(range(size))
        for _ in range(size // 100):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif data_type == "few_unique":
        return [random.randint(1, size // 10) for _ in range(size)]


def time_sort(algorithm, data, runs=5):
    """Time a sorting algorithm over multiple runs."""
    times = []
    
    for _ in range(runs):
        data_copy = data[:]
        start = time.perf_counter()
        result = algorithm(data_copy)
        end = time.perf_counter()
        times.append(end - start)
        
        # Verify correctness
        if result != sorted(data_copy):
            print(f"ERROR: {algorithm.__name__} failed on {data_copy[:10]}...")
            return None
    
    return {
        'avg': sum(times) / runs,
        'min': min(times),
        'max': max(times),
        'runs': runs
    }


# ==================== MEMORY ANALYSIS ====================

def analyze_memory():
    """Print memory requirements for both algorithms."""
    print("\n" + "=" * 70)
    print("MEMORY REQUIREMENTS")
    print("=" * 70)
    
    sizes = [1000, 10000, 100000]
    
    print(f"\n{'Size':<12} {'Algorithm':<15} {'Space Complexity':<20} {'Est. Memory':<15}")
    print("-" * 70)
    
    for size in sizes:
        # Python int ~28 bytes overhead
        array_bytes = size * 28
        
        # Merge Sort: O(n) extra space (creates copies)
        merge_memory = array_bytes * 2
        
        # Quick Sort: O(log n) for recursion stack
        import math
        quick_memory = array_bytes + (int(math.log2(size)) * 1000)
        
        print(f"{size:<12} {'Merge Sort':<15} {'O(n)':<20} {merge_memory/1024:>6.1f} KB")
        print(f"{size:<12} {'Quick Sort':<15} {'O(log n)':<20} {quick_memory/1024:>6.1f} KB")
        print()
    
    print("\nCONCLUSION: Merge Sort uses 2x memory (O(n)), Quick Sort uses minimal extra (O(log n))")
    print("Quick Sort is more memory efficient.\n")


# ==================== MAIN COMPARISON ====================

def run_comparison():
    """Run comprehensive comparison tests."""
    print("=" * 70)
    print("QUICKSORT vs MERGESORT - PERFORMANCE COMPARISON")
    print("=" * 70)
    
    # Large datasets to show clear winner (requirement)
    sizes = [1000, 5000, 10000, 25000, 50000]
    runs_per_test = 5
    
    results = []
    
    for size in sizes:
        print(f"\n--- Testing {size:,} elements ({runs_per_test} runs each) ---")
        
        # Generate random test data
        data = generate_data(size, "random")
        
        # Time Quicksort
        q_result = time_sort(quicksort, data, runs_per_test)
        if q_result:
            print(f"  Quicksort: {q_result['avg']:.4f}s avg")
        
        # Time Mergesort
        m_result = time_sort(mergesort, data, runs_per_test)
        if m_result:
            print(f"  Mergesort: {m_result['avg']:.4f}s avg")
        
        # Determine winner
        if q_result and m_result:
            if q_result['avg'] < m_result['avg']:
                winner = "Quicksort"
                ratio = m_result['avg'] / q_result['avg']
            else:
                winner = "Mergesort"
                ratio = q_result['avg'] / m_result['avg']
            
            print(f"  ★ WINNER: {winner} ({ratio:.2f}x faster)")
            
            results.append({
                'size': size,
                'quick': q_result['avg'],
                'merge': m_result['avg'],
                'winner': winner
            })
    
    return results


def test_edge_cases():
    """Test both algorithms on edge cases."""
    print("\n" + "=" * 70)
    print("EDGE CASE VERIFICATION")
    print("=" * 70)
    
    test_cases = [
        ([], "Empty array"),
        ([1], "Single element"),
        ([5,5,5,5], "All identical"),
        ([5,4,3,2,1], "Reverse sorted"),
        ([1,2,3,4,5], "Already sorted"),
        ([-5, 10, -3, 0, 7], "Negative numbers"),
    ]
    
    all_pass = True
    for test_case, name in test_cases:
        expected = sorted(test_case)
        q_pass = quicksort(test_case) == expected
        m_pass = mergesort(test_case) == expected
        
        status = "✓" if (q_pass and m_pass) else "✗"
        print(f"  {status} {name}: Quicksort={q_pass}, Mergesort={m_pass}")
        
        if not (q_pass and m_pass):
            all_pass = False
    
    return all_pass


def print_conclusion(results):
    """Print final analysis and conclusion."""
    print("\n" + "=" * 70)
    print("CONCLUSION & RECOMMENDATIONS")
    print("=" * 70)
    
    if not results:
        print("No results to analyze.")
        return
    
    # Count wins
    quick_wins = sum(1 for r in results if r['winner'] == 'Quicksort')
    merge_wins = len(results) - quick_wins
    
    print(f"\nFINAL SCORE:")
    print(f"  Quicksort wins: {quick_wins}/{len(results)} test sizes")
    print(f"  Mergesort wins: {merge_wins}/{len(results)} test sizes")
    
    # Time complexity summary
    print("\n" + "-" * 70)
    print("TIME COMPLEXITY:")
    print(f"  {'Algorithm':<15} {'Best':<15} {'Average':<15} {'Worst':<15}")
    print("  " + "-" * 60)
    print(f"  {'Quicksort':<15} {'O(n log n)':<15} {'O(n log n)':<15} {'O(n²)':<15}")
    print(f"  {'Mergesort':<15} {'O(n log n)':<15} {'O(n log n)':<15} {'O(n log n)':<15}")
    
    print("\n" + "-" * 70)
    print("WHEN TO USE WHICH:")
    print("  • Use QUICKSORT for general purpose, random data, when memory matters")
    print("  • Use MERGESORT for sorted/reverse sorted data, or when stability is needed")
    print("  • Use MERGESORT for linked lists or external sorting (too large for memory)")
    
    # Final verdict
    print("\n" + "-" * 70)
    if quick_wins > merge_wins:
        print("★ FINAL VERDICT: QUICKSORT is generally faster for random data")
    else:
        print("★ FINAL VERDICT: MERGESORT provides more predictable performance")
    
    print("\n*Note: Results may vary based on data distribution and pivot selection strategy\n")


# ==================== RUN EVERYTHING ====================

if __name__ == "__main__":
    # Step 1: Test edge cases
    edge_pass = test_edge_cases()
    
    # Step 2: Memory analysis
    analyze_memory()
    
    # Step 3: Performance comparison
    results = run_comparison()
    
    # Step 4: Final conclusion
    print_conclusion(results)
    
    # Success message
    if edge_pass:
        print("\n✓ ALL TESTS PASSED - Both algorithms work correctly!")
    else:
        print("\n✗ SOME TESTS FAILED - Check implementations")
