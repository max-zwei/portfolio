

from optimization.optimization_problem import Optimization_Problem


class Optimization_Algorithms():
    """
        Optimization class with different optimization method implementations
    """

    @classmethod
    def exhaustive_search(cls):
        """
            calculate the best values for toast and wait duration by searching all values exhaustively.
        """
        best_utility = float('-inf')
        best_solution = None

        for toast_duration in range(1,101):
            for wait_duration in range(1,101):
                utility = Optimization_Problem.utility(
                                toast_duration = toast_duration,
                                wait_duration = wait_duration)
                
                if utility > best_utility:
                    best_utility = utility
                    best_solution = (toast_duration,wait_duration)
        return best_solution, best_utility
    
    # 1) Implement hill-climbing for the parameters *toast_duration* and *wait_duration*
    # 2) Implement gradient-ascent for the parameters *toast_duration*,  *wait_duration* and *power*

    @classmethod
    def hill_climbing(cls):
        """
            calculate the best values for toast and wait duration by implementing Hill Climbing
        """

        def finding_next_climb(toast_duration, wait_duration):
            # Calculate the utility of the current position and its neighbours. 
            # 1 is the neighbor at +1, 0 at 0 and n1 at -1. 
            # The first index is for the toast_duration and the second index for the wait_duration.
            # Checking if the neighbor is withing the range of 1-100

            utility = Optimization_Problem.utility(toast_duration = toast_duration, wait_duration = wait_duration)

            if toast_duration < 100:
                utility_1_0 = Optimization_Problem.utility(toast_duration = (toast_duration + 1), wait_duration = wait_duration)
            else:
                utility_1_0 = 0
            if toast_duration > 1:
                utility_n1_0 = Optimization_Problem.utility(toast_duration = (toast_duration - 1), wait_duration = wait_duration)
            else:
                utility_n1_0 = 0
            if wait_duration > 1:
                utility_0_n1 = Optimization_Problem.utility(toast_duration = (toast_duration), wait_duration = (wait_duration - 1))  
            else:
                utility_0_n1 = 0
            if wait_duration < 100:
                utility_0_1 = Optimization_Problem.utility(toast_duration = (toast_duration), wait_duration = (wait_duration + 1))
            else:
                utility_0_1 = 0
            if toast_duration < 100 and wait_duration < 100:
                utility_1_1 = Optimization_Problem.utility(toast_duration = (toast_duration + 1), wait_duration = (wait_duration +1))
            else:
                utility_1_1 = 0
            if toast_duration > 1 and wait_duration > 1:
                utility_n1_n1 = Optimization_Problem.utility(toast_duration = (toast_duration - 1), wait_duration = (wait_duration - 1))                                  
            else:
                utility_n1_n1 = 0
            if toast_duration < 100 and wait_duration > 1:
                utility_1_n1 = Optimization_Problem.utility(toast_duration = (toast_duration + 1), wait_duration = (wait_duration - 1))
            else:
                utility_1_n1 = 0
            if toast_duration > 1 and wait_duration < 100:
                utility_n1_1 = Optimization_Problem.utility(toast_duration = (toast_duration - 1), wait_duration = (wait_duration +1))
            else:
                utility_n1_1 = 0

            neighbors = [[utility_1_0, toast_duration + 1, wait_duration], 
                         [utility_n1_0, toast_duration - 1, wait_duration],
                         [utility_0_n1, toast_duration, wait_duration -1],
                         [utility_0_1, toast_duration, wait_duration + 1],
                         [utility_1_1, toast_duration + 1, wait_duration + 1],
                         [utility_n1_n1, toast_duration - 1, wait_duration - 1],
                         [utility_1_n1, toast_duration + 1, wait_duration - 1],
                         [utility_n1_1, toast_duration - 1, wait_duration + 1]]

            # sort the utilities of the neighbors from max to min
            neighbors.sort(reverse=True)

            # check if the current utility is better or worse than its best neighbor. 
            # run the function again, if better neighbor was found.
            if utility > neighbors[0][0]:
                return (toast_duration, wait_duration), utility
            else:
                return finding_next_climb(neighbors[0][1], neighbors[0][2])

        # random starting point
        return finding_next_climb(50, 50)
                
    @classmethod
    def gradient_ascent(cls):
        """
            Calculate the best values for toast_duration, wait_duration and power.
            This will require a mixture of hill climbing and Gradient Ascent
        """
        # TODO: implement me
        return None, float('-inf')
    
