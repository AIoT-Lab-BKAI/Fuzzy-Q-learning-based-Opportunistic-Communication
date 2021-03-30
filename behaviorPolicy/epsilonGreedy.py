from behaviorPolicy.policy import Policy
import numpy as np


class EpsilonGreedy(Policy):
    """
    Epsilon Greedy:
    With probability 1-ɛ : we do exploitation (aka our agent selects the action with the highest state-action pair value).
    With probability ɛ: we do exploration (trying random action).
    """

    def __init__(self, nActions, epsilon=0.1):
        self.nActions = nActions
        self.epsilon = epsilon

    def getPolicy(self):
        def chooseAction(values_of_all_actions, exclude_indexs=[]):
            """
            :param values_of_all_actions:
            :return: action
            """
            n_actions = len(values_of_all_actions)
            prob_taking_best_action_only = 1 - self.epsilon
            prob_taking_any_random_action = self.epsilon / (n_actions - len(exclude_indexs))
            action_prob_vertor = [prob_taking_any_random_action] * n_actions
            min_values = np.min(values_of_all_actions)
            for i in exclude_indexs:
                action_prob_vertor[i] = 0
                values_of_all_actions[i] = min_values - 1
            exploitation_action_index = np.argmax(values_of_all_actions)
            action_prob_vertor[exploitation_action_index] += prob_taking_best_action_only
            chosen_action = np.random.choice(np.arange(n_actions), p=action_prob_vertor)
            return chosen_action

        return chooseAction

# values_of_all_actioins = [3, 5, 1, 2]
# greedy = EpsilonGreedy(4, 1)
# x = greedy.getPolicy()(values_of_all_actioins)
# print(x)
