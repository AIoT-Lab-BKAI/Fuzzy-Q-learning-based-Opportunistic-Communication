from .fuzzy_system.fuzzy_variable_output import FuzzyOutputVariable
from .fuzzy_system.fuzzy_variable_input import FuzzyInputVariable
from .fuzzy_system.fuzzy_system import FuzzySystem


class FuzzyInference:
    def __init__(self, MAX_CAPACITY, MAX_DELAY_TIME):
        self.MAX_CAPACITY = MAX_CAPACITY
        self.MAX_DELAY_TIME = MAX_DELAY_TIME
        self.system = None
        self.initFuzzySystem()
        self.rule()

    def initFuzzySystem(self):
        ### INPUT
        MAX_CAPACITY = self.MAX_CAPACITY
        capacity = FuzzyInputVariable('Capacity', 0, MAX_CAPACITY, 100)
        capacity.add_trapezoidal('Low', 0, 0, 0.4 * MAX_CAPACITY, 0.5 * MAX_CAPACITY)
        capacity.add_trapezoidal('Medium', 0.4 * MAX_CAPACITY, 0.5 * MAX_CAPACITY, 0.7 * MAX_CAPACITY, 0.8 * MAX_CAPACITY)
        # capacity.add_triangular('Medium', 0.6 * MAX_CAPACITY, 0.7 * MAX_CAPACITY, 0.85 * MAX_CAPACITY)
        capacity.add_trapezoidal('High', 0.7 * MAX_CAPACITY, 0.8 * MAX_CAPACITY, MAX_CAPACITY, MAX_CAPACITY)

        MAX_DELAY_TIME = self.MAX_DELAY_TIME
        timeDelay = FuzzyInputVariable('Time Delay', 0, MAX_DELAY_TIME, 100)
        timeDelay.add_trapezoidal('Low', 0, 0, 0.4 * MAX_DELAY_TIME, 0.5 * MAX_DELAY_TIME)
        timeDelay.add_trapezoidal('Medium', 0.4 * MAX_DELAY_TIME, 0.5 * MAX_DELAY_TIME, 0.7 * MAX_DELAY_TIME,
                                  0.8 * MAX_DELAY_TIME)
        timeDelay.add_trapezoidal('High', 0.7 * MAX_DELAY_TIME, 0.8 * MAX_DELAY_TIME, MAX_DELAY_TIME, MAX_DELAY_TIME)

        ### OUTPUT
        thetaValue = FuzzyOutputVariable('Theta', 0, 1, 100)
        # thetaValue.add_triangular('Very Low', 0, 0, 0.2)
        thetaValue.add_trapezoidal('Low', 0, 0, 0.3, 0.4)
        thetaValue.add_trapezoidal('Medium', 0.3, 0.4, 0.6, 0.7)
        thetaValue.add_trapezoidal('High', 0.6, 0.7, 1, 1)
        # thetaValue.add_triangular('High', 0.75, 0.85, 0.95)
        # thetaValue.add_triangular('Very High', 0.8, 1, 1)

        self.system = FuzzySystem()
        self.system.add_input_variable(capacity)
        self.system.add_input_variable(timeDelay)
        self.system.add_output_variable(thetaValue)

    def rule(self):
        self.system.add_rule(
            {'Capacity': 'Low',
             'Time Delay': 'Low'},
            {'Theta': 'High'}
        )

        self.system.add_rule(
            {'Capacity': 'Low',
             'Time Delay': 'Medium'},
            {'Theta': 'High'}
        )

        self.system.add_rule(
            {'Capacity': 'Low',
             'Time Delay': 'High'},
            {'Theta': 'Low'}
        )

        self.system.add_rule(
            {'Capacity': 'Medium',
             'Time Delay': 'Low'},
            {'Theta': 'High'}
        )

        self.system.add_rule(
            {'Capacity': 'Medium',
             'Time Delay': 'Medium'},
            {'Theta': 'High'}
        )

        self.system.add_rule(
            {'Capacity': 'Medium',
             'Time Delay': 'High'},
            {'Theta': 'Low'}
        )

        self.system.add_rule(
            {'Capacity': 'High',
             'Time Delay': 'Low'},
            {'Theta': 'Medium'}
        )

        self.system.add_rule(
            {'Capacity': 'High',
             'Time Delay': 'Medium'},
            {'Theta': 'Medium'}
        )

        self.system.add_rule(
            {'Capacity': 'High',
             'Time Delay': 'High'},
            {'Theta': 'Low'}
        )

    def inference(self, capacity, timeDelay, showResult=False, plot=False):
        output = self.system.evaluate_output({
            'Capacity': capacity,
            'Time Delay': timeDelay
        })

        if showResult:
            print(output)
        if plot:
            self.system.plot_system()

        return output


# fuzzy = FuzzyInference(10, 10)
#
# currentC = 8
# deltaTime = 8
# x = fuzzy.inference(currentC, deltaTime, showResult=True, plot=True)
#
# theta = x['Theta']
# print(theta)
# print("Reward RSU: ", (10 - theta * currentC) / (1 + deltaTime))
# print("Reward Gnb: ", - (theta * 10 - currentC) / (1 + deltaTime))
# print("Reward noChange: ", - 1 / (1 + deltaTime))
# print(1 / theta)
