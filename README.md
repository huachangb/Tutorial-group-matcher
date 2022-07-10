# Python module to find the best possible planning
This is a reimplementation of [optimal calendar](https://github.com/huachangb/optimal_calendar). The difference is that this code, i.e. code in the current repository, has more tests written for it and this contains an algorithm that generalizes the clique-based one in the original repo.

## Features
- Search for a schedule to limit the number of overlapping lectures 
- Search within a given range of time
- Adding custom events

# Installation
It is assumed that [Python](https://www.python.org/) (code has been tested using Python 3.8.5 and 3.8.8) and [Git](https://github.com/git-guides/install-git) are installed
```
git clone https://github.com/huachangb/calendar_ps.git
cd calendar_ps
pip install -r requirements.txt
jupyter notebook
```
Then select the notebook called ```demo``` and follow the instructions inside this notebook.

# Testing 
See [testing](https://github.com/huachangb/calendar_ps/tree/main/optimal_calendar/tests).

# Disclaimer
The code is written using Python 3.8.8. No guarantuee that it also works on older versions of Python. I will not take any responsibility if the code, for example, produces a wrong result. Never blindly trust something.
