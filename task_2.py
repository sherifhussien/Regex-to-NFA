import argparse

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def top(self):
        if self.items == []:
            return None
        else:
            return self.items[-1]

    def is_empty(self):
        return (self.items == [])
    
    def has_more_than_one(self):
        return len(self.items)>1
    
    def __str__(self):
        return str(self.items)


class Transition:
    def __init__(self, state_from, transition_symbol, state_to):
        self.state_from = state_from
        self.transition_symbol = transition_symbol
        self.state_to = state_to
    
    def __str__(self):
        return '(' + 'q'+str(self.state_from)+', '+str(self.transition_symbol)+', '+'q'+str(self.state_to)+ ')'


class NFA:
    all_states = Stack()
    alphabets = []
    def __init__(self, states, transitions , initial_state, final_state):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_state = final_state
    
    def __str__(self):
        states = ''
        for i, s in enumerate(self.states):
            if(i<len(self.states)-1):
                states+= 'q'+str(s) +', '
            else:
                states+= 'q'+str(s)
        alpha = ''
        for i, a in enumerate(NFA.alphabets):
            if(i<len(NFA.alphabets)-1):
                alpha+= str(a) +', '
            else:
                alpha+= str(a)
        trans = ''
        for i, t in enumerate(self.transitions):
            if(i<len(self.transitions)-1):
                trans+= str(t) +', '
            else:
                trans+= str(t)
        return states+'\n'+alpha+'\n'+'q'+str(self.initial_state)+'\n'+'q'+str(self.final_state)+'\n'+trans

#done
def symbol_epsilon_nfa(c):
    if NFA.all_states.top() == None:
        state_value = 0
    else:
        state_value = NFA.all_states.top()+1

    if c == ' ' or (c>='a' and c<='z') or c=='1' or c =='0':
        if c not in NFA.alphabets:
            NFA.alphabets.append(c)

        initial_state = state_value
        final_state = state_value+1
        states = [initial_state, final_state]
        transitions = [Transition(initial_state, c, final_state)]

        NFA.all_states.push(initial_state)
        NFA.all_states.push(final_state)

    return  NFA(states, transitions, initial_state, final_state)

#done
def concat(nfa_1, nfa_2):
    initial_state = nfa_1.initial_state
    final_state = nfa_2.final_state

    remove_state = nfa_1.final_state
    replaced_state = nfa_2.initial_state

    nfa_1.states.remove(remove_state)
    states = nfa_1.states + nfa_2.states

    for transition in nfa_1.transitions:
        if transition.state_from == remove_state:
            transition.state_from = replaced_state

        if transition.state_to == remove_state:
            transition.state_to = replaced_state

    transitions = nfa_1.transitions + nfa_2.transitions

    return NFA(states, transitions, initial_state, final_state)

# done
def union(nfa_1, nfa_2):
    if NFA.all_states.top() == None:
        state_value = 0
    else:
        state_value = NFA.all_states.top()+1
    
    if ' ' not in NFA.alphabets:
            NFA.alphabets.append(' ')

    initial_state = state_value
    final_state = state_value + 1
    states = nfa_1.states + nfa_2.states + [initial_state, final_state]
    transitions = nfa_1.transitions + nfa_2.transitions + [Transition(initial_state, ' ', nfa_1.initial_state), 
                    Transition(initial_state, ' ', nfa_2.initial_state), Transition(nfa_1.final_state, ' ', final_state), 
                    Transition(nfa_2.final_state, ' ', final_state)]

    NFA.all_states.push(initial_state)
    NFA.all_states.push(final_state)

    return NFA(states, transitions, initial_state, final_state)

#done
def optional(nfa):
    if NFA.all_states.top() == None:
        state_value = 0
    else:
        state_value = NFA.all_states.top()+1
    
    if ' ' not in NFA.alphabets:
            NFA.alphabets.append(' ')

    initial_state = state_value
    final_state = state_value+1
    states = nfa.states + [initial_state, final_state]
    transitions = nfa.transitions + [Transition(initial_state, ' ', nfa.initial_state), 
                    Transition(initial_state, ' ', final_state), Transition(nfa.final_state, ' ', final_state)]

    NFA.all_states.push(initial_state)
    NFA.all_states.push(final_state)

    # return NFA(states, transitions, initial_state, final_state)
    return union(nfa, symbol_epsilon_nfa(' '))

