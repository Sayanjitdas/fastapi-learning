from util import engine


def take_input():

    context = []
    print("Write the query below:")
    while True:
        each_line = input()
        if each_line[-1] == ";":
            if input("Execute the query? y/n ").lower() == "y":
                context.append(each_line)
                break
        else:
            context.append(each_line)
    
    return " ".join(context)

def execute_query(query: str):

    cursor = engine.connect()
    obj = cursor.execute(query)
    try:
        print(obj.fetchall())
    except Exception as _:
        print("executed!!")
    cursor.close()

while True:
    execute_query(take_input())