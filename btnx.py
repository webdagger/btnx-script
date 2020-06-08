""" 
This script is to automate the call of the shell command 'sudo btnx' 
and automatically restart it with minimum user input
"""

import sys
import subprocess

class Btnx:
    
    def __init__(self):
        self.password : str = input('Enter sudo password_:')
        self.command : str = f'echo {self.password} | sudo -S btnx'
        self.process = None
        self.restart_count = 0
        try:
            run = self.run()
            if run:
                # Means that the process has terminated gracefully, perhaps due to a lack of activity from the mouse
                self.display()
        except subprocess.CalledProcessError as e:
            self.display(e)


    def run(self) -> bool:
     
        # The subprocess.run() is called with the check=True option which throws a subprocess.CalledProcessError.
        # This event will be true in instances where the sudo password is wrong or when the btnx config does not detect the configured mouse.
        # We are also at this point unable to explicitly know when the process runs successfully
        # Except that it takes a longer time for the .run method to return CompletedProcess
        # After which it exits with return code 0
        while True:
            self.process = subprocess.run(self.command, shell=True, capture_output=True, check=True)
            if self.process.returncode == 0:
                return True
                break

    def display(self, error=None):
        # The error arg is the instance of subprocess.CalledProcessError
        print("The process could not be completed")
        print("There are usually 3 reasons for this.")
        print("1 :> Wrong sudo password entered")
        print("2 :> The configured mouse to be redirected is not currently connected")
        print("3 :> There is an issue with the btnx-config.")
        
        while True:
            print(
                    """
                    What would you like to do?
                    1 - QUIT
                    2 - RETRY
                    3 - lunch sudo btnx-config and restart this script after configuration.
                    4 - Endless Retries( Use this sparingly, the only way to exit is to in CTRL C or kill terminal)
                    """
                )
            choices : dict = {"1" : self.quit, "2": self.retry, "3": self.btnx_config, "4": self.endless}
            choice = input("Enter choice: ")
            if type(int(choice)) != int or int(choice) < 0:
                # The entered choice must be an integer
                print("You have entered a non integer. Program will exit")
                print(error.stdout)
                sys.exit(1)
            action = choices.get(choice)
            if action:
                action()
            else: 
                print("The action you chose is not valid")
                break
        if error:
            print(f"Error-> {error.args}")
        else:
            print("There was an error processing your action.")
        exit(1)
    
    def quit(self):
        sys.exit(0)
    
    def retry(self):
        try:
            self.restart_count + 1
            self.run()
        except subprocess.CalledProcessError as e:
            self.display(e)
    
    def btnx_config(self):
        # launch the btnx_config
        command = f"echo {self.password} | sudo -S btnx-config"
        print("Launching the Btnx-config panel")
        print("After configuring, simply quit the config panel")
        print("This script will attempt to restart btnx after")
        if self.process:
            # Btnx or btnx-config is already running
            print("Exiting because another process was dectected")
            sys.exit(1)
        try:
            self.process = subprocess.run(command, shell=True, capture_output=True, check=True)
            if self.process.returncode == 0:
                # This means that the user exited the btnx-config process
                print("Attempting to start btnx")
                self.restart_count + 1
                self.run()
        except subprocess.CalledProcessError as e:
            # If the user hits the next block of code, then it means that the process to launch btnx-config ended in an error    
            print("Fatal error calling sudo btnx-config")
            print(e.with_traceback())
            sys.exit(1)
    
    def endless(self):
        "This method runs the command without allowing an option to exit"
        try:
            self.restart_count + 1
            self.run()
        except subprocess.CalledProcessError:
            self.restart_count + 1
            self.run()
        except KeyboardInterrupt:
            print("Exiting")
            sys.exit(0)

if __name__ == "__main__":
    Btnx().run()
