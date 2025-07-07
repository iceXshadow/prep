def get_sum(a, b):
    return a + b


def print_name():
    print(__name__)


print("I am in a sample file.")
# what is __name__?
# __name__ is a special variable in Python that represents the name of the module.
# If the module is being run directly, __name__ will be set to "__main__".
# If the module is being imported, __name__ will be set to the name of the module.
if __name__ == "__main__":
    print(get_sum(5, 10))
