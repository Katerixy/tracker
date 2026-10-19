#add function, check all function, check next function, remove function
import datetime
import calendar

def add_date(file_name):
    date = get_date()
    if not date:
        print("Addition cancelled.")
        return
    amount = get_number("How long was it? (If none yet, input 0 then come back later)")
    with (open(file_name, "a") as file):
        file.write(f"{date.strftime('%Y-%m-%d')}_{amount}\n")
    clean_file(file_name)
    print("Added successfully")

def clean_file(file_name):
    with (open(file_name, "r") as file):
        lines = file.readlines()
    lines.sort()
    with open(file_name, "w") as file:
        for line in lines:
            file.write(line)

def check_past(file_name):
    gen_amount = get_number("How many dates to generate? (Input 0 for all)")
    with (open(file_name, "r") as file):
        lines = file.readlines()
    if gen_amount <= 0 or gen_amount > len(lines):
        gen_amount = len(lines)
    for i in range(1, gen_amount+1):
        date, amount = lines[-i].strip("\n").split("_")
        date = date.strip("\n").split("-")
        print(f"{calendar.month_abbr[int(date[1])]}. {date[2]}, {date[0]} days: {amount}")
def check_future(file_name):
    gen_amount = get_number("How many dates to generate?")
    date_list, avg_dif, avg_len = calculate_avg(file_name)
    i = 0
    while i < gen_amount:
        d3 = date_list[-1][0] + datetime.timedelta(days = avg_dif)
        amount = avg_len
        date_list.append([d3, amount])
        ##if d3 >= datetime.datetime.now().date():
        print(f"{calendar.month_abbr[int(d3.month)]}. {d3.day}, {d3.year} days:{amount}")
        i+=1

def calculate_avg(file_name):
    date_list = []
    with (open(file_name, "r") as file):
        for line in file:
            date, amount = line.strip("\n").split("_")
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            date_list.append([date, int(amount)])
    sum_dif = 0
    sum_len = 0
    total_items = 0
    for i in range(1, len(date_list)):
        d1 = date_list[i - 1][0]
        d2 = date_list[i][0]
        dif = d2 - d1
        if 20 < dif.days < 36:
            sum_dif += dif.days
            sum_len += date_list[i - 1][1]
            total_items += 1
    avg_dif = round(sum_dif / (total_items))
    avg_len = round(sum_len / (total_items))
    print(f"difference: {avg_dif}; length: {avg_len}")
    return date_list, avg_dif, avg_len


def get_number(sentence = ""):
    print(sentence)
    while True:
        choice = input()
        try:
            int(choice)
        except:
            print("not valid. Try again.")
            continue
        return int(choice)

def remove_date(file_name):
    date = get_date()
    if not date:
        print("Removal cancelled.")
        return
    with (open(file_name, "r") as file):
        lines = file.readlines()
    with open(file_name, "w") as file:
        for line in lines:
            if line.strip("\n") != date.strftime('%Y-%m-%d'):
                file.write(line)
    print("Removed successfully")

def main():
    file_name = "periodgrrl_dates"
    print("Welcome to PeriodGrrl!")
    while True:
        choice = get_input("Would you like to [add] a date, [remove] a date, or [check] dates?", ["add", "remove", "check"])
        if choice == "add":
            add_date(file_name)
        elif choice == "remove":
            remove_date(file_name)
        elif choice == "check":
            choice = get_input("Check [past] dates, or [future] predictions?", ["past", "future"])
            if choice == "past":
                check_past(file_name)
            elif choice == "future":
                check_future(file_name)
            else:
                return
        else:
            return

def get_date():
    while True:
        choice = input("Which date? (dd-mm-yyyy) ")
        if choice == "cancel" or choice == "":
            return False

        choice = choice.split("-")
        if len(choice) != 3:
            print("incorrect format. Don't forget the dashes.")
            continue
        if len(choice[0]) != 2 or len(choice[1]) != 2 or len(choice[2]) != 4:
            print("incorrect lengths. Don't forget zeroes where needed.")
            continue
        for item in choice:
            try:
                int(item)
            except:
                print("cannot convert to number")
                continue
        if choice[0][0] == "0":
            choice[0] = choice[0][1]
        if choice[1][0] == "0":
            choice[1] = choice[1][1]
        try:
            date = datetime.date(int(choice[2]), int(choice[1]), int(choice[0]))
        except:
            print("An error occurred. Try again.")
            continue
        return date

def get_input(sentence, choices):
    while True:
        try:
            choice = input(sentence+" ")
        except KeyboardInterrupt:
            print("\nAn error occurred.")
            return None
        if choice in choices:
            return choice
        else:
            print(f"Choose from the following: {choices}")



if __name__ == "__main__":
    main()