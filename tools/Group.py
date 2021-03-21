from typing import List


class Group:

    def __init__(self, owner: str, name: str, my_role: str, group_type: str=None, 
                    rating: int=None, scheduled_time: str=None, composition: List[int]=None):
        """Init method for Group

        Intended to be used for either Arena 2v2, 3v3 or 10v10 BGs

        Args:
            owner (str): Player who created the group
            name (str): Name of group for storing in GroupManager
            my_role (str): Role of player who created group, <tank | healer | dps>
            group_type (str, optional): <arena2 | arena3 | rbg>. Defaults to None.
            rating (int, optional): Rating of group. Defaults to None.
            scheduled_time (str, optional): If desired, specify a scheduled server time for group. Defaults to None.
            composition (List[int], optional): Desired composition for group. Defaults to None.
        """
        
        self.owner, self.name, self.group_type, self._total = owner, name, group_type, 0
        
        if group_type == 'arena2':
            self._max = 2
        elif group_type == 'arena3':
            self._max = 3
        elif group_type == 'rbg':
            self._max = 10
        else:
            self._max = 20  # for raids? TODO flesh this out later

        if rating:
            self.rating = rating
        if scheduled_time:
            self.time = scheduled_time
        if composition:
            tanks = composition[0]
            healers = composition[1]
            dps = composition[2]
        else:
            tanks = 10
            healers = 10
            dps = 10

        self.comp = {
                        'tank': 
                            {
                                'number': tanks,
                                'players': []
                            },

                        'healer':
                            {
                                'number': healers,
                                'players': []
                            },

                        'dps':
                            {
                                'number': dps,
                                'players': []
                            }
                    }  # type: ignore

        self.add_member(owner, my_role)
        
        for role in self.comp:
            self._total += len(self.comp[role]['players'])

    def add_member(self, member: str, role: str):
        """Function to add a member to group

        Args:
            member (str): Member to add
            role (str): Role that member will play
        """

        # if adding this player conflicts with desired comp, handle here
        if len(self.comp[role]['players']) + 1 > self.comp[role]['number']:
            print(f'{role} already at max capacity!')  # placeholder for now
        
        # else, add the player to the comp list
        else:
            self.comp[role]['players'].append(member)

    def remove_member(self, member: str):
        """Function to remove a member from group

        Args:
            member (str): Member to remove
        """

        for role in self.comp:
            if member in self.comp[role]['players']:
                self.comp[role]['players'].pop(self.comp[role]['players'].index(member)) 


class GroupManager:

    def __init__(self):
        self.groups = {}

    def add_group(self, leader: str, group: Group):
        if not self.groups.get(leader):
            self.groups[leader] = {'groups': []}
            self.groups[leader]['groups'].append(group)
        else:
            self.groups[leader]['groups'].append(group)

    def remove_group(self, leader: str, group_name: str) -> int:
        if leader in self.groups:
            groups = [group.name for group in self.groups[leader]['groups']]

            if group_name in groups:
                self.groups[leader]['groups'].pop(groups.index(group_name))
                return 1
        
        return 0

    def get_groups(self, leader: str, group: str=None) -> List[Group]:
        if leader in self.groups:
            groups = [group.name for group in self.groups[leader]['groups']]

            if group and group in groups:
                return [self.groups[leader]['groups'][groups.index(group)]]
            elif group and group not in groups:
                return []
            else:
                return self.groups[leader]['groups']
        
        return []

if __name__ == '__main__':
    group = Group('Kyle', 'healer')
    group.add_member('Chris', 'dps')
    group.add_member('Natalie', 'tank')
    group.add_member('Kirsten', 'dps')
    group.add_member('Anish', 'dps')
    group.add_member('Kevin', 'healer')
    group.add_member('Alex', 'healer')
    group.add_member('Ryan', 'healer')

    print(group.comp)
