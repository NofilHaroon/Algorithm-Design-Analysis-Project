import numpy as np
import time
import matplotlib.pyplot as plt
plt.rcdefaults()


def bruteforce(pattern, string):
    M = len(pattern)
    N = len(string)
    for i in range(N - M + 1):
        j = 0

        while(j < M):
            if (string[i + j] != pattern[j]):
                break
            j += 1

        # if (j == M):
        #     print("Pattern found at index", i, 'using Brute Force.')


def knuth_morris_pratt(pattern, string):
    M = len(pattern)
    N = len(string)
    lps = [0]*M
    j = 0
    computeLPSArray(pattern, M, lps)

    i = 0
    while i < N:
        if pattern[j] == string[i]:
            i += 1
            j += 1

        if j == M:
            # print("Pattern found at index " + str(i-j),
            #       'using Knuth-Morris-Pratt.')
            j = lps[j-1]
        elif i < N and pattern[j] != string[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1


def computeLPSArray(pattern, M, lps):
    len = 0
    i = 1
    while i < M:
        if pattern[i] == pattern[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1


NO_OF_CHARS = 256


def getNextState(pat, M, state, x):
    ''' 
    calculate the next state  
    '''
    if state < M and x == ord(pat[state]):
        return state+1

    i = 0

    for ns in range(state, 0, -1):
        if ord(pat[ns-1]) == x:
            while(i < ns-1):
                if pat[i] != pat[state-ns+1+i]:
                    break
                i += 1
            if i == ns-1:
                return ns
    return 0


def computeTF(pat, M):
    ''' 
    This function builds the TF table which  
    represents Finite Automata for a given pattern 
    '''
    global NO_OF_CHARS

    TF = [[0 for i in range(NO_OF_CHARS)]
          for _ in range(M+1)]

    for state in range(M+1):
        for x in range(NO_OF_CHARS):
            z = getNextState(pat, M, state, x)
            TF[state][x] = z

    return TF


def finite_automaton(pat, txt):
    ''' 
    Prints all occurrences of pat in txt 
    '''
    global NO_OF_CHARS
    M = len(pat)
    N = len(txt)
    TF = computeTF(pat, M)

    # Process txt over FA.
    state = 0
    for i in range(N):
        state = TF[state][ord(txt[i])]
        # if state == M:
        # print("Pattern found at index: {}".
        #       format(i-M+1), 'using Finite Automata.')


def read_data(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
    # print(data)
    return data


time_naive = []
time_kmp = []
time_fa = []


def find_time(string, pattern):

    start = time.time()
    bruteforce(pattern, string)
    # print(time.time() - start)
    time_naive.append(time.time() - start)

    start = time.time()
    knuth_morris_pratt(pattern, string)
    # print(time.time() - start)
    time_kmp.append(time.time() - start)

    start = time.time()
    finite_automaton(pattern, string)
    # print(time.time() - start)
    time_fa.append(time.time() - start)


string = read_data('txt1.txt')
pattern = "Above sixth sea the"
find_time(string, pattern)

string = read_data('txt2.txt')
pattern = "Above sixth sea the"
find_time(string, pattern)

string = read_data('txt3.txt')
pattern = "Above sixth sea the"
find_time(string, pattern)

string = read_data('txt4.txt')
pattern = "Above sixth sea the"
find_time(string, pattern)

string = read_data('txt5.txt')
pattern = "Above sixth sea the"
find_time(string, pattern)

# print(time_naive, time_kmp, time_fa)
plt.plot([2, 4, 6, 8, 10], time_naive, label='naive')
plt.plot([2, 4, 6, 8, 10], time_kmp, label='kmp')
plt.plot([2, 4, 6, 8, 10], time_fa, label='finite_automata')
plt.xlabel("No. of Words (in thousands)")
plt.ylabel("Time (s)")
plt.legend()
plt.show()
