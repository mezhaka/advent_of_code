#--- Day 7: The Sum of Its Parts ---
#You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

#"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

#"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

#"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

#The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

#Step C must be finished before step A can begin.
#Step C must be finished before step F can begin.
#Step A must be finished before step B can begin.
#Step A must be finished before step D can begin.
#Step B must be finished before step E can begin.
#Step D must be finished before step E can begin.
#Step F must be finished before step E can begin.
#Visually, these requirements look like this:


  #-->A--->B--
 #/    \      \
#C      -->D----->E
 #\           /
  #---->F-----
#Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

#Only C is available, and so it is done first.
#Next, both A and F are available. A is first alphabetically, so it is done next.
#Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
#After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
#F is the only choice, so it is done next.
#Finally, E is completed.
#So, in this example, the correct order is CABDFE.

#In what order should the steps in your instructions be completed?

#Your puzzle answer was EUGJKYFQSCLTWXNIZMAPVORDBH.

#--- Part Two ---
#As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

#Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

#To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

#Second   Worker 1   Worker 2   Done
   #0        C          .
   #1        C          .
   #2        C          .
   #3        A          F       C
   #4        B          F       CA
   #5        B          F       CA
   #6        D          F       CAB
   #7        D          F       CAB
   #8        D          F       CAB
   #9        D          .       CABF
  #10        E          .       CABFD
  #11        E          .       CABFD
  #12        E          .       CABFD
  #13        E          .       CABFD
  #14        E          .       CABFD
  #15        .          .       CABFDE
#Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

#Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

#In this example, it would take 15 seconds for two workers to complete these steps.

#With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?

#Your puzzle answer was 1014.

import collections
import itertools

input = '''Step E must be finished before step H can begin.
Step Y must be finished before step T can begin.
Step F must be finished before step S can begin.
Step U must be finished before step K can begin.
Step X must be finished before step Z can begin.
Step Q must be finished before step W can begin.
Step W must be finished before step O can begin.
Step G must be finished before step A can begin.
Step N must be finished before step H can begin.
Step S must be finished before step H can begin.
Step K must be finished before step C can begin.
Step J must be finished before step H can begin.
Step T must be finished before step B can begin.
Step C must be finished before step P can begin.
Step L must be finished before step V can begin.
Step Z must be finished before step A can begin.
Step M must be finished before step A can begin.
Step A must be finished before step P can begin.
Step V must be finished before step O can begin.
Step I must be finished before step O can begin.
Step P must be finished before step H can begin.
Step O must be finished before step D can begin.
Step R must be finished before step B can begin.
Step D must be finished before step B can begin.
Step B must be finished before step H can begin.
Step J must be finished before step L can begin.
Step T must be finished before step V can begin.
Step Z must be finished before step M can begin.
Step G must be finished before step B can begin.
Step K must be finished before step L can begin.
Step Z must be finished before step H can begin.
Step L must be finished before step M can begin.
Step X must be finished before step A can begin.
Step N must be finished before step M can begin.
Step G must be finished before step M can begin.
Step A must be finished before step V can begin.
Step G must be finished before step S can begin.
Step G must be finished before step J can begin.
Step L must be finished before step A can begin.
Step A must be finished before step H can begin.
Step T must be finished before step M can begin.
Step X must be finished before step N can begin.
Step P must be finished before step O can begin.
Step Y must be finished before step F can begin.
Step U must be finished before step G can begin.
Step G must be finished before step O can begin.
Step P must be finished before step D can begin.
Step G must be finished before step L can begin.
Step Z must be finished before step P can begin.
Step C must be finished before step L can begin.
Step E must be finished before step B can begin.
Step T must be finished before step Z can begin.
Step D must be finished before step H can begin.
Step U must be finished before step N can begin.
Step E must be finished before step V can begin.
Step L must be finished before step D can begin.
Step K must be finished before step Z can begin.
Step O must be finished before step R can begin.
Step V must be finished before step R can begin.
Step L must be finished before step O can begin.
Step T must be finished before step H can begin.
Step E must be finished before step Q can begin.
Step S must be finished before step T can begin.
Step U must be finished before step M can begin.
Step Q must be finished before step V can begin.
Step I must be finished before step B can begin.
Step L must be finished before step Z can begin.
Step Y must be finished before step B can begin.
Step J must be finished before step C can begin.
Step F must be finished before step Q can begin.
Step J must be finished before step D can begin.
Step Q must be finished before step L can begin.
Step I must be finished before step D can begin.
Step N must be finished before step V can begin.
Step U must be finished before step H can begin.
Step J must be finished before step R can begin.
Step K must be finished before step V can begin.
Step G must be finished before step P can begin.
Step Y must be finished before step X can begin.
Step L must be finished before step H can begin.
Step R must be finished before step D can begin.
Step S must be finished before step C can begin.
Step Q must be finished before step A can begin.
Step U must be finished before step X can begin.
Step V must be finished before step B can begin.
Step U must be finished before step Z can begin.
Step F must be finished before step P can begin.
Step G must be finished before step D can begin.
Step O must be finished before step H can begin.
Step C must be finished before step D can begin.
Step L must be finished before step P can begin.
Step N must be finished before step I can begin.
Step Q must be finished before step O can begin.
Step Q must be finished before step D can begin.
Step Z must be finished before step D can begin.
Step Y must be finished before step N can begin.
Step M must be finished before step O can begin.
Step W must be finished before step R can begin.
Step S must be finished before step D can begin.
Step O must be finished before step B can begin.
Step I must be finished before step P can begin.'''

