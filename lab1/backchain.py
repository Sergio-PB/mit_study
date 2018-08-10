from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

##def backchain_to_goal_tree(rules, hypothesis):
##    tree = []
##    if isinstance(hypothesis, AND):
##        new_rules = []
##        for option in hypothesis:
##            new_rules += backchain_to_goal_tree(rules, option)
##        tree += AND(new_rules)
##    elif isinstance(hypothesis, OR):
##        new_rules = []
##        for option in hypothesis:
##            new_rules += backchain_to_goal_tree(rules, option)
##        tree += OR(new_rules)
##    else:
##        tree.append(hypothesis)
##        for rule in rules:
##            for c in rule.consequent():
##                m = match(c, hypothesis)
##                if m != None:
##                    print m
##                    new_rules = []
##                    for ant in rule.antecedent():
##                        if not isinstance(ant, list):
##                            ant = populate(ant, m)
##                        if isinstance(rule.antecedent(), AND):
##                            new_rules.append(AND(backchain_to_goal_tree(rules, ant)))
##                        elif isinstance(rule.antecedent(), OR):
##                            new_rules.append(OR(backchain_to_goal_tree(rules, ant)))
##                        else:
##                            new_rules.append(backchain_to_goal_tree(rules, ant))
##                    if isinstance(rule.antecedent(), AND):
##                        tree.append(AND(new_rules))
##                    elif isinstance(rule.antecedent(), OR):
##                        tree.append(OR(new_rules))
##                    else:
##                        tree += new_rules
##    return simplify(OR(tree))

def backchain_to_goal_tree(rules, hypothesis):
    tree = []
    tree.append(hypothesis)
    for rule in rules:
        for c in rule.consequent():
            m = match(c, hypothesis)
            if m != None:
                if isinstance(rule.antecedent(), list):
                    new_rules = []
                    for ant in rule.antecedent():
                        print ant
                        ant = populate(ant, m)
                        new_rules.append(backchain_to_goal_tree(rules, ant))
                    if isinstance(rule.antecedent(), AND):
                        tree.append(AND(new_rules))
                    elif isinstance(rule.antecedent(), OR):
                        tree.append(OR(new_rules))
                    else:
                        tree += new_rules
                else:
                    ant = populate(rule.antecedent(), m)
                    tree.append(backchain_to_goal_tree(rules, ant))
    return simplify(OR(tree))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')

