
# Build a minimal web path brute-forcer: Optimized memory, CPU usage
It has 3 inputs; all are required.
First input is url; second input is the wordlist file; last input is the comma seperated or list input of success codes.
The sample success codes are : 200, 204, 301, 302, 307, 401, 403.

[Brute_force_Single_input.py](https://github.com/Rtiwary-1/Web_Path_Brute_Forcer/blob/main/Brute_force_Single_input.py):
This code contains the application for single url input.

[multiple_input.py](https://github.com/Rtiwary-1/Web_Path_Brute_Forcer/blob/main/multiple_input.py):
This code contains the application for multiple url input.

#[OUTPUT](https://github.com/Rtiwary-1/Web_Path_Brute_Forcer/blob/main/Output_code.PNG):
![RESULT](https://github.com/Rtiwary-1/Web_Path_Brute_Forcer/blob/main/Output_code.PNG)

# DEPENDENCIES:
1. urllib.parse
2. urllib3
3. argparse
4. requests
5. sys
6. threading
7. queue
8. time

# TO RUN:
python filename.py -u url -w wordlist -s success_codes
Here: python Brute_force_Single_input.py -u https://www.github.com -w wordlist.txt -s "[200, 204, 301, 302, 307, 401, 403]"