#done
def kleene(nfa):
    if NFA.all_states.top() == None:
        state_value = 0
    else:
        state_value = NFA.all_states.top()+1
    
    if ' ' not in NFA.alphabets:
            NFA.alphabets.append(' ')

    initial_state = state_value
    final_state = state_value+1

    states = nfa.states + [initial_state, final_state]
    transitions = nfa.transitions + [Transition(initial_state, ' ', nfa.initial_state), 
                    Transition(initial_state, ' ', final_state), Transition(nfa.final_state, ' ', final_state), Transition(nfa.final_state, ' ', nfa.initial_state)]

    NFA.all_states.push(initial_state)
    NFA.all_states.push(final_state)

    return NFA(states, transitions, initial_state, final_state)


# a+ --> a.a*
def plus(nfa):
    dup_nfa = duplicate_nfa(nfa)
    return concat(dup_nfa, kleene(nfa))


def duplicate_nfa(nfa):
    new_initial_state = 0
    new_final_state = 0
    states = []

    transitions = []
    for transition in nfa.transitions:
       transitions.append(Transition(transition.state_from, transition.transition_symbol, transition.state_to)) 

    for state in nfa.states:
        state_value = NFA.all_states.top()+1
        
        if nfa.initial_state == state:
            new_initial_state = state_value
        if nfa.final_state == state:
            new_final_state = state_value
        
        states+=[state_value]

        for trasnition in transitions:
            if trasnition.state_from == state:
                trasnition.state_from = state_value
            if trasnition.state_to == state:
                trasnition.state_to = state_value
        

        NFA.all_states.push(state_value)

    return NFA(states, transitions, new_initial_state, new_final_state)


def is_alphabet_or_epsilon(c):
    return (c>='a' and c<='z') or c==' ' or c=='1' or c=='0'


def convert_to_postfix(s):
    temp = ''
    for index, c in enumerate(s):
        if index>0 and (is_alphabet_or_epsilon(s[index]) or s[index] =='(') and s[index-1] != '|' and s[index-1] != '(':
            temp+='.'+c
        else:
            temp+=c
    preced = {"|":1, ".":2}
    stack = Stack()
    postfix = ''
    for c in temp:
        if (c>='a' and c<='z') or c=='1' or c =='0' or (c == '*') or (c == '+') or (c == '?') or (c == ' '):
            postfix += c
        elif c == '(':
            stack.push(c)
        elif c == '|' or (c == '.'):
            while not stack.is_empty() and stack.top()!='(' and preced[stack.top()] >= preced[c]:
                postfix += stack.pop()
            stack.push(c)
        elif c == ')':
            if not stack.is_empty():
                t = stack.pop()
            while not stack.is_empty() and t!='(':
                postfix += t
                t = stack.pop()
    while not stack.is_empty():
        postfix += stack.pop()
    print(postfix)
    return postfix


def compile(s):
    stack = Stack()
    for c in s:
        if is_alphabet_or_epsilon(c):
            stack.push(symbol_epsilon_nfa(c))
        elif c == '.':
            nfa_1 = stack.pop()
            nfa_2 = stack.pop()
            stack.push(concat(nfa_2, nfa_1))
        elif c == '|':
            nfa_1 = stack.pop()
            nfa_2 = stack.pop()
            stack.push(union(nfa_2, nfa_1))
        elif c == '?':
            nfa_1 = stack.pop()
            stack.push(optional(nfa_1))
        elif c == '*':
            nfa_1 = stack.pop()
            stack.push(kleene(nfa_1))
        elif c == '+':
            nfa_1 = stack.pop()
            stack.push(plus(nfa_1))
    
    if stack.has_more_than_one():
        return None
    else:
        return stack.pop()


def main(s):
    postfix = convert_to_postfix(s)
    print(postfix)
    return compile(postfix)

def output(nfa):
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    # get the file object
    output_file = open("task_2_result.txt", "w+")

    with open(args.file, "r") as file:
        for line in file:
            output_file.write(str(main(line)) + "\n")

    output_file.close()
    

    # convert_to_postfix('ab')
    # convert_to_postfix('ab+')
    # convert_to_postfix('ab*')
    # convert_to_postfix('a|b')
    # convert_to_postfix('a|b*')
    # convert_to_postfix('( x)|y*')
    # convert_to_postfix('a|bcd')
    # convert_to_postfix('(a|b)*abb(a|b)*')
    
    #1
    # nfa_1 = symbol_epsilon_nfa(' ')
    # print(nfa_1)
    #2
    # nfa_2  =symbol_epsilon_nfa('a')
    # print(nfa_2)
    #3
    # nfa_3 = union(nfa_1, nfa_2)
    # print(nfa_3)
    #4
    # nfa_4 = concat(nfa_1, nfa_2)
    # print(nfa_4)
    #4
    # nfa_5 = optional(nfa_1)
    # print(nfa_5)
    #5
    # nfa_6 = duplicate_nfa(nfa_3)
    # print(nfa_6)