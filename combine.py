def combine(list1, list2):
    result = []
    elements = sorted(list1 + list2, key=lambda x: x["positions"][0])
    for curr in elements:
        merged = False
        for prev in result:
            l1, r1 = prev["positions"]
            l2, r2 = curr["positions"]
            overlap = max(0, min(r1, r2) - max(l1, l2))
            if overlap > 0.5 * (r2 - l2):
                prev["values"].extend(curr["values"])
                merged = True
                break
        if not merged:
            result.append(curr)
    return result

list1 = eval(input())  
list2 = eval(input())  
print(combine(list1, list2))
