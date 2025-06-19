

def get_map_structure(map_id):
    structured_environment = [2, 3, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44, 50,
                              51, 52, 53, 54, 60, 61, 62, 63, 64, 70, 71, 72, 73, 74, 80, 81, 82, 83, 84, 90, 91, 92,
                              93, 94, 100, 101, 102, 103, 104, 110, 111, 112, 113, 114, 120, 121, 122, 123, 124]

    return map_id in structured_environment


def get_map_type(map_id):

    if map_id < 5:
        return 'Tutorial'

    if (5 <= map_id <= 14) or (25 <= map_id <= 34) or (45 <= map_id <= 54) or (65 <= map_id <= 74):
        return 'CSH'
    elif (15 <= map_id <= 24) or (35 <= map_id <= 44) or (55 <= map_id <= 64) or (75 <= map_id <= 84):
        return 'SH'
    elif map_id > 84:
        return 'CH'


class Event():

    def __init__(self, event_string):
        time, x, y, event_type = event_string.split(';')
        self.time = float(time)
        self.x = int(x)
        self.y = int(y)
        self.event_type = event_type

    def __str__(self):
        return f'{self.event_type} at time {self.time}, in position ({self.x},{self.y})'

    def __repr__(self):
        return self.__str__()


class GoalEvent():
    def __init__(self, base_event, goal_type):

        self.time = base_event.time
        self.x = base_event.x
        self.y = base_event.y
        self.goal_type = goal_type

    def __str__(self):
        return f'Goal {self.goal_type} at time {self.time}, in position ({self.x},{self.y})'

    def __repr__(self):
        return self.__str__()


class TrialResult():
    def __init__(self, trial_name, trial_data):

        self.trial_name = trial_name
        self.trial_code = int(trial_name.split("Trial_")[1])
        self.map_identification_number = trial_data['mapIdentificationNumber']
        self.landmarks = trial_data['landmarks']

        # Map type
        self.is_structured = get_map_structure(self.map_identification_number)
        self.trial_type = get_map_type(self.map_identification_number)

        # Identify which landdmarks are oals and where they are
        self.goals = []
        for landmark in self.landmarks:
            if landmark['isGoal']:
                goal_id = int(landmark['goalIndex'])
                goal_x = int(landmark['x'])
                goal_y = int(landmark['y'])
                self.goals.append((goal_x, goal_y, goal_id))

        # Create a list of events
        self.events = [Event(e) for e in trial_data['events']]

        # Only consider events of type GoalTaken and identify their type
        self.goal_events = []

        for event in self.events:
            if event.event_type == 'GoalTaken':
                for goal in self.goals:
                    if goal[0] == event.x and goal[1] == event.y:
                        goal_id = goal[2]

                        if goal_id == 0:
                            goal_type = 'START'

                        # 1 = C, 2 = S, 3 = H
                        if self.trial_type == 'CSH':
                            if goal_id == 1:
                                goal_type = 'C'
                            if goal_id == 2:
                                goal_type = 'S'
                            if goal_id == 3:
                                goal_type = 'H'
                        if self.trial_type == 'SH':
                            if goal_id == 1:
                                goal_type = 'S'
                            if goal_id == 2:
                                goal_type = 'H'
                        if self.trial_type == 'CH':
                            if goal_id == 1:
                                goal_type = 'C'
                            if goal_id == 2:
                                goal_type = 'H'

                        goal_event = GoalEvent(event, goal_type)
                        self.goal_events.append((goal_event))

        # Reaction times
        self.reaction_times = []
        first_movement_after_goal_or_start = False
        last_time = 0
        for event in self.events:
            if event.event_type.startswith('Movement'):
                if first_movement_after_goal_or_start is False:
                    first_movement_after_goal_or_start = True
                    self.reaction_times.append(event.time - last_time)
            if event.event_type == 'GoalTaken':
                first_movement_after_goal_or_start = False
                last_time = event.time

    def __str__(self):
        s = f'{self.trial_name:10}\tid:{self.map_identification_number}\tstructured: {self.is_structured}'
        s += f'\ttrial type: {self.trial_type}\n'
        s += '\n'.join([str(e) for e in self.goal_events])
        return s


class SubjectResult():

    def __init__(self, info, trials_data, final_data):
        self.username = info['username'][0:-3]
        self.age = int(info['age'])
        self.gender = info['gender']
        self.nationality = info['nationality'][0:-3].lower().strip()
        self.gamer = info['gamer']

        if self.nationality == 'british' or self.nationality == 'english':
            self.nationality = 'uk'
        if self.nationality == 'american' or self.nationality == 'united states of america':
            self.nationality = 'usa'
        if self.gamer == '< 1 h>':
            self.gamer = '< 1 h'
        if self.gamer == '< 4 h':
            self.gamer = '> 4 h'

        self.final_code = final_data['code']
        self.final_score = final_data['score']

        self.trials_results = []

        for trial_name in trials_data:
            trial_result = TrialResult(trial_name, trials_data[trial_name])
            if len(trial_result.goal_events) == 0:
                continue
            if trial_result.trial_type != 'Tutorial':
                self.trials_results.append(trial_result)

    def __repr__(self):
        s = f'Subject: {self.username:25}\t age: {self.age}\t gender: {self.gender:20}'
        s += f'\t nationality: {self.nationality:10}\t gamer: {self.gamer}\t score: {self.final_score}'
        return s
