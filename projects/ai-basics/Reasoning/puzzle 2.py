from logic import Biconditional, And, Or, Implication, model_check, Not, Symbol

# Once you're done with a task, you can run this file by typing in the terminal:
# python puzzle.py


# ******************************************
# 1. OVERVIEW
# ******************************************
# In a Knights and Knaves puzzle, the following information is given:
# Each character is either a knight or a knave. A knight will always tell the truth:
# if knight states a sentence, then that sentence is true. Conversely, a knave
# will always lie: if a knave states a sentence, then that sentence is false.
#
# The objective of the puzzle is, given a set of sentences spoken by each of the characters,
# determine, for each character, whether that character is a knight or a knave.
#
# For example, consider a simple puzzle with just a single character named A.
# A says “I am both a knight and a knave.”
#
# Logically, we might reason that if A were a knight, then that sentence would have to be true.
# But we know that the sentence cannot possibly be true, because A cannot be both a knight
# and a knave – we know that each character is either a knight or a knave, but not both.
# So, we could conclude, A must be a knave.
#
# Your task in this problem is to determine how to represent these puzzles using propositional logic,
# such that an AI running a model-checking algorithm could solve these puzzles for us.


# ******************************************
# 2. PROPOSITIONS
# ******************************************
# Our puzzles contain only very few and simple propositions - that is, logical statements that
# can be either true or false. You can think about them as variables that can take these two values -
# [True, False]. Later, we can define logical relationships between them, but first things first.
#
# These are the propositions that our program will check for each of the puzzles:

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Note that the Symbol class is defined in logic.py and serves as a way to represent a logical
# proposition within our propositional logic framework.


# ******************************************
# 3. LOGICAL RELATIONSHIPS
# ******************************************
# Remember that in propositional logic, we can define logical relationships between our propositions.
# Those relationships are AND, OR, NOT, IMPLICATION, BICONDITIONAL.

# The package logic provides us with a lot of handy functionality. Below are short descriptions
# of the different relationships and examples of how to represent them in this program.

# AND chains together at least two propositions and evaluates to true
# if both the propositions are true.
And(AKnave, BKnight)  # true if both AKnave and BKnight are true.

# OR chains together at least two propositions and evaluates to true
# if at least one of the propositions is true.
Or(AKnight, AKnave)  # true if AKnight or AKnave or both are true.

# NOT negates the truthiness of a proposition.
Not(CKnave)  # true if CKnave is false.

# IMPLICATION means that if the first sentence is true, the second one is also true.
Implication(AKnave, BKnight)  # If AKnave is true, BKnight is also true.

# BICONDITIONAL means that the first and second sentence are logically equivalent. If one is true,
# the other is also true. If one is false, the other is also false.
Biconditional(BKnight, CKnave)  # If BKnight is true [/false], CKnave is true [/false] (and vice versa).

# Note that you can chain these relationships and propositions together however you like.
Implication(And(Not(AKnight), CKnave), Or(BKnight, CKnight))


# ******************************************
# 4. KNOWLEDGE BASES
# ******************************************
# This is where you enter the stage!
#
# The goal here is to represent everything we know about the puzzles in Python code, such that
# our program can later use that knowledge to solve the puzzle.
#
# TODO: Now the only thing YOU have to do is define the knowledge base for each of the following puzzles.
#
# Hint: For each knowledge base, you’ll likely want to encode two different types of information:
# (1) information about the structure of the problem itself (i.e., information given in the
# definition of a Knight and Knave puzzle), and (2) information about what the characters actually said.
#
# Remark: You should attempt to choose the most direct translation of the information in
# the puzzle, rather than performing logical reasoning on your own. For instance,
# for Puzzle 0, setting knowledge0 = AKnave would result in correct output, since through our own
# reasoning we know A must be a knave. But doing so would be against the spirit of this problem:
# the goal is to have your AI do the reasoning for you.


# *******************************************
# Puzzle 0
# A says "I am both a knight and a knave."

