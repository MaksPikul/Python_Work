import re


def main():
    print(convert(input("Hours: ")))


def convert(s):
    #checks if input is valid
        #input will match with either, if statement checks which one is matched

        hr12 = re.search(r'^(([0-9]|1[0-2]):(0[0-9]|[1-5][0-9])|([0-9]|1[0-2]))\s(AM|PM)\sto\s(([0-9]|1[0-2]):(0[0-9]|[1-5][0-9])|([0-9]|1[0-2]))\s(AM|PM)$',s)
        if hr12:
            time1 = hr12.group(1).strip()
            time2 = hr12.group(6).strip()


            if ":" not in time1 and ":" not in time2:
                time1 = time1 + ":00"
                time2 = time2 + ":00"


            hour1, minute1 = time1.split(":")
            hour2, minute2 = time2.split(":")
            if int(hour1) == 12:
                hour1 = int(hour1) - 12
            if int(hour2) == 12:
                hour2 = int(hour2) - 12



            if hr12.group(5) == "PM":
                hour1 = int(hour1) + 12
            time1 = str(hour1) + ":" + minute1


            if hr12.group(10) == "PM":
                hour2 = int(hour2) + 12
            time2 = str(hour2) + ":" + minute2

            if int(hour1) < 10:
                time1= "0" + time1

            if int(hour2) < 10:
                time2 = "0" + time2

            return time1 + " to " + time2
        else:
            raise ValueError

if __name__ == "__main__":
    main()