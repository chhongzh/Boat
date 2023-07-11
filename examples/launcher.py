import os, importlib, sys

sys.path.append("..")
import runner


print("Welcome Boat AST examples!")

print("Select an example and run it.")

print("Some example there...")
lst = os.listdir()
index = 0
ignore = ["launcher.py", "README.md"]
print("Index\tName")
for item in lst:
    if item in ignore:
        continue

    print(f"{index+1}\t{item}")
    index += 1

ans = input("Select one to run.(Type 'n' to exit):")
if ans.lower() == "n":
    exit(0)
elif not ans.isdigit() or int(ans) > index:
    print("Invalid Number")
    exit(1)

folder_name = lst[int(ans) - 1]
print(f"Will run {folder_name}...")
CODE = importlib.import_module(f"examples.{folder_name}.code").CODE

print("--- Start Run! ---")
print()

r = runner.Runner(CODE)
r.run()

print()
print("--- Run done! ---")
