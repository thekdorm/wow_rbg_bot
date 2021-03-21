from typing import List


class Group:

    def __init__(self, owner: str, scheduled_time: str, composition: List[int], my_role: str):
        """Init method for Group

        Args:
            owner (str): Player name of person creating group
            scheduled_time (str): Server time that group will start
            composition (list): Tank/DPS/Healer i.e. for 1/3/6 -> [1, 3, 6]
            my_role (str): The role that the creator will be playing for composition
        """
        
        self.owner, self.time = owner, scheduled_time
        self.comp = {
                        'tank': 
                            {
                                'number': composition[0],
                                'players': []
                            },

                        'healer':
                            {
                                'number': composition[1],
                                'players': []
                            },

                        'dps':
                            {
                                'number': composition[2],
                                'players': []
                            }
                    }  # type: ignore
        
        self.add_member(owner, my_role)

    def add_member(self, member: str, role: str):
        """Function to add a member to group

        Args:
            member (str): Member to add
            role (str): Role that member will play
        """

        # if adding this player conflicts with desired comp, handle here
        if len(self.comp[role]['players']) + 1 > self.comp[role]['number']:  # type: ignore
            print(f'{role} already at max capacity!')  # placeholder for now
        
        # else, add the player to the comp list
        else:
            self.comp[role]['players'].append(member)  # type: ignore

    def remove_member(self, member: str):
        """Function to remove a member from group

        Args:
            member (str): Member to remove
        """

        for role in self.comp:
            if member in self.comp[role]['players']:  # type: ignore
                self.comp[role]['players'].pop(self.comp[role]['players'].index(member))  # type: ignore


if __name__ == '__main__':
    group = Group('Kyle', '20210321:120000', [1, 3, 6], 'healer')
    group.add_member('Chris', 'dps')
    group.add_member('Natalie', 'tank')
    group.add_member('Kirsten', 'dps')
    group.add_member('Anish', 'dps')
    group.add_member('Kevin', 'healer')
    group.add_member('Alex', 'healer')
    group.add_member('Ryan', 'healer')

    print(group.comp)
    print(group.time)