# TODO: understand how knowledge 0 models this condition.
knowledge0 = And( 
    Biconditional(AKnight,Not(AKnave)), # Iff A is a knight they cannot be a knave
    Biconditional(AKnight,And(AKnave,AKnight)) # if the statement is true, A is a knight.
)

# *******************************************
# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# TODO: Define knowledge1

knowledge1 = And(
    Biconditional(AKnight,Not(AKnave)), # If A is a knight they cannot be a knave
    Biconditional(BKnight,Not(BKnave)), # If B is a knight they cannot be a knave
    
    # A is a knight, if A and B are a knaves
    Biconditional(AKnight, And(AKnave, BKnave))        
)

# *********************************************
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# TODO: Define knowledge2

knowledge2 = And(
    Biconditional(AKnight,Not(AKnave)), # If A is a knight they cannot be a knave
    Biconditional(BKnight,Not(BKnave)), # If B is a knight they cannot be a knave

    #If A is a knight, A must be a knight and B must be a knight OR A must be a knave and B must be a knave
    Biconditional(AKnight, 
                  Or(
                      And(AKnight, BKnight), 
                      And(AKnave, BKnave)
                  )),

    #If B is a knight, A must be a knight and B must be a knave OR A must be a knave and B must be a knight
    Biconditional(BKnight, 
                      Or(
                          And(AKnight, BKnave), 
                          And(AKnave, BKnight)
                      ))
)

# *********************************************
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# TODO: Define knowledge3

knowledge3 = And(
    Biconditional(AKnight,Not(AKnave)), # If A is a knight they cannot be a knave
    Biconditional(BKnight,Not(BKnave)), # If B is a knight they cannot be a knave
    Biconditional(CKnight,Not(CKnave)), # If B is a knight they cannot be a knave

    # A says either:

    ## "I am a knight". If A is a knight, A is a knight.
    Or(
    And(
    Biconditional(AKnight,
                  AKnight),

    # B must be a knave
    BKnave,

    # If B is a knight, B must be a knight and C a knave
    Biconditional(BKnight, 
                  CKnave),

    # If C is a knight, A a knight
    Biconditional(CKnight, AKnight)
    ),
    
    ## "I am a knave" If A is a knight, A is a knave.
    And(
    Biconditional(AKnight,
                  AKnave),
    
    # B must be a knight
    BKnight, 
   
    # If B is a knight, B must be a knight and C a knave
    Biconditional(BKnight, 
                 CKnave),
    
    # If C is a knight, A must be a knight
    Biconditional(CKnight, AKnight)
    ))
)

# *********************************************
# Now you only have to call this file from the terminal like this:
# python puzzle.py
#
# The rest is already taken care of.
#
# How does the automatic puzzle solving work?
#
# Step one: The program will create all possible combinations of our variables' values.
# Each of these combinations can be considered a model of the scenario.
# For example, in the simple case where we just have to deal with person A, these are
# 2 of the 4 possible models:
#
# {"AKnight is true", "AKnave is false"}
# {"AKnight is true", "AKnave is true"}
#
# Step two: Note that some of the models will be consistent with our knowledge base - the
# information we have about the puzzle - and some won't (i.e., they are counterfactual models).
# The second model is obviously counterfactual, because we know that a person cannot be a knight
# and a knave at the same time.
# Hence, step two is to discard all of the models that are not consistent with our knowledge base.
#
# Step three: The last step is to look at all the models that are consistent with out knowledge
# base. For each proposition we want to check (e.g., "A is a Knave", as defined under section 2),
# we will ask:
# Is this proposition true in all of the knowledge-consistent models? If the answer is yes, we
# can be sure that the proposition is always true! If we find at least one knowledge-consistent model
# where the proposition is false, then we have disproved its general validity.
#
# (Note that in practice, the function model_check() in logic.py handles
# all of those steps at the same time.)


# DO NOT CHANGE THIS!
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
