# import sample
from sample import get_sum, print_name

# The code above imports the sample module and runs it.
# The sample module will execute its code, including the print statements and the function calls.
# The output will show the result of the get_sum function and the value of __name__.
# The output will also include the print statements from the sample module.

print(get_sum(15, 10))
print_name()  # since we imported it from sample, it will print the name of the module!