#input = '''Step C must be finished before step A can begin.
#Step C must be finished before step F can begin.
#Step A must be finished before step B can begin.
#Step A must be finished before step D can begin.
#Step B must be finished before step E can begin.
#Step D must be finished before step E can begin.
#Step F must be finished before step E can begin.'''


def get_adjlist(input):
    forward_adjlist = collections.defaultdict(list)
    backward_adjlist = collections.defaultdict(list)
    for before, after in ((s[5], s[36]) for s in input.split('\n')):
        forward_adjlist[before].append(after)
        backward_adjlist[after].append(before)
    return forward_adjlist, backward_adjlist


def get_leafs(forward, backward):
    return set(backward.keys())- set(forward.keys())


def part1(input):
    forward, backward = get_adjlist(input)

    seq = []
    bottoms = get_leafs(forward, backward)
    while bottoms:
        tops = get_leafs(backward, forward)
        n = min(tops)
        seq.append(n)

        children = forward.pop(n)
        for c in children:
            backward[c].remove(n)
            if not backward[c]:
                del backward[c]
        previous_bottoms, bottoms = bottoms, get_leafs(forward, backward)
    seq.append(next(iter(previous_bottoms)))
    return ''.join(seq)


def task_cost(t):
    return 60 + ord(t) - ord('A') + 1


def part2(input, worker_num):
    forward, backward = get_adjlist(input)

    elapsed = 0
    workers, pending  = [], []
    bottoms =  get_leafs(forward, backward)
    while bottoms:
        tops = (get_leafs(backward, forward)
                - set(task for _, task in itertools.chain(workers, pending)))
        pending.extend([task_cost(t), t] for t in tops)
        pending.sort(key=lambda cost_name: cost_name[1])

        free_num = worker_num - len(workers)
        workers.extend(pending[:free_num])
        del pending[:free_num]
        workers.sort()

        roll = workers[0][0]
        done_num = 0
        for i in range(len(workers)):
            workers[i][0] -= roll
            if workers[i][0] == 0:
                done_num += 1
        elapsed += roll

        for _, n in workers[:done_num]:
            children = forward.pop(n)
            for c in children:
                backward[c].remove(n)
                if not backward[c]:
                    del backward[c]
        previous_bottoms, bottoms = bottoms, get_leafs(forward, backward)
        del workers[:done_num]
    last_task = next(iter(previous_bottoms))
    return elapsed + task_cost(last_task)


if __name__ == '__main__':
    print(part1(input) == 'EUGJKYFQSCLTWXNIZMAPVORDBH')
    print(part2(input, worker_num=5) == 1014)
