from interval import Interval

total = int(input("How many time intervals do you want? "))
interval_list: list[Interval] = []

while len(interval_list) < total:
    print("Please enter a new interval.")
    sh = int(input("Start hour: "))
    sm = int(input("Start minute: "))
    eh = int(input("End hour: "))
    em = int(input("End minute: "))
    new_interval = Interval(sh, sm, eh, em)

    # Check existence
    exists = any(new_interval == it for it in interval_list)

    if exists:
        print("The interval already exists:")
        print(new_interval)
        continue

    # Find insertion position (keep list ordered by duration descending)
    insert_pos = -1
    for idx, current in enumerate(interval_list):
        # If new interval duration is >= current duration, insert here
        if not (new_interval < current):
            insert_pos = idx
            break

    if insert_pos >= 0:
        interval_list.insert(insert_pos, new_interval)
    else:
        interval_list.append(new_interval)

for it in interval_list:
    print(it)
