a = range(1, 10001)

# for b in a:
#     if b%2 != 0:
#         print(b)

def get_simple(a):
    answer = list()
    for numbers in range(1, a+1):
        if a % numbers == 0:
            answer.append(numbers)
    return answer
    # if len(answer) >= 1:
    #     pass
    # else:
    #     return a
print(get_simple(500))
print(1965/131)
# arr = list()
# for b in a:
#     num = get_simple(b)
#     if type(num) is int:
#         arr.append(num)

# print(arr)

