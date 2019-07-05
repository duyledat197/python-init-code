def update(arr: list, arr_update: list):
    for i, item in enumerate(arr):
        if i < len(arr_update):
            arr[i] = arr_update[i]

    for i, item in enumerate(arr_update):
        if i >= len(arr):
            arr[i] = item

    return arr
