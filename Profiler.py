import subprocess
import os
from datetime import datetime

def main():
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%m-%d-%Y_%H:%M:%S")

    # Create the directory if it doesn't exist
    if not os.path.exists("profiles"):
        os.makedirs("profiles")
    
    # Write the profiles to a file
    folder_name = "profiles"
    file_name = "Profile_" + dt_string + ".txt"
    with open(folder_name + os.sep + file_name, "w") as file:
        ping = subprocess.run(
            ['kernprof', '-lv', 'ProfileTest.py'],
            text=True,
            stdout=subprocess.PIPE,
            check=True)
        file.write(ping.stdout)
        print(ping.stdout)
        print("Profile saved to: " + folder_name + os.sep + file_name)
        print()

if __name__ == "__main__":
    main()